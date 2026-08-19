We have several agents that know how to perform specific jobs/tasks. So, for this week's deliverable, the goal is to build one orchestrator that decides which agent(s) should handle a user's question, runs them when necessary, and combines their outputs into one response.

There are currently 5 specialized agents:
1. propertySearchAgent: Responsible for questions about specific properties/listings & queries rets_property with structured fliters
2. marketStatsAgent: Responsible for market-level analysis & aggregates california_sold for trends and comps
3. recommendationAgent: Responsible for similar-property recommendations & surfaces similar listings with comp validation
4. ragAgent: Responsible for knowledge/conceptual questions & answers conceptual and definitional questions
5. emailDraftAgent: Composes formatted property or market summaries (have not created yet)

There are five different intents: seaarch, market, recommend, knowledge, and mixed. We would have to create a classifier that can categorize the kind of query the user asks for and then call the accurate agent to carry out its key role. 