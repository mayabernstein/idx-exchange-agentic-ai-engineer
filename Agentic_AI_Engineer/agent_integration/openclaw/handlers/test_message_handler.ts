import { handleMessage } from "./messageHandler.ts";


async function normalHandler(message: string) {
    return {
        text: `Normal LLM response: ${message}`
    };
}


async function test() {

    const userId = "test-user";


    console.log("=== PROPERTY CONVERSATION TEST ===");


    const messages = [
        "Show me homes in Irvine",
        "under $1.2M",
        "single family",
        "at least 3 bedrooms",
        "2 bathrooms",
        "yes"
    ];


    for (const message of messages) {

        console.log("\nUSER:", message);

        const response = await handleMessage(
            userId,
            message,
            normalHandler
        );

        console.log("BOT:", response);
    }


    console.log("\n=== NORMAL TEST ===");


    const normalResponse = await handleMessage(
        "test-user-2",
        "Tell me a joke",
        normalHandler
    );


    console.log(normalResponse);
}


test();