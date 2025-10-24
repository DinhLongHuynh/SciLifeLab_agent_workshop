import requests
import json

class MCPClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.request_id = 1

    def _send_request(self, method, params=None):
        payload = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method
        }
        if params:
            payload["params"] = params

        self.request_id += 1
        response = requests.post(self.server_url, json=payload)
        return response.json()

    def initialize(self):
        return self._send_request("initialize")

    def list_resources(self):
        return self._send_request("resources/list")

    def read_resource(self, uri):
        return self._send_request("resources/read", {"uri": uri})

    def list_tools(self):
        return self._send_request("tools/list")

    def call_tool(self, name, arguments):
        return self._send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })

# Demo the client
def demo_basic_mcp():
    client = MCPClient("http://localhost:8501/mcp")

    print("=== MCP Basic Client Demo ===\n")

    # 1. Initialize
    print("1. Initializing MCP connection...")
    init_result = client.initialize()
    print(f"   Server: {init_result['result']['serverInfo']['name']}")
    print(f"   Protocol: {init_result['result']['protocolVersion']}\n")

    # 2. List Resources
    print("2. Listing available resources...")
    resources = client.list_resources()
    for resource in resources['result']['resources']:
        print(f"   {resource['name']}: {resource['uri']}")
    print()

    # 3. Read Resource
    print("3. Reading protein resource...")
    protein_data = client.read_resource("protein://proteins")
    data = json.loads(protein_data['result']['contents'][0]['value'])
    print(f"   Found {len(data)} proteins in database\n")

    # 4. List Tools
    print("4. Listing available tools...")
    tools = client.list_tools()
    for tool in tools['result']['tools']:
        print(f"   {tool['name']}: {tool['description']}")
    print()

    # 5. Call Tool
    print("5. Calling tool to get protein function...")
    tool_result = client.call_tool("get_protein_function", {"protein_id": "P53_HUMAN"})
    print(f"   Result: {tool_result['result']['content'][0]['text']}")

if __name__ == '__main__':
    try:
        demo_basic_mcp()
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to MCP server. Is basic_server.py running?")
