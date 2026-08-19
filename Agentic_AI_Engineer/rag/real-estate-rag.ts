import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

function looksLikeRealEstateRAGQuestion(text: string) {
    return /(what\s+does\s+.*\s+mean|what\s+is\s+.*|difference\s+between|different\s+from|different\s+than|compare|comparison|versus|vs\.?|define|definition|explain|meaning|terminology|real\s+estate\s+concept|real\s+estate\s+term|mls\s+field|mls\s+fields?|field\s+definition|field\s+definitions|column\s+definition|column\s+definitions|database\s+schema|schema|columns?\s+(in|of)|fields?\s+(in|of)|reso|trestle|metadata|days\s+on\s+market|\bdom\b|list.?to.?close|list\s+to\s+close\s+ratio|months\s+of\s+ supply|price\s+per\s+square\s+foot|price\s+per\s+sq\s*ft|cap\s+rate|escrow|comps?|comparable\s+sales?|appraisal|equity|closing\s+costs?)/i.test(text);
}

export async function tryRealEstateRAG(
    userId: string,
    message: string
) {

    console.log(
        "REAL ESTATE RAG CALLED:",
        message
    );


    if (
        !looksLikeRealEstateRAGQuestion(
            message
        )
    ) {
        return null;
    }


    console.log(
        "REAL ESTATE RAG MATCHED"
    );


    try {

        const { stdout } = await execAsync(
            `python ../rag/rag_answer.py "${message}"`
        );

        return stdout.trim();

    } catch (error) {

        console.error(
            "Real Estate RAG Error:",
            error
        );

        return "Sorry, I couldn't find an answer in the available real estate documents.";
    }
}