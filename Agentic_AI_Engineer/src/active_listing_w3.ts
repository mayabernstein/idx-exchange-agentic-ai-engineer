import { query } from "./db";
import { PropertyFilters, ListingRow} from "./types";

// rets_property
export async function searchActiveListings(filters: PropertyFilters, page = 1, 
limit = 10) { 
  const offset = (page - 1) * limit; 
  let sql = ` 
    SELECT 
      L_ListingID, L_DisplayId, L_Address, L_City, L_Zip, 
      L_SystemPrice AS price, L_Keyword2 AS beds, LM_Dec_3 AS baths, 
      LM_Int2_3 AS sqft, L_Type_ AS type, L_Status AS status, 
      LMD_MP_Latitude AS lat, LMD_MP_Longitude AS lng, 
      YearBuilt, AssociationFee, DaysOnMarket, 
      PoolPrivateYN, ViewYN, FireplaceYN, PhotoCount, 
      LA1_UserFirstName, LA1_UserLastName, LO1_OrganizationName 
    FROM rets_property WHERE L_Status = "Active" 
  `; 
  const params: any[] = []; 
// city
  if (filters.L_City)     { sql += " AND L_City = ?";           
params.push(filters.L_City); } 
// max price
  if (filters.L_SystemPrice) { sql += " AND L_SystemPrice <= ?";   
params.push(filters.L_SystemPrice); } 
// beds
  if (filters.L_Keyword2)     { sql += " AND L_Keyword2 >= ?";      
params.push(filters.L_Keyword2); } 
// baths
  if (filters.LM_Dec_3)    { sql += " AND LM_Dec_3 >= ?";        
params.push(filters.LM_Dec_3); } 
// sqft
 if (filters.LM_Int2_3)     { sql += " AND LM_Int2_3 >= ?";       
params.push(filters.LM_Int2_3); } 
// type
  if (filters.L_Type_)     { sql += " AND L_Type_ = ?";          
params.push(filters.L_Type_); } 
// pool
  if (filters.PoolPrivateYN)     { sql += " AND PoolPrivateYN = ?";    
params.push(filters.PoolPrivateYN); } 
// view
  if (filters.ViewYN)  { sql += " AND ViewYN = ?";           
params.push(filters.ViewYN); } 
 
  // Temporarily hardcode (LIMIT ? OFFSET ? to LIMIT 10 OFFSET 0)
  sql += " ORDER BY L_SystemPrice ASC LIMIT 10 OFFSET 0"; 
  params.push(limit, offset); 
  
 
  return query<ListingRow>(sql, params); 
}
