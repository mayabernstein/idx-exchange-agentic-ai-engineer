import { hasActiveConversation } from "../conversational_property/session.js";
import dotenv from "dotenv";
import mysql from "mysql2/promise";


dotenv.config();

export type Intent =
    | "search"
    | "market"
    | "recommendation"
    | "knowledge"
    | "email"
    | "mixed"
    | "uncategorized";

export type ClassifiedSegment = {
    query: string;
    intents: Intent[];
};

export type ClassificationResult = {
    intent: Intent;
    intents: Intent[];
    segments: ClassifiedSegment[];
}

export class classifyIntent {
    private validCities: string[] = [];

    public async initialize(): Promise<void> {
        await this.loadValidCities();
    }

    private async loadValidCities(): Promise<void> {
        try {
            const connection = await mysql.createConnection({
                host: process.env.MYSQL_HOST,
                user: process.env.MYSQL_USER,
                password: process.env.MYSQL_PASSWORD,
                database: process.env.MYSQL_DATABASE
            });

            const [rows] = await connection.execute(
                `
                SELECT DISTINCT City
                FROM california_sold
                WHERE City IS NOT NULL
                ORDER BY City
                `
            );

            this.validCities = (rows as { City: string }[])
                .map(row => row.City.trim())
                .filter(city => city.length > 0);

            await connection.end();

            console.log(
                "VALID CITIES LOADED:",
                this.validCities.length
            );

        } catch (error) {
            console.error(
                "Failed to load valid cities:",
                error
            );
        }
    }

    private containsValidCity(text: string): boolean {
        return this.validCities.some(city => {
            const escapedCity = city.replace(
                /[.*+?^${}()|[\]\\]/g,
                "\\$&"
            );

            return new RegExp(
                `\\b${escapedCity}\\b`,
                "i"
            ).test(text);
        });
    }
    
    private splitQuery(text: string): string[] {
        return text
            .split(
                /(?:\band\s+|,\s*)(?=(tell me|what is|what does|explain|show me|find|search|recommend|compare|give me|let me know)\b)/i
            )
            .map(part => part.trim())
            .filter(part => part.length > 0);
    }
        
    private looksLikePropertySearch(text: string): boolean {
        const searchAction =
            /(find|search|show me|looking for|find me)/i.test(text);

        const propertyTerm =
            /(home|house|property|properties|condo|condominium|townhouse|townhome|listing|listings|bed(room)?|bath(room)?)/i.test(text);

        const priceFilter =
            /\b(under|below)\s+\$?\s*[\d,]+/i.test(text);

        const recommendationTerm = /(similar|recommend|recommendation|like this|comparable properties|properties like|homes like)/i.test(text);

        return (
            !recommendationTerm &&
            (
                (searchAction && propertyTerm) ||
                (searchAction && priceFilter)
            )
        );
    }

    private looksLikePropertyFollowUp(text: string): boolean {
        return (
            /^\$?\s*[\d,]+(?:\.\d+)?\s*$/.test(text) ||

            /\b(condo|condominium|townhouse|townhome|house|single[- ]family|any)\b/i.test(text) ||

            /\b\d+\s*(bed|beds|bedroom|bedrooms|bath|baths|bathroom|bathrooms)\b/i.test(text) ||

            /^(yes|no|yeah|yep|nope|no pool|with pool)$/i.test(
                text.trim()
            )
        );
    }

    private looksLikeMarketQuestion(text: string): boolean {
        const marketTopic =
            /(market|housing market|buyer's market|seller's market|average price|median price|home prices?|housing prices?|prices? (are )?(rising|falling|increasing|decreasing)|price per square foot|price per sqft|inventory|days on market|dom|trend|good time to buy|good time to sell)/i.test(text);

        return (
            marketTopic &&
            this.containsValidCity(text)
        );
    }

    private looksLikeRecommendation(text: string): boolean {
        return /(similar|recommend|recommendation|like this|comparable properties|properties like|homes like)/i.test(text);
    }

    private looksLikeKnowledgeQuestion(text: string): boolean {
        const knowledgeTopic = /(what does|what is|difference between|different from|different than|compare|comparison|versus|vs\.?|define|definition|explain|meaning|terminology|mls field|field definition|schema|reso|trestle|metadata)/i.test(text);

        return (
            knowledgeTopic && !this.containsValidCity(text)
        )
    }

    private looksLikeEmailRequest(text: string): boolean {
        return /(email|e-mail|send.*email|send.*e-mail|gmail|g-mail)/i.test(text);
    }

    private detectIntentsForSegment(text: string): Intent[] {

        const isSearch =
            this.looksLikePropertySearch(text);

        const isMarket =
            this.looksLikeMarketQuestion(text);

        const isRecommendation =
            this.looksLikeRecommendation(text);

        const isKnowledge =
            this.looksLikeKnowledgeQuestion(text);

        const isEmail = 
            this.looksLikeEmailRequest(text);

        const detectedIntents: Intent[] = [];

        if (isSearch) {
            detectedIntents.push("search");
        }

        if (isMarket) {
            detectedIntents.push("market");
        }

        if (isRecommendation) {
            detectedIntents.push("recommendation");
        }

        if (isKnowledge) {
            detectedIntents.push("knowledge");
        }
        
        if (isEmail) {
            detectedIntents.push("email");
        }

        return detectedIntents;
    }

    public async classify(
        message: string,
        userId: string
    ): Promise<ClassificationResult> {

        const text = message.trim();

        const activeConversation =
            hasActiveConversation(userId);

        console.log(
            "ACTIVE PROPERTY CONVERSATION:",
            activeConversation
        );

        // --------------------------------
        // Property conversation follow-up
        // --------------------------------

        if (
            activeConversation &&
            this.looksLikePropertyFollowUp(text)
        ) {
            return {
                intent: "search",
                intents: ["search"],
                segments: [
                    {
                        query: text,
                        intents: ["search"]
                    }
                ]
            };
        }

        // Split the message into separate clauses
        const queryParts = this.splitQuery(text);

        console.log(
            "QUERY PARTS:",
            queryParts
        );

        // Detect intents for each clause 
        const detectedIntents: Intent[] = [];
        const segments: ClassifiedSegment[] = [];

        let contextHasCity = false;

        for (const part of queryParts) {
            const partContainsCity = this.containsValidCity(part);
            const partIntents = this.detectIntentsForSegment(part);

            if (
                contextHasCity &&
                !partContainsCity
            ) {
                const marketTopic =
                    /(market|housing market|buyer's market|seller's market|average price|median price|home prices?|housing prices?|prices? (are )?(rising|falling|increasing|decreasing)|price per square foot|price per sqft|inventory|days on market|dom|trend|good time to buy|good time to sell)/i.test(part);

                if (
                    marketTopic &&
                    !partIntents.includes("market")
                ) {
                    partIntents.push("market");
                }
            }
            console.log("PART:", part);
            console.log("PART INTENTS:", partIntents);

            segments.push({
                query:part,
                intents:partIntents
            });

            for (const intent of partIntents) {
                if (!detectedIntents.includes(intent)) {
                    detectedIntents.push(intent);
                }
            }
            if (partContainsCity) {
                contextHasCity = true;
            }
        }
 
        console.log(
            "DETECTED INTENTS:",
            detectedIntents
        );

        console.log(
            "CLASSIFIED SEGMENTS:",
            segments
        );

        // Mixed intent
        if (detectedIntents.length > 1) {
            return {
                intent: "mixed",
                intents: detectedIntents,
                segments
            };
        }

        // Single intent
        if (detectedIntents.length === 1) {
            return {
                intent: detectedIntents[0],
                intents: detectedIntents,
                segments
            };
        }

        // No recognized intent
        return {
            intent: "uncategorized",
            intents: [],
            segments
        };
    }
}