# mcp_basic_server.py
# Official MCP Python SDK version of the workshop's *basic_server.py*.
# It exposes:
#   - Resources:
#       dataset://proteins            -> overview of the dataset
#       protein://{protein_id}        -> a specific protein record
#   - Tools:
#       get_protein_function(protein_id) -> returns the function string
#
# Run (choose one):
#   python mcp_basic_server.py
#   # or with uv tool:
#   # uv run mcp run mcp_basic_server.py
#
# Connect via Streamable HTTP at: http://localhost:8501/mcp

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Tuple

from mcp.server.fastmcp import FastMCP, Context

HERE = Path(__file__).parent
DB_PATH = HERE / "protein_db.json"
DB: dict[str, dict[str, Any]] = json.loads(DB_PATH.read_text(encoding="utf-8"))

mcp = FastMCP(
    name="MCP Workshop (Official SDK) - Basic",
    instructions="Basic MCP server exposing a toy protein dataset and a simple tool.",
    #host="0.0.0.0", 
    #port=8501
)

# ---- Resources -----------------------------------------------------------------
# Dataset overview (mirrors '/mcp/datasets/list' in the REST version conceptually)
@mcp.resource("dataset://proteins")
def dataset_overview() -> str:
    overview = {
        "id": "proteins",
        "count": len(DB),
        "ids": sorted(DB.keys()),
        "description": "Toy protein dataset used for the MCP workshop",
    }
    # Returning a string will be sent to the client as text content
    return json.dumps(overview, indent=2)

# Per-protein resource (mirrors '/mcp/datasets/get' + selection)
@mcp.resource("protein://{protein_id}")
def get_protein(protein_id: str) -> Tuple[bytes, str]:
    record = DB.get(protein_id)
    if not record:
        payload = {"error": f"Unknown protein_id: {protein_id}"}
        return json.dumps(payload).encode("utf-8"), "application/json"
    payload = {"id": protein_id, **record}
    # Returning (bytes, mime_type) uses the non-deprecated ReadResource return
    # pattern in the official SDK examples.
    return json.dumps(payload, indent=2).encode("utf-8"), "application/json"

# ---- Tools ---------------------------------------------------------------------
@mcp.tool()
def get_protein_function(protein_id: str) -> str:
    """Return the functional annotation for a given protein ID."""
    rec = DB.get(protein_id)
    if not rec:
        raise ValueError(f"Unknown protein_id: {protein_id}")
    return rec["function"]


app = mcp.streamable_http_app()

if __name__ == "__main__":
    # Streamable HTTP is the recommended network transport in the official SDK.
    # You can pass host/port here; defaults are host='127.0.0.1', port=8000.
    # We bind to the same port (8501) used in the REST workshop.
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)