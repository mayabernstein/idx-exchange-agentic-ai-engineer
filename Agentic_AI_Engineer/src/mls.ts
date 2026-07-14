import { query } from "./db";

interface Listing {
  ListingKey: string;
  ListPrice: number;
}

export async function getListings() {
  return await query<Listing>(
    "SELECT ListingKey, ListPrice FROM Property LIMIT ?",
    [10]
  );
}