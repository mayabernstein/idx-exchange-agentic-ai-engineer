import { hasActiveConversation } from "../conversational_property/session.js";
import dotenv from "dotenv";
import mysql from "mysql2/promise";

dotenv.config();

export type Intent =
    | "search"
    | "market"
    | "recommendation"
    | "knowledge"
    | "mixed"
    | "uncategorized";

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

    private looksLikePropertySearch(text: string): boolean {
        const searchAction =
            /(find|search|show me|looking for|find me)/i.test(text);

        const propertyTerm =
            /(home|house|property|properties|condo|condominium|townhouse|townhome|listing|listings|bed(room)?|bath(room)?)/i.test(text);

        const priceFilter =
            /\b(under|below)\s+\$?\s*[\d,]+/i.test(text);

        return (
            (searchAction && propertyTerm) ||
            (searchAction && priceFilter)
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
        return /(what does|what is|difference between|different from|different than|compare|comparison|versus|vs\.?|define|definition|explain|meaning|terminology|mls field|field definition|schema|reso|trestle|metadata)/i.test(text);
    }

    public async classify(
        message: string,
        userId: string
    ): Promise<Intent> {

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
            return "search";
        }

        // --------------------------------
        // Detect individual intent signals
        // --------------------------------

        const isSearch =
            this.looksLikePropertySearch(text);

        const isMarket =
            this.looksLikeMarketQuestion(text);

        const isRecommendation =
            this.looksLikeRecommendation(text);

        const isKnowledge =
            this.looksLikeKnowledgeQuestion(text);

        const containsValidCity =
            this.containsValidCity(text);

        console.log("CLASSIFIER DEBUG:");
        console.log("isSearch:", isSearch);
        console.log("isMarket:", isMarket);
        console.log(
            "containsValidCity:",
            containsValidCity
        );
        console.log(
            "isRecommendation:",
            isRecommendation
        );
        console.log("isKnowledge:", isKnowledge);

        // --------------------------------
        // Mixed intent
        // --------------------------------
        
        if (isSearch && isMarket) {
            return "mixed";
        }

        // --------------------------------
        // Recommendation
        // --------------------------------

        if (isRecommendation) {
            return "recommendation";
        }

        // --------------------------------
        // Market
        // --------------------------------

        if (isMarket) {
            return "market";
        }

        // --------------------------------
        // Property search
        // --------------------------------

        if (isSearch) {
            return "search";
        }

        // --------------------------------
        // Knowledge
        // --------------------------------

        if (isKnowledge) {
            return "knowledge";
        }

        // --------------------------------
        // Uncategorized
        // --------------------------------

        return "uncategorized";
    }
}