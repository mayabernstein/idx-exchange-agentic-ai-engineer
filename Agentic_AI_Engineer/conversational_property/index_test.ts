import { handlePropertyConversation } from "./index";
import { getSession } from "./session";

console.log("\n--- USER 1 ---");

console.log(
    await handlePropertyConversation(
        "demo-user",
        "Find homes in Irvine"
    )
);

console.log("\nSESSION AFTER USER 1:");
console.log(getSession("demo-user"));

console.log("\n--- USER 2 ---");

console.log(
    await handlePropertyConversation(
        "demo-user",
        "$1.2M"
    )
);

console.log("\nSESSION AFTER USER 2:");
console.log(getSession("demo-user"));

console.log("\n--- USER 3 ---");

console.log(
    await handlePropertyConversation(
        "demo-user",
        "Any"
    )
);

console.log("\nSESSION AFTER USER 3:");
console.log(getSession("demo-user"));