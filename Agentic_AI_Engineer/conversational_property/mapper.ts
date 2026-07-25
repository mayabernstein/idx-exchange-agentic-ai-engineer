import type { UserSession } from "./types";
import type { PropertyFilters } from "../mls_engine/types/types";

export function sessionToPropertyFilters(
    session: UserSession
): PropertyFilters {

    return {
        L_City: session.city ?? null,
        L_SystemPrice: session.maxPrice ?? null,
        L_Keyword2: session.beds ?? null, 
        LM_Dec_3: session.baths ?? null, 
        L_Type_: session.type ?? null, 
        PoolPrivateYN: 
            session.pool == true
                ? 1
                : null,
        LM_Int2_3: session.sqft ?? null, 
        ViewYN: session.pool == true
                ? 1
                : null,
        AssociationFee: session.maxHoa ?? null
    };
}