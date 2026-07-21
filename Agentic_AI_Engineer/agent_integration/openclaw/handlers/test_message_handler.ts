import { handleMessage } from "./messageHandler.ts";


async function normalHandler(message: string) {
    return {
        response: `Normal LLM response: ${message}`
    };
}


async function test() {

    const propertyQuery =
        "Show me 3 bedroom condos in Irvine under `$1.5M with a pool";


    const normalQuery =
        "Tell me a joke";


    console.log("=== PROPERTY TEST ===");

    console.log(
        await handleMessage(
            propertyQuery,
            normalHandler
        )
    );


    console.log("\n=== NORMAL TEST ===");

    console.log(
        await handleMessage(
            normalQuery,
            normalHandler
        )
    );
}


test();