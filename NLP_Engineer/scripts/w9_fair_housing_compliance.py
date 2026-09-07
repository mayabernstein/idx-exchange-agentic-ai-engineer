import re
class ComplianceChecker: 
    def __init__(self): 
        self.prohibited_patterns = { 
            'familial': {
                'error': [
                    r'\bno children\b', 
                    r'\bchildren not allowed\b',
                    r'\bchildren are not allowed\b',
                    r'\bno kids\b',
                    r'\bkids not allowed\b',
                    r'\badults only\b',
                    r'\badults-only\b'
                ],
                'warning': [
                    r'\bperfect for singles\b', 
                    r'\bideal for singles\b',
                    r'\bnot suitable for families\b',
                    r'\bperfect for couples\b'
                ],
                'info': [
                    r'\bfamily-friendly\b',
                    r'\bfamily friendly\b', 
                    r'\bideal for families\b'
                ]
            }, 
            'disability': {
                'error': [
                    r'\bno wheelchairs\b',
                    r'\bwheelchairs not allowed\b',
                    r'\bwheelchairs are not allowed\b',
                    r'\bonly able[- ]bodied\b',
                    r'\bmust be able[- ]bodied\b',
                    r'\bable[- ]bodied only\b',
                    r'\bfor able[- ]bodied individuals only\b'
                ],
                'warning': [
                    r'\bnot wheelchair accessible\b',
                    r'\bno wheelchair access\b'
                ],
                'info': [
                    r'\bwheelchair accessible\b',
                    r'\baccessible home\b',
                    r'\baccessible property\b'
                ]
            },
            'race': {
                'error': [
                    r'\bwhite neighborhood\b',
                    r'\bwhite community\b',
                    r'\bwhites only\b'
                ],
                'warning': [
                    r'\bexclusive neighborhood\b',
                    r'\bexclusive community\b'
                ]
            },

            'religion': {
                'error': [
                    r'\bchristian community\b',
                    r'\bchristian neighborhood\b',
                    r'\bjewish neighborhood\b',
                    r'\bjewish community\b',
                    r'\bmuslim neighborhood\b',
                    r'\bmuslim community\b'
                ]
            },

            'sex': {
                'error': [
                    r'\bmen only\b',
                    r'\bwomen only\b',
                    r'\bmales only\b',
                    r'\bfemales only\b'
                ],
                'warning': [
                    r'\bperfect for women\b',
                    r'\bperfect for men\b'
                ]
            },

            'national_origin': {
                'error': [
                    r'\bnative[- ]born only\b',
                    r'\bamericans only\b'
                ]
            }
        }

    def check_listing(self, text): 

        if not isinstance(text, str):
            return {
                'compliant': True,
                'can_public': True,
                'violations': []
            }
        violations = []

        text_lower = text.lower()

        for category, severity_patterns in self.prohibited_patterns.items():
            for severity, patterns in severity_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, text_lower):
                        matched_text = re.search(pattern, text_lower).group()

                        violations.append({
                            'category': category,
                            'pattern': matched_text,
                            'severity': severity,
                            'message': self._get_message(
                                category,
                                matched_text,
                                severity
                            )
                        })
        has_errors = any(
            violation['severity'] == 'error'
            for violation in violations
        )

        has_warnings = any(
            violation['severity'] == 'warning'
            for violation in violations
        )

        return {
            'compliant': not (has_errors or has_warnings),
            'can_publish': not has_errors,
            'violations': violations
        }
    
    def _get_message(self, category, pattern, severity):

        if severity == 'error':
            return (
                f'Potential Fair Housing violation: '
                f'"{pattern}". Remove or revise before publication.'
            )

        elif severity == 'warning':
            return (
                f'Potentially problematic Fair Housing language: '
                f'"{pattern}". Human review recommended.'
            )

        elif severity == 'info':
            return (
                f'Fair Housing review note: '
                f'"{pattern}". Consider the context of this language.'
            )
        
    def submit_listing(listing, checker):

        result = checker.check_listing(
            listing["remarks"]
        )

        if not result["can_publish"]:

            return {
                "status": "blocked",
                "message": "Listing requires compliance review.",
                "violations": result["violations"]
            }

        return {
            "status": "approved",
            "message": "Listing passed Fair Housing compliance screening.",
            "listing": listing
        }