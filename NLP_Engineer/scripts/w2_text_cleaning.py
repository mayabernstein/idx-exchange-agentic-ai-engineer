import re
import pandas as pd
from collections import Counter
import re
import unicodedata
import nltk
from pathlib import Path

class TextCleaner: 
    def __init__(self): 
        # Abbreviation map
        self.abbrev_map = { 
        'bd': 'bedroom', 'br': 'bedroom', 'ba': 'bathroom', 'sqft': 'square feet', 
        'w/': 'with', 'w/o': 'without', 'mbr': 'master bedroom', "gar": "garage",
        'adu': 'accessory dwelling unit', 'hoa': 'Homeowners Association',
        'sq ft': 'square feet', 'sq': 'square', 'ft': 'feet', 'condo': 'condominium',
        'rv': 'recreational vehicle', 'ev': 'electric vehicle', 'hvac': 'heating, ventilation, and air conditioning',
        'ac': 'air conditioning', 'sf': 'square feet', 'va': 'Veterans Affairs',
        'fha': 'Federal Housing Administration', 'blvd': 'boulevard', 'bbq': 'barbecue', 'tv': 'television',
        "hwy": "highway", "dr": "drive", "rd": "road", "metro": "metropolitan", "bbqs": "barbecues",
        "apn": "Assessors Parcel Number", "combo": "combination", "lvp": "luxury vinyl plank", 
        "etc": "et cetera", "ct": "court", "mt": "mount", "uc": "university of california",
        "jr": "junior", "pga": "professional golfers' association", "rvs": "recreational vehicles", 
        "fwy": "freeway", "eco": "ecology", "thru": "through", "ucla": "University of California, Los Angeles",
        "decor": "decoration", "oc": "orange county", "socal": "southern california", "dtla": "downtown Los Angeles", 
        "appx": "approximately", "str": "short-term rental", "cvs": "consumer value stores",
        "pusd": "Unified School District", "tlc": "tender loving cleaner", "sofi": "social finance", 
        "bdrm": "bedroom", "sdsu": "San Diego State University", "jadu": "junior accessory dwelling unit",
        "ss": "stainless steel", "spc": "stone plastic composite", "adt": "american district telegraph",
        "ln": "lane", "bdrms": "bedrooms", "flrs": "floors", "fam": "family"
        }
        self.words_to_ignore = {
            "views", "has", "areas", "parks", "doors", "newer", "ll", "feet", "trees", "hills", "flows", 
            "opens", "baths", "multi", "homes", "adds", "dryer", "pools", "cul", "shops", "rooms", "sinks", 
            "walls", "feels", "los", "acres", "steps", "makes", "owned", "sits", "paid", "units", "fans", "years", 
            "dues", "meets", "costs", "ins", "lakes", "mini", "spas", "sets", "meals", "plans", "lines", 
            "spans", "oaks", "mello", "roos", "gates", "decks", "toys", "paths", "fills", "tesla", 
            "taxes", "beds", "stars", "fees", "foods", "cafes", "ve", "pets", "epoxy", "viejo", 
            "beams", "clubs", "gives", "cared", "uses", "shows", "miele", "boxes", "yards", "lives",
            "jolla", "cars", "runs", "cruz", "tiles", "spots", "palms", "loved", "wells", "ovens", "lg", "rey", 
            "paseo", "yorba", "tons", "mahal", "pits", "poway", "looks", "means", "keeps", "vibe", "chefs", 
            "users", "arts", "pre", "com", "ii", "indio", "italy", "petco", "roads", "tones", "woods", "chula", 
            "mateo", "sheds", "zones", "pairs", "mills", "takes", "palos", "cafe", "alta", "famed", "bars", "boats", 
            "farms", "bi", "amp", "brea", "isn", "doesn", "hubs", "paved", "sales", "dacor", "studs", "banks", "sonos", 
            "norco", "laws", "terms", "ones", "app", "pipes", "walks", "edges", "fits", "joes", "co", "hours", "bones", 
            "heads", "lanai", "pours", "pex", "ups", "terra", "helps", "falls", "rates", "aptos", "azul", "hosts", 
            "joses", "perks", "faces", "tubs", "bikes", "fewer", "adams", "youre", "youll", "bays", "bills", "roots",
            "paso", "backs", "dates", "using", "lawns", "iid", "lagos"
        }
        self.stop_words = {
            "and", "the", "a", "with", "to", "in", "of", "for", "this", "is", "an", 
            "or", "on", "from", "that"
        }
        self.proper_case = {
            "hoa",
            "fha",
            "ucla",
            "pusd",
            "apn",
            "sdsu",
            "va"
        }
    def clean_text(self, text): 
        text = self.normalize_html(text)
        text = self.normalize_unicode(text) 
        text = self.normalize_smart_quotes(text)
        text = self.normalize_prices(text) 
        text = self.normalize_measurements(text) 
        text = self.expand_abbreviations(text) 
        text = self.normalize_whitespace(text)
        return text.strip() 
    def normalize_unicode(self, text):
        # Standardizes Unicode forms and removes invisible Unicode characters."""
        if not isinstance(text, str):
            return ""
        # Fix common Windows-1252 mojibake
        text = (
            text.replace("â€™", "'")
                .replace("â€œ", '"')
                .replace("â€\x9d", '"')
                .replace("Â", "")
        )
        # Remove invisible Unicode characters
        text = re.sub(r'[\u200B\u200C\u200D\uFEFF]', '', text)
        # Normalize Unicode representation
        return unicodedata.normalize("NFC", text)
    def normalize_smart_quotes(self, text):
        """Converts curly/smart punctuation to standard straight ASCII characters."""
        if not isinstance(text, str): return ""
        smart_map = {
            '’': "'", '‘': "'", '`': "'",
            '“': '"', '”': '"',
            '–': '-', '—': '-'  # En-dash and em-dash to regular hyphen
        }
        for curly, straight in smart_map.items():
            text = text.replace(curly, straight)
        return text
    def normalize_prices(self, text): 
        if not isinstance(text, str): return ""
        # 450k → 450000 
        text = re.sub(r'\b(\d+\.?\d*)\s*k\b', 
                      lambda m: str(int(float(m.group(1)) * 1000)), 
                      text, 
                      flags=re.I) 
        # 1.2m → 1200000 
        text = re.sub(r'\b(\d+\.?\d*)\s*m\b', 
                      lambda m: str(int(float(m.group(1))*1000000)), 
                      text, 
                      flags=re.I) 
        # $1,200,000 → $1200000
        text = re.sub(
            r'\$(\d{1,3}(?:,\d{3})+)',
            lambda m: "$" + m.group(1).replace(",", ""),
            text
        )
        return text 
    def normalize_measurements(self, text):
        if not isinstance(text, str):
            return ""
        # Standardize square footage abbreviations
        text = re.sub(r'\bsq\.?\s*ft\.?\b|\bsf\b', 'sqft', text, flags=re.I)
        # Remove approximation symbols after numbers
        text = re.sub(r'(\d[\d,]*)\s*(?:±|\+/-|\+)', r'\1', text)
        # Convert dimensions like 10x12 -> 10 by 12
        text = re.sub(r'(\d+)\s*x\s*(\d+)', r'\1 by \2', text, flags=re.I)
        return text
    def normalize_html(self, text):
        """Remove HTML tags while preserving the enclosed text."""
        if not isinstance(text, str):
            return ""

        return re.sub(r"<[^>]+>", "", text)
    def _extract_top_ngrams(self, series, n=20):
        words = []
        for text in series.dropna().astype(str): 
            extracted_words = re.findall(r'\b\w+\b', text.lower())
            filtered_words = [w for w in extracted_words if w not in self.stop_words]
            words.extend(filtered_words)
        return Counter(words).most_common(n)
    def normalize_whitespace(self, text):
        if not isinstance(text, str): return ""
        text = re.sub(r'[\r\n\t]+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    def expand_abbreviations(self, text):
        if not isinstance(text, str):
            return ""
        for abbrev, full in sorted(
            self.abbrev_map.items(),
            key=lambda x: len(x[0]),
            reverse=True
        ):
            if abbrev in ["w/", "w/o"]:
                pattern = rf"{re.escape(abbrev)}(?=\s|$)"
            else:
                pattern = rf"\b{re.escape(abbrev)}\b"
            
            def replace(match):
                original = match.group(0)
                if abbrev in self.proper_case:
                    return full
                if original[0].isupper():
                    return full.capitalize()
                return full.lower()
            text = re.sub(pattern, replace, text, flags=re.I)
        return text
    def _find_hidden_abbreviations(self, series):
        # Load all real English words from NLTK corpus
        english_words = set(w.lower() for w in nltk.corpus.words.words())

        counts = Counter()
        for text in series.dropna().astype(str):
            # Find 2-5 letter words/tokens (including things like
            # w/ or w/o if you adjust regex)
            words = re.findall(r'\b[a-zA-Z]{2,5}\b', text.lower())
            for word in words:
                # If it's not a normal English word and NOT already captured
                if word not in english_words and word not in self.abbrev_map and word not in self.words_to_ignore:
                    counts[word] += 1
            
        # Returns a list of top 20 uncaptured abbreviation
        return counts.most_common(20)
    def _detect_abbreviations(self, series):
        counts = Counter()
        for text in series.dropna():
            words = re.findall(r'\b\w+\b', text.lower())
            for word in words:
                if word in self.abbrev_map:
                    counts[word] += 1
        return counts.most_common(10)
    def _detect_unicode(self, series):
        count = 0
        for text in series.dropna():
            if any(ord(char) > 127 for char in text):
                count += 1
        return count
    def _detect_smart_quotes(self, series):
        pattern = r"[‘’“”]"
        return series.str.contains(pattern, regex=True).sum()
    def _detect_measurements(self, series):
        pattern = r'\d[\d,]*(?:[±+]|\+/-)?\s*(?:square\s+feet|sq\s*ft|sqft|\bsf\b)'
        return series.str.contains(pattern, regex=True, case=False).sum()
    def _detect_dimensions(self, series):
        pattern = r"\b\d+\s*x\s*\d+\b"
        return series.str.contains(pattern, regex=True).sum()
    def _detect_whitespace(self, series):
        pattern = r"[\r\n\t]| {2,}"
        return series.str.contains(pattern, regex=True).sum()
    def identify_phone_numbers(self, text):
        """Finds and standardizes raw phone numbers aggressively, ignoring APN formats."""
        # Clean out APNs first 
        apn_regex = r'\b\d{3,4}-\d{3}-\d{3,4}\b'
        cleaned_text = re.sub(apn_regex, '[PARCEL NUMBER]', text)
        
        # Now find and substitute actual phone layouts
        phone_regex = r'(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        return re.sub(phone_regex, '[PHONE NUMBER]', cleaned_text)
    # Before cleaning, understand what needs cleaning
    def profile_column(self, df, column_name): 
        """Analyze what's actually in L_Remarks""" 
        series = df[column_name]
        apn_regex = r'\b\d{3,4}-\d{3}-\d{3,4}\b'
        phone_regex = r'(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        parcel_count = series.str.contains(apn_regex, regex=True).sum()
        masked_series = series.str.replace(apn_regex, '[PARCEL]', regex=True)
        phone_count = masked_series.str.contains(phone_regex, regex=True).sum()
        return {
            "total_rows": len(series),
            "null_rate": series.isnull().mean(),
            "avg_length": series.str.len().mean(),
            "parcel_number_counts": parcel_count,
            "phone_number_counts": phone_count,
            "common_terms": self._extract_top_ngrams(series),
            "price_mentions":
                series.str.contains(r'\$\d').sum(),
            "has_html":
                series.str.contains('<[^>]+>').sum(),
            "measurement_mentions":
                self._detect_measurements(series),
            "room_dimensions":
                self._detect_dimensions(series),
            "unicode_issues":
                self._detect_unicode(series),
            "smart_quotes":
                self._detect_smart_quotes(series),
            "whitespace_issues":
                self._detect_whitespace(series),
            "common_abbreviations":
                self._detect_abbreviations(series),
            "unknown_abbreviations":
                self._find_hidden_abbreviations(series)
        }

# Use this to guide your cleaning strategy: 
cleaner = TextCleaner()
# ALWAYS works no matter where you run pytest from
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "listing_sample.csv"
df = pd.read_csv(DATA_PATH)
profile = cleaner.profile_column(df, 'remarks') 
print("========== REMARKS PROFILE ==========\n")

print(f"Total listings: {profile['total_rows']}")
print(f"Null rate: {profile['null_rate']:.2%}")
print(f"Average length: {profile['avg_length']:.2f} characters")

print(f"\nPrice mentions: {profile['price_mentions']}")
print(f"Measurement mentions: {profile['measurement_mentions']}")
print(f"Room dimensions: {profile['room_dimensions']}")

print(f"\nHTML tags: {profile['has_html']}")
print(f"Unicode usages: {profile['unicode_issues']}")
print(f"Smart quotes: {profile['smart_quotes']}")
print(f"Whitespace issues: {profile['whitespace_issues']}")
print(f"APN Counts: {profile['parcel_number_counts']}")
print(f"Phone Number Counts: {profile['phone_number_counts']}")

print("\nKnown abbreviations")
for word, count in profile["common_abbreviations"]:
    print(f"{word:8} {count}")

print("\nUnknown abbreviations")
for word, count in profile["unknown_abbreviations"]:
    print(f"{word:8} {count}")

print("\nTop 20 words")
for word, count in profile["common_terms"]:
    print(f"{word:12} {count}")