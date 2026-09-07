from pathlib import Path
import sys
import os 

project_root = os.path.abspath('../')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from scripts.w8_listing_summarizer import ListingSummarizer

BASE_DIR = Path(__file__).resolve().parent.parent

TAXONOMY_PATH = BASE_DIR / "data" / "processed" / "taxonomy.json"
summarizer = ListingSummarizer(
    taxonomy_path=TAXONOMY_PATH
)


remarks = """
Beautiful three-bedroom home located in Irvine's desirable Woodbridge community.
The spacious living room features an open floor plan and abundant natural light.
The kitchen has been recently remodeled with quartz countertops and stainless steel appliances.
The primary bedroom includes a large walk-in closet and updated bathroom.
The private backyard features a sparkling swimming pool and covered patio.
The property also includes an attached two-car garage.
Conveniently located near parks, shopping, restaurants, and highly rated schools.
Schedule your private showing today!
"""


summary = summarizer.extractive_summary(
    remarks,
    num_sentences=2
)


print("Original Listing:")
print(remarks)

print("\nExtractive Summary:")
print(summary)