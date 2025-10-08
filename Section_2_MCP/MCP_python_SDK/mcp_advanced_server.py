# mcp_advanced_server.py
from __future__ import annotations

import asyncio
import json
import uuid
from pathlib import Path
from typing import Any, Tuple, AsyncGenerator

from mcp.server.fastmcp import FastMCP, Context

HERE = Path(__file__).parent
DB_PATH = HERE / "protein_db.json"
DB: dict[str, dict[str, Any]] = json.loads(DB_PATH.read_text(encoding="utf-8"))

# Store for client registrations and pending callbacks (in-memory for demo)
registered_clients: dict[str, str] = {}
pending_callbacks: dict[str, dict] = {}

mcp = FastMCP(
    name="MCP Workshop (Official SDK) - Advanced",
    instructions=(
        "Advanced MCP server demonstrating notifications, elicitation, "
        "sampling, and streaming using the official MCP SDK."
    ),
)

# ---- Basic Resources & Tools (same as basic server) ----
@mcp.resource("dataset://proteins")
def dataset_overview() -> Tuple[bytes, str]:
    overview = {
        "id": "proteins",
        "count": len(DB),
        "ids": sorted(DB.keys()),
        "description": "Toy protein dataset used for the MCP workshop",
    }
    return json.dumps(overview, indent=2).encode("utf-8"), "application/json"

@mcp.resource("protein://{protein_id}")
def get_protein(protein_id: str) -> Tuple[bytes, str]:
    record = DB.get(protein_id)
    if not record:
        payload = {"error": f"Unknown protein_id: {protein_id}"}
        return json.dumps(payload).encode("utf-8"), "application/json"
    payload = {"id": protein_id, **record}
    return json.dumps(payload, indent=2).encode("utf-8"), "application/json"

@mcp.tool()
def get_protein_function(protein_id: str) -> str:
    """Return the functional annotation for a given protein ID."""
    rec = DB.get(protein_id)
    if not rec:
        raise ValueError(f"Unknown protein_id: {protein_id}")
    return rec["function"]

# ---- Advanced Features ----

# 1. Notification System
@mcp.tool()
async def register_client(client_id: str, callback_url: str, ctx: Context) -> str:
    """Register a client to receive notifications."""
    registered_clients[client_id] = callback_url
    await ctx.info(f"Client '{client_id}' registered for notifications at {callback_url}")
    return f"Successfully registered client '{client_id}'"

@mcp.tool()
async def trigger_notification(ctx: Context) -> str:
    """Trigger a notification to all registered clients."""
    notification_msg = {"message": "Database was updated!"}
    
    # In a real implementation, you'd send HTTP requests to callback URLs
    # For this demo, we'll just log the notifications
    for client_id, callback_url in registered_clients.items():
        await ctx.info(f"Sending notification to {client_id} at {callback_url}: {notification_msg}")
    
    return f"Notifications sent to {len(registered_clients)} clients"

# 2. Elicitation Example
@mcp.tool()
def find_protein(protein_name: str) -> str:
    """
    Find proteins by name. Demonstrates elicitation by asking for clarification
    when multiple matches are found.
    """
    protein_name = protein_name.lower()
    
    if protein_name == "p53":
        # Return elicitation response as structured data
        return json.dumps({
            "result_type": "elicitation",
            "message": "Multiple proteins match 'p53'. Please specify:",
            "choices": [
                {"label": "Human p53", "value": "P53_HUMAN"},
                {"label": "Mouse p53", "value": "P53_MOUSE"}
            ]
        }, indent=2)
    
    # Search for other proteins
    matches = []
    for protein_id, data in DB.items():
        if protein_name in data.get("name", "").lower():
            matches.append({"id": protein_id, "name": data["name"]})
    
    if matches:
        return json.dumps({
            "result_type": "matches",
            "matches": matches
        }, indent=2)
    else:
        return json.dumps({
            "result_type": "error",
            "message": f"No proteins found matching '{protein_name}'"
        }, indent=2)

# 3. Sampling Example
@mcp.tool()
def generate_hypothesis(protein_id: str) -> str:
    """
    Generate a research hypothesis for a protein. Demonstrates sampling by
    providing a prompt that should be completed by an LLM.
    """
    if protein_id not in DB:
        raise ValueError(f"Unknown protein_id: {protein_id}")
    
    info = DB[protein_id]
    token = str(uuid.uuid4())
    pending_callbacks[token] = {"protein_id": protein_id}
    
    prompt = f"The protein {info['name']} is known to {info['function']}. Generate a novel research hypothesis."
    
    return json.dumps({
        "result_type": "sampling",
        "prompt": prompt,
        "callback_token": token
    }, indent=2)

@mcp.tool()
def submit_sampling_result(callback_token: str, llm_result: str) -> str:
    """Submit the result from LLM sampling."""
    if callback_token not in pending_callbacks:
        raise ValueError("Invalid callback token")
    
    protein_info = pending_callbacks.pop(callback_token)
    protein_id = protein_info["protein_id"]
    
    return json.dumps({
        "result_type": "sampling_complete",
        "protein_id": protein_id,
        "llm_result": llm_result,
        "status": "success"
    }, indent=2)

# 4. Streaming Example - Simplified without ToolMessage
@mcp.tool()
async def stream_analysis_log(protein_id: str, ctx: Context) -> str:
    """
    Stream analysis log for a protein. Demonstrates real-time streaming
    of data back to the client using progress updates.
    """
    if protein_id not in DB:
        raise ValueError(f"Unknown protein_id: {protein_id}")
    
    # Get log data or use default steps
    protein_data = DB[protein_id]
    log_data = protein_data.get("log", [
        f"Starting analysis of {protein_data.get('name', protein_id)}",
        "Loading sequence data...",
        "Analyzing domain structure...",
        "Predicting secondary structure...",
        "Identifying functional motifs...",
        "Comparing with homologs...",
        "Checking post-translational modifications...",
        "Validating structural predictions...",
        "Assessing stability...",
        "Evaluating interaction partners...",
        "Generating final report...",
        f"Analysis complete. Function: {protein_data.get('function', 'Unknown')}"
    ])
    
    if isinstance(log_data, str):
        log_lines = log_data.split('\n')
    else:
        log_lines = log_data
    
    # Process each line with progress updates
    results = []
    for i, line in enumerate(log_lines, 1):
        results.append(line)
        
        # Report progress - this will be sent as notifications to the client
        await ctx.report_progress(progress=i, total=len(log_lines), message=line)
        
        # Send log message
        await ctx.info(f"Step {i}/{len(log_lines)}: {line}")
        
        # Simulate processing time
        await asyncio.sleep(0.3)
    
    return "\n".join(results)

app = mcp.streamable_http_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)