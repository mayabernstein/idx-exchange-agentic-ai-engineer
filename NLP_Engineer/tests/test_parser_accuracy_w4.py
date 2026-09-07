from scripts.w4_queryparser import QueryParser
from data.sample_queries_w1 import WEEK1_QUERIES
import pytest

parser = QueryParser()


def calculate_accuracy(results):

    total_fields = 0
    correct_fields = 0

    for query, expected, actual in results:

        for key, value in expected.items():

            total_fields += 1

            if actual.get(key) == value:
                correct_fields += 1

    return (correct_fields / total_fields) * 100



def test_week1_query_accuracy():

    results = []

    for query, expected in WEEK1_QUERIES:

        try:
            actual = parser.parse(query)

        except ValueError as e:
            actual = {
                "error": str(e)
            }

        results.append(
            (
                query,
                expected,
                actual
            )
        )


    accuracy = calculate_accuracy(results)

    print(f"\nAccuracy: {accuracy:.2f}%")

    
    for query, expected, actual in results:

        for key, value in expected.items():

            if actual.get(key) != value:

                print("\nFAILED:")
                print("Query:", query)
                print("Expected:", expected)
                print("Got:", actual)
                break


    assert accuracy >= 90