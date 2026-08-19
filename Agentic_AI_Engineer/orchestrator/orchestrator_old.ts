import { tryPropertySearch } from "./property-search";
import { tryMarketAnalytics } from "./market-analytics";
import { recommendationEngine } from "./recommendation_agent";
import { tryRealEstateRAG } from "./real-estate-rag";
import { getSession } from "../conversational_property/session";
import { formatCombinedResponse } from "./format-combined-response";
import { hasActiveConversation } from "../conversational_property/session";
import { classifyIntent } from "./classifyIntent";

const classifier = new classifyIntent();
await classifier.initialize();

function splitMixedQuery(query: string) {
    const parts = query.split(/\band\b/i);

    const propertyQuery = parts[0].trim();
    let marketQuery = parts.slice(1).join(" and ").trim();

    const cityMatch = propertyQuery.match(
        /\bin\s+(.+)$/i
    );

    if (cityMatch) {
        const city = cityMatch[1].trim();
        marketQuery = `${marketQuery} in ${city}`;
    }

    return {
        propertyQuery,
        marketQuery
    };
}
// Main entry point for the multi-agent system
export async function orchestrate(
    query: string,
    userId: string,
): Promise<string> {
    console.log("ORCHESTRATOR QUERY:", query);

    const activePropertyConversation = hasActiveConversation(userId);

    console.log(
        "ACTIVE PROPERTY CONVERSATION:",
        activePropertyConversation
    );

    if (activePropertyConversation) {
        console.log(
            "CONTINUING PROPERTY CONVERSATION"
        );  

        return await tryPropertySearch(
            userId,
            query
        );
    }
    // Step 1: Determine what the user is asking
    const intent = await classifier.classify(query, userId);

    console.log("CLASSIFIED INTENT:", intent);

    // Step 2: Route the query to the appropriate agent
    switch (intent) {

        case "search":
            // Call MLS/property search functionality
            return await tryPropertySearch(userId, query);

        case "market":
            // Call market analytics functionality
            return await tryMarketAnalytics(userId, query);

        case "recommendation": 
            const session = getSession(userId);

            // Call recommendation engine
            if (!session.lastResults?.length) {
                return "Please search for a property first so I can find similar listings.";
            }

            return await recommendationEngine(
                session.lastResults[0]
            )

        case "knowledge":
            // Call RAG system
            return await tryRealEstateRAG(
                userId,
                query
            );

        case "mixed": {

            const { propertyQuery, marketQuery } =
                splitMixedQuery(query);

            const [listings, stats] = await Promise.all([
                tryPropertySearch(userId, propertyQuery),
                tryMarketAnalytics(userId, marketQuery)
            ]);

            console.log("MIXED PROPERTY RESULT:", listings);
            console.log("MIXED MARKET RESULT:", stats);

            return formatCombinedResponse(
                listings,
                stats
            );
        }

        // case "uncategorized"
        default:
            return {
                response:
                    "I'm not sure how to help with that. " +
                    "Try asking about properties, recommendations, " +
                    "market trends, or real estate concepts."
            };
    }
}