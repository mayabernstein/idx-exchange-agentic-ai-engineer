import { spawn } from "child_process";
import type { ConversationListing } from "../conversational_property/types.js";

function toRecommendationListing(
    listing: ConversationListing
) {
    return {
        L_ListingID: listing.listingId,
        L_City: listing.city,
        L_SystemPrice: listing.price,
        L_Keyword2: listing.bedrooms,
        LM_Dec_3: String(listing.bathrooms),
        LM_Int2_3: listing.sqft
    }
}
function formatRecommendationResponse(
    recommendations: any[] 
): string {
    if (!recommendations.length) {
        return "I couldn't find any similar properties.";
    }
    let response = "🏠 Similar Properties\n\n";

    recommendations.forEach((recommendation, index) => {
        const listing = recommendation.listing;
        const comp = recommendation.comp_validation;

        response += `${index + 1}. ${listing.L_Address}, ${listing.L_City} — $${listing.L_SystemPrice.toLocaleString()}\n`;

        response += `   ${listing.L_Keyword2} beds • ${listing.LM_Dec_3} baths • ${listing.LM_Int2_3?.toLocaleString()} sqft\n`;

        response += `   Similarity Score: ${recommendation.score}\n`;

        if (comp.comp_price) {
            response += `   Recent Comp Estimate: $${comp.comp_price.toLocaleString()}\n`;
        }

        if (comp.delta_pct !== null) {
            response += `   Price vs. Comps: ${Math.abs(comp.delta_pct)}% ${
                comp.delta_pct < 0 ? "below" : "above"
            }\n`;
        }

        response += `   Assessment: ${comp.assessment}\n\n`;
    });

    return response;
}
export async function recommendationEngine(
    listing: ConversationListing
): Promise<string> {
    console.log("RECOMMENDATION ENGINE CALLED");

    if (!listing) {
        return "I need a property to generate recommendations.";
    }

    const target = toRecommendationListing(listing);

    return new Promise((resolve) => {
        const python = spawn(
            "python",
            ["../recommendation_engine/recommendation.py"]
        );

        let stdout = "";
        let stderr = "";

        python.stdout.on("data", (data) => {
            stdout += data.toString();
        });

        python.stderr.on("data", (data) => {
            stderr += data.toString();
        });

        python.on("close", (code) => {
            if (code !== 0) {
                console.error(
                    "Recommendation Engine Error:",
                    stderr
                );
                resolve(
                    "Sorry, I couldn't generate property recommendations."
                );
                return;
            }
            try {
                const recommendations = JSON.parse(stdout.trim());

                resolve(
                    formatRecommendationResponse(recommendations)
                );
            } catch (error) {
                console.error(
                    "Recommendation Formatting Error:",
                    error
                );
                resolve(
                    "Sorry, I couldn't format the property recommendations."
                );
            }
        });
        // Send target listing to Python through stdin
        python.stdin.write(JSON.stringify(target));
        python.stdin.end();
    });
}