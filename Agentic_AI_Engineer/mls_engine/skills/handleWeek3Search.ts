import { searchActiveListings } from "../search/active_listing_w3.js";
import { getSoldComps } from "../search/sold_comps_w3.js";
import { formatListing } from "../formatters/format_listing.js";
import { formatSold } from "../formatters/format_sold.js";
import { formatPropertyResponse } from "../formatters/format_response.js";
import type { PropertyFilters } from "../types/types.js";

export async function handleWeek3Search(input: {
    filters: PropertyFilters;
}) {

    console.log("Filters:", input.filters);

    const listings = await searchActiveListings(input.filters);

    console.log("Active listings found:", listings.length);

    const soldComps = input.filters.L_City
        ? await getSoldComps(input.filters.L_City)
        : [];

    const formattedListings = listings.map(formatListing);
    const formattedSoldComps = soldComps.map(formatSold);

    return {
        response: formatPropertyResponse(
            formattedListings,
            formattedSoldComps
        ),
        listings: formattedListings,
        soldComps: formattedSoldComps
    };
}