---
name: real-estate-rag
description: Answer questions about real estate concepts, MLS field definitions, and market terminology using authoritative source documents.
---

# Real Estate RAG

Use this skill when the user asks about:

- Real estate concepts and terminology
- MLS field definitions
- RESO/Trestle metadata
- Database fields and schemas
- Market terminology

The skill uses a document-aware RAG pipeline to retrieve
relevant information from authoritative source documents.

Knowledge sources include:

- Real Estate Data Analyst Primer
- Trestle Property Metadata documentation
- Week 5 market summaries
- MLS schema documentation

## Behavior

- Ground answers in retrieved source documents.
- Do not invent information that is not supported by the retrieved context.
- Do not use web search for questions covered by the indexed documents.
- Return the answer along with the sources used.

## Example questions

- What does DOM mean?
- What is a list-to-close ratio?
- What columns are in california_sold?
- What does StandardStatus mean?
- What does LivingArea mean?
- What is months of supply?
- What is a cap rate?