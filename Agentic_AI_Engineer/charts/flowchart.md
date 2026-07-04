## OpenClaw Architecture Flow
How OpenClaw handles routing, session state, channel integration, and tool execution

```mermaid
graph TD
    1[User<br><small>User sends a message or a request</small>]
    2[WhatsApp<br><small>Message received via WhatsApp API</small>]
    3[OpenClaw Runtime<br><small>Acts as the brain of the application to ...</small>]
    4[Skill Selector<br><small>Determines which skill to use based on t...</small>]
    5[Tool Executor<br><small>Using the selected skill to perform the ...</small>]
    6[Memory Update<br><small>Stores any new information or context ga...</small>]
    7[Response<br><small>OpenClaw builds the reply based on every...</small>]

    1 --> 2
    2 --> 3
    3 --> 4
    4 --> 5
    5 --> 6
    6 --> 7
    7 -->|The response travels back via WhatsApp to the user, completing the interaction loop| 1
