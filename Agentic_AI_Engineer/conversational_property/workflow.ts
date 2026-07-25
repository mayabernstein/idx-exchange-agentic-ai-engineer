// This contains the conversational logic. 
// Through this file, it will accomplish things like asking for
// clarification and further questions on what the user is looking for
import {getSession, updateSession} from "./session";
import type {ConversationResponse, UserSession} from "./types";
import {sessionToPropertyFilters} from "./mapper";
import { handleWeek3Search } from "../mls_engine/skills/handleWeek3Search";

// First, if the user is like find homes in Irvine - it is quite broad, so the agent may ask further questions to narrow the search
const QUESTION_ORDER = ["maxPrice", "type", "beds", "baths", "pool"] as const; 

const QUESTIONS = {
    maxPrice: "What is your maximum budget?",
    type: "What kind of property are you looking for (e.g., condo, townhouse, single-family house, any)?",
    beds: "How many bedrooms would you like?",
    baths: "How many bathrooms would you like?",
    pool: "Would you like a pool?"
};

function getNextQuestion(session: UserSession): string | null {
    for (const filter of QUESTION_ORDER) {
        if (filter == "type") {
            if (!session.typeAnswered) {
                return QUESTIONS.type;
            }
            continue;
        }
        if (filter == "beds") {
            if (!session.beds && !session.minBeds && !session.maxBeds) {
                return QUESTIONS.beds;
            }
            continue;
        }
        if (filter == "baths") {
            if (!session.baths && !session.minBaths && !session.maxBaths) {
                return QUESTIONS.baths;
            }
            continue;
        }
        if (filter == "pool") {
            if (!session.poolAnswered) {
                return QUESTIONS.pool;
            }
            continue;
        }
        if (!session[filter]) {
            return QUESTIONS[filter];
        }
    }
    return null;
} 

export async function continueConversation(
    userId: string
): Promise<ConversationResponse> {
    // Get current conversation memory
    const session = getSession(userId);
    // Convert conversational memory into database filters
    const filters = sessionToPropertyFilters(session);
    // Seaarch using the filters collected so far
    const results = await handleWeek3Search({filters});
    // Save current results
    updateSession(userId, {lastResults:results.listings});
    // Determine the next question
    const nextQuestion = getNextQuestion(session);
    // More information still needed
    if (nextQuestion) {
        return {
            complete: false,
            message: `I found ${results.listings.length} homes matching your current search.\n\n${nextQuestion}`,
            filtersCollected: false
        };
    }
    
    return {
        complete: true,
        message: `I found ${results.listings.length} homes matching your preferences.`,
        filtersCollected: true,
        results: results.listings
    };
}