import { parsePropertyQuery } from "../../../idx-exchange-nlp-engineer/Agentic_AI_Engineer/week_2/service.ts";
import { handleWeek3Search } from "../../../idx-exchange-nlp-engineer/Agentic_AI_Engineer/mls_engine/skills/handleWeek3Search.ts";

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
/*
export async function tryPropertySearch(message: string) {

    if (!looksLikePropertySearch(message)) {
        return null;
    }

    const filters = await parsePropertyQuery(message);

    const result = await handleWeek3Search({
        filters
    });

    return result;
}
*/