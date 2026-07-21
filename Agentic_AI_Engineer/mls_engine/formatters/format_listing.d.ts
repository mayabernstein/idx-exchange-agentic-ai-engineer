import type { ListingRow } from "../types/types";
export declare function formatListing(listing: ListingRow): {
    address: string;
    city: string;
    price: number;
    bedrooms: number;
    bathrooms: number;
    sqft: number;
    propertyType: string;
    status: string;
    yearBuilt: number | null;
    daysOnMarket: number | null;
    agent: string;
    office: string | null;
};
