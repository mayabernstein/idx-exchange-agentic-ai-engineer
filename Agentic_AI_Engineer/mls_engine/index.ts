import { parsePropertyQuery } from "./parser/service";
import { handleWeek3Search } from "./skills/handleWeek3Search";

export async function run(query: string) {

    const filters = await parsePropertyQuery(query);

    return await handleWeek3Search({
        filters
    });
}