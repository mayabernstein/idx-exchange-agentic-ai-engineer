import {
    looksLikePropertySearch,
    handlePropertySearch
} from "../routers/propertySearchRouter.ts";


export async function handleMessage(
    userId: string,
    message: string,
    normalHandler: (message:string)=>Promise<any>
) {

    if (looksLikePropertySearch(message)) {
        console.log("MLS route activated");

        const propertyResult = await handlePropertySearch(
            userId,
            message
        );

        if (propertyResult) {
            return propertyResult;
        }
    }

    return await normalHandler(message);
}
/*
import { run } from "../../mls_engine/index.ts";

export function isPropertySearch(message: string): boolean {
    const keywords = [
        "home",
        "house",
        "condo",
        "listing",
        "property",
        "bedroom",
        "bathroom",
        "pool",
        "sold",
        "mls"
    ];

    const text = message.toLowerCase();

    return keywords.some(keyword =>
        text.includes(keyword)
    );
}

export async function handlePropertySearch(message: string) {
    return await run(message);
}
*/