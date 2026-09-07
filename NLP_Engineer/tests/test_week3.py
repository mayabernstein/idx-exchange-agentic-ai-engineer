import sys
import pandas as pd
from pathlib import Path
import sys
import os 

project_root = os.path.abspath('../')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from scripts.w3_entity_extractor import EntityExtractor, taxonomy


extractor = EntityExtractor(taxonomy)

text = """
Beautiful three-bedroom home in Irvine with 2.5 bathrooms and 2,350 sqft.
"""

print(extractor.extract_all(text))