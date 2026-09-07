from scripts.w4_queryparser import SchemaValidator
import pytest

validator = SchemaValidator()
def test_validate_invalid_city():
    with pytest.raises(ValueError, match="Invalid city"):
        validator.validate_query({
            "city": "FakeCity"
        })
def test_validate_invalid_view():
    with pytest.raises(ValueError, match="Invalid view"):
        validator.validate_query({
            "view_type": "Galaxy"
        })
def test_validate_negative_price():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        validator.validate_query({
            "price_max": -100
        })
def test_validate_negative_bedrooms():
    with pytest.raises(ValueError, match="Bedrooms cannot be negative"):
        validator.validate_query({
            "bedrooms": -2
        })
def test_validate_negative_bathrooms():
    with pytest.raises(ValueError, match="Bathrooms cannot be negative"):
        validator.validate_query({
            "bathrooms": -1
        })
def test_validate_negative_sqft():
    with pytest.raises(ValueError, match="Square footage cannot be negative"):
        validator.validate_query({
            "sqft": -1500
        })
def test_validate_negative_hoa():
    with pytest.raises(ValueError, match="HOA fee cannot be negative"):
        validator.validate_query({
            "hoa_max": -200
        })
def test_validate_negative_dom():
    with pytest.raises(ValueError, match="Days on market cannot be negative"):
        validator.validate_query({
            "dom_max": -30
        })
def test_validate_year_too_old():
    with pytest.raises(ValueError, match="Invalid year"):
        validator.validate_query({
            "year_built": 1500
        })
def test_validate_future_year():
    with pytest.raises(ValueError, match="Invalid year"):
        validator.validate_query({
            "year_built": 3000
        })
def test_validate_price_range():
    with pytest.raises(
        ValueError,
        match="Minimum price cannot exceed maximum price"
    ):
        validator.validate_query({
            "price_min": 900000,
            "price_max": 700000
        })
def test_validate_sqft_range():
    with pytest.raises(
        ValueError,
        match="Minimum square footage cannot exceed maximum square footage"
    ):
        validator.validate_query({
            "sqft_min": 3000,
            "sqft_max": 2000
        })
def test_validate_year_range():
    with pytest.raises(
        ValueError,
        match="Minimum year built cannot exceed maximum year built"
    ):
        validator.validate_query({
            "year_built_min": 2020,
            "year_built_max": 2010
        })
def test_validate_valid_filters():
    validator.validate_query({
        "city": "Irvine",
        "price_max": 700000,
        "bedrooms": 3,
        "bathrooms": 2,
        "year_built": 2015
    })