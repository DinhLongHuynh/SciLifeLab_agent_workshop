from flask import Flask, jsonify, request
import json

app = Flask(__name__)

with open('MCP_scratch/protein_db.json') as f:
    protein_db = json.load(f)

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

    # Initialize method (MCP handshake)
    if method == 'initialize':
        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "resources": {},
                    "tools": {},
                    "logging": {}
                },
                "serverInfo": {
                    "name": "Protein MCP Server",
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
                    "description": "Sample protein data",
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

    # Tools methods
    elif method == 'tools/list':
        return jsonify({
            "jsonrpc": "2.0",
            "result": {
                "tools": [{
                    "name": "get_protein_function",
                    "description": "Get protein function by ID",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "protein_id": {"type": "string", "description": "Protein ID (e.g., P53_HUMAN)"}
                        },
                        "required": ["protein_id"]
                    }
                }]
            },
            "id": request_id
        })

    elif method == 'tools/call':
        tool_name = params.get('name')
        arguments = params.get('arguments', {})

        if tool_name == 'get_protein_function':
            protein_id = arguments.get('protein_id')
            if protein_id in protein_db:
                return jsonify({
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": f"Function of {protein_id}: {protein_db[protein_id]['function']}"
                        }]
                    },
                    "id": request_id
                })
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": -32602, "message": f"Protein {protein_id} not found"},
                "id": request_id
            })

        return jsonify({
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Tool not found"},
            "id": request_id
        })

    elif method == 'notifications/initialized':
        # Acknowledge initialization
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

if __name__ == '__main__':
    print("MCP Basic Server running on http://localhost:8501")
    print("This server follows the official MCP specification with JSON-RPC 2.0")
    app.run(port=8501)
