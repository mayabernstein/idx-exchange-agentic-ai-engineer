import re 
from collections import Counter
import json
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from io import StringIO
import sys
import math
import spacy
from spacy.matcher import Matcher
import os

sys.path.append("../scripts")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

taxonomy_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "taxonomy.json"
)

with open(taxonomy_path, "r") as f:
    taxonomy = json.load(f)

class EntityExtractor: 
    def __init__(self, taxonomy):
        self.taxonomy = taxonomy['terms']
        self.nlp = spacy.load("en_core_web_sm")

        self.matcher = Matcher(self.nlp.vocab)

    def process_text(self, text):
        if not isinstance(text, str):
            return None
        return self.nlp(text)

    def extract_bedrooms(self, text): 
            if not isinstance(text, str):
                return None
            
            patterns = [
            # Numeric values
            r'\b(\d+)\s*[- ]?(?:bed|beds|bedroom|bedrooms|br|bd|bdrm|bdrms)\b', 
            # Number words
            r'(one|two|three|four|five|six|seven|eight|nine|ten)[- ]?(?:bed|beds|bedroom|bedrooms|br|bd|bdrm|bdrms)\b'
            ]

            if re.search(r"\bone of (the )?bedrooms\b", text, re.IGNORECASE):
                return ">1"
            
            number_words = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10
            }

            # Exact bedroom counts
            for pattern in patterns: 
                match = re.search(pattern, text, re.I) 
                if match: 
                    value = match.group(1).lower()
                    if value.isdigit():
                        return int(value)
                    else:
                        extracted = number_words[value]

                    return self.add_additional_bedrooms(text, extracted)
                
                
            # Ordinal bedroom references
            ordinal_map = {
            "primary": 1,
            "first": 1,
            "second": 2,
            "third": 3,
            "fourth": 4,
            "fifth": 5,
            "sixth": 6,
            "seventh": 7,
            "eighth": 8,
            "ninth": 9,
            "tenth": 10
            }
            matches = re.findall(
                r'\b(primary|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+(?:bedroom|bed)\b',
                text,
                re.I
            )

            if matches:
                extracted = max(ordinal_map[word.lower()] for word in matches)

                return self.add_additional_bedrooms(text, extracted)
            
            ordinal_numeric_matches = re.findall(
                r'\b(\d+)(?:st|nd|rd|th)\s+(?:bedroom|bed)\b',
                text,
                re.I
            )

            if ordinal_numeric_matches:
                extracted = max(
                    int(value)
                    for value in ordinal_numeric_matches
                )
                return self.add_additional_bedrooms(text, extracted)
            
            # Plural bedroom mention
            if re.search(r'\b(beds|bedrooms)\b', text, re.I):
                return ">1"
            
            # Singular bedroom mention
            if re.search(r'\b(bed|bedroom)\b', text, re.I):
                return 1
            return None 
    
    def add_additional_bedrooms(self, text, extracted_bedrooms):
        if not isinstance(text, str):
            return extracted_bedrooms

        # Nothing to increment
        if extracted_bedrooms is None:
            return extracted_bedrooms

        # If the original extractor returned ">1",
        # we don't have a numeric base to increment.
        if extracted_bedrooms == ">1":
            return extracted_bedrooms

        number_words = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10
        }

        additional_total = 0

        # --------------------------------------------------
        # Numeric additional bedrooms
        # Example:
        # "3 additional bedrooms"
        # --------------------------------------------------

        numeric_matches = re.findall(
            r'\b(\d+)\s+additional\s+'
            r'(?:bed|beds|bedroom|bedrooms|br|bd|bdrm|bdrms)\b',
            text,
            re.I
        )

        for value in numeric_matches:
            additional_total += int(value)

        # --------------------------------------------------
        # Written additional bedrooms
        # Example:
        # "three additional bedrooms"
        # --------------------------------------------------

        word_matches = re.findall(
            r'\b(one|two|three|four|five|six|seven|eight|nine|ten)'
            r'\s+additional\s+'
            r'(?:bed|beds|bedroom|bedrooms|br|bd|bdrm|bdrms)\b',
            text,
            re.I
        )

        for word in word_matches:
            additional_total += number_words[word.lower()]

        if additional_total > 0:
            return extracted_bedrooms + additional_total
        return extracted_bedrooms

    def extract_price(self, text):
        if not isinstance(text, str):
            return None

        # --------------------------------------------------
        # Ignore price reductions / discounts
        # --------------------------------------------------

        reduction_pattern = re.compile(
            r'(?:'
            r'-\s*\$\s*[\d,]+'
            r'|\$\s*[\d,]+'
            r'|\b[\d,]+'
            r')'
            r'\s*(?:k|K)?'
            r'\s*(?:price\s+reduction|reduction|reduced|off)'
            r'|'
            r'(?:price\s+reduction|reduction|reduced\s+by|reduced)'
            r'\s*(?:of|by)?\s*'
            r'\$?\s*[\d,]+'
            r'(?:\s*[kK])?',
            re.I
        )

        cleaned_text = reduction_pattern.sub("", text)

        # --------------------------------------------------
        # Explicit CURRENT listing price
        # --------------------------------------------------

        current_price_patterns = [

            # NOW $674,777
            r'\bnow\s+\$?\s*([\d,]+(?:\.\d+)?)\s*([kK])?\b',

            # CURRENTLY $674,777
            r'\bcurrently\s+\$?\s*([\d,]+(?:\.\d+)?)\s*([kK])?\b',

            # CURRENT PRICE: $674,777
            r'\bcurrent\s+(?:price|asking\s+price)'
            r'\s*[:\-]?\s*\$?\s*([\d,]+(?:\.\d+)?)\s*([kK])?\b',

            # PRICE IS $674,777
            r'\bprice\s+is\s+\$?\s*([\d,]+(?:\.\d+)?)\s*([kK])?\b',

            # OFFERED AT/FOR $920,000
            r'\boffered\s+(?:at|for)\s+\$?\s*'
            r'([\d,]+(?:\.\d+)?)\s*([kK])?\b',

            # PRICED AT/FOR $920,000
            r'\bpriced\s+(?:at|for)\s+\$?\s*'
            r'([\d,]+(?:\.\d+)?)\s*([kK])?\b',

            # LISTED AT/FOR $920,000
            r'\blisted\s+(?:at|for)\s+\$?\s*'
            r'([\d,]+(?:\.\d+)?)\s*([kK])?\b',

            # ASKING $920,000
            r'\basking\s+(?:price\s+)?\$?\s*'
            r'([\d,]+(?:\.\d+)?)\s*([kK])?\b',
        ]

        for pattern in current_price_patterns:

            match = re.search(pattern, cleaned_text, re.I)

            if match:

                value = match.group(1).replace(",", "")

                try:
                    number = float(value)
                except ValueError:
                    continue

                if match.group(2):
                    number *= 1000

                if number >= 100000:
                    return int(number)

        # --------------------------------------------------
        # Auction / bidding price
        # --------------------------------------------------

        auction_patterns = [

            # Current High Bid is $3,000,000
            r'\bcurrent\s+high\s+bid\s+(?:is|of)\s+\$?\s*'
            r'([\d,]+(?:\.\d+)?)\s*([kK])?\b',

            # Current Bid is $3,000,000
            r'\bcurrent\s+bid\s+(?:is|of)\s+\$?\s*'
            r'([\d,]+(?:\.\d+)?)\s*([kK])?\b',

            # Winning Bid is $3,000,000
            r'\bwinning\s+bid\s+(?:is|of)\s+\$?\s*'
            r'([\d,]+(?:\.\d+)?)\s*([kK])?\b',

            # High Bid is $3,000,000
            r'\bhigh\s+bid\s+(?:is|of)\s+\$?\s*'
            r'([\d,]+(?:\.\d+)?)\s*([kK])?\b',
        ]

        for pattern in auction_patterns:

            match = re.search(pattern, cleaned_text, re.I)

            if match:

                value = match.group(1).replace(",", "")

                try:
                    number = float(value)
                except ValueError:
                    continue

                if match.group(2):
                    number *= 1000

                if number >= 100000:
                    return int(number)

        # --------------------------------------------------
        # Current listing price ranges
        #
        # Example:
        # "$499,000-$527,000"
        # "New Range Pricing $499,000-$527,000"
        # --------------------------------------------------

        range_match = re.search(
            r'(?:'
            r'new\s+range\s+pricing|'
            r'range\s+pricing|'
            r'price\s+range|'
            r'pricing\s+range|'
            r'priced\s+between'
            r')'
            r'.{0,40}?'
            r'\$?\s*([\d,]+(?:\.\d+)?)\s*([kK])?'
            r'\s*[-–—]\s*'
            r'\$?\s*([\d,]+(?:\.\d+)?)\s*([kK])?',
            cleaned_text,
            re.I
        )

        if range_match:

            low = float(
                range_match.group(1).replace(",", "")
            )

            high = float(
                range_match.group(3).replace(",", "")
            )

            if range_match.group(2):
                low *= 1000

            if range_match.group(4):
                high *= 1000

            if high >= 100000:
                return int(high)

        # --------------------------------------------------
        # Prices expressed as ranges / bounds
        # --------------------------------------------------

        inequality_match = re.search(
            r'\b(over|above|more\s+than|greater\s+than|under|below|less\s+than)'
            r'\s+\$?\s*([\d,]+)'
            r'\s*([kK])?\b',
            cleaned_text,
            re.I
        )

        if inequality_match:

            operator_word = inequality_match.group(1).lower()

            value = (
                inequality_match.group(2)
                .replace(",", "")
                .strip()
            )

            suffix = inequality_match.group(3)

            try:
                number = int(value)
            except ValueError:
                number = None

            if number is not None:

                if suffix:
                    number *= 1000

                if number >= 100000:

                    if operator_word in [
                        "over",
                        "above",
                        "more than",
                        "greater than"
                    ]:
                        return f">{number}"

                    if operator_word in [
                        "under",
                        "below",
                        "less than"
                    ]:
                        return f"<{number}"

        # --------------------------------------------------
        # Collect all explicit $ price candidates
        # --------------------------------------------------

        matches = re.finditer(
            r'\$\s*([\d,]+)(?:\s*[kK])?',
            cleaned_text,
            re.I
        )

        candidates = []

        for match in matches:

            value = match.group(1).replace(",", "").strip()

            if not value:
                continue

            try:
                number = int(value)
            except ValueError:
                continue

            # Handle $500K
            if re.search(
                rf'\$\s*{re.escape(match.group(1))}\s*[kK]\b',
                match.group(0),
                re.I
            ):
                number *= 1000

            # Ignore small dollar amounts
            if number < 100000:
                continue

            # --------------------------------------------------
            # Look at surrounding context
            # --------------------------------------------------

            start = max(0, match.start() - 200)
            end = min(len(cleaned_text), match.end() + 200)

            context = cleaned_text[start:end].lower()

            score = 0

            # --------------------------------------------------
            # STRONG positive listing-price signals
            # --------------------------------------------------

            positive_terms = [
                "listed at",
                "listed for",
                "listing price",
                "list price",
                "asking price",
                "asking",
                "offered at",
                "offered for",
                "priced at",
                "priced for",
                "price is",
                "selling price",
                "sale price",
            ]

            for term in positive_terms:
                if term in context:
                    score += 10

            # --------------------------------------------------
            # STRONG negative signals
            # --------------------------------------------------

            negative_terms = [

                # Previous / historical prices
                "sold for",
                "sold at",
                "last sold",
                "last condo sold",
                "condo sold",
                "home sold",
                "property sold",
                "sold this year",
                "sold off market",
                "previously sold",

                "previously listed",
                "originally listed",
                "originally priced",
                "original list price",
                "original asking price",
                "previous asking price",
                "former asking price",
                "former list price",
                "was listed",
                "was priced",
                "listed previously",

                # Sales / comps
                "closed for",
                "closed at",
                "recently closed",
                "recent sale",
                "same model",
                "same model home",
                "comparable sale",
                "comparable",
                "comparables",
                "sales between",
                "sales in",
                "regularly sees sales",
                "neighborhood",

                # Auction / bidding
                "current high bid",
                "current bid",
                "high bid",
                "starting bid",
                "winning bid",

                # Approval / appraisal
                "approval at",
                "approved at",
                "appraised for",
                "appraised at",
                "appraisal",
                "valued at",

                # Financing / down payment
                "down",
                "down payment",
                "minimum down",
                "cash down",
                "deposit",
                "earnest money",
                "monthly payment",
                "payment of",

                # Income qualification
                "maximum income",
                "area median income",
                "median income",
                "income for",
                "income eligible",

                # Parcels / additional property
                "adjacent parcel",
                "additional",
                "can be purchased separately",
                "purchased separately",
                "separately",
                "available together or individually",
                "available individually",
                "individually",
                "each",
                "parcel",
                "lot",

                # Membership / fees
                "membership",
                "initiation fee",
                "membership dues",
                "dues",

                # Other non-price dollar amounts
                "upgrades",
                "upgrade",
                "renovation",
                "perimeter walls",
                "garage",
                "business",
                "rental income",
            ]

            strong_negative_terms = [

                "previously listed",
                "previously sold",
                "last sold",

                "originally listed",
                "original list price",
                "original asking price",
                "previous asking price",
                "former asking price",

                "current high bid",
                "starting bid",

                "appraised for",
                "appraised at",
            ]

            # --------------------------------------------------
            # Apply strong penalties
            # --------------------------------------------------

            for term in strong_negative_terms:
                if term in context:
                    score -= 20

            # --------------------------------------------------
            # Apply normal penalties
            # --------------------------------------------------

            for term in negative_terms:
                if term in context:
                    score -= 10

            candidates.append((score, number))

        # --------------------------------------------------
        # Return highest-scoring candidate
        # --------------------------------------------------

        if candidates:

            candidates.sort(
                key=lambda x: x[0],
                reverse=True
            )

            best_score, best_price = candidates[0]

            if best_score >= 0:
                return best_price

        # --------------------------------------------------
        # Price mentioned with keywords
        # --------------------------------------------------

        match = re.search(
            r'(?:listed|listing|asking|offered|priced|price|sale)'
            r'\s*(?:at|for|:)?\s*\$?\s*([\d,]+)',
            cleaned_text,
            re.I
        )

        if match:

            value = match.group(1).replace(",", "").strip()

            if not value:
                return None

            try:
                value = int(value)
            except ValueError:
                return None

            if value >= 100000:
                return value

        return None

    def extract_bathrooms(self, text):
        if not isinstance(text, str):
            return None
        # Normalize Unicode fractions
        text = (
            text.replace("½", ".5")
                .replace("¼", ".25")
                .replace("¾", ".75")
        )
        def normalize_bath(value):
            """
            Normalize bathroom values to match MLS ground truth.
            Half baths are counted as whole bathrooms.
            Example:
                2.5 -> 3
                1.5 -> 2
            """
            value = float(value)
            return int(math.ceil(value))
        patterns = [
            # Numeric bathrooms: 2 bath, 2 baths, 2 bathroom, 2.5 ba
            r'(\d+(?:\.\d+)?)\s*[- ]?(?:bath|baths|bathroom|bathrooms|ba)\b',

            # Written numbers: one bath, two bathrooms
            r'\b(one|two|three|four|five)\s+(?:full\s+|half\s+)?(?:bath|baths|bathroom|bathrooms)\b'
        ]
        number_words = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5
        }
        for pattern in patterns:
            match = re.search(pattern, text, re.I)
            if match:
                value = match.group(1).lower()
                # Numeric values
                if value.replace(".", "", 1).isdigit():
                    return normalize_bath(value)
                # Written numbers
                return number_words[value]
        # Half bath mentions without a number
        # Example: "includes a half bath"
        if re.search(r'\bhalf[- ]bath\b', text, re.I):
            return 1
        # Full bath mentions without a number
        # Example: "one full bath"
        if re.search(r'\bfull[- ]bath\b', text, re.I):
            return 1
        # Plural bathroom mention without count
        if re.search(r'\b(baths|bathrooms)\b', text, re.I):
            return ">1"
        # Singular bathroom mention
        if re.search(r'\b(bath|bathroom)\b', text, re.I):
            return 1
        return None
    
    def extract_sqft(self, text):
        if not isinstance(text, str):
            return None

        patterns = [
            r'(\d[\d,]*)\s*(?:square\s*feet)\b',
            r'(\d[\d,]*)\s*(?:sq\.?\s*ft\.?)\b',
            r'(\d[\d,]*)\s*sqft\b',
            r'(\d[\d,]*)\s*sf\b'
        ]

        # --------------------------------------------------
        # 1. Strongest signal:
        #    "2,350 square feet of living space"
        # --------------------------------------------------

        living_patterns = [
            r'(\d[\d,]*)\s*(?:square\s*feet|sq\.?\s*ft\.?|sqft|sf)'
            r'\s*(?:of\s+)?living\s+(?:space|area)',

            r'living\s+(?:space|area)'
            r'\s*(?:of|is|:)?\s*(\d[\d,]*)\s*'
            r'(?:square\s*feet|sq\.?\s*ft\.?|sqft|sf)'
        ]

        for pattern in living_patterns:

            match = re.search(pattern, text, re.I)

            if match:
                value = match.group(1).replace(",", "")

                if value:
                    return int(value)

        # --------------------------------------------------
        # 2. Find all normal sqft mentions
        # --------------------------------------------------

        candidates = []

        for pattern in patterns:

            for match in re.finditer(pattern, text, re.I):

                value = match.group(1).replace(",", "")

                if not value:
                    continue

                # --------------------------------------------------
                # Look immediately around the sqft mention
                # --------------------------------------------------

                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)

                context = text[start:end].lower()

                # --------------------------------------------------
                # Reject clearly unrelated sqft
                # --------------------------------------------------

                excluded_terms = [
                    "lot",
                    "lot size",
                    "garage",
                    "barn",
                    "stable",
                    "adu",
                    "guest house",
                    "guest home",
                    "studio",
                    "grounds",
                    "patio",
                    "deck",
                    "roof deck"
                ]

                if any(term in context for term in excluded_terms):
                    continue

                candidates.append(
                    (
                        int(value),
                        match.start()
                    )
                )

        # --------------------------------------------------
        # 3. If valid candidates exist, use the first one
        # --------------------------------------------------

        if candidates:
            return candidates[0][0]

        return None
    
    def extract_amenities(self, text):
        amenities = []
        text = text.lower()
        for item in self.taxonomy:
            term = item["term"].lower()
            if term in text:
                amenities.append({
                    "term": item["term"],
                    "category": item["category"]
                })
        return amenities
    
    
    def extract_all(self, text):

        bedrooms = self.extract_bedrooms(text)
        bathrooms = self.extract_bathrooms(text)
        price = self.extract_price(text)
        sqft = self.extract_sqft(text)

        return {
            'bedrooms': bedrooms,
            'bathrooms': bathrooms, 
            'price': price, 
            'sqft': sqft,
            #'amenities': self.extract_amenities(text)
        }
