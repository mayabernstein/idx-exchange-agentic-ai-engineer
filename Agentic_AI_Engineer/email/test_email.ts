import "dotenv/config";

import {
    approveEmail,
    sendApprovedEmail
} from "../email/email";

import { emailAgent } from "../email/email_agent";

import readline from "readline/promises";
import { stdin as input, stdout as output } from "process";

async function testEmail() {

    const rl = readline.createInterface({
        input,
        output
    });

    const to = process.env.EMAIL_USER!;

    const testCases = [
        {
            topic: "search",
            response:
                "I found 3 homes matching your search in Irvine."
        },
        {
            topic: "market",
            response:
                "The Irvine market has a median sale price of $1.2 million. " +
                "Homes are averaging 24 days on market."
        },
        {
            topic: "recommendation",
            response:
                "I found 3 properties similar to the home you were interested in."
        },
        {
            topic: "knowledge",
            response:
                "A seller's market occurs when demand for homes is greater " +
                "than the available inventory."
        }
    ];

    for (const testCase of testCases) {

        console.log("\n==============================");
        console.log(`Testing: ${testCase.topic}`);
        console.log("==============================");

        const draft = emailAgent(
            to,
            testCase.topic,
            testCase.response
        );

        console.log("\nEMAIL DRAFT");
        console.log("To: [hidden]");
        console.log("Subject:", draft.draft.subject);
        console.log("Body:", draft.draft.body);
        console.log("Status:", draft.status);

        const answer = await rl.question(
            "\nSend this email? (y/n): "
        );

        if (answer.trim().toLowerCase() === "y") {

            const approved = approveEmail(draft, true);

            console.log("\nApproval status:", approved.status);

            const result = await sendApprovedEmail(approved);

            console.log(result);

        } else {

            const rejected = approveEmail(draft, false);

            console.log("\nApproval status:", rejected.status);
            console.log("Email was NOT sent.");
        }
    }

    rl.close();
}

testEmail();