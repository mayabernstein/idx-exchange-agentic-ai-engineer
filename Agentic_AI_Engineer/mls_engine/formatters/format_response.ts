export function formatPropertyResponse(
    listings: any[],
    soldComps: any[]
): string {

    let response = "";

    if (listings.length) {
        response += `🏠 Active Listings (showing ${Math.min(listings.length, 5)} results)\n\n`;

        response += listings
            .slice(0, 5)
            .map((listing, index) => [
                `${index + 1}. Address: ${listing.address}`,
                `City: ${listing.city}`,
                `Price: $${listing.price?.toLocaleString()}`,
                `Beds | Baths: ${listing.bedrooms} br | ${listing.bathrooms} ba`,
                `Sqft: ${listing.sqft?.toLocaleString()} sqft`,
                `Type: ${listing.propertyType}`
            ].join("\n"))
            .join("\n\n");
    } else {
        response += "No active listings found.\n";
    }

    if (soldComps.length) {
        response += "\n\n--------------------\n\n";
        response += `📊 Sold Comparables (showing ${Math.min(soldComps.length, 5)} results)\n\n`;

        response += soldComps
            .slice(0, 5)
            .map((sold, index) => [
                `${index + 1}. Address: ${sold.address}`,
                `City: ${sold.city}`,
                `Sold Price: $${sold.soldPrice?.toLocaleString()}`,
                `Sold Date: ${sold.soldDate}`,
                `Beds | Baths: ${sold.bedrooms} br | ${sold.bathrooms} ba`,
                `Sqft: ${sold.sqft?.toLocaleString()} sqft`,
                `Type: ${sold.propertyType}`
            ].join("\n"))
            .join("\n\n");
    }
    
    return response;
} 