import { classifyIntent } from "./classifyIntent.js";

const classifier = new classifyIntent();
await classifier.initialize();

type TestCase = {
    query: string;
    expectedIntent: string;
    expectedIntents: string[];
};

const testCases: TestCase[] = [

    // =====================================================
    // SINGLE INTENT: SEARCH
    // =====================================================
    {
        query: "Find me a 3 bedroom and a 2 bathroom home with no pool in Irvine.",
        expectedIntent: "search",
        expectedIntents: ["search"]
    },
    {
        query: "Find me a 3 bedroom home in Irvine",
        expectedIntent: "search",
        expectedIntents: ["search"]
    },
    {
        query: "Show me condos in Pasadena",
        expectedIntent: "search",
        expectedIntents: ["search"]
    },
    {
        query: "Search for houses in Anaheim",
        expectedIntent: "search",
        expectedIntents: ["search"]
    },
    {
        query: "Looking for a townhouse in Santa Ana",
        expectedIntent: "search",
        expectedIntents: ["search"]
    },
    {
        query: "Find homes under $700,000 in Irvine",
        expectedIntent: "search",
        expectedIntents: ["search"]
    },


    // =====================================================
    // SINGLE INTENT: MARKET
    // =====================================================

    {
        query: "What is the median price in Irvine?",
        expectedIntent: "market",
        expectedIntents: ["market"]
    },
    {
        query: "Are home prices rising in Pasadena?",
        expectedIntent: "market",
        expectedIntents: ["market"]
    },
    {
        query: "What is the average price in Anaheim?",
        expectedIntent: "market",
        expectedIntents: ["market"]
    },
    {
        query: "How many days on market are homes in Irvine?",
        expectedIntent: "market",
        expectedIntents: ["market"]
    },
    {
        query: "What is the housing trend in Santa Ana?",
        expectedIntent: "market",
        expectedIntents: ["market"]
    },


    // =====================================================
    // SINGLE INTENT: KNOWLEDGE
    // =====================================================

    {
        query: "What does DOM mean?",
        expectedIntent: "knowledge",
        expectedIntents: ["knowledge"]
    },
    {
        query: "What is a list-to-close ratio?",
        expectedIntent: "knowledge",
        expectedIntents: ["knowledge"]
    },
    {
        query: "What does original list price mean?",
        expectedIntent: "knowledge",
        expectedIntents: ["knowledge"]
    },
    {
        query: "What is an MLS field?",
        expectedIntent: "knowledge",
        expectedIntents: ["knowledge"]
    },
    {
        query: "Explain the difference between list price and close price",
        expectedIntent: "knowledge",
        expectedIntents: ["knowledge"]
    },
    {
        query: "What does RESO mean?",
        expectedIntent: "knowledge",
        expectedIntents: ["knowledge"]
    },


    // =====================================================
    // SINGLE INTENT: RECOMMENDATION
    // =====================================================

    {
        query: "Find similar properties",
        expectedIntent: "recommendation",
        expectedIntents: ["recommendation"]
    },
    {
        query: "Recommend similar homes",
        expectedIntent: "recommendation",
        expectedIntents: ["recommendation"]
    },
    {
        query: "Show me properties like this one",
        expectedIntent: "recommendation",
        expectedIntents: ["recommendation"]
    },
    {
        query: "Can you recommend comparable properties?",
        expectedIntent: "recommendation",
        expectedIntents: ["recommendation"]
    },


    // =====================================================
    // MIXED: SEARCH + MARKET
    // =====================================================

    {
        query: "Find me 3 bedroom homes in Irvine and tell me the median price",
        expectedIntent: "mixed",
        expectedIntents: ["search", "market"]
    },
    {
        query: "Show me condos in Pasadena and tell me if prices are rising",
        expectedIntent: "mixed",
        expectedIntents: ["search", "market"]
    },
    {
        query: "Find homes under $800,000 in Irvine and tell me the average days on market",
        expectedIntent: "mixed",
        expectedIntents: ["search", "market"]
    },
    {
        query: "Search for houses in Anaheim and tell me the housing trend",
        expectedIntent: "mixed",
        expectedIntents: ["search", "market"]
    },


    // =====================================================
    // MIXED: SEARCH + RECOMMENDATION
    // =====================================================

    {
        query: "Find me 3 bedroom homes in Irvine and recommend similar properties",
        expectedIntent: "mixed",
        expectedIntents: ["search", "recommendation"]
    },
    {
        query: "Show me condos in Pasadena and find similar properties",
        expectedIntent: "mixed",
        expectedIntents: ["search", "recommendation"]
    },
    {
        query: "Find houses in Anaheim and show me comparable properties",
        expectedIntent: "mixed",
        expectedIntents: ["search", "recommendation"]
    },


    // =====================================================
    // MIXED: MARKET + KNOWLEDGE
    // =====================================================

    {
        query: "What is the median price in Irvine and what does DOM mean?",
        expectedIntent: "mixed",
        expectedIntents: ["market", "knowledge"]
    },
    {
        query: "Tell me the housing trend in Pasadena and explain what days on market means",
        expectedIntent: "mixed",
        expectedIntents: ["market", "knowledge"]
    },
    {
        query: "What is the average price in Anaheim and what is a list-to-close ratio?",
        expectedIntent: "mixed",
        expectedIntents: ["market", "knowledge"]
    },


    // =====================================================
    // MIXED: SEARCH + MARKET + KNOWLEDGE
    // =====================================================

    {
        query: "Find me 3 bedroom homes in Irvine, tell me the median price, and explain what DOM means",
        expectedIntent: "mixed",
        expectedIntents: ["search", "market", "knowledge"]
    },
    {
        query: "Show me condos in Pasadena, tell me the housing trend, and explain list-to-close ratio",
        expectedIntent: "mixed",
        expectedIntents: ["search", "market", "knowledge"]
    },


    // =====================================================
    // MIXED: SEARCH + MARKET + RECOMMENDATION
    // =====================================================

    {
        query: "Find me condos in Pasadena, tell me the median price, and recommend similar properties",
        expectedIntent: "mixed",
        expectedIntents: ["search", "market", "recommendation"]
    },
    {
        query: "Find homes in Irvine, tell me the average price, and show me similar properties",
        expectedIntent: "mixed",
        expectedIntents: ["search", "market", "recommendation"]
    },


    // =====================================================
    // MIXED: ALL FOUR
    // =====================================================

    {
        query: "Find me 3 bedroom homes in Irvine, tell me the median price, explain DOM, and recommend similar properties",
        expectedIntent: "mixed",
        expectedIntents: [
            "search",
            "market",
            "knowledge",
            "recommendation"
        ]
    },


    // =====================================================
    // COMMA-BASED MIXED QUERIES
    // =====================================================

    {
        query: "Find me homes in Irvine, tell me the median price",
        expectedIntent: "mixed",
        expectedIntents: ["search", "market"]
    },
    {
        query: "Find me homes in Irvine and recommend similar properties",
        expectedIntent: "mixed",
        expectedIntents: ["search", "recommendation"]
    },
    {
        query: "What is the median price in Irvine, explain DOM", // fail due to the comma (only market, but expects market + knowledge)
        expectedIntent: "mixed",
        expectedIntents: ["market", "knowledge"]
    },


    // =====================================================
    // UNCATEGORIZED
    // =====================================================

    {
        query: "Hello",
        expectedIntent: "uncategorized",
        expectedIntents: []
    },
    {
        query: "How are you?",
        expectedIntent: "uncategorized",
        expectedIntents: []
    },
    {
        query: "Tell me something interesting",
        expectedIntent: "uncategorized",
        expectedIntents: []
    }
];


// =====================================================
// RUN TESTS
// =====================================================

let passed = 0;
let failed = 0;

console.log("========================================");
console.log("INTENT CLASSIFIER TESTS");
console.log("========================================");

for (const test of testCases) {

    const result = await classifier.classify(
        test.query,
        "test-user"
    );

    const detectedIntents = result.intents;

    const intentsMatch =
        JSON.stringify(detectedIntents) ===
        JSON.stringify(test.expectedIntents);

    const intentMatch =
        result.intent === test.expectedIntent;

    const passedTest =
        intentsMatch && intentMatch;

    if (passedTest) {
        passed++;
    } else {
        failed++;
    }

    console.log("----------------------------------------");
    console.log(`Query: ${test.query}`);
    console.log(`Expected: ${JSON.stringify(test.expectedIntents)}`);
    console.log(`Detected: ${JSON.stringify(detectedIntents)}`);
    console.log(`Expected Overall Intent: ${test.expectedIntent}`);
    console.log(`Detected Overall Intent: ${result.intent}`);
    console.log(`Result: ${passedTest ? "PASS" : "FAIL"}`);

    if (!passedTest) {
        console.log("Segments:");
        console.log(result.segments);
    }
}

console.log("----------------------------------------");
console.log(`PASSED: ${passed}`);
console.log(`FAILED: ${failed}`);
console.log(`TOTAL: ${testCases.length}`);
console.log("========================================");