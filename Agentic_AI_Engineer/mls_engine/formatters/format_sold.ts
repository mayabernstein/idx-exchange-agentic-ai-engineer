import type { SoldRow } from "../types/types.js";

export function formatSold(sold: SoldRow) {
    return {
        address: sold.UnparsedAddress,
        city: sold.City,
        soldPrice: sold.ClosePrice,
        soldDate: sold.CloseDate, 
        originalListPrice: sold.OriginalListPrice, 
        listPrice: sold.ListPrice, 
        bedrooms: sold.BedroomsTotal,
        bathrooms: sold.BathroomsTotalInteger,
        sqft: sold.LivingArea,
        propertyType: sold.PropertyType,
        propertySubType: sold.PropertySubType,
        yearBuilt: sold.YearBuilt,
        daysOnMarket: sold.DaysOnMarket,
        listingAgent: sold.ListAgentFullName,
        listingOffice: sold.ListOfficeName,
        buyerOffice: sold.BuyerOfficeName,
    };
}