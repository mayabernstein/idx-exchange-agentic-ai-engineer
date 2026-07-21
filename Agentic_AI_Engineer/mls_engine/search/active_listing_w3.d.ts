import type { PropertyFilters, ListingRow } from "../types/types";
export declare function searchActiveListings(filters: PropertyFilters, page?: number, limit?: number): Promise<ListingRow[]>;
