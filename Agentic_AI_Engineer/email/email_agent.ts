import { draftEmail } from "./email";
import { formatEmail } from "./email_formatter";

type EmailTopic = 
    | "search"
    | "market"
    | "recommendation"
    | "knowledge";

export function emailAgent(
    to: string,
    topic: string,
    response: string
) {
    let subject: string;

    switch (topic) {
        case "search":
            subject = "New Listings Matching Your Search";
            break;

        case "market":
            subject = "Weekly California Market Report";
            break;

        case "recommendation":
            subject = "Personalized Property Recommendations";
            break;

        case "knowledge":
            subject = "Real Estate Information";
            break;

        default:
            subject = "Real Estate Information";
    }

    const formattedEmail = formatEmail(subject, response);

    return draftEmail(
        to, 
        formattedEmail.subject,
        formattedEmail.body
    );
}