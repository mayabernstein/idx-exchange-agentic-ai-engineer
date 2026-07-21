import type { PropertyFilters } from "../types/types";
export declare function handleWeek3Search(input: {
    filters: PropertyFilters;
}): Promise<{
    response: string;
    listings: {
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
    }[];
    soldComps: {
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
    }[];
}>;
