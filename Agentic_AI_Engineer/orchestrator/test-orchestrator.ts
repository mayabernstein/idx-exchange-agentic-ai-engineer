import { orchestrate } from "./orchestrator.js";

async function runTests() {

    const userId = "test-user";

    console.log("\n=== TEST 1: PROPERTY SEARCH ===");

    const searchResponse = await orchestrate(
        "Find me a 3 bedroom home in Irvine",
        userId
    );

    console.log(searchResponse);


    console.log("\n=== TEST 2: MARKET ===");

    const marketResponse = await orchestrate(
        "What is the median price in Irvine?",
        userId
    );

    console.log(marketResponse);


    console.log("\n=== TEST 3: RECOMMENDATION ===");

    const recommendationResponse = await orchestrate(
        "Find properties similar to this one",
        userId
    );

    console.log(recommendationResponse);


    console.log("\n=== TEST 4: KNOWLEDGE / RAG ===");

    const ragResponse = await orchestrate(
        "What does DOM mean?",
        userId
    );

    console.log(ragResponse);


    console.log("\n=== TEST 5: MIXED QUERY ===");

    const mixedResponse = await orchestrate(
        "Find me affordable homes in Pasadena and tell me whether prices are rising",
        userId
    );

    console.log(mixedResponse);


    console.log("\n=== TEST 6: UNCATEGORIZED ===");

    const unknownResponse = await orchestrate(
        "What's the weather tomorrow?",
        userId
    );

    console.log(unknownResponse);
}

runTests();