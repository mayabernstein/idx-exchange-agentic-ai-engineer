import re

class SignalExtractor: 
    def __init__(self, taxonomy, entity_extractor): 
        self.taxonomy = taxonomy 
        self.extractor = entity_extractor 
        
    def extract_signals(self, listing_record): 
        remarks = listing_record.get('cleaned_remarks', '') 

        # Get entities from Week 3 
        entities = self.extractor.extract_all(remarks) 

        # Get amenities from taxonomy 
        amenities = self._match_amenities(remarks) 

        # Detect signals 
        return { 
        'entities': entities, 
        'amenities': amenities, 
        'condition_keywords': self._extract_condition(remarks), 
        'financing_terms': self._extract_financing(remarks), 
        'location_features': self._extract_location(remarks) 
        }

    def _match_amenities(self, remarks):
        matches = []
        remarks = remarks.lower()

        for item in self.taxonomy['terms']:
            term = item['term'].lower()

            if term in remarks:
                matches.append({
                    "term": item["term"],
                    "category": item["category"]
                })

        return matches

    def _extract_condition(self, remarks):

        if not isinstance(remarks, str):
            return []

        condition_patterns = {
            "updated": [
                r"\bupdated\b",
                r"\bupgraded\b",
                r"\bmodernized\b",
            ],

            "renovated": [
                r"\brenovat(?:ed|ion|ions|ing)\b",
            ],

            "remodeled": [
                r"\bremodel(?:ed|ing)?\b",
                r"\bremodeled\b",
                r"\bfully remodeled\b",
                r"\bpartially remodeled\b",
            ],

            "new construction": [
                r"\bnew construction\b",
                r"\bnewly constructed\b",
                r"\bnew construction home\b",
            ],

            "newly built": [
                r"\bnewly built\b",
                r"\bnew build\b",
                r"\bnewly constructed\b",
            ],

            "needs renovation": [
                r"\bneeds renovation\b",
                r"\bneeds renovations\b",
                r"\bneeds updating\b",
                r"\bneeds repair\b",
                r"\bneeds repairs\b",
                r"\bneeds work\b",
                r"\bfixer[- ]upper\b",
                r"\bfixer\b",
            ],

            "move-in ready": [
                r"\bmove[- ]in ready\b",
                r"\bmove[- ]in condition\b",
            ],

            "well-maintained": [
                r"\bwell[- ]maintained\b",
                r"\bwell[- ]kept\b",
                r"\bmeticulously maintained\b",
                r"\bpride of ownership\b",
            ],

            "recently updated": [
                r"\brecently updated\b",
                r"\brecently upgraded\b",
            ],

            "recently renovated": [
                r"\brecently renovated\b",
            ],

            "recently remodeled": [
                r"\brecently remodeled\b",
            ],

            "brand new": [
                r"\bbrand new\b",
            ],
        }

        remarks = remarks.lower()

        matches = []

        for label, patterns in condition_patterns.items():

            for pattern in patterns:

                if re.search(pattern, remarks):
                    matches.append(label)
                    break

        return matches

    def _extract_financing(self, remarks):

        if not isinstance(remarks, str):
            return []

        financing_patterns = {

            "seller financing": [
                r"\bseller financing\b",
                r"\bseller[- ]financed\b",
                r"\bseller[- ]financing\b",
                r"\bseller carry\b",
                r"\bseller carryback\b",
                r"\bseller will finance\b",
            ],

            "owner financing": [
                r"\bowner financing\b",
                r"\bowner[- ]financed\b",
                r"\bowner[- ]financing\b",
                r"\bowner carry\b",
                r"\bowner carryback\b",
                r"\bowner will finance\b",
            ],

            "assumable loan": [
                r"\bassumable loan\b",
                r"\bassumable mortgage\b",
                r"\bloan assumption\b",
                r"\bmortgage assumption\b",
                r"\bassume the loan\b",
                r"\bassume existing loan\b",
            ],

            "financing available": [
                r"\bfinancing available\b",
                r"\bfinancing options?\b",
                r"\bfinancing option\b",
                r"\bfinancing terms\b",
                r"\bfinancing offered\b",
            ],

            "cash only": [
                r"\bcash only\b",
                r"\bcash buyers? only\b",
                r"\bcash purchase\b",
                r"\bcash offers? only\b",
            ],

            "cash offer": [
                r"\bcash offer\b",
                r"\bcash offers\b",
            ],

            "lease option": [
                r"\blease option\b",
                r"\blease[- ]to[- ]own\b",
                r"\brent[- ]to[- ]own\b",
                r"\blease purchase\b",
                r"\blease[- ]purchase\b",
            ],

            "loan approved": [
                r"\bloan approved\b",
                r"\bapproved loan\b",
                r"\bpre[- ]approved\b",
                r"\bpreapproved\b",
            ],
        }

        remarks = remarks.lower()

        matches = []

        for label, patterns in financing_patterns.items():

            for pattern in patterns:

                if re.search(pattern, remarks):
                    matches.append(label)
                    break

        return matches

    def _extract_location(self, remarks):

        if not isinstance(remarks, str):
            return []

        location_patterns = {

            "near schools": [
                r"\bnear schools?\b",
                r"\bclose to schools?\b",
                r"\bclose to local schools?\b",
            ],

            "near shopping": [
                r"\bnear shopping\b",
                r"\bclose to shopping\b",
                r"\bnear shopping centers?\b",
                r"\bclose to shopping centers?\b",
            ],

            "near restaurants": [
                r"\bnear restaurants?\b",
                r"\bclose to restaurants?\b",
                r"\bnear dining\b",
                r"\bclose to dining\b",
            ],

            "near downtown": [
                r"\bnear downtown\b",
                r"\bclose to downtown\b",
                r"\bminutes from downtown\b",
                r"\bnearby downtown\b",
            ],

            "near parks": [
                r"\bnear parks?\b",
                r"\bclose to parks?\b",
                r"\bnearby parks?\b",
            ],

            "freeway access": [
                r"\bnear freeways?\b",
                r"\bclose to freeways?\b",
                r"\beasy freeway access\b",
                r"\beasy access to (?:the )?freeways?\b",
                r"\bfreeway access\b",
                r"\bnear major highways?\b",
                r"\bclose to major highways?\b",
            ],

            "public transportation": [
                r"\bnear public transportation\b",
                r"\bnear public transit\b",
                r"\bnear transit\b",
                r"\bpublic transportation\b",
            ],

            "walking distance": [
                r"\bwalking distance\b",
                r"\bwithin walking distance\b",
                r"\bwalkable\b",
            ],

            "near beach": [
                r"\bnear beaches?\b",
                r"\bclose to beaches?\b",
                r"\bnear the beach\b",
                r"\bclose to the beach\b",
            ],

            "mountain views": [
                r"\bmountain views?\b",
                r"\bviews of the mountains\b",
                r"\bmountain view\b",
            ],

            "hill views": [
                r"\bhill views?\b",
                r"\bhillside views?\b",
            ],

            "city views": [
                r"\bcity views?\b",
                r"\bviews of the city\b",
            ],

            "ocean views": [
                r"\bocean views?\b",
                r"\bocean view\b",
                r"\bviews of the ocean\b",
            ],

            "water views": [
                r"\bwater views?\b",
                r"\bwater view\b",
            ],

            "lake views": [
                r"\blake views?\b",
                r"\blake view\b",
            ],

            "valley views": [
                r"\bvalley views?\b",
                r"\bvalley view\b",
            ],

            "scenic views": [
                r"\bscenic views?\b",
                r"\bscenic view\b",
                r"\bpanoramic views?\b",
                r"\bpanoramic view\b",
            ],

            "golf course": [
                r"\bgolf course\b",
                r"\bgolf course views?\b",
                r"\bgolf course view\b",
            ],

            "private beach access": [
                r"\bprivate beach access\b",
            ],
        }

        remarks = remarks.lower()

        matches = []

        for label, patterns in location_patterns.items():

            for pattern in patterns:

                if re.search(pattern, remarks):
                    matches.append(label)
                    break

        return matches