import type { SoldRow } from "../types/types";
export declare function formatSold(sold: SoldRow): {
    address: string;
    city: string;
    soldPrice: number;
    soldDate: string;
    originalListPrice: number | null;
    listPrice: number | null;
    bedrooms: number | null;
    bathrooms: number | null;
    sqft: number | null;
    propertyType: string | null;
    propertySubType: string | null;
    yearBuilt: number | null;
    daysOnMarket: number | null;
    listingAgent: string | null;
    listingOffice: string | null;
    buyerOffice: string | null;
};
