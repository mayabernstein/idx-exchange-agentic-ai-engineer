import { orchestrate } from "./orchestrator";

async function testOrchestrator() {

    console.log("\n=== TEST 3: MIXED QUERY ===");

    const response = await orchestrate(
        "Find me affordable homes in Pasadena and tell me whether prices are rising.",
        "test-user-mixed"
    );

    console.log(response);
}

testOrchestrator();