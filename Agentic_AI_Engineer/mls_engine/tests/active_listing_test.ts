import { parsePropertyQuery } from "../../week_2/service";
import { searchActiveListings } from "../search/active_listing_w3";
import { formatListing } from "../formatters/format_listing";

async function test() {
    const userQuery =
        "Show me 3-bedroom condos in Irvine under $1.5M with a pool.";

    // Week 2: NLP parser
    const filters = await parsePropertyQuery(userQuery);

    console.log("Filters:");
    console.log(filters);

    // Week 3: Database query
    const listings = await searchActiveListings(filters);

    console.log("Number of listings:");
    console.log(listings.length);

    // Make sure we actually got results
    if (listings.length > 0) {
        // Format first result
        const formattedListing = formatListing(listings[0]);

        console.log("First Formatted Property Card:");
        console.log(formattedListing);
    } else {
        console.log("No listings found.");
    }
}

test();