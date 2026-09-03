import { looksLikeEmailRequest } from "./email_intent";

function testEmailIntent() {
    console.log(
        "Send me an email:",
        looksLikeEmailRequest("Send me an email")
    );

    console.log(
        "Email me the listings:",
        looksLikeEmailRequest("Email me the listings")
    );

    console.log(
        "Find homes in Irvine:",
        looksLikeEmailRequest("Find homes in Irvine")
    );

    console.log(
        "What is the market doing?:",
        looksLikeEmailRequest("What is the market doing?")
    );
}

testEmailIntent();