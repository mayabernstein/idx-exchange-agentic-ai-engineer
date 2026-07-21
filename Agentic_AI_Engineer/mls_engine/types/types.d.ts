export interface PropertyFilters {
    L_City: string | null;
    L_SystemPrice: number | null;
    L_Keyword2: number | null;
    LM_Dec_3: number | null;
    LM_Int2_3: number | null;
    L_Type_: string | null;
    PoolPrivateYN: number | null;
    ViewYN: number | null;
    AssociationFee: number | null;
}
export interface ListingRow {
    L_ListingID: string;
    L_DisplayId: string;
    L_Address: string;
    L_City: string;
    L_Zip: string;
    price: number;
    beds: number;
    baths: number;
    sqft: number;
    type: string;
    status: string;
    lat: number;
    lng: number;
    YearBuilt: number | null;
    AssociationFee: number | null;
    DaysOnMarket: number | null;
    PoolPrivateYN: number | null;
    ViewYN: number | null;
    FireplaceYN: number | null;
    PhotoCount: number | null;
    LA1_UserFirstName: string | null;
    LA1_UserLastName: string | null;
    LO1_OrganizationName: string | null;
}
export interface SoldRow {
    ListingKey: number;
    UnparsedAddress: string;
    City: string;
    CloseDate: string;
    ClosePrice: number;
    OriginalListPrice: number | null;
    ListPrice: number | null;
    DaysOnMarket: number | null;
    BedroomsTotal: number | null;
    BathroomsTotalInteger: number | null;
    LivingArea: number | null;
    PropertyType: string | null;
    PropertySubType: string | null;
    YearBuilt: number | null;
    ListAgentFullName: string | null;
    ListOfficeName: string | null;
    BuyerOfficeName: string | null;
}
