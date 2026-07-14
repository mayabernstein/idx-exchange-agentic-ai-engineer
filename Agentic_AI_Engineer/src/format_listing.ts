import { ListingRow } from "./types";

export function formatListing(listing: ListingRow) {
    return {
        address: listing.L_Address,
        city: listing.L_City,
        price: listing.price,
        bedrooms: listing.beds,
        bathrooms: listing.baths,
        sqft: listing.sqft,
        propertyType: listing.type,
        status: listing.status,
        yearBuilt: listing.YearBuilt,
        daysOnMarket: listing.DaysOnMarket,
        agent:
            `${listing.LA1_UserFirstName ?? ""} ${listing.LA1_UserLastName ?? ""}`.trim(),
        office: listing.LO1_OrganizationName,
    };
}