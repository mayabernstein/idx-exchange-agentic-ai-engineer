import re
import sqlite3
import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import math

load_dotenv()
def get_connection():
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )

        return conn

class QueryParser: 
    def __init__(self):
        self.valid_cities = self._load_valid_cities()
        self.valid_views = self._load_valid_views()
        self.valid_amenities = self._load_valid_amenities()
        self.amenity_aliases = {
            "pets allowed": "PetsAllowed",
            "pet allowed": "PetsAllowed",
            "allows pets": "PetsAllowed",
            "pet friendly": "PetsAllowed",
            "pets": "PetsAllowed",

            "fitness center": "FitnessCenter",
            "sport court": "SportCourt",
            "dog park": "DogPark",
            "fire pit": "FirePit",
            "gaming room": "GameRoom",
            "outdoor cooking area": "OutdoorCookingArea",
            "picnic area": "PicnicArea",
            "billiard room": "BilliardRoom", 
            "golf course": "GolfCourse"
        }
        self.property_types = {
            # BoatSlip
            "boatslip": "BoatSlip",
            "boatslips": "BoatSlip",
            "boat slip": "BoatSlip",
            "boat slips": "BoatSlip",
            "boatdock": "BoatSlip",
            "boat dock": "BoatSlip",
            "marina berth": "BoatSlip",
            "wet slip": "BoatSlip",

            # Cabin
            "cabin": "Cabin",
            "cabins": "Cabin",
            "cottage": "Cabin",
            "cottages": "Cabin",
            "lodge": "Cabin",
            "chalet": "Cabin",

            # CoOwnership
            "coownership": "CoOwnership",
            "co-ownership": "CoOwnership",
            "fractional ownership": "CoOwnership",
            "shared equity": "CoOwnership",
            "tic": "CoOwnership",
            "tenancy in common": "CoOwnership",

            # Condominium
            "condo": "Condominium",
            "condos": "Condominium", 
            "condominium": "Condominium",
            "condominiums": "Condominium",

            # Duplex
            "duplex": "Duplex",
            "duplexes": "Duplex",
            "two-family": "Duplex",
            "2-family": "Duplex",
            "twin home": "Duplex",

            # Farm
            "farm": "Farm",
            "farms": "Farm",
            "farmland": "Farm",
            "ranch": "Farm",
            "ranches": "Farm",
            "acreage": "Farm",
            "hobby farm": "Farm",

            # Loft
            "loft": "Loft",
            "lofts": "Loft",
            "studio loft": "Loft",

            # ManufacturedHome
            "manufacturedhome": "ManufacturedHome",
            "manufactured home": "ManufacturedHome",
            "manufactured homes": "ManufacturedHome",
            "prefab": "ManufacturedHome",
            "prefab home": "ManufacturedHome",
            "factory-built home": "ManufacturedHome",

            # ManufacturedOnLand
            "manufacturedonland": "ManufacturedOnLand",
            "manufactured on land": "ManufacturedOnLand",
            "land-owned prefab": "ManufacturedOnLand",
            "manufactured with land": "ManufacturedOnLand",

            # MixedUse
            "mixeduse": "MixedUse",
            "mixed-use": "MixedUse",
            "mixed use": "MixedUse",
            "live-work": "MixedUse",
            "live/work": "MixedUse",

            # MobileHome
            "mobilehome": "MobileHome",
            "mobile home": "MobileHome",
            "mobile homes": "MobileHome",
            "trailer": "MobileHome",
            "trailers": "MobileHome",

            # OwnYourOwn
            "ownyourown": "OwnYourOwn",
            "own your own": "OwnYourOwn",
            "oyo": "OwnYourOwn",

            # Quadruplex
            "quadruplex": "Quadruplex",
            "quadruplexes": "Quadruplex",
            "fourplex": "Quadruplex",
            "fourplexes": "Quadruplex",
            "four-family": "Quadruplex",
            "4-family": "Quadruplex",

            # SingleFamilyResidence
            "singlefamilyresidence": "SingleFamilyResidence",
            "single family residence": "SingleFamilyResidence",
            "single-family residence": "SingleFamilyResidence",
            "sfr": "SingleFamilyResidence",
            "single family home": "SingleFamilyResidence",
            "single family": "SingleFamilyResidence",

            # StockCooperative
            "stockcooperative": "StockCooperative",
            "stock cooperative": "StockCooperative",
            "coop": "StockCooperative",
            "co-op": "StockCooperative",
            "cooperatives": "StockCooperative",
            "housing cooperative": "StockCooperative",

            # Studio
            "studio": "Studio",
            "studios": "Studio",
            "studio apartment": "Studio",
            "efficiency": "Studio",
            "bachelor apartment": "Studio",

            # Timeshare
            "timeshare": "Timeshare",
            "timeshares": "Timeshare",
            "vacation ownership": "Timeshare",
            "interval ownership": "Timeshare",

            # Townhouse
            "townhouse": "Townhouse",
            "townhouses": "Townhouse",
            "townhome": "Townhouse",
            "townhomes": "Townhouse",
            "row house": "Townhouse",
            "rowhouse": "Townhouse",

            # Triplex
            "triplex": "Triplex",
            "triplexes": "Triplex",
            "three-family": "Triplex",
            "3-family": "Triplex",
            "threeplex": "Triplex",
        }

    def parse(self, query): 
        filters = {} 
        # Price ranges
        if match := re.search(
            r'(?:between|from)\s+\$?([\d,\.]+)\s*(k|m|million|thousand)?\s+(?:and|to)\s+\$?([\d,\.]+)\s*(k|m|million|thousand)?',
            query,
            re.I
        ):
            filters["price_min"] = self._parse_number(
                match.group(1),
                match.group(2)
            )

            filters["price_max"] = self._parse_number(
                match.group(3),
                match.group(4)
            )


        # Hyphen ranges
        elif match := re.search(
            r'\$?([\d,\.]+)\s*(k|m|million|thousand)?\s*-\s*\$?([\d,\.]+)\s*(k|m|million|thousand)?',
            query,
            re.I
        ):
            filters["price_min"] = self._parse_number(
                match.group(1),
                match.group(2)
            )

            filters["price_max"] = self._parse_number(
                match.group(3),
                match.group(4)
            )
        # Approximate price
        elif match := re.search(
            r'(around|about|approximately|roughly)\s+\$?([\d,\.]+)\s*(k|m|million|thousand)?',
            query,
            re.I
        ):
            value = self._parse_number(
                match.group(2),
                match.group(3)
            )

            filters["price_min"] = value
            filters["price_max"] = value

        # Maximum price
        elif match := re.search(
            r'(under|below|less than|max(?:imum)?|budget is)\s+\$?([\d,\.]+)\s*(k|m|million|thousand)?',
            query,
            re.I
        ):
            filters["price_max"] = self._parse_number(
                match.group(2),
                match.group(3)
            )


        # Minimum price
        elif match := re.search(
            r'(above|over|more than|minimum|min)(?:\s+price)?(?:\s+of)?\s+\$?([\d,\.]+)\s*(k|m|million|thousand)?',
            query,
            re.I
        ):
            filters["price_min"] = self._parse_number(
                match.group(2),
                match.group(3)
            )
        # Bedroom patterns 
        if match := re.search(
            r'(?:at least|minimum|min|more than|over)?\s*(\d+)\+?[\s-]*(?:bed|beds|bedroom|bedrooms|br)',
            query,
            re.I
        ):
            number = int(match.group(1))
            text = match.group(0).lower()

            if (
                "+" in text
                or "at least" in text
                or "minimum" in text
                or "min" in text
            ):
                filters["bedrooms_min"] = number

            elif "more than" in text or "over" in text:
                filters["bedrooms_min"] = number + 1

            else:
                filters["bedrooms"] = number
        # Shared minimum intent applies to bathrooms
        if re.search(r'\b(at least|minimum|min|more than|over)\b', query, re.I):
            if match := re.search(
                r'(\d+(?:\.\d+)?)\s*(?:bath|baths|bathroom|bathrooms|ba)',
                query,
                re.I
            ):
                filters["bathrooms_min"] = math.floor(
                    float(match.group(1)) + 0.5
                )
        # Bathroom patterns
        # Minimum bathroom queries
        if match := re.search(
            r'(?:(at least|minimum|min|more than|over)\s+)?'
            r'(\d+(?:\.\d+)?)\+?[\s-]*'
            r'(?:bath|baths|bathroom|bathrooms|ba)'
            r'(?:\s+(minimum|min|at least))?',
            query,
            re.I
        ):
            value = math.floor(float(match.group(2)) + 0.5)

            text = match.group(0).lower()

            if (
                "+" in text
                or "at least" in text
                or "minimum" in text
                or "min" in text
            ):
                filters["bathrooms_min"] = value

            elif "more than" in text or "over" in text:
                filters["bathrooms_min"] = value + 1

            else:
                filters["bathrooms"] = value
        # City patterns
        for city in self.valid_cities:
            if re.search(
                rf'\b{re.escape(city)}\b',
                query,
                re.I
            ):
                filters["city"] = city
                break

        # Property type patterns
        for keyword, db_value in self.property_types.items():
            pattern = rf"\b{re.escape(keyword)}\b"
            if re.search(pattern, query, re.I):
                filters["property_type"] = db_value
                break

        # Pool patterns
        if re.search(
            r"\b(without|no|exclude|excluding|not)\s+(a\s+)?(?:swimming\s+|private\s+)?pool\b",
            query,
            re.I
        ):
            filters["pool"] = False

        elif re.search(
            r"\b(with|has|include|including)?\s*(a\s+)?(?:swimming\s+|private\s+)?pool\b",
            query,
            re.I
        ):
            filters["pool"] = True


        # View patterns
        if re.search(
            r"\b(without|no|exclude|excluding|not)\s+(a\s+)?(?:ocean\s+|mountain\s+|waterfront\s+)?views?\b",
            query,
            re.I
        ):
            filters["view"] = False

        elif re.search(
            r"\b(with|has|include|including)?\s*(a\s+)?(?:ocean\s+|mountain\s+|waterfront\s+)?views?\b",
            query,
            re.I
        ):
            filters["view"] = True


        # Fireplace patterns
        if re.search(
            r"\b(without|no|exclude|excluding|not)\s+(a\s+)?fireplaces?\b"
            r"|\bfireplace\s+excluded\b",
            query,
            re.I
        ):
            filters["fireplace"] = False

        elif re.search(
            r"\b(with|has|include|including)?\s*(a\s+)?fireplaces?\b"
            r"|\bfireplace\s+included\b",
            query,
            re.I
        ):
            filters["fireplace"] = True

        # Square footage patterns
        # Range
        if match := re.search(
            r'(?:between|from)\s+(\d+)\s+(?:and|to)\s+(\d+)\s*(?:sq\s*ft|sqft|square\s+feet)',
            query,
            re.I
        ):
            filters["sqft_min"] = int(match.group(1))
            filters["sqft_max"] = int(match.group(2))
        elif match := re.search(
            r'(\d+)\s*-\s*(\d+)\s*(?:sq\s*ft|sqft|square\s+feet)',
            query,
            re.I
        ):
            filters["sqft_min"] = int(match.group(1))
            filters["sqft_max"] = int(match.group(2))
        # Minimum
        elif match := re.search(
            r'(?:over|above|more than|at least)\s+(\d+)\s*(?:sq\s*ft|SF|sqft|square\s+feet)',
            query,
            re.I
        ):
            filters["sqft_min"] = int(match.group(1))
        # Maximum
        elif match := re.search(
            r'(?:under|below|less than)\s+(\d+)\s*(?:sq\s*ft|SF|sqft|square\s+feet)',
            query,
            re.I
        ):
            filters["sqft_max"] = int(match.group(1))
        # Exact
        elif match := re.search(
            r'(\d+)\s*(?:sq\s*ft|SF|sqft|square\s+feet)',
            query,
            re.I
        ):
            filters["sqft"] = int(match.group(1))

        # View type patterns
        for view in self.valid_views:
            normalized_view = view.lower()

            # Mountain(s) view = Mountains
            # Handle singular/plural differences
            singular_view = normalized_view.rstrip("s")
            pattern = rf"\b({re.escape(normalized_view)}|{re.escape(singular_view)})\s+view\b"
            if re.search(pattern, query, re.I):
                filters["view_type"] = view
                break

        # Year Built patterns
        # Minimum
        if match := re.search(
            r'(?:built after|built since|newer than|after)\s+(\d{4})',
            query,
            re.I
        ):
            filters["year_built_min"] = int(match.group(1))
        # Maximum
        elif match := re.search(
            r'(?:built before|older than|before)\s+(\d{4})',
            query,
            re.I
        ):
            filters["year_built_max"] = int(match.group(1))
        # Exact
        elif match := re.search(
            r'built (?:in|on)\s+(\d{4})',
            query,
            re.I
        ):
            filters["year_built"] = int(match.group(1))

        # Days on Market patterns
        if match := re.search(
            r'(?:under|less than|below)\s+(\d+)\s*(?:days?\s+on\s+market|dom)',
            query,
            re.I
        ):
            filters["dom_max"] = int(match.group(1))

        elif match := re.search(
            r'(?:over|more than|above)\s+(\d+)\s*(?:days?\s+on\s+market|dom)',
            query,
            re.I
        ):
            filters["dom_min"] = int(match.group(1))

        # Association Fee / HOA patterns

        # First handle no HOA cases
        if re.search(
            r"\b(no|without|exclude|excluding|zero)\s+(hoa|association\s+fee|association\s+fees?)\b",
            query,
            re.I
        ):
            filters["hoa_max"] = 0

        # Then handle HOA ranges
        elif match := re.search(
            r"(?:hoa|association\s+fee|association\s+fees?)\s+(under|below|less than)\s+\$?([\d.]+)([km]?)",
            query,
            re.I
        ):
            filters["hoa_max"] = self._parse_number(
                match.group(2),
                match.group(3)
            )

        elif match := re.search(
            r"(?:hoa|association\s+fee|association\s+fees?)\s+(over|above|more than)\s+\$?([\d.]+)([km]?)",
            query,
            re.I
        ):
            filters["hoa_min"] = self._parse_number(
                match.group(2),
                match.group(3)
            )

        # Association amenities
        # Only generic amenities should reach this section

        # Have their own columns
        excluded_amenities = {
            "Pool",
            "Fireplace",
            "View"
        }

        # First check aliases
        for keyword, db_value in self.amenity_aliases.items():

            if db_value in excluded_amenities:
                continue

            if re.search(
                rf"\b{re.escape(keyword)}\b",
                query,
                re.I
            ):
                filters["amenity"] = db_value
                break


        # Then check database amenities
        else:
            for amenity in self.valid_amenities:

                if amenity in excluded_amenities:
                    continue

                if re.search(
                    rf"\b{re.escape(amenity)}\b",
                    query,
                    re.I
                ):
                    filters["amenity"] = amenity
                    break

        return filters
    
    def _parse_number(self, number, suffix=""):
        '''
        Convert values like:
        700k -> 700000
        1m -> 1000000
        1.5 million -> 1500000
        500,000 -> 500000
        '''
        number = number.replace(",", "")
        value = float(number)
        # Handles None from sqft/dom/hoa parsing
        suffix = (suffix or "").lower().strip()

        if suffix in ("k", "thousand"):
            value *= 1000

        elif suffix in ("m", "million"):
            value *= 1000000

        return int(value)
    
    def _load_valid_cities(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT DISTINCT L_City
        FROM rets_property
        WHERE L_City IS NOT NULL
        ORDER BY L_City
        """
        cursor.execute(query)
        cities = {row[0] for row in cursor.fetchall()}

        cursor.close()
        conn.close()

        return sorted(cities, key=len, reverse=True)
    def _load_valid_views(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT DISTINCT View
        FROM rets_property
        WHERE View IS NOT NULL
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        views = set()
        for row in rows:
            values = row[0].split(",")
            for value in values:
                views.add(value.strip())

        return sorted(views, key=len, reverse=True)
    def _load_valid_amenities(self):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT DISTINCT AssociationAmenities
        FROM rets_property
        WHERE AssociationAmenities IS NOT NULL
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        amenities = set()

        for row in rows:
            values = row[0].split(",")

            for value in values:
                amenities.add(value.strip())

        return sorted(
            amenities,
            key=len,
            reverse=True
        )
    
    def to_sql(self, filters): 
        conditions = [] 
        params = [] 

        if 'price_max' in filters: 
            conditions.append('L_SystemPrice <= %s') 
            params.append(filters['price_max']) 

        if 'price_min' in filters: 
            conditions.append('L_SystemPrice >= %s') 
            params.append(filters['price_min']) 

        if 'bedrooms' in filters: 
            conditions.append('L_Keyword2 = %s') 
            params.append(filters['bedrooms']) 

        if 'bedrooms_min' in filters: 
            conditions.append('L_Keyword2 >= %s') 
            params.append(filters['bedrooms_min']) 

        if 'bathrooms' in filters: 
            conditions.append('LM_Dec_3 = %s') 
            params.append(filters['bathrooms'])

        if 'bathrooms_min' in filters:
            conditions.append('LM_Dec_3 >= %s')
            params.append(filters['bathrooms_min'])

        if 'city' in filters:
            conditions.append('L_City = %s')
            params.append(filters['city'])

        if 'year_built_min' in filters:
            conditions.append('YearBuilt >= %s')
            params.append(filters['year_built_min'])

        if 'year_built_max' in filters:
            conditions.append('YearBuilt <= %s')
            params.append(filters['year_built_max'])

        if 'year_built' in filters:
            conditions.append('YearBuilt = %s')
            params.append(filters['year_built'])

        if "dom_max" in filters:
            conditions.append(
                "DaysOnMarket <= %s"
            )
            params.append(
                filters["dom_max"]
            )

        if "dom_min" in filters:
            conditions.append(
                "DaysOnMarket >= %s"
            )
            params.append(
                filters["dom_min"]
            )

        if "hoa_max" in filters:
            conditions.append(
                "AssociationFee <= %s"
            )
            params.append(
                filters["hoa_max"]
            )

        if "hoa_min" in filters:
            conditions.append(
                "AssociationFee >= %s"
            )
            params.append(
                filters["hoa_min"]
            )

        if 'sqft' in filters:
            conditions.append('LM_Int2_3 = %s')
            params.append(filters['sqft'])

        if 'sqft_min' in filters:
            conditions.append('LM_Int2_3 >= %s')
            params.append(filters['sqft_min'])

        if 'sqft_max' in filters:
            conditions.append('LM_Int2_3 <= %s')
            params.append(filters['sqft_max'])

        if 'property_type' in filters:
            conditions.append('L_Type_ = %s')
            params.append(filters['property_type'])

        if 'view_type' in filters:
            conditions.append('FIND_IN_SET(%s, View)')
            params.append(f"%{filters['view_type']}%")

        if 'view' in filters:
            if filters['view']:
                conditions.append('ViewYN = 1')
            else:
                conditions.append('ViewYN IS NULL')

        if 'fireplace' in filters:
                    if filters['fireplace']:
                        conditions.append('FireplaceYN = 1')
                    else:
                        conditions.append('FireplaceYN IS NULL')

        if 'pool' in filters:
                    if filters['pool']:
                        conditions.append('PoolPrivateYN = 1')
                    else:
                        conditions.append('PoolPrivateYN IS NULL')

        if 'amenity' in filters:
            conditions.append('FIND_IN_SET(%s, AssociationAmenities)')
            params.append(f"%{filters['amenity']}%")
        where_clause = ' AND '.join(conditions) 
        
        if not conditions:
            return None, []

        return f"SELECT * FROM rets_property WHERE {where_clause}", params 



class SchemaValidator:
    def __init__(self):
        self.valid_cities = self._load_valid_cities()
        self.valid_views = self._load_valid_views()
        self.valid_amenities = self._load_valid_amenities()

    def validate_query(self, filters):
        errors = []
            
        if "city" in filters:
            city = filters['city']
            if city not in self.valid_cities:
                errors.append("Invalid city")
        if "view_type" in filters:
            if filters["view_type"] not in self.valid_views:
                errors.append(
                    f"Invalid view: {filters['view_type']}"
                )
        if "amenity" in filters:
            if filters["amenity"] not in self.valid_amenities:
                errors.append(
                    f"Invalid amenity: {filters['amenity']}"
                )
        if (
            "price_min" in filters
            and "price_max" in filters
            and filters["price_min"] > filters["price_max"]
        ):
            errors.append("Minimum price cannot exceed maximum price")

        if "bedrooms" in filters and filters["bedrooms"] < 0:
            errors.append("Bedrooms cannot be negative")

        if "bathrooms" in filters and filters["bathrooms"] < 0:
            errors.append("Bathrooms cannot be negative")
        for key in ("price_min", "price_max"):
                if key in filters and filters[key] < 0:
                    errors.append("Price cannot be negative")
        for key in ("sqft", "sqft_min", "sqft_max"):
            if key in filters and filters[key] < 0:
                errors.append("Square footage cannot be negative")
        if (
            "sqft_min" in filters
            and "sqft_max" in filters
            and filters["sqft_min"] > filters["sqft_max"]
        ):
            errors.append("Minimum square footage cannot exceed maximum square footage")
        for key in ("hoa_min", "hoa_max"):
            if key in filters and filters[key] < 0:
                errors.append("HOA fee cannot be negative")
        if (
            "hoa_min" in filters
            and "hoa_max" in filters
            and filters["hoa_min"] > filters["hoa_max"]
        ):
            errors.append("Minimum HOA fee cannot exceed maximum HOA fee")
        for key in ("dom_min", "dom_max"):
            if key in filters and filters[key] < 0:
                errors.append("Days on market cannot be negative")
        if (
            "dom_min" in filters
            and "dom_max" in filters
            and filters["dom_min"] > filters["dom_max"]
        ):
            errors.append("Minimum DOM cannot exceed maximum DOM")
        for key in ("year_built", "year_built_min", "year_built_max"):
            if key in filters:
                if filters[key] < 1792 or filters[key] > 2026:
                    errors.append(f"Invalid {key.replace('_', ' ')}")
        if (
            "year_built_min" in filters
            and "year_built_max" in filters
            and filters["year_built_min"] > filters["year_built_max"]
        ):
            errors.append("Minimum year built cannot exceed maximum year built")
        for key in ("pool", "view", "fireplace"):
            if key in filters and not isinstance(filters[key], bool):
                errors.append(f"{key} must be True or False")
        if errors:
            raise ValueError("; ".join(errors))

        return filters
     
    def _parse_number(self, number, suffix=""):
        '''
        Convert values like:
        700k -> 700000
        1m -> 1000000
        1.5 million -> 1500000
        500,000 -> 500000
        '''
        number = number.replace(",", "")
        value = float(number)
        # Handles None from sqft/dom/hoa parsing
        suffix = (suffix or "").lower().strip()

        if suffix in ("k", "thousand"):
            value *= 1000

        elif suffix in ("m", "million"):
            value *= 1000000

        return int(value)
    def _load_valid_cities(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT DISTINCT L_City
        FROM rets_property
        WHERE L_City IS NOT NULL
        ORDER BY L_City
        """
        cursor.execute(query)
        cities = {row[0] for row in cursor.fetchall()}

        cursor.close()
        conn.close()

        return sorted(cities, key=len, reverse=True)
    def _load_valid_views(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        SELECT DISTINCT View
        FROM rets_property
        WHERE View IS NOT NULL
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        views = set()
        for row in rows:
            values = row[0].split(",")
            for value in values:
                views.add(value.strip())

        return sorted(views, key=len, reverse=True)
    def _load_valid_amenities(self):
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT DISTINCT AssociationAmenities
        FROM rets_property
        WHERE AssociationAmenities IS NOT NULL
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        amenities = set()

        for row in rows:
            values = row[0].split(",")

            for value in values:
                amenities.add(value.strip())

        return sorted(
            amenities,
            key=len,
            reverse=True
        )
    
    