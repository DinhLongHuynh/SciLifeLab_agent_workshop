from flask import Flask, jsonify, request, Response, stream_with_context
import json
import uuid
import time
from threading import Thread
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load data
with open('MCP_scratch/protein_db.json') as f:
    protein_db = json.load(f)

# Server state
server_state = {
    "clients": {},
    "pending_requests": {}
}

@app.route('/mcp', methods=['POST'])
def handle_mcp():
    data = request.json

    # Validate JSON-RPC 2.0
    if data.get('jsonrpc') != '2.0':
        return jsonify({
            "jsonrpc": "2.0",
            "error": {"code": -32600, "message": "Invalid Request"},
            "id": None
        })

    method = data.get('method')
    params = data.get('params', {})
    request_id = data.get('id')

    logger.info(f"MCP Method: {method}")

    # Initialize method (MCP handshake)
    if method == 'initialize':
        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "resources": {"listChanged": True},
                    "tools": {},
                    "logging": {},
                    "prompts": {}
                },
                "serverInfo": {
                    "name": "Advanced Protein MCP Server",
                    "version": "1.0.0"
                }
            },
            "id": request_id
        })

    # Resources methods
    elif method == 'resources/list':
        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "resources": [{
                    "uri": "protein://proteins",
                    "name": "Protein Database",
                    "description": "Sample protein data with streaming capability",
                    "mimeType": "application/json"
                }]
            },
            "id": request_id
        })

    elif method == 'resources/read':
        uri = params.get('uri')
        if uri == 'protein://proteins':
            return jsonify({
                "jsonrpc": "2.0",
                "result": {
                    "contents": [{
                        "uri": uri,
                        "mimeType": "application/json", 
                        "value": json.dumps(protein_db)
                    }]
                },
                "id": request_id
            })
        return jsonify({
            "jsonrpc": "2.0", 
            "error": {"code": -32601, "message": "Resource not found"},
            "id": request_id
        })

    # Tools methods with advanced features
    elif method == 'tools/list':
        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "tools": [
                    {
                        "name": "find_protein",
                        "description": "Find protein by name with disambiguation",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "protein_name": {"type": "string", "description": "Protein name to search for"}
                            },
                            "required": ["protein_name"]
                        }
                    },
                    {
                        "name": "analyze_protein_stream",
                        "description": "Stream protein analysis in real-time", 
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "protein_id": {"type": "string", "description": "Protein ID to analyze"}
                            },
                            "required": ["protein_id"]
                        }
                    },
                    {
                        "name": "get_protein_hypothesis",
                        "description": "Generate research hypothesis for a protein",
                        "inputSchema": {
                            "type": "object", 
                            "properties": {
                                "protein_id": {"type": "string", "description": "Protein ID"}
                            },
                            "required": ["protein_id"]
                        }
                    }
                ]
            },
            "id": request_id
        })

    elif method == 'tools/call':
        tool_name = params.get('name')
        arguments = params.get('arguments', {})

        # Tool 1: Find protein with disambiguation (Elicitation simulation)
        if tool_name == 'find_protein':
            protein_name = arguments.get('protein_name', '').lower()

            # Simulate elicitation by returning multiple options
            if protein_name == 'p53':
                return jsonify({
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": "Multiple proteins match 'p53'. Please specify:\n- P53_HUMAN (Human p53)\n- P53_MOUSE (Mouse p53)"
                        }],
                        "isError": False
                    },
                    "id": request_id
                })

            # Search for exact matches
            matches = []
            for protein_id, info in protein_db.items():
                if protein_name in info['name'].lower():
                    matches.append(f"{protein_id}: {info['name']} ({info['organism']})")

            if matches:
                return jsonify({
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{
                            "type": "text", 
                            "text": f"Found {len(matches)} proteins:\n" + "\n".join(f"- {m}" for m in matches)
                        }]
                    },
                    "id": request_id
                })
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": -32602, "message": "No proteins found"},
                "id": request_id
            })

        # Tool 2: Streaming analysis
        elif tool_name == 'analyze_protein_stream':
            protein_id = arguments.get('protein_id')

            if protein_id not in protein_db:
                return jsonify({
                    "jsonrpc": "2.0",
                    "error": {"code": -32602, "message": "Protein not found"},
                    "id": request_id
                })

            # For streaming, we'd normally use Server-Sent Events or websockets
            # For this demo, we'll simulate streaming with delayed chunks
            def generate_stream():
                protein = protein_db[protein_id]
                log_lines = protein.get('log', '').split('\n')

                for i, line in enumerate(log_lines):
                    if line.strip():
                        chunk = {
                            "jsonrpc": "2.0",
                            "method": "tools/call/progress",
                            "params": {
                                "progress": {
                                    "progress": (i + 1) / len(log_lines),
                                    "message": line
                                }
                            }
                        }
                        # In real MCP, this would be a server-initiated notification
                        # For HTTP, we simulate with multiple responses
                        yield f"data: {json.dumps(chunk)}\n\n"
                        time.sleep(0.5)

            return Response(stream_with_context(generate_stream()), mimetype='text/plain')

        # Tool 3: Hypothesis generation (Sampling simulation)
        elif tool_name == 'get_protein_hypothesis':
            protein_id = arguments.get('protein_id')

            if protein_id not in protein_db:
                return jsonify({
                    "jsonrpc": "2.0", 
                    "error": {"code": -32602, "message": "Protein not found"},
                    "id": request_id
                })

            protein_info = protein_db[protein_id]

            # Return a prompt that the client can use with their LLM
            return jsonify({
                "jsonrpc": "2.0",
                "result": {
                    "content": [{
                        "type": "text",
                        "text": f"PROMPT FOR LLM: Based on this protein information, generate a novel research hypothesis.\n\nProtein: {protein_info['name']}\nOrganism: {protein_info['organism']}\nFunction: {protein_info['function']}\n\nHypothesis:"
                    }]
                },
                "id": request_id
            })

        return jsonify({
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Tool not found"},
            "id": request_id
        })

    # Prompts method (MCP standard for template-based generation)
    elif method == 'prompts/list':
        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "prompts": [{
                    "name": "protein_analysis",
                    "description": "Generate comprehensive protein analysis",
                    "arguments": [{
                        "name": "protein_id",
                        "description": "ID of the protein to analyze",
                        "required": True
                    }]
                }]
            },
            "id": request_id
        })

    elif method == 'prompts/get':
        prompt_name = params.get('name')
        prompt_args = params.get('arguments', {})

        if prompt_name == 'protein_analysis':
            protein_id = prompt_args.get('protein_id')
            if protein_id in protein_db:
                protein = protein_db[protein_id]
                return jsonify({
                    "jsonrpc": "2.0",
                    "result": {
                        "description": f"Analysis of {protein['name']}",
                        "messages": [{
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": f"Analyze this protein and provide insights:\n\nName: {protein['name']}\nOrganism: {protein['organism']}\nFunction: {protein['function']}"
                            }
                        }]
                    },
                    "id": request_id
                })

        return jsonify({
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Prompt not found"},
            "id": request_id
        })

    elif method == 'notifications/initialized':
        # Client is ready - we could send notifications here
        client_info = params.get('clientInfo', {})
        logger.info(f"Client initialized: {client_info}")
        return jsonify({
            "jsonrpc": "2.0",
            "result": None,
            "id": request_id
        })

    return jsonify({
        "jsonrpc": "2.0", 
        "error": {"code": -32601, "message": "Method not found"},
        "id": request_id
    })

# Background thread for simulating notifications
def send_periodic_notifications():
    """Simulate server-initiated notifications"""
    while True:
        time.sleep(30)  # Every 30 seconds
        # In real MCP with bidirectional transport, we'd send notifications here
        logger.info("Simulated: Server would send notification to clients now")

if __name__ == '__main__':
    print("MCP Advanced Server running on http://localhost:8502")

    # Start notification thread
    notification_thread = Thread(target=send_periodic_notifications, daemon=True)
    notification_thread.start()

    app.run(port=8502, debug=False)
