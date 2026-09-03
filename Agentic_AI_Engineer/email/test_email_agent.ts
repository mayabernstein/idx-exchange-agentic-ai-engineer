import "dotenv/config";

import { emailAgent } from "./email_agent";

function testEmailAgent() {

    const response =
        "I found 3 homes matching your search in Irvine.";

    const result = emailAgent(
        process.env.EMAIL_USER!,
        "search",
        response
    );

    console.log("Email Agent Result:");
    console.log(result);
}

testEmailAgent();