import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

export async function run(query: string) {

    console.log("MARKET ANALYTICS SKILL WAS CALLED");

    // Temporary while testing
    const city = "Irvine";

    try {
        const { stdout } = await execAsync(
            `python market_agent.py "${city}"`
        );

        return {
            success: true,
            response: stdout.trim(),
        };
    } catch (error) {
        console.error(error);

        return {
            success: false,
            response: "Failed to generate market report.",
        };
    }
}