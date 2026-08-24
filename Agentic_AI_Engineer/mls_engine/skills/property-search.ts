//import { parsePropertyQuery } from "../../../idx-exchange-nlp-engineer/Agentic_AI_Engineer/week_2/service.ts";
//import { handleWeek3Search } from "../../../idx-exchange-nlp-engineer/Agentic_AI_Engineer/mls_engine/skills/handleWeek3Search.ts";
import { handlePropertyConversation } from "../../conversational_property/index";
import { hasActiveConversation } from "../../conversational_property/session";
import { formatPropertyResponse } from "../../mls_engine/formatters/format_response";
import { formatListing } from "../../mls_engine/formatters/format_listing";
import { semanticPropertySearch } from "../../embeddings/semanticSearch";

function looksLikePropertySearch(text: string) {
    return /(\d+\s*(bed|bedroom|br)|\d+\s*(bath|bathroom|ba)|condo|townhome|townhouse|single\s+family|active\s+listing|show\s+me|find\s+homes|listings?|properties?|homes?\s+under|\$\d+)/i.test(text);
}
function looksLikeSemanticSearch(text: string) {
    return /(charming|character|cozy|luxurious|spacious|modern|elegant|beautiful|scenic|mountain views|ocean views|natural light|open concept|quiet|peaceful|craftsman|entertaining)/i.test(text);
}

export async function tryPropertySearch(userId: string, message: string) {
    console.log("PROPERTY SEARCH CALLED:", message);

    if (looksLikeSemanticSearch(message)) {
            console.log("SEMANTIC SEARCH MATCHED");
    
            const results = await semanticPropertySearch(message);
            console.log("SEMANTIC RESULTS:", results);

            const formattedListings = results.map(formatListing);
    
            const response = {
                complete: true, 
                message: formatPropertyResponse(
                formattedListings,
                []
            ),
            results: formattedListings
        };
        return response;
    } 

    if (!looksLikePropertySearch(message) && !hasActiveConversation(userId)) {
        const response = {
            complete: false,
            message: "",
            results: []
        }; 
        return response;
    }

    console.log("PROPERTY SEARCH MATCHED");

    const result = await handlePropertyConversation(
        userId,
        message
    );

    console.log("CONVERSATION RESULT:", result);

    if (result.complete && result.results) {
        return {
            complete: true,
            message: `${result.message}\n\n${formatPropertyResponse(
            result.results,
            []
        )}`,
        results: result.results
        };
    }
    const response = {
        complete: result.complete,
        message: result.message,
        results: result.results ?? []
    }
    
    return response;
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