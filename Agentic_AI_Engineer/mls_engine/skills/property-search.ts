//import { parsePropertyQuery } from "../../../idx-exchange-nlp-engineer/Agentic_AI_Engineer/week_2/service.ts";
//import { handleWeek3Search } from "../../../idx-exchange-nlp-engineer/Agentic_AI_Engineer/mls_engine/skills/handleWeek3Search.ts";
import { handlePropertyConversation } from "../conversational_property/index";
import { hasActiveConversation } from "../conversational_property/session";
import { formatPropertyResponse } from "../mls_engine/formatters/format_response";
function looksLikePropertySearch(text: string) {
    return /(bed(room)?|bath|condo|house|townhome|irvine|price|under|\$|\d+\s*br)/i.test(text);
}

export async function tryPropertySearch(userId: string, message: string) {
    console.log("PROPERTY SEARCH CALLED:", message);

    if (!looksLikePropertySearch(message) && !hasActiveConversation(userId)) {
        return null; 
    }

    console.log("PROPERTY SEARCH MATCHED");

    const result = await handlePropertyConversation(
        userId,
        message
    );

    console.log("CONVERSATION RESULT:", result);

    if (result.complete && result.results) {
        return `${result.message}\n\n${formatPropertyResponse(
            result.results,
            []
        )}`;
    }

    return result.message;
}
/*
function looksLikePropertySearch(text: string) {
    return /(bed(room)?|bath|condo|house|townhome|irvine|price|under|\$|\d+\s*br)/i.test(text);
}

export async function tryPropertySearch(message: string) {
    console.log("PROPERTY SEARCH CALLED:", message);

    if (!looksLikePropertySearch(message))
        return null;

    console.log("PROPERTY SEARCH MATCHED");

    const filters = await parsePropertyQuery(message);

    console.log("FILTERS:", filters);

    const result = await handleWeek3Search({
        filters
    });

    console.log("MLS RESULT:", result);

    return result.response;
}
*/