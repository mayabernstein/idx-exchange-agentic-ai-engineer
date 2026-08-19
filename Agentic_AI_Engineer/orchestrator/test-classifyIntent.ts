import { classifyIntent } from "./classifyIntent.js";

const classifier = new classifyIntent();
await classifier.initialize();

// Note: Make sure to run npx tsx orchestrator/test-classifyIntent.ts from Agentic_AI_Engineer base directory
const tests = [
    "Find me a 3 bedroom home in Irvine", // search
    "What is the median price in Irvine?", // market
    "Find properties similar to this one", // recommendation
    "What does DOM mean?", // knowledge
    "Find me affordable homes in Pasadena and tell me whether prices are rising", // mixed
    "What is the difference between list price and close price?", // knowledge
    "Test me a joke" // uncategorized
];

for (const query of tests) {

    const intent = await classifier.classify(
        query,
        "test-user"
    );

    console.log("\nQuery:", query);
    console.log("Intent:", intent);
}