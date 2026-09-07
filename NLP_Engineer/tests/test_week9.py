import os
import sys

project_root = os.path.abspath('../')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from scripts.w9_fair_housing_compliance import ComplianceChecker

test_cases = [

    # ============================================================
    # KNOWN VIOLATIONS - FAMILIAL STATUS
    # ============================================================

    {
        "text": "Beautiful home in an adults only community.",
        "expected_violation": True,
        "category": "familial"
    },
    {
        "text": "No children allowed in this neighborhood.",
        "expected_violation": True,
        "category": "familial"
    },
    {
        "text": "Perfect for singles looking for a quiet home.",
        "expected_violation": True,
        "category": "familial"
    },
    {
        "text": "No kids permitted.",
        "expected_violation": True,
        "category": "familial"
    },
    {
        "text": "Children are not allowed in this community.",
        "expected_violation": True,
        "category": "familial"
    },
    {
        "text": "This adults-only community offers a peaceful environment.",
        "expected_violation": True,
        "category": "familial"
    },


    # ============================================================
    # KNOWN VIOLATIONS - DISABILITY
    # ============================================================

    {
        "text": "Must be able-bodied to access the property.",
        "expected_violation": True,
        "category": "disability"
    },
    {
        "text": "No wheelchairs permitted.",
        "expected_violation": True,
        "category": "disability"
    },
    {
        "text": "Wheelchairs are not allowed.",
        "expected_violation": True,
        "category": "disability"
    },
    {
        "text": "Only able-bodied residents are permitted.",
        "expected_violation": True,
        "category": "disability"
    },
    {
        "text": "This property is for able-bodied individuals only.",
        "expected_violation": True,
        "category": "disability"
    },


    # ============================================================
    # KNOWN VIOLATIONS - RACE / COLOR
    # ============================================================

    {
        "text": "Located in a white neighborhood.",
        "expected_violation": True,
        "category": "race"
    },
    {
        "text": "This is a white community with excellent schools.",
        "expected_violation": True,
        "category": "race"
    },
    {
        "text": "Located in a white community.",
        "expected_violation": True,
        "category": "race"
    },
    {
        "text": "Whites only neighborhood.",
        "expected_violation": True,
        "category": "race"
    },


    # ============================================================
    # KNOWN VIOLATIONS - RELIGION
    # ============================================================

    {
        "text": "Located in a Christian community.",
        "expected_violation": True,
        "category": "religion"
    },
    {
        "text": "Beautiful Jewish neighborhood.",
        "expected_violation": True,
        "category": "religion"
    },
    {
        "text": "Located in a Christian neighborhood.",
        "expected_violation": True,
        "category": "religion"
    },
    {
        "text": "This Muslim community offers a welcoming environment.",
        "expected_violation": True,
        "category": "religion"
    },
    {
        "text": "Located in a Jewish community.",
        "expected_violation": True,
        "category": "religion"
    },


    # ============================================================
    # KNOWN VIOLATIONS - SEX / GENDER
    # ============================================================

    {
        "text": "Women only apartment community.",
        "expected_violation": True,
        "category": "sex"
    },
    {
        "text": "Men only housing.",
        "expected_violation": True,
        "category": "sex"
    },
    {
        "text": "This apartment is for women only.",
        "expected_violation": True,
        "category": "sex"
    },
    {
        "text": "Males only.",
        "expected_violation": True,
        "category": "sex"
    },
    {
        "text": "Females only community.",
        "expected_violation": True,
        "category": "sex"
    },


    # ============================================================
    # KNOWN VIOLATIONS - NATIONAL ORIGIN
    # ============================================================

    {
        "text": "Native-born Americans only.",
        "expected_violation": True,
        "category": "national_origin"
    },
    {
        "text": "Native born only.",
        "expected_violation": True,
        "category": "national_origin"
    },
    {
        "text": "Americans only.",
        "expected_violation": True,
        "category": "national_origin"
    },


    # ============================================================
    # FALSE-POSITIVE / COMPLIANT CASES
    # ============================================================

    {
        "text": "Beautiful three-bedroom home with a spacious backyard.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "Large kitchen with updated appliances and granite countertops.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "Quiet neighborhood near shopping, restaurants, and parks.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "Spacious home with two bathrooms and an attached garage.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "Beautiful community pool and walking trails.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "Family-friendly neighborhood with excellent parks.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "Wheelchair accessible entrance and wide hallways.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "Diverse neighborhood with restaurants and local businesses.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "Ethnic restaurants and cultural attractions are located nearby.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "The home features a bright white kitchen.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "Christian Dior-inspired design elements throughout the home.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "The property includes a private wheelchair-accessible ramp.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "The home has a family room with a fireplace.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "This property is located near a Jewish cultural center.",
        "expected_violation": False,
        "category": None
    },
    {
        "text": "The neighborhood has a Christian church nearby.",
        "expected_violation": False,
        "category": None
    }
]

def evaluate_checker(checker, test_cases):

    true_positives = 0
    false_positives = 0
    false_negatives = 0
    true_negatives = 0

    for case in test_cases:

        result = checker.check_listing(case["text"])

        predicted_violation = not result["compliant"]
        actual_violation = case["expected_violation"]

        if predicted_violation and actual_violation:
            true_positives += 1

        elif predicted_violation and not actual_violation:
            false_positives += 1

        elif not predicted_violation and actual_violation:
            false_negatives += 1

        else:
            true_negatives += 1

    precision = (
        true_positives /
        (true_positives + false_positives)
        if true_positives + false_positives > 0
        else 0
    )

    recall = (
        true_positives /
        (true_positives + false_negatives)
        if true_positives + false_negatives > 0
        else 0
    )

    accuracy = (
        (true_positives + true_negatives) /
        (
            true_positives +
            true_negatives +
            false_positives +
            false_negatives
        )
    )

    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "true_negatives": true_negatives,
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy
    }

def show_evaluation_errors(checker, test_cases):

    for i, case in enumerate(test_cases, start=1):

        result = checker.check_listing(case["text"])

        predicted_violation = not result["compliant"]
        actual_violation = case["expected_violation"]

        if predicted_violation != actual_violation:

            print(f"\nTest case {i} FAILED")
            print(f"Text: {case['text']}")
            print(f"Expected violation: {actual_violation}")
            print(f"Predicted violation: {predicted_violation}")
            print(f"Result: {result}")

if __name__ == "__main__":

    checker = ComplianceChecker()

    results = evaluate_checker(
        checker,
        test_cases
    )

    print("Compliance Checker Evaluation")
    print("-----------------------------")

    print(f"True positives:  {results['true_positives']}")
    print(f"False positives: {results['false_positives']}")
    print(f"False negatives: {results['false_negatives']}")
    print(f"True negatives:  {results['true_negatives']}")

    print(
        f"Precision: {results['precision']:.2%}"
    )

    print(
        f"Recall:    {results['recall']:.2%}"
    )

    print(
        f"Accuracy:  {results['accuracy']:.2%}"
    )
    
    show_evaluation_errors(checker, test_cases)

severity_test_cases = [

    {
        "text": "Adults only community.",
        "expected_severity": "error"
    },

    {
        "text": "Perfect for singles looking for a quiet home.",
        "expected_severity": "warning"
    },

    {
        "text": "Family-friendly neighborhood with parks nearby.",
        "expected_severity": "info"
    },

    {
        "text": "Wheelchair accessible home with an accessible entrance.",
        "expected_severity": "info"
    }
]
def test_severity_levels(checker, test_cases):

    for case in test_cases:

        result = checker.check_listing(case["text"])

        severities = [
            violation["severity"]
            for violation in result["violations"]
        ]

        expected = case["expected_severity"]

        assert expected in severities, (
            f"Expected {expected} for: {case['text']}"
        )

    print("All severity-level tests passed.")

checker = ComplianceChecker()

test_severity_levels(
    checker,
    severity_test_cases
)