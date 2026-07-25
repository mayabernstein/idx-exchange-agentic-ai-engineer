import type { UserSession } from "./types.js";
// This is where the session memory lives. 
const sessions = new Map<string, UserSession>();

export function getSession(userId: string): UserSession {
    if (!sessions.has(userId)) {
        sessions.set(userId, {
            city: null,
            maxPrice: null,
            beds: null,
            minBeds: null,
            maxBeds: null, 
            baths: null,
            minBaths: null,
            maxBaths: null, 
            sqft: null,
            type: null,
            typeAnswered: false, 
            pool: null,
            poolAnswered: false, 
            view: null,
            maxHoa: null,
            conversationStep: 0
        });
    }
    return sessions.get(userId)!;
}
export function updateSession(userId: string, updates: Partial<UserSession>) {
    const session = getSession(userId);
    sessions.set(userId, {...session, ...updates});
}
export function clearSession(userId: string) {
    sessions.delete(userId);
}
export function hasActiveConversation(userId: string): boolean {
    const session = getSession(userId);

    return (
        session.city != null ||
        session.maxPrice != null ||
        session.beds != null ||
        session.baths != null ||
        session.type != null
    );
}