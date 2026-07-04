## OpenClaw Architecture Flow
How OpenClaw handles routing, session state, channel integration, and tool execution

```mermaid
%%{init: {'theme':'base','flowchart':{'htmlLabels':true},'themeVariables':{'primaryTextColor':'#000000','lineColor':'#333333','fontFamily':'Arial'}}}%%
flowchart TD

    1["<b>User</b><br/>User sends a message or a request"]
    2["<b>WhatsApp</b><br/>Message received via WhatsApp API"]
    3["<b>OpenClaw Runtime</b><br/>Acts as the brain of the application to which<br/>it prepares everything needed before deciding<br/>what to do by managing the session, gathering<br/>context, and rejects any potentially harmful<br/>requests."]
    4["<b>Skill Selector</b><br/>Determines which skill to use based on the<br/>user request and context"]
    5["<b>Tool Executor</b><br/>Using the selected skill to perform the work<br/>requested or prompted by the user, which may<br/>include extra needed tools like API calls,<br/>database queries, or other external services."]
    6["<b>Memory Update</b><br/>Stores any new information or context<br/>gathered during the interaction for future<br/>reference"]
    7["<b>Response</b><br/>OpenClaw builds the reply based on everything<br/>it has gathered and sends it back to the user<br/>via WhatsApp"]

    1 --> 2
    2 --> 3
    3 --> 4
    4 --> 5
    5 --> 6
    6 --> 7
    7 -->|The response travels back via WhatsApp to the user, completing the interaction loop| 1


%% Default node style
classDef default fill:#F5F5F5,stroke:#333333,stroke-width:2px,color:#000000;

%% Arrow style
linkStyle default stroke:#333333,stroke-width:2px,color:#000000;

```