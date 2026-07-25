import { getSession, updateSession, clearSession } from "./session";
import { continueConversation } from "./workflow";


async function runTests() {

    const userId = "test-user";


    console.log("\n--- TEST 1: City only ---");

    clearSession(userId);

    updateSession(userId, {
        city: "Irvine"
    });

    console.log(
        await continueConversation(userId)
    );


    console.log("\n--- TEST 2: Add budget ---");

    updateSession(userId, {
        maxPrice: 1200000
    });

    console.log(
        await continueConversation(userId)
    );


    console.log("\n--- TEST 3: Add bedrooms ---");

    updateSession(userId, {
        beds: 3
    });

    console.log(
        await continueConversation(userId)
    );


    console.log("\n--- TEST 4: Add property type ---");

    updateSession(userId, {
        type: "SingleFamilyResidence"
    });

    console.log(
        await continueConversation(userId)
    );


    console.log("\n--- TEST 5: Add bathrooms ---");

    updateSession(userId, {
        baths: 2
    });

    console.log(
        await continueConversation(userId)
    );


    console.log("\n--- TEST 6: Add pool ---");

    updateSession(userId, {
        pool: false
    });

    console.log(
        await continueConversation(userId)
    );
}


runTests();