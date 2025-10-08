# mcp_basic_client.py — debug-wrapped
import asyncio
import os
import sys
import traceback
import urllib.request
from typing import Any

from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
from mcp.shared.exceptions import McpError

SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:8501/mcp")


def content_to_text(obj: Any) -> str:
    """Convert SDK content variants to printable text."""
    if obj is None:
        return ""
    # Tool/Read responses are lists of content items.
    parts = []
    try:
        contents = getattr(obj, "contents", None)
        if contents is None and isinstance(obj, list):
            contents = obj
        if contents is None:
            return str(obj)

        for item in contents:
            # TextContent
            if hasattr(item, "text") and item.text is not None:
                parts.append(item.text)
            # BlobContent
            elif hasattr(item, "blob") and item.blob is not None:
                try:
                    parts.append(item.blob.decode("utf-8"))
                except Exception:
                    parts.append(
                        f"<{len(item.blob)} bytes; mime={getattr(item, 'mimeType', 'application/octet-stream')}>"
                    )
    except Exception as e:
        parts.append(f"<error formatting content: {e}>")
    return "".join(parts)


async def main() -> None:
    print(f"[client] Connecting to: {SERVER_URL}")

    
    try:
        async with streamablehttp_client(SERVER_URL) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                # --- initialize -------------------------------------------------
                try:
                    print("[client] Initializing session...")
                    await session.initialize()
                    print("[client] Session initialized.")
                except McpError as e:
                    print("[MCP ERROR] initialize failed:", repr(e))
                    traceback.print_exc()
                    return
                except Exception as e:
                    print("[UNEXPECTED ERROR] initialize failed:", repr(e))
                    traceback.print_exc()
                    return

                # --- list resources --------------------------------------------
                try:
                    resources_result = await session.list_resources()
                    print("[client] Resources:")
                    # Resources are returned as tuples/namedtuples, access by index or attribute if namedtuple
                    for r in resources_result:
                        # Try accessing by attribute first, then by index
                        if hasattr(r, 'uri'):
                            print(" -", r.uri)
                        elif hasattr(r, '__getitem__') and len(r) > 0:
                            print(" -", r[0])  # First element is likely the URI
                        else:
                            print(" -", r)
                except Exception as e:
                    print("[client] list_resources failed:", repr(e))
                    traceback.print_exc()

                # --- read dataset overview -------------------------------------
                try:
                    overview = await session.read_resource("dataset://proteins")
                    print("\n[client] Dataset overview:")
                    print(content_to_text(overview))
                except Exception as e:
                    print("[client] read_resource(dataset://proteins) failed:", repr(e))
                    traceback.print_exc()

                # --- list tools -------------------------------------------------
                try:
                    tools_result = await session.list_tools()
                    print("\n[client] Tools:")
                    # Tools are returned as tuples/namedtuples
                    for t in tools_result:
                        # Try accessing by attributes first, then by indices
                        if hasattr(t, 'name') and hasattr(t, 'description'):
                            print(" -", t.name, ":", t.description)
                        elif hasattr(t, '__getitem__') and len(t) >= 2:
                            print(" -", t[0], ":", t[1])  # First is name, second is description
                        else:
                            print(" -", t)
                except Exception as e:
                    print("[client] list_tools failed:", repr(e))
                    traceback.print_exc()

                # --- call tool --------------------------------------------------
                try:
                    result = await session.call_tool(
                        "get_protein_function",
                        arguments={"protein_id": "P53_HUMAN"},
                    )
                    print("\n[client] Tool result:")
                    print(content_to_text(result))
                except Exception as e:
                    print("[client] call_tool(get_protein_function) failed:", repr(e))
                    traceback.print_exc()

    except* Exception as eg:
        # Unpack ExceptionGroup from anyio/asyncio to show root causes
        print("\n[client] Caught ExceptionGroup from streamable HTTP context.")
        for i, exc in enumerate(eg.exceptions, 1):
            print(f"  [{i}] {type(exc).__name__}: {exc}")
            traceback.print_exception(type(exc), exc, exc.__traceback__)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())