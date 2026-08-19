export function formatCombinedResponse(
    listings: string | null,
    stats: string | null
): string {

    let response = "";

    if (listings) {
        response += "🏠 PROPERTY SEARCH\n\n";
        response += listings;
        response += "\n\n";
    }

    if (stats) {
        response += "📊 MARKET ANALYSIS\n\n";
        response += stats;
    }

    if (!response) {
        return "Sorry, I couldn't find information for that request.";
    }

    return response.trim();
}