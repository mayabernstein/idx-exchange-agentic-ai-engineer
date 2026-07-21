import { parsePropertyQuery } from "../../week_2/service"; // week 2 parser
import { getSoldComps } from "../search/sold_comps_w3";
import { formatSold } from "../formatters/format_sold";

async function test() {
    const userQuery = 
    "Show me 3-bedroom condos in Irvine under $1.5M with a pool.";
    // Week 2: NLP parser
    const filters = await parsePropertyQuery(userQuery);
    
    console.log("Filters:");
    console.log(filters);

    // Week 3: Database query
    if( filters.L_City) {
        const soldComps = await getSoldComps(filters.L_City);
        console.log("Number of sold comps:");
        console.log(soldComps.length);
        
        if (soldComps.length > 0) {
            // First formatted sold comp
            const formatted = formatSold(soldComps[0]);

            console.log("First Formatted Sold Comp:");
            console.log(formatted);
        }
    } else {
        console.log("No city found in query");
    }
}

test()
