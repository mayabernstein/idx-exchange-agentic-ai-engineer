import json

# 1. Load your JSON file
with open("architecture_flow.json", "r") as f:
    data = json.load(f)

# 2. Start building the Mermaid string
mermaid_output = f"## {data['title']}\n{data['description']}\n\n```mermaid\ngraph TD\n"

# 3. Loop through your nodes (the "flow" array)
for node in data["flow"]:
    # Shorten description for readability
    desc = node["description"][:40] + "..." if len(node["description"]) > 40 else node["description"]
    mermaid_output += f'    {node["id"]}[{node["name"]}<br><small>{desc}</small>]\n'

mermaid_output += "\n"

# 4. Loop through your connections
for edge in data["connections"]:
    mermaid_output += f"    {edge[0]} --> {edge[1]}\n"

mermaid_output += "```"

# 5. Save it as a markdown file for GitHub
with open("flowchart.md", "w") as f:
    f.write(mermaid_output)