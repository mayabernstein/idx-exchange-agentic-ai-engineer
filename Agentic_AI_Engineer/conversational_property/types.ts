export interface ConversationListing {
    listingId: string;
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
}

export interface UserSession {
    city?: string | null;
    maxPrice?: number | null;

    beds?: number | null;
    minBeds?: number | null;
    maxBeds?: number | null;

    baths?: number | null;
    minBaths?: number | null;
    maxBaths?: number | null;

    type?: string | null;
    typeAnswered?: boolean;

    pool?: boolean | null;
    poolAnswered?: boolean;
    
    sqft?: number | null;
    view?: boolean | null;
    maxHoa?: number | null;

    lastResults?: ConversationListing[];

    conversationStep: number;
}

// For the multi-conversational piece
export interface ConversationResponse {
    complete: boolean;
    message: string;
    filtersCollected: boolean;
    results?: ConversationListing[];
}