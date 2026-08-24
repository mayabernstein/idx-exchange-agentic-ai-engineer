import { execFile } from "child_process";
import { promisify } from "util";

const execFileAsync = promisify(execFile);

export async function semanticPropertySearch(query: string) {

    console.log("SEMANTIC SEARCH CALLED:", query);

    const result = await execFileAsync(
        "python",
        [
            "../idx-exchange-nlp-engineer/Agentic_AI_Engineer/embeddings/semantic_search.py",
            query
        ],
        {
            maxBuffer: 10 * 1024 * 1024
        }
    );

    console.log("SEMANTIC SEARCH RESULT:", result.stdout);

    return JSON.parse(result.stdout);
}

/*
// Temporary test
semanticPropertySearch(
    "charming craftsman with mountain views and character"
)
    .then((results) => {
        console.log("FINAL RESULTS:");
        console.log(results);
    })
    .catch((error) => {
        console.error("SEMANTIC SEARCH ERROR:");
        console.error(error);
    });
*/