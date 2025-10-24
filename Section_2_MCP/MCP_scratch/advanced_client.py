import requests
import json
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class MCPAdvancedClient:
    def __init__(self, server_url):
        self.server_url = server_url
        self.request_id = 1
        self.llm_client = OpenAI() if os.getenv('OPENAI_API_KEY') else None

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

    def list_tools(self):
        return self._send_request("tools/list")

    def call_tool(self, name, arguments):
        return self._send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })

    def list_prompts(self):
        return self._send_request("prompts/list")

    def get_prompt(self, name, arguments=None):
        params = {"name": name}
        if arguments:
            params["arguments"] = arguments
        return self._send_request("prompts/get", params)

def demo_advanced_mcp():
    client = MCPAdvancedClient("http://localhost:8502/mcp")

    print("=== MCP Advanced Client Demo ===\n")

    # 1. Initialize
    print("1. Initializing advanced MCP connection...")
    init_result = client.initialize()
    print(f"Connected to {init_result['result']['serverInfo']['name']}\n")

    # 2. List and demonstrate tools
    print("2. Available advanced tools:")
    tools = client.list_tools()
    for tool in tools['result']['tools']:
        print(f"{tool['name']}: {tool['description']}")
    print()

    # 3. Demonstrate elicitation-like behavior
    print("3. Testing protein search (elicitation simulation)...")
    search_result = client.call_tool("find_protein", {"protein_name": "p53"})
    print(f"   {search_result['result']['content'][0]['text']}\n")

    # 4. Demonstrate hypothesis generation
    print("4. Testing hypothesis generation (sampling simulation)...")
    hypothesis_result = client.call_tool("get_protein_hypothesis", {"protein_id": "P0DTC2"})
    prompt_text = hypothesis_result['result']['content'][0]['text']
    print(f"   Prompt: {prompt_text.split('PROMPT FOR LLM: ')[1]}...")

    # Use LLM if available
    if client.llm_client:
        try:
            completion = client.llm_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt_text}]
            )
            hypothesis = completion.choices[0].message.content
            print(f"LLM Hypothesis: {hypothesis}...\n")
        except Exception as e:
            print(f"LLM call failed: {e}\n")
    else:
        print("Set OPENAI_API_KEY to see LLM sampling in action\n")

    # 5. Demonstrate prompts feature
    print("5. Testing MCP prompts feature...")
    prompts = client.list_prompts()
    for prompt in prompts['result']['prompts']:
        print(f"{prompt['name']}: {prompt['description']}")

    prompt_result = client.get_prompt("protein_analysis", {"protein_id": "P53_HUMAN"})
    print(f"Prompt messages: {len(prompt_result['result']['messages'])} message(s)\n")

    print("6. Streaming simulation...")
    print("(In real MCP with bidirectional transport, streaming would happen here)")
    print("This demo shows the progress notification pattern\n")

if __name__ == '__main__':
    try:
        demo_advanced_mcp()
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to MCP server. Is advanced_server.py running?")
    except Exception as e:
        print(f"ERROR: {e}")
