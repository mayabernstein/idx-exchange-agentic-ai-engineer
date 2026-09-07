from scripts.w4_queryparser import QueryParser
import pytest

parser = QueryParser()

@pytest.mark.parametrize(
    "query, expected",
    [
        ("House under 700k ", 700000),
        ("less than 1m", 1000000),
        ("below 1.5m", 1500000),
        ("condo under 650k", 650000),
    ],
)
def test_price_parser(query, expected):
    result = parser.parse(query)
    assert result["price_max"] == expected
@pytest.mark.parametrize(
    "query, expected",
    [
        # New upper bound patterns
        (
            "homes above 500k",
            {
                "price_min":500000
            }
        ),
        (
            "properties over $750000",
            {
                "price_min":750000
            }
        ),
        (
            "houses more than 1m",
            {
                "price_min":1000000
            }
        ),
        # Price ranges
        (
            "homes between 500k and 700k",
            {
                "price_min":500000,
                "price_max":700000
            }
        ),
        (
            "houses 500k-700k",
            {
                "price_min":500000,
                "price_max":700000
            }
        ),
        (
            "properties from $400k to $600k",
            {
                "price_min":400000,
                "price_max":600000
            }
        )
    ]
)
def test_price_patterns2(query, expected):
    result = parser.parse(query)
    for key,value in expected.items():
        assert result[key] == value
@pytest.mark.parametrize(
    "query, expected",
    [
        ("3-bed", 3),
        ("3 bed", 3),
        ("3 bedroom", 3),
        ("3 bedrooms", 3),
        ("3 br", 3),
    ],
)
def test_bedroom_variations(query, expected):
    result = parser.parse(query)
    assert result["bedrooms"] == expected

def test_more_than_three_bed():
    result = parser.parse("3+ bed")
    assert result["bedrooms_min"] == 3

@pytest.mark.parametrize(
    "query, expected",
    [
        ("3-bath", 3),
        ("3 bath", 3),
        ("3 bathroom", 3),
        ("3 bathrooms", 3),
        ("3 ba", 3),
        ("2.5 baths", 3)
    ],
)
def test_bathroom_variations(query, expected):
    result = parser.parse(query)
    assert result["bathrooms"] == expected


def test_more_than_three_bath():
    result = parser.parse("3+ bath")
    assert result["bathrooms_min"] == 3

@pytest.mark.parametrize(
    "query, expected_city, expected_property_type",
    [
        ("Homes in Irvine", "Irvine", None),
        ("Condos in Campbell", "Campbell", "Condominium"),
        ("Studios in Delano", "Delano", "Studio"),
        ("Townhouses in Lake Almanor", "Lake Almanor", "Townhouse"),
        ("Duplexes in Pacheco", "Pacheco", "Duplex"),
    ],
)
def test_property_type_and_city(query, expected_city, expected_property_type):
    result = parser.parse(query)
    assert result["city"] == expected_city
    if expected_property_type:
        assert result["property_type"] == expected_property_type
    else:
        assert "property_type" not in result

def test_city():
    result = parser.parse("Homes in Irvine")
    assert result["city"] == "Irvine"

def test_pool():
    result = parser.parse("Homes with a pool in Irvine")
    assert result["pool"] == True

    result = parser.parse("Homes without a pool in Irvine")
    assert result["pool"] == False

@pytest.mark.parametrize(
    "query, expected",
    [
        ("home with fireplace", True),
        ("home has fireplace", True),
        ("home without fireplace", False),
        ("home no fireplace", False),
        ("fireplace excluded", False),
    ],
)
def test_fireplace_negation(query, expected):

    result = parser.parse(query)

    assert result["fireplace"] == expected

@pytest.mark.parametrize(
    "query, expected",
    [
        ("ocean view home", True),
        ("home with a view", True),
        ("home without a view", False),
        ("home no view", False),
    ],
)
def test_view_negation(query, expected):

    result = parser.parse(query)

    assert result["view"] == expected

@pytest.mark.parametrize(
    "query, expected",
    [
        ("Homes with a pool", True),
        ("Homes has pool", True),
        ("Homes including pool", True),
        ("Homes without a pool", False),
        ("Homes no pool", False),
        ("Homes excluding pool", False),
        ("Homes with no pool", False),
    ],
)
def test_pool_negation(query, expected):
    result = parser.parse(query)
    assert result["pool"] == expected

@pytest.mark.parametrize(
    "query, expected",
    [
        ("2000 sqft", 2000),
        ("2000 sq ft", 2000),
        ("2000 square feet", 2000),
        ("1500 SF", 1500),
    ],
)
def test_sqft_variations(query, expected):
    result = parser.parse(query)
    assert result["sqft"] == expected
@pytest.mark.parametrize(
    "query, expected",
    [
        ("over 2000 sqft", 2000),
        ("above 1500 sq ft", 1500),
        ("more than 2500 square feet", 2500),
        ("at least 3000 sqft", 3000),
    ],
)
def test_sqft_minimum(query, expected):
    result = parser.parse(query)
    assert result["sqft_min"] == expected
@pytest.mark.parametrize(
    "query, expected",
    [
        ("under 3000 sqft", 3000),
        ("below 2500 sq ft", 2500),
        ("less than 1800 square feet", 1800),
    ],
)
def test_sqft_maximum(query, expected):
    result = parser.parse(query)
    assert result["sqft_max"] == expected
@pytest.mark.parametrize(
    "query, minimum, maximum",
    [
        ("between 1500 and 2500 sqft", 1500, 2500),
        ("1500-2500 sqft", 1500, 2500),
        ("from 2000 to 3000 sq ft", 2000, 3000),
    ],
)
def test_sqft_range(query, minimum, maximum):
    result = parser.parse(query)
    assert result["sqft_min"] == minimum
    assert result["sqft_max"] == maximum
@pytest.mark.parametrize(
    "query, expected",
    [
        ("Ocean view condo", "Ocean"),
        ("Mountain view home", "Mountains"),
        ("Marina view property", "Marina"),
        ("Bay view house", "Bay"),
        ("Panoramic view condo", "Panoramic"),
    ],
)
def test_view_types(query, expected):
    result = parser.parse(query)
    assert result["view_type"] == expected
@pytest.mark.parametrize(
    "query, expected",
    [
        ("built after 2020", 2020),
        ("built since 2015", 2015),
        ("newer than 2018", 2018),
    ],
)
def test_year_built_min(query, expected):
    result = parser.parse(query)
    assert result["year_built_min"] == expected
@pytest.mark.parametrize(
    "query, expected",
    [
        ("built before 1990", 1990),
        ("older than 1970", 1970),
    ],
)
def test_year_built_max(query, expected):
    result = parser.parse(query)
    assert result["year_built_max"] == expected
def test_exact_year_built():
    result = parser.parse("homes built in 2005")
    assert result["year_built"] == 2005
@pytest.mark.parametrize(
    "query, expected",
    [
        ("under 30 days on market", 30),
        ("less than 10 DOM", 10),
        ("below 15 days on market", 15),
    ],
)
def test_days_on_market_max(query, expected):
    result = parser.parse(query)
    assert result["dom_max"] == expected
def test_days_on_market_min():
    result = parser.parse(
        "over 100 days on market"
    )
    assert result["dom_min"] == 100
@pytest.mark.parametrize(
    "query, expected",
    [
        ("HOA under 500", 500),
        ("association fee below 300", 300),
    ],
)
def test_hoa_max(query, expected):
    result = parser.parse(query)
    assert result["hoa_max"] == expected
def test_hoa_min():
    result = parser.parse(
        "HOA over 100"
    )
    assert result["hoa_min"] == 100
@pytest.mark.parametrize(
    "query, expected",
    [
        ("condo with a fire pit", "FirePit"),
        ("home with pets allowed", "PetsAllowed"),
        ("property with clubhouse", "Clubhouse"),
    ],
)
def test_association_amenities(query, expected):
    result = parser.parse(query)
    assert result["amenity"] == expected
def test_price_and_bedrooms():
    parser = QueryParser()
    result = parser.parse("3 bedrooms under 700k")

    assert result["bedrooms"] == 3
    assert result["price_max"] == 700000

def test_price_and_city():
    parser = QueryParser()
    result = parser.parse("Homes under 700k in Irvine")

    assert result["city"] == "Irvine"
    assert result["price_max"] == 700000