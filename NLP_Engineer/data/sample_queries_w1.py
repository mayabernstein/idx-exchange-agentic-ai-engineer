# sample_queries_w1.py

WEEK1_QUERIES = [
    # --- Property Search ---
    # Pricing Inquiry 
    (
        "Find homes under $500,000",
        {"price_max": 500000}
    ),
    (
        "Show me houses below 750k in Irvine",
        {
            "city": "Irvine",
            "price_max": 750000
        }
    ),
    (
        "Looking for properties between $800k and $1.2 million",
        {
            "price_min": 800000,
            "price_max": 1200000
        }
    ),
    (
        "Homes priced from 1 million to 2 million",
        {
            "price_min": 1000000,
            "price_max": 2000000
        }
    ),
    (
        "Maximum budget is $900,000",
        {
            "price_max": 900000
        }
    ),
    (
        "I want a luxury home over 2 million",
        {
            "price_min": 2000000
        }
    ),
    (
        "Affordable condos under 600k",
        {
            "property_type": "Condominium",
            "price_max": 600000
        }
    ),
    (
        "Properties around 1.5 million",
        {
            "price_min": 1500000,
            "price_max": 1500000
        }
    ),
    (
        "Homes with a minimum of $700k",
        {
            "price_min": 700000
        }
    ),
    (
        "Show me listings between 500 thousand and 900 thousand",
        {
            "price_min": 500000,
            "price_max": 900000
        }
    ),
    # Bedroom/bathroom queries
    (
        "Find me a 3 bedroom house",
        {
            "bedrooms": 3
        }
    ),
    (
        "Need at least 4 bedrooms",
        {
            "bedrooms_min": 4
        }
    ),
    (
        "Looking for a 2 bedroom condo",
        {
            "bedrooms": 2,
            "property_type": "Condominium"
        }
    ),
    (
        "Show me homes with 5 beds",
        {
            "bedrooms": 5
        }
    ),
    (
        "Need 2 bathrooms minimum",
        {
            "bathrooms_min": 2
        }
    ),
    (
        "Looking for houses with 3.5 baths",
        {
            "bathrooms": 4.0
        }
    ),
    (
        "At least 4 beds and 3 baths",
        {
            "bedrooms_min": 4,
            "bathrooms_min": 3
        }
    ),
    (
        "2 bedroom 2 bathroom condo",
        {
            "bedrooms": 2,
            "bathrooms": 2,
            "property_type": "Condominium"
        }
    ),
    (
        "Need a home with more than 3 bedrooms",
        {
            "bedrooms_min": 4
        }
    ),
    (
        "Show properties with 1 bathroom",
        {
            "bathrooms": 1
        }
    ),

    # Location queries 
    (
        "Homes in Irvine",
        {
            "city": "Irvine"
        }
    ),
    (
        "Find properties in Newport Beach",
        {
            "city": "Newport Beach"
        }
    ),
    (
        "Show me houses in Anaheim",
        {
            "city": "Anaheim"
        }
    ),
    (
        "Looking for condos in Costa Mesa",
        {
            "city": "Costa Mesa",
            "property_type": "Condominium"
        }
    ),
    (
        "Properties near Irvine",
        {
            "city": "Irvine"
        }
    ),
    (
        "Homes located in Laguna Beach",
        {
            "city": "Laguna Beach"
        }
    ),
    (
        "Find me a duplex in Santa Ana",
        {
            "city": "Santa Ana",
            "property_type": "Duplex"
        }
    ),
    (
        "Listings around Huntington Beach",
        {
            "city": "Huntington Beach"
        }
    ),
    (
        "Show homes in Bloomington",
        {
            "city": "Bloomington"
        }
    ),
    (
        "I want a house in Tustin",
        {
            "city": "Tustin"
        }
    ),
    # Amenities
    (
        "Homes with a swimming pool",
        {
            "pool": True
        }
    ),
    (
        "Find properties with ocean views",
        {
            "view": True
        }
    ),
    (
        "Show me homes with fireplaces",
        {
            "fireplace": True
        }
    ),
    (
        "Homes with a dock",
        {
            "amenity": 'Dock'
        }
    ),
    (
        "Looking for a place with a clubhouse properties",
        {
            "amenity": 'Clubhouse'
        }
    ),
    (
        "Find homes with mountain views",
        {
            "view": True
        }
    ),
    (
        "Show me houses with a private pool",
        {
            "pool": True
        }
    ),
    (
        "Properties with fitness center",
        {
            "amenity": 'FitnessCenter'
        }
    ),
    (
        "Homes with community a gaming room",
        {
            "amenity": "GameRoom"
        }
    ),
    (
        "Find condos with a picnic area",
        {
            "property_type": "Condominium",
            "amenity": "PicnicArea"
        }
    ),
    # Negation
    (
        "House without a pool",
        {
            "pool": False
        }
    ),
    (
        "Find houses without fireplaces",
        {
            "fireplace": False
        }
    ),
    (
        "A place with a mountain views",
        {
            "view": True
        }
    ),
    (
        "A place without a fireplace",
        {
            "fireplace": False
        }
    ),

    (
        "Exclude homes with ocean views",
        {
            "view": True
        }
    ),
    # Complex queries
    (
        "Find me a 4 bedroom Irvine home under 1.5 million with a pool",
        {
            "city": "Irvine",
            "bedrooms": 4,
            "price_max": 1500000,
            "pool": True
        }
    ),
    (
        "Looking for a Newport Beach condo with 2 bedrooms and ocean view",
        {
            "city": "Newport Beach",
            "property_type": "Condominium",
            "bedrooms": 2,
            "view": True
        }
    ),

    (
        "Show me houses in Irvine with no HOA under $900k",
        {
            "city": "Irvine",
            "hoa_max": 0,
            "price_max": 900000
        }
    ),
    (
        "Need a 3 bedroom 2 bath home with a fireplace",
        {
            "bedrooms": 3,
            "bathrooms": 2,
            "fireplace": True
        }
    ),
    (
        "Find luxury homes over 2 million with ocean views and a pool",
        {
            "price_min": 2000000,
            "view": True,
            "pool": True
        }
    ),
]