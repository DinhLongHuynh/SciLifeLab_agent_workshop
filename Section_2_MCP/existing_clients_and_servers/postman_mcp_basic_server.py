# mcp_basic_server.py

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
)

# ---- Resources -----------------------------------------------------------------
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

if __name__ == "__main__":
    
    mcp.run(transport="stdio")