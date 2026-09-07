from fastapi import FastAPI, Request
import os
import boto3
import sys
import time
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware


'''project_root = os.path.abspath('../')
if project_root not in sys.path:
    sys.path.insert(0, project_root)
'''
# Existing NLP skills
from scripts.w3_entity_extractor import EntityExtractor
from scripts.w6_listing_signal_extraction import SignalExtractor
from scripts.w4_queryparser import QueryParser, SchemaValidator 
from scripts.w5_semantic_search import SemanticSearcher
from scripts.w7_search_query_intent import QueryIntentClassifier
from scripts.w8_listing_summarizer import ListingSummarizer
from scripts.w9_fair_housing_compliance import ComplianceChecker

from pydantic import BaseModel

limiter = Limiter(key_func=get_remote_address)

# ALlows React frontend to access the FastAPI backend
# The React application is running on http://localhost:5173 while FastAPI is running on http://localhost:8000, so we need to allow that origin
# through CORS (Cross-Origin Resource Sharing) middleware. This is necessary because browsers enforce the same-origin policy, which restricts 
# web pages from making requests to a different domain than the one that served the web page. By adding this middleware, we allow the React frontend to communicate with the FastAPI backend without being blocked by the browser's security features.

app = FastAPI(
    title="Real Estate NLP API",
    description="REST API for the Real Estate NLP Engineer project",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

taxonomy_path = "data/processed/taxonomy.json"

# Load taxonomy
with open(taxonomy_path, "r") as f:
    taxonomy = json.load(f)

# Initialize NLP skills
extractor = EntityExtractor(taxonomy) # entity extracter
signal_extractor = SignalExtractor(taxonomy, extractor) # listing signals extractor
query_parser = QueryParser() # query parser
schema_validator = SchemaValidator() # validator
semantic_searcher = SemanticSearcher() # searcher
intent_classifier = QueryIntentClassifier() # classify the query intent
with open("data/query_intent_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)
X = df["query"]
y = df["intent"] # classification: browsing, researching, and high intent
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.2,
    random_state=42, 
    stratify=y
)
intent_classifier.train(
    X_train,
    y_train
)
# listings_df = pd.read_csv("data/processed/cleaned_listing_full.csv")
# For FASTAPI deployment on Railway
bucket = os.environ["BUCKET"]

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ["ENDPOINT"],
    aws_access_key_id=os.environ["ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"],
    region_name=os.environ.get("REGION", "auto"),
)

os.makedirs("/tmp/private_data", exist_ok=True)

s3.download_file(
    bucket,
    "private_data/cleaned_listing_sample.csv",
    "/tmp/private_data/cleaned_listing_sample.csv",
)

s3.download_file(
    bucket,
    "private_data/listing_index_sample.faiss",
    "/tmp/private_data/listing_index_sample.faiss",
)

listings_df = pd.read_csv("/tmp/private_data/cleaned_listing_sample.csv")

remarks_list = listings_df["cleaned_remarks"].fillna("").tolist()

''' semantic_searcher.load_index(
    "data/processed/listing_index_sample.faiss",
    remarks_list
)'''

# For FASTAPI deployment on Railway
semantic_searcher.load_index(
    "/tmp/private_data/listing_index_sample.faiss",
    remarks_list
)

listings_df = listings_df.reset_index(drop=True)

summarizer = ListingSummarizer(taxonomy_path) # summarization
compliance_checker = ComplianceChecker() # compliance checker

# Response caching
response_cache = {}

# Metrics
metrics = {
    "total_queries": 0,
    "total_latency": 0.0,
    "latency_history": [],
    "positive_feedback": 0,
    "negative_feedback": 0,
    "browsing_queries": 0,
    "researching_queries": 0,
    "high_intent_queries": 0
}

# Pydantic request models
class EntityRequest(BaseModel):
    text: str

class ListingSignalRequest(BaseModel):
    remark: str

class QueryRequest(BaseModel):
    query: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 10

class SummaryRequest(BaseModel):
    text: str

class ComplianceRequest(BaseModel):
    text: str

# Response model
class SemanticResponse(BaseModel):
    text: str
    results: list
    count: int
    intent: str
    confidence: float
    search_strategy: str
    latency: float

# Confirms API is running
@app.get("/")
async def root():
    return {
        "message": "Real Estate NLP API is running"
    }

# Health check
@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }

# Extracts entities
@app.post("/extract-entities")
@limiter.limit("10/second")
async def extract_entities(request: Request, entity_request: EntityRequest):

    cache_key = f"entities:{entity_request.text}"

    if cache_key in response_cache:
        print("Cache Hit")
        return response_cache[cache_key]
    
    result = extractor.extract_all(entity_request.text)

    response =  {
        "text": entity_request.text,
        "entities": result
    }

    response_cache[cache_key] = response

    return response

# Extracts types of signals (e.g. amenities, financial, condition, location) from listing description
@app.post("/listing-signals")
@limiter.limit("10/second")
async def listing_signals(request: Request, listing_request: ListingSignalRequest):

    cache_key = f"signals:{listing_request.remark}"

    if cache_key in response_cache:
        print("Cache Hit")
        return response_cache[cache_key]

    listing_record = {
        "cleaned_remarks": listing_request.remark
    }

    result = signal_extractor.extract_signals(listing_record)

    response = {
        "text": listing_request.remark,
        "signals": result
    }

    response_cache[cache_key] = response

    return response

# Parses and validates a property query
@app.post("/parse-query")
@limiter.limit("10/second")
async def parse_query(request: Request, query_request: QueryRequest):

    cache_key = f"parse:{query_request.query}"

    if cache_key in response_cache:
        print("Cache Hit")
        return response_cache[cache_key]
    
    parsed_query = query_parser.parse(query_request.query)
    validated_query = schema_validator.validate_query(parsed_query)

    response = {
        "query": query_request.query,
        "parsed_query": parsed_query,
        "validated_query": validated_query
    }

    response_cache[cache_key] = response

    return response

def normalize_scores(results):
    if not results:
        return []

    scores = [score for _, score in results]

    min_score = min(scores)
    max_score = max(scores)

    if max_score == min_score:
        return [
            (index, 1.0)
            for index, _ in results
        ]

    return [
        (
            index,
            (score - min_score) / (max_score - min_score)
        )
        for index, score in results
    ]

# Finds semantically similar listings
@app.post("/search", response_model=SemanticResponse)
@limiter.limit("10/second")
async def semantic_search(request: Request, search_request: SearchRequest):

    cache_key = f"search:{search_request.query}:{search_request.top_k}"

    if cache_key in response_cache:
        print("Cache Hit")
        return response_cache[cache_key]

    start_time = time.time()

    intent, confidence = intent_classifier.predict(search_request.query)

    search_strategy = choose_search_strategy(intent)

    if intent == "browsing":
        metrics["browsing_queries"] += 1
    elif intent == "researching":
        metrics["researching_queries"] += 1
    elif intent == "high_intent_inquiry":
        metrics["high_intent_queries"] += 1

    parsed_query = query_parser.parse(search_request.query)

    print("QUERY:", search_request.query)
    print("PARSED QUERY:", parsed_query)

    # Apply structured filters
    filtered_listings = listings_df.copy()

    if "bedrooms" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["beds"] == parsed_query["bedrooms"]
        ]

    if "bedrooms_min" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["beds"] >= parsed_query["bedrooms_min"]
        ]

    if "bathrooms" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["baths"] == parsed_query["bathrooms"]
        ]

    if "bathrooms_min" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["baths"] >= parsed_query["bathrooms_min"]
        ]

    if "price_min" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["price"] >= parsed_query["price_min"]
        ]

    if "price_max" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["price"] <= parsed_query["price_max"]
        ]

    if "sqft" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["sqft"] == parsed_query["sqft"]
        ]

    if "sqft_min" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["sqft"] >= parsed_query["sqft_min"]
        ]

    if "sqft_max" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["sqft"] <= parsed_query["sqft_max"]
        ]

    if "city" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["L_City"].str.lower()
            == parsed_query["city"].lower()
        ]

    # Get the original dataframe indices of the filtered listings
    filtered_indices = set(filtered_listings.index.tolist())

    print("FILTERED LISTINGS:", len(filtered_listings))

    if search_strategy == "semantic":

        candidate_results = semantic_searcher.search_indices(
            search_request.query, 
            top_k = len(listings_df)
        )

        search_results = [
            (index, score)
            for index, score in candidate_results
            if index in filtered_indices
        ][:search_request.top_k]

    elif search_strategy == "keyword":

        search_results = perform_keyword_search(
            search_request.query, 
            filtered_listings,
            search_request.top_k
        )

    elif search_strategy == "hybrid":

        candidate_results = semantic_searcher.search_indices(
            search_request.query,
            top_k = len(listings_df)
        )

        semantic_results = [
            (index, score)
            for index, score in candidate_results
            if index in filtered_indices
        ]

        keyword_results = perform_keyword_search(
            search_request.query,
            filtered_listings,
            search_request.top_k
        )

        # Normalize both scores to 0-1
        semantic_results = normalize_scores(semantic_results)
        keyword_results = normalize_scores(keyword_results)

        # Keep the top semantic results
        semantic_results = semantic_results[:search_request.top_k]

        # Combine the two result sets
        combined_results = {}

        for index, score in semantic_results:
            combined_results[index] = {
                "semantic_score": score,
                "keyword_score": 0
            }
        for index, score in keyword_results:
            if index not in combined_results:
                combined_results[index] = {
                    "semantic_score": 0,
                    "keyword_score": score
                }
            else:
                combined_results[index]["keyword_score"] = score

        # Calculate a combined score
        search_results = []

        for index, scores in combined_results.items():

            combined_score = (
                0.7 * scores["semantic_score"]
                + 0.3 * scores["keyword_score"]
            )

            search_results.append(
                (index, combined_score)
            )

        search_results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        search_results = search_results[:search_request.top_k]
    
    results = []

    for original_index, score in search_results:
        listing = listings_df.loc[original_index]

        remark = listing["cleaned_remarks"]
        summary = summarizer.extractive_summary(remark)

        compliance = compliance_checker.check_listing(remark)

        results.append({
            "listing_id": int(listing["L_ListingID"]),
            "address": listing["L_Address"],
            "city": listing["L_City"],
            "zip": listing["L_Zip"],
            "bedrooms": float(listing["beds"]),
            "bathrooms": float(listing["baths"]),
            "price": float(listing["price"]),
            "sqft": float(listing["sqft"]),
            "remark": listing["cleaned_remarks"],
            "summary": summary,
            "score": float(score),
            "compliance": compliance
        })

    response = {
        "text": search_request.query,
        "results": results,
        "count": len(results),
        "intent": intent,
        "confidence": confidence,
        "search_strategy": search_strategy
    }

    response_cache[cache_key] = response

    latency = time.time() - start_time

    metrics["total_queries"] += 1
    metrics["total_latency"] += latency
    metrics["latency_history"].append(latency)

    response["latency"] = latency

    return response

# Finds listings using structured filtering and basic keyword matching
@app.post("/keyword-search", response_model=SemanticResponse)
@limiter.limit("10/second")
async def keyword_search(
    request: Request,
    search_request: SearchRequest
):

    cache_key = f"keyword:{search_request.query}:{search_request.top_k}"

    if cache_key in response_cache:
        print("Cache Hit")
        return response_cache[cache_key]

    # Parse the natural-language query
    parsed_query = query_parser.parse(search_request.query)

    # Apply structured filters
    filtered_listings = listings_df.copy()

    if "bedrooms" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["beds"] == parsed_query["bedrooms"]
        ]

    if "bedrooms_min" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["beds"] >= parsed_query["bedrooms_min"]
        ]

    if "bathrooms" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["baths"] == parsed_query["bathrooms"]
        ]

    if "bathrooms_min" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["baths"] >= parsed_query["bathrooms_min"]
        ]

    if "price_min" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["price"] >= parsed_query["price_min"]
        ]

    if "price_max" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["price"] <= parsed_query["price_max"]
        ]

    if "sqft" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["sqft"] == parsed_query["sqft"]
        ]

    if "sqft_min" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["sqft"] >= parsed_query["sqft_min"]
        ]

    if "sqft_max" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["sqft"] <= parsed_query["sqft_max"]
        ]

    if "city" in parsed_query:
        filtered_listings = filtered_listings[
            filtered_listings["L_City"].str.lower()
            == parsed_query["city"].lower()
        ]

    keyword_results = perform_keyword_search(
        search_request.query, 
        filtered_listings, 
        search_request.top_k
    )

    results = []

    for index, score in keyword_results:

        listing = filtered_listings.loc[index]

        results.append({
            "listing_id": int(listing["L_ListingID"]),
            "address": listing["L_Address"],
            "city": listing["L_City"],
            "zip": listing["L_Zip"],
            "bedrooms": float(listing["beds"]),
            "bathrooms": float(listing["baths"]),
            "price": float(listing["price"]),
            "sqft": float(listing["sqft"]),
            "remark": listing["cleaned_remarks"],
            "score": float(score)
        })

    response = SemanticResponse(
        text=search_request.query,
        results=results,
        count=len(results)
    )

    response_cache[cache_key] = response

    return response

def perform_keyword_search(query, filtered_listings, top_k):
    recognized_terms = extractor.extract_amenities(query)

    query_words = [
        item["term"].lower()
        for item in recognized_terms
    ]

    if not query_words:
        stopwords = {
            "in", "a", "an", "the",
            "with", "and", "for", "of", "to"
        }

        query_words = [
            word.lower()
            for word in query.split()
            if word.lower() not in stopwords
        ]

    keyword_results = []

    for index, row in filtered_listings.iterrows():
        remark = str(row["cleaned_remarks"]).lower()

        matches = sum(
            1 for word in query_words
            if word in remark
        )

        if matches > 0:
            keyword_results.append((index, matches))

    keyword_results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return keyword_results[:top_k]

# Classifies the intents of the queries 
@app.post("/classify-intent")
@limiter.limit("10/second")
async def classify_intent(request: Request, query_request: QueryRequest):

    cache_key = f"intent:{query_request.query}"

    if cache_key in response_cache:
        print("Cache Hit")
        return response_cache[cache_key]
    
    intent, confidence = intent_classifier.predict(query_request.query)

    search_strategy = choose_search_strategy(intent)

    response = {
        "query": query_request.query,
        "intent": intent,
        "confidence": confidence,
        "search_strategy": search_strategy
    }

    response_cache[cache_key] = response

    return response

def choose_search_strategy(intent):
    if intent == "browsing":
        return "semantic"
    elif intent == "researching":
        return "keyword"
    elif intent == "high_intent_inquiry":
        return "hybrid"
    return "semantic"

# Creates listing summary
@app.post("/summarize")
@limiter.limit("10/second")
async def summarize_listing(request: Request, summary_request: SummaryRequest):

    cache_key = f"summary:{summary_request.text}"

    if cache_key in response_cache:
        print("Cache Hit")
        return response_cache[cache_key]
    
    summary = summarizer.extractive_summary(summary_request.text)
    
    response = {
        "text": summary_request.text,
        "summary": summary
    }

    response_cache[cache_key] = response

    return response

# Checks Fair Housing language
@app.post("/check-compliance")
@limiter.limit("10/second")
async def check_compliance(request: Request, compliance_request: ComplianceRequest):

    cache_key = f"compliance:{compliance_request.text}"

    if cache_key in response_cache:
        print("Cache Hit")
        return response_cache[cache_key]
    
    result = compliance_checker.check_listing(compliance_request.text)

    response = {
        "text": compliance_request.text,
        "compliance": result
    }

    response_cache[cache_key] = response

    return response

@app.get("/metrics")
def get_metrics():
    total_queries = metrics["total_queries"]
    total_latency = metrics["total_latency"]

    if total_queries > 0:
        average_latency = total_latency / total_queries
    else:
        average_latency = None

    total_feedback = (
        metrics["positive_feedback"]
        + metrics["negative_feedback"]
    )

    if total_feedback > 0:
        satisfaction_rate = (
            metrics["positive_feedback"] / total_feedback
        ) * 100
    else:
        satisfaction_rate = None

    return {
        "total_queries": total_queries,
        "average_latency": average_latency,
        "positive_feedback": metrics["positive_feedback"],
        "negative_feedback": metrics["negative_feedback"],
        "satisfaction_rate": satisfaction_rate,
        "browsing_queries": metrics["browsing_queries"],
        "researching_queries": metrics["researching_queries"],
        "high_intent_queries": metrics["high_intent_queries"],
        "latency_history": metrics["latency_history"]
    }

@app.post("/feedback")
def submit_feedback(feedback: dict):
    rating = feedback.get("rating")
    previous_rating = feedback.get("previous_rating")

    if rating not in ["positive", "negative", None]:
        return {"error": "Invalid feedback rating"}

    # Remove the previous rating if one exists
    if previous_rating == "positive":
        metrics["positive_feedback"] = max(
            0, metrics["positive_feedback"] - 1
        )

    elif previous_rating == "negative":
        metrics["negative_feedback"] = max(
            0, metrics["negative_feedback"] - 1
        )

    # Add the new rating if there is one
    if rating == "positive":
        metrics["positive_feedback"] += 1

    elif rating == "negative":
        metrics["negative_feedback"] += 1

    return {
        "message": "Feedback recorded",
        "positive_feedback": metrics["positive_feedback"],
        "negative_feedback": metrics["negative_feedback"]
    }