---
name: mls-property-search
description: Use this skill whenever a user asks for real estate listings, homes, condos, houses, properties, MLS searches, prices, bedrooms, bathrooms, pools, locations, active listings, or sold comparable properties. This skill queries the MLS database and should be used instead of web search for real estate property requests.
---

# MLS Property Search Skill

This skill searches MLS data.

Use this skill for requests such as:
- "Show me 3 bedroom condos in Irvine under $1.5M"
- "Find active homes with a pool"
- "What condos recently sold in Irvine?"
- "Find comparable sales"

The skill:
1. Parses the user's natural language request.
2. Converts it into property filters.
3. Queries active MLS listings.
4. Queries sold comparable properties.
5. Returns formatted property cards.