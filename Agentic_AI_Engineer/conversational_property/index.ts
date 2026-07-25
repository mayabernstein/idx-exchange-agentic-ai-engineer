import { updateSession, getSession } from "./session";
import { continueConversation } from "./workflow";
import { parsePropertyQuery } from "../mls_engine/parser/service.ts";

export async function handlePropertyConversation(
    userId: string,
    message: string
) {

    const parsed = await parsePropertyQuery(message);

    const updates = {
        city: parsed.L_City,
        maxPrice: parsed.L_SystemPrice,
        beds: parsed.L_Keyword2,
        minBeds: parsed.MinBeds,
        maxBeds: parsed.MaxBeds,
        baths: parsed.LM_Dec_3,
        minBaths: parsed.MinBaths,
        maxBaths: parsed.MaxBaths,
        sqft: parsed.LM_Int2_3,
        type: parsed.L_Type_,
        pool: parsed.PoolPrivateYN === 1 ? true : null,
        poolAnswered: parsed.PoolAnswered ? true: undefined,
        view: parsed.ViewYN === 1 ? true : null,
        maxHoa: parsed.AssociationFee
    };
    if (parsed.AnyType || parsed.L_Type_ !== null) {
        updates.typeAnswered = true;
    }
    if (parsed.PoolAnswered || parsed.PoolPrivateYN !== null) {
        updates.poolAnswered = true;
    }
    updateSession(
        userId,
        Object.fromEntries(
            Object.entries(updates)
                .filter(([_, value]) => value !== null && value !== undefined)
        )
    );

    const response = await continueConversation(userId);

    return response;
}