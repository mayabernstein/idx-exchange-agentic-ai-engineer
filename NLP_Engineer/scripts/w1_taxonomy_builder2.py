import nltk
import json
import pandas as pd
from collections import Counter
from nltk.util import ngrams
from nltk.corpus import stopwords
#nltk.download('stopwords')

# Load data
df = pd.read_csv(
    "../data/processed/listing_sample.csv"
)

# Combine remarks
text = " ".join(
    df["remarks"]
    .dropna()
    .astype(str)
    .str.lower()
)

# Tokenize
tokens = nltk.word_tokenize(text)

# Remove stop words
stop_words = set(stopwords.words("english"))

tokens = [
    token 
    for token in tokens
    if token.isalpha()
    and token not in stop_words
]

# Generate bigrams + trigrams
bigrams = list(ngrams(tokens, 2))
trigrams = list(ngrams(tokens, 3))

phrases = (
    [" ".join(x) for x in bigrams]
    +
    [" ".join(x) for x in trigrams]
)

# Count phrases
freq = Counter(phrases)

# Candidate real estate terms
candidates = [
    {
        "term": phrase,
        "count": count
    }
    for phrase, count in freq.most_common(500)
]

# Categories
categories = {
    "kitchen": [
        "kitchen",
        "granite countertops",
        "stainless steel",
        "island", 
        "sink", 
        "oven",
        "stove", 
        "pantry", 
        "cabinets", 
        "countertops", 
        "bar",
        "cooktop",
        "refrigerator", 
        "microwave", 
        "garbage",
        "disposal",
        "dishwater", 
        "fridge", 
        "beverage", "combo"
    ],

    "flooring": [
        "hardwood floors",
        "tile floor",
        "wood floors", 
        "engineered hardwood",
        "laminate flooring",
        "tile flooring",
        "ceramic tile",
        "porcelain tile",
        "vinyl flooring",
        "luxury vinyl plank",
        "lvp",
        "carpet",
        "carpeted bedrooms",
        "stone flooring",
        "polished concrete",
        "new flooring",
        "upgraded flooring",
        "floors",
        "floor",
        "spc", "flrs", "tile"
    ],

    "outdoor": [
        "pool",
        "patio",
        "deck",
        "backyard",
        "fenced yard",
        "large backyard",
        "private yard",
        "private backyard",
        "porch", 
        "front porch", 
        "balcony",
        "outdoor kitchen",
        "pool", "pools", "trees", 
        "yards", "decks", 
        "swimming pool", 
        "heated pool", 
        "spa", 
        "hot tub", 
        "garden", 
        "landscaping", 
        "sprinkler system", 
        "path", "lawn", "lanai", 
        "pit", "farm"
    ],

    "parking": [
        "garage",
        "car garage",
        "attached garage",
        "detached garage",
        "oversized garage",
        "driveway", "cars", 
        "carport", 
        "RV parking", 
        "covered parking", 
        "gar", 
        "rv",
        "rvs", 
        "ev"
    ],

    "housing_layout": [
        "master suite",
        "walk closet",
        "living room",
        "mbr", 
        "single story", 
        "master bedroom", 
        "guest bedroom", 
        "office", 
        "family room", 
        "living room", 
        "dining room", 
        "walk-in closest",
        "media room", 
        "large bedroom",
        "bedroom", "rooms", 
        "bd", 
        "br", 
        "bdrm", 
        "bdrms", 
        "bedrooms", 
        "bathroom",
        "suite", 
        "bath", "decor"
    ],

    "housing_features": [
        "fireplace",
        "high ceilings",
        "open floor", 
        "ac", "hvac", 
        "gas fireplace", 
        "vaulted ceilings", 
        "high ceilings", 
        "natural light", 
        "energy efficient", 
        "smart home", 
        "security system", 
        "solar panels", 
        "new roof", 
        "new windows", 
        "laundry room", 
        "laundry", 
        "mud room", 
        "hub", 
        "basement", 
        "attic", 
        "storage space", 
        "hvac", "adu", 
        "jadu", "bbq", "ss", 
    ],

    "location": [
        "near schools",
        "downtown",
        "quiet neighborhood", 
        "suburban", 
        "urban", 
        "established neighborhood", 
        "corner lost", 
        "cul-de-sac", 
        "near shopping", 
        "near parks",
        "waterfront", 
        "lake view", 
        "mountain view", 
        "golf course", 
        "convenient location",
        "university", "views", 
        "UCLA", 
        "ucla",
        "SDSU", 
        "sdsu",
        "USC", 
        "near campus", 
        "college", 
        "shopping", 
        "town", "oc", "socal", 
        "SoCal", "dtla", "pga"
    ],

    "community_amenities": [
        "clubhouse",
        "fitness center",
        "community pool",
        "pool", 
        "gym", 
        "tennis court", 
        "playground", 
        "walking trails", 
        "gated community", 
        "HOA", 
        "community center", 
        "dog park",
        "recreation center", 
        "neighborhood park"
    ]
}

# Assign category
taxonomy_terms = []

term_id = 1

for item in candidates:

    phrase = item["term"]

    assigned_category = None

    for category, words in categories.items():
        
        for word in words:

            if word in phrase:
                assigned_category = category
                break

        if assigned_category:
            break


    if assigned_category:
        taxonomy_terms.append(
            {
                "id": term_id,
                "term": phrase,
                "category": assigned_category,
                "frequency": item["count"]
            }
        )
        term_id += 1


    if len(taxonomy_terms) >= 200:
        break

# Save taxonomy

output = {
    "categories": list(categories.keys()),
    "terms": taxonomy_terms
}

with open(
    "../data/processed/taxonomy.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        output,
        f,
        indent=4
    )

print(
    f"Created taxonomy with {len(taxonomy_terms)} terms"
)

# Output: Many are stop words (e.g. and, the, etc.). If we want to perform a better analysis 
# on the remarks, it would be best to focus on looking into more informative terms. 

# Let's save the top 200 bigrams and counts as a json file
'''import json

results = [
    {
        "bigram": " ".join(bigram),
        "count": count
    }
    for bigram, count in freq.most_common(200)
]

with open("data/processed/taxonomy.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

print("Saved to taxonomy.json")'''