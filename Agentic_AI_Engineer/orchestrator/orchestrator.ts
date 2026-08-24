import { tryPropertySearch } from "./property-search";
import { tryMarketAnalytics } from "./market-analytics";
import { recommendationEngine } from "./recommendation_agent";
import { tryRealEstateRAG } from "./real-estate-rag";
import { getSession, updateSession } from "../conversational_property/session";
import { formatCombinedResponse } from "./format-combined-response";
import { hasActiveConversation } from "../conversational_property/session";
import { classifyIntent } from "./classifyIntent";

const classifier = new classifyIntent();
await classifier.initialize();

// Main entry point for the multi-agent system
export async function orchestrate(
    query: string,
    userId: string,
): Promise<string> {
    console.log("ORCHESTRATOR QUERY:", query);

    const activePropertyConversation = 
        hasActiveConversation(userId);

    console.log(
        "ACTIVE PROPERTY CONVERSATION:",
        activePropertyConversation
    );

    // Continue active property conversation
    if (activePropertyConversation) {
        console.log(
            "CONTINUING PROPERTY CONVERSATION"
        );
        const propertyResult = await tryPropertySearch(userId, query);

        console.log("PROPERTY RESULT:", propertyResult);

        if (!propertyResult.complete) {
            return propertyResult.message;
        }

        const session = getSession(userId);

        console.log(
            "PENDING RECOMMENDATION:",
            session.pendingRecommendation
        );

        if (
            session.pendingRecommendation && 
            propertyResult.results?.length
        ) {
            console.log("RUNNING PENDING RECOMMENDATION");

            const recommendationResult = 
                await recommendationEngine(
                    propertyResult.results[0]
                );
            
            updateSession(userId, {
                pendingRecommendation: false
            });

            return `${propertyResult.message}\n\n${recommendationResult}`;
        }
        return propertyResult.message;
    }
    // Classify query 
    const classification = 
        await classifier.classify(query, userId);
    
    console.log(
        "CLASSIFIED INTENT:",
        classification.intent
    )

    console.log(
        "DETECTED INTENTS:",
        classification.intents
    )

    /*
    // Continue active property conversation
   ''' if (
        activePropertyConversation && 
        classification.intent === "search"
    ) {
        console.log(
            "CONTINUING PROPERTY CONVERSATION"
        );  

        return await tryPropertySearch(
            userId,
            query
        );
    }'''*/

    // Single intent
    switch (classification.intent) {

        case "search": {
            // Call MLS/property search functionality
            const propertyResult = 
                await tryPropertySearch(userId, query);
            return propertyResult.message; 
        }
        
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
            const results: string[] = [];

            if (classification.intents.includes("search")) {
                const searchSegment = 
                    classification.segments.find(segment => 
                        segment.intents.includes("search")
                    );
                if (searchSegment) {
                    const propertyResult = 
                        await tryPropertySearch(
                            userId, 
                            searchSegment.query
                        );
                    
                    results.push(propertyResult.message);

                    if (!propertyResult.complete) {
                        if (classification.intents.includes("recommendation")) {
                            updateSession(userId, {
                                pendingRecommendation: true
                            });
                            console.log(
                                "PENDING RECOMMENDATION SET TO TRUE"
                            );
                        }
                        
                        return results.join("\n\n");
                    }
                }
            }
            if (classification.intents.includes("market")) {
                const marketResult = 
                    await tryMarketAnalytics(userId, query);
                results.push(marketResult);
            }
            if (classification.intents.includes("recommendation")) {
                const session = getSession(userId);
                
                // If the search already finished, recommend immediately 
                if (session.lastResults?.length) {
                    const recommendationResult = 
                        await recommendationEngine(
                            session.lastResults[0]
                        );

                    results.push(recommendationResult);
                } else {
                    updateSession(userId, {
                        pendingRecommendation: true
                    //results.push("Please search for a property first so I can find similar listings.");
                    });
                    console.log("PENDING RECOMMENDATION SET TO TRUE");
                }
            }
            if (classification.intents.includes("knowledge")) {
                const knowledgeResult = await tryRealEstateRAG(userId, query);

                results.push(knowledgeResult);
            }
            return results.join("\n\n");
        }

        // case "uncategorized"
        default:
            return (
                    "I'm not sure how to help with that. " +
                    "Try asking about properties, recommendations, " +
                    "market trends, or real estate concepts."
            );
    }
}