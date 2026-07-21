import { parsePropertyQuery } from "../../week_2/service.ts";
import { searchActiveListings } from "../search/active_listing_w3";
import { getSoldComps } from "../search/sold_comps_w3";
import { formatListing } from "../formatters/format_listing";
import { formatSold } from "../formatters/format_sold";
import { SoldRow } from "../types/types";

// Use propertySearch function to coordinate both functions that connects
// to the two tables (rets_property and california_sold) to allow the AI Agent
// to make queries based on the user's request
export async function propertySearch(userQuery: string) {
    const filters = await parsePropertyQuery(userQuery);

    const listings = await searchActiveListings(filters);

    let soldComps: SoldRow[] = [];

    if (filters.L_City) {
        soldComps = await getSoldComps(filters.L_City);
    }

    return {
        filters,
        listings: listings.map(formatListing),
        soldComps: soldComps.map(formatSold),
    };
}