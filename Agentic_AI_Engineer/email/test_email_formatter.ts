import { formatEmail } from "./email_formatter";

function testFormatEmail() {
    const result = formatEmail(
        "New Listings Matching Your Search",
        "I found 3 homes matching your search."
    );

    console.log("Formatted Email:");
    console.log(result);
}

testFormatEmail();