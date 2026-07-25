import { handlePropertyConversation } from "../../../conversational_property/index.ts";
import { hasActiveConversation } from "../../../conversational_property/session.ts";

export function looksLikePropertySearch(text: string) {
    return /(bed(room)?|bath|condo|house|townhome|townhouse|single\s*family|irvine|price|under|\$|\d+\s*br|pool)/i.test(text);
}


export async function handlePropertySearch(
    userId: string,
    message: string
) {

    console.log("PROPERTY SEARCH CALLED:", message);

    if (!looksLikePropertySearch(message) &&
        !hasActiveConversation(userId)) {
        return null;
    }

    console.log("PROPERTY SEARCH MATCHED");

    const result = await handlePropertyConversation(
        userId,
        message
    );

    console.log("CONVERSATION RESULT:", result);

    return result;
}


/*import { parsePropertyQuery } from "../../../week_2/service";
import { handleWeek3Search } from "../../../mls_engine/skills/handleWeek3Search";

function looksLikePropertySearch(text: string) {
    return /(bed(room)?|bath|condo|house|townhome|irvine|price|under|\$|\d+\s*br)/i.test(text);
}

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