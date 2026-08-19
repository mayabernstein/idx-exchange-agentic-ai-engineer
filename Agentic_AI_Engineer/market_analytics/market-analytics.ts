import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

function looksLikeMarketQuestion(text: string) {
    return /(market|housing market|buyer'?s market|seller'?s market|average price|median price|price per square foot|price per sqft|inventory|days on market|dom|trend|prices? (are|is) (rising|falling|increasing|decreasing)|(rising|falling|increasing|decreasing) prices?|good time to buy|good time to sell)/i.test(text);
}

export async function tryMarketAnalytics(
    userId: string,
    message: string
) {
    console.log("MARKET ANALYTICS CALLED:", message);

    if (!looksLikeMarketQuestion(message)) {
        return null;
    }

    console.log("MARKET ANALYTICS MATCHED");

    // Temporary until we parse the city
    const city = "Irvine";

    try {
        const { stdout } = await execAsync(
            `python ../market_analytics/market_agent.py "${message}"`
        );

        return stdout.trim();

    } catch (error) {
        console.error("Market Analytics Error:", error);
        return "Sorry, I couldn't generate the market report.";
    }
}