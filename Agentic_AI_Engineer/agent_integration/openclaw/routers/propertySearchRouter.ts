import { parsePropertyQuery } from "../../../week_2/service";
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