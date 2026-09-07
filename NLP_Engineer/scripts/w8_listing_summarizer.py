# Summarizes the listing description into 2-3 sentences
import nltk
import re
import json 
import sys
import os
from pathlib import Path
import pandas as pd
from scripts.w3_entity_extractor import EntityExtractor
from scripts.w4_queryparser import QueryParser, SchemaValidator

import mysql.connector
from dotenv import load_dotenv

load_dotenv()
def get_connection():
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )

        return conn

class ListingSummarizer:
    def __init__(self, taxonomy_path="taxonomy.json"):
        # Load existing taxonomy
        with open(taxonomy_path, "r", encoding="utf-8") as f:
            self.taxonomy = json.load(f)

        # Extract amenity/feature terms from taxonomy
        self.feature_keywords = []

        for category, terms in self.taxonomy.items():
            if category.lower() == "amenities":
                for term, variations in terms.items():
                    self.feature_keywords.append(term)
                    self.feature_keywords.extend(variations)

        # Use your existing entity extractor
        self.entity_extractor = EntityExtractor(self.taxonomy)

    def extractive_summary(self, remarks, entities=None, num_sentences=3):
        """
        Generate a concise extractive summary from listing remarks.

        Prioritizes:
        - First sentence
        - Sentences containing extracted entities
        - Common high-value property features
        """

        # Check if the remarks actually exist
        if not isinstance(remarks, str) or not remarks.strip():
            return ""

        # Extract entities from the listing
        entities = self.entity_extractor.extract_all(remarks)

        # Split the listing into sentences
        sentences = nltk.sent_tokenize(remarks)

        # Remove very short/non-informative sentences
        sentences = [
            sentence.strip()
            for sentence in sentences
            if len(sentence.split()) >= 5
        ]

        # If there are only 2 sentences, return them
        if len(sentences) <= num_sentences:
            return " ".join(sentences)

        scores = []

        # Look at each sentence 
        for i, sentence in enumerate(sentences):

            # Keep cases the same
            sentence_lower = sentence.lower()
            score = 0

            # First sentence often contains the main property description
            if i == 0:
                score += 2

            # Match extracted entity values
            for field, value in entities.items():

                if value is None:
                    continue

                if isinstance(value, list):
                    values = value
                else:
                    values = [value]

                for item in values:
                    if item is not None and str(item).lower() in sentence_lower:
                        score += 2

            # High-value real estate features (taxonomy feature/amenity matches)
            for keyword in self.feature_keywords:
                if keyword in sentence_lower:
                    score += 1

            scores.append((score, i, sentence))

        # Select highest scoring sentences
        top_sentences = sorted(
            scores,
            key=lambda x: (-x[0], x[1])
        )[:num_sentences]

        # Restore original order
        top_sentences = sorted(
            top_sentences,
            key=lambda x: x[1]
        )

        return " ".join(sentence for _, _, sentence in top_sentences)

class AnswerabilityChecker: 
    def __init__(self, taxonomy_path): 
        with open(taxonomy_path, "r", encoding="utf-8") as f:
            self.taxonomy = json.load(f)

        self.validator = SchemaValidator()

        self.real_estate_keywords = ['house', 'home', 'bed', 'bath', 
        'property', 'listing', 'price', 'sqft', 'pool', 'garage'] 

    def check_pre_query(self, query): 
        """Check BEFORE generating SQL""" 
        query_lower = query.lower() 

        # Check 1: Is this a real estate question? 
        has_re_terms = any(
            kw in query_lower 
            for kw in self.real_estate_keywords
        ) 

        if not has_re_terms: 
            return False, "This doesn't appear to be a real estate question" 

        # Check 2: Does query reference valid data? 
        # (Use Week 4's schema validator) 
        parser = QueryParser()

        try:
            filters = parser.parse(query)
        except (ValueError, KeyError, TypeError):
            return False, "I couldn't identify a supported property criterion in your question."

        # Check 3: Make sure something was actually extracted
        if not filters:
            return False, (
                "I couldn't identify a supported property criterion "
                "in your question."
            )

        # Check 4: Validate parsed filters
        try:
            self.validator.validate_query(filters)
        except ValueError as e:
            return False, f"Query references invalid data: {e}" 

        return True, "Query is answerable" 

    def check_post_query(self, results_df): 
        """Check AFTER executing SQL""" 
        if len(results_df) == 0: 
            return False, "No listings match your criteria" 

        # Check for all-null results 
        if results_df.isnull().all().all(): 
            return False, "Query returned no meaningful data" 

        return True, "Results found" 

def process_query(user_query):
    # Use Answerability layer to process the query
    checker = AnswerabilityChecker()

    # 1. Check whether query is answerable
    can_answer, message = checker.check_pre_query(user_query)

    if not can_answer:
        return {
            "error": message,
            "answerable": False
        }

    # 2. Parse query
    parser = QueryParser()
    filters = parser.parse(user_query)

    # 3. Convert filters to SQL
    sql, params = parser.to_sql(filters)

    # 4. Execute SQL
    results = execute_query(sql, params)

    # 5. Check results
    can_answer, message = checker.check_post_query(results)

    if not can_answer:
        return {
            "message": message,
            "answerable": False,
            "results": []
        }

    # 6. Return results
    return {
        "answerable": True,
        "message": message,
        "results": results
    }


def execute_query(sql, params):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(sql, params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return pd.DataFrame(results)

if __name__ == "__main__":
    result = process_query("3 bedrooms in Irvine")

    print("RESULT:")
    print(result)

    if result.get("results") is not None:
        print("COLUMNS:")
        print(result["results"].columns.tolist())

        print("FIRST ROWS:")
        print(result["results"].head())
