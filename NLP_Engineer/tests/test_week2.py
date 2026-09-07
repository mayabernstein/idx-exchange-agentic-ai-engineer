import sys
from pathlib import Path
import pytest
import pandas as pd

from scripts.w2_text_cleaning import TextCleaner

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "listing_sample.csv"

def setup_module(module):
    print("\nRunning comprehensive tests for week 2...\n")


# Price Normalization
@pytest.mark.parametrize("input_text, expected_output", [
    # Basic K/M conversions
    ("priced at 450k", "priced at 450000"),
    ("$1.2m home", "$1200000 home"),
    ("Asking 850K", "Asking 850000"),
    ("Value is 3M", "Value is 3000000"),
    # Decimals and rounding stability
    ("costing 1.5k", "costing 1500"),
    ("reduced to 0.75m", "reduced to 750000"),
    ("only 1.234m left", "only 1234000 left"),
    ("priced at $0.5k", "priced at $500"),
    # Spacing issues around multipliers
    ("price is 450 k", "price is 450000"),
    ("asking 1.2 m", "asking 1200000"),
    ("reduced to 750   K", "reduced to 750000"),
    ("Beautiful home listed at $1,200,000.", "Beautiful home listed at $1200000."),
])
def test_price_normalization_edge_cases(input_text, expected_output):
    cleaner = TextCleaner()
    # Assuming your method is named normalize_prices or handles it inside a clean pipeline
    assert cleaner.normalize_prices(input_text) == expected_output
# Structural text cleaning & unicode
@pytest.mark.parametrize("input_text, expected_output", [
    # HTML Tag Stripping
    ("Offers welcome at <span>$450</span>k", "Offers welcome at $450000"),
    ("<div>Beautiful home</div>", "Beautiful home"),
    ("<p>Price reduced!</p>", "Price reduced!"),
    ("Click <a href='#'>here</a> to see", "Click here to see"),

    # Smart & Curly Quotes
    ("Owner noted “$750K” as firm", "Owner noted \"$750000\" as firm"),
    ("Agent‘s notes say ‘firm’", "Agent's notes say 'firm'"),
    ("“Spacious” living area", "\"Spacious\" living area"),
    
    # Unicode & Punctuation Normalization (en-dashes, full-width, non-breaking spaces)
    ("Victorville – Spacious Layout", "Victorville - Spacious Layout"), # en-dash to hyphen
    ("Price is $1.2\xa0m total", "Price is $1200000 total"),       # \xa0 non-breaking space
    ("HOA fee is $250\u200b per month", "Homeowners Association fee is $250 per month"), # Zero-width space

    # Whitespace Chaos (Tabs, multiple spaces, linebreaks)
    ("Price    is   $350k", "Price is $350000"),
    ("Line 1\nLine 2\r\nLine 3", "Line 1 Line 2 Line 3"),
    ("\t\tStunning entry way  ", "Stunning entry way"),
    ("stunning 4,146± square feet", "stunning 4,146 square feet"),
    
    # Non-string data type safety checks
    (None, ""),
    (12345, ""),
])
def test_structural_cleaning_edge_cases(input_text, expected_output):
    cleaner = TextCleaner()
    # Assuming your master clean function is called clean() or clean_text()
    assert cleaner.clean_text(input_text) == expected_output

# Abbreviation Dictionary
@pytest.mark.parametrize("input_text, expected_output", [
    ("Stunning 4 bd, 3 ba home", "Stunning 4 bedroom, 3 bathroom home"),
    ("Large 15k sqft lot", "Large 15000 square feet lot"), # Combined K expansion and text shorthand
    ("Spacious master suite w/ walk-in closet", "Spacious master suite with walk-in closet"),
    ("Includes 2-car gar.", "Includes 2-car garage."),
    ("Hwy 395 commuter route access", "Highway 395 commuter route access"),
    ("New laminate flrs throughout", "New laminate floors throughout"),
    ("Beautiful single fam residence", "Beautiful single family residence"),
    ("There are 4 bdrms at the Liberty Ln.", "There are 4 bedrooms at the Liberty Lane."), 
    ("APN 5571-027-008 (13,570 sq ft)", "Assessors Parcel Number 5571-027-008 (13,570 square feet)"),
    ("w/o kitchen", "without kitchen"),
])
def test_abbreviation_expansion(input_text, expected_output):
    cleaner = TextCleaner()
    # Assuming your method is named expand_abbreviations
    assert cleaner.clean_text(input_text) == expected_output

# More test cases
@pytest.mark.parametrize("input_text, expected_output", [
    # Smart mojibake
    ("Chefâ€™s kitchen", "Chef's kitchen"),
    ("â€œLuxuryâ€\x9d home", '"Luxury" home'),
    ("Beautiful homeÂ", "Beautiful home"),

    # Zero-width characters
    ("Price\u200b reduced", "Price reduced"),
    ("Great\uFEFF home", "Great home"),
    ("Move\u200C in ready", "Move in ready"),

    # Normal unicode should remain
    ("Café style kitchen", "Café style kitchen"),
])
def test_unicode_normalization(input_text, expected_output):
    cleaner = TextCleaner()
    assert cleaner.normalize_unicode(input_text) == expected_output

# Data Profiling Compliance 
def test_profiling_metrics():
    cleaner = TextCleaner()
    
    # Read the data sample safely
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        # Fallback to a mock DataFrame if running isolated unit tests without sample data
        df = pd.DataFrame({'remarks': ["Price $450k", "<div>HTML</div>", None, "Lot 15m"]})
        
    profile = cleaner.profile_column(df, 'remarks')
    
    # Ensure all your deliverable metrics are fully accounted for
    assert 'null_rate' in profile
    assert 'avg_length' in profile
    assert 'price_mentions' in profile
    assert 'has_html' in profile
    assert 'common_abbreviations' in profile  # Making sure profiling matches deliverables