## OpenClaw Architecture Flow
How OpenClaw handles routing, session state, channel integration, and tool execution

```mermaid
flowchart TD

    1["<b>User</b><br/><small>User sends a message or a request</small>"]
    2["<b>WhatsApp</b><br/><small>Message received via WhatsApp API</small>"]
    3["<b>OpenClaw Runtime</b><br/><small>Acts as the brain of the<br/>application to which it prepares<br/>everything needed before deciding<br/>what to do by managing the session,<br/>gathering context, and rejects any<br/>potentially harmful requests.</small>"]
    4["<b>Skill Selector</b><br/><small>Determines which skill to use based<br/>on the user request and context</small>"]
    5["<b>Tool Executor</b><br/><small>Using the selected skill to perform<br/>the work requested or prompted by<br/>the user, which may include extra<br/>needed tools like API calls,<br/>database queries, or other external<br/>services.</small>"]
    6["<b>Memory Update</b><br/><small>Stores any new information or<br/>context gathered during the<br/>interaction for future reference</small>"]
    7["<b>Response</b><br/><small>OpenClaw builds the reply based on<br/>everything it has gathered and<br/>sends it back to the user via<br/>WhatsApp</small>"]

    1 --> 2
    2 --> 3
    3 --> 4
    4 --> 5
    5 --> 6
    6 --> 7
    7 -->|The response travels back via WhatsApp to the user, completing the interaction loop| 1

classDef default fill:#f9f9f9,stroke:#333,stroke-width:1.5px;

```