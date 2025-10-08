# **MCP Workshop \- Official SDK Implementation**

This directory contains production-ready MCP servers and clients built using the official Model Context Protocol Python SDK.

## **Quick Start**

### Run the Server and Client

1.  Open a terminal and navigate to the project directory:

    ```bash
    cd Section_2_MCP/
    ```

2.  Create and activate a virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
4.  Provide the correct API key that was sent to you via email in the ```MCP_python_SDK/.env``` file.
Replace ```"PASTE-YOUR_KEY-HERE"``` with your actual key, making sure to keep the double quotes.

    ```bash
    OPENAI_API_KEY="PASTE-YOUR_KEY-HERE"
    ```

5.  Start the server in the same terminal:

    ```bash
    python MCP_scratch/advanced_server.py
    ```

    Keep this terminal open.  **Do not disconnect it.**

6.  Open another terminal and run the client:

    ```bash
    python MCP_python_SDK/advanced_client.py
    ```

7.  Observe the output in both terminals to see the communication flow.

## **File Structure**

text

MCP_python_SDK/  
├── README.md                 \# This file  
├── protein\_db.json          \# Enhanced protein database  
├── mcp\_basic\_server.py      \# Basic server (resources \+ tools)  
├── mcp\_basic\_client.py      \# Basic client (debug-enabled)  
├── mcp\_advanced\_server.py   \# Advanced server (streaming, sampling, prompts)
└── mcp\_advanced\_client.py   \# Advanced client (OpenAI integration)

## **SDK Features Demonstrated**

### **Basic Server (mcp\_basic\_server.py)**

* Resources: dataset://proteins, protein://{id}  
* Tools: get\_protein\_function  
* Transport: Streamable HTTP  
* Error Handling: Proper MCP error responses

### **Advanced Server (mcp\_advanced\_server.py)**

* Notifications: Client registration and push updates  
* Elicitation: Dynamic user clarification requests  
* Sampling: LLM hypothesis generation with callbacks  
* Streaming: Real-time progress updates  
* Prompts: Template-based conversation patterns

### **Clients**

* Basdksic Client: Simple resource and tool exploration  
* Advanced Client: Full-featured with OpenAI integration

## **Key SDK Benefits**

### **1\. Protocol Compliance**

python

from mcp.server.fastmcp import FastMCP

mcp \= FastMCP("My Server")

*\# Automatically handles JSON-RPC 2.0 compliance*

### **2\. Type Safety & Validation**

python

@mcp.tool()  
def get\_protein\_function(protein\_id: str) \-\> str:  
    *\# SDK validates input types and return values*

    return "Function description"

### **3\. Built-in Transport Support**

python

*\# HTTP, SSE, and STDIO out of the box*  
app \= mcp.streamable\_http\_app()

uvicorn.run(app, host\="0.0.0.0", port\=8501)

### **4\. Progress Reporting**

python

async def stream\_analysis(ctx: Context):

    await ctx.report\_progress(progress\=50, total\=100, message\="Processing...")

## **Comparison with Custom Implementation**

| Aspect | Custom Implementation | SDK Implementation |
| :---- | :---- | :---- |
| Protocol Handling | Manual JSON-RPC 2.0 | Automatic |
| Error Handling | Custom error codes | Standardized MCP errors |
| Transport | Raw HTTP only | HTTP, SSE, STDIO |
| Type Safety | Basic validation | Full type hints |
| Production Ready | Learning purposes | Yes |

## **Advanced Features**

### **Streaming with Progress**

python

@mcp.tool()  
async def stream\_analysis(protein\_id: str, ctx: Context):  
    for i, step in enumerate(steps):  
        await ctx.report\_progress(progress\=i, total\=len(steps), message\=step)

        await asyncio.sleep(0.3)

### **Sampling with LLM Integration**

python

*\# Server provides prompt*  
result \= await session.call\_tool("generate\_hypothesis", {"protein\_id": "P53\_HUMAN"})

*\# Client uses OpenAI to complete*  
completion \= llm\_client.chat.completions.create(  
    model\="gpt-3.5-turbo",   
    messages\=\[{"role": "user", "content": prompt}\]

)

### **Elicitation Pattern**

python

@mcp.tool()  
def find\_protein(protein\_name: str):  
    if protein\_name \== "p53":  
        return json.dumps({  
            "result\_type": "elicitation",  
            "message": "Multiple matches found",  
            "choices": \[  
                {"label": "Human p53", "value": "P53\_HUMAN"},  
                {"label": "Mouse p53", "value": "P53\_MOUSE"}  
            \]

        })

## **Debugging Tips**

### **Enable Debug Output**

The basic client includes comprehensive debug output:

python

def content\_to\_text(obj: Any) \-\> str:  
    """Convert SDK content variants to printable text"""

    *\# Handles TextContent, BlobContent, and errors*

### **Check Server Logs**

bash

*\# Server shows all MCP method calls*

python mcp\_basic\_server.py

### **Environment Variables**

bash

*\# For advanced features*  
export OPENAI\_API\_KEY="your-key-here"

export MCP\_SERVER\_URL="http://localhost:8501/mcp"

## **Deployment**

### **Production Server**

python

import uvicorn  
from mcp\_basic\_server import app

if \_\_name\_\_ \== "\_\_main\_\_":

    uvicorn.run(app, host\="0.0.0.0", port\=8501, log\_level\="info")

### **Docker Deployment**

dockerfile

FROM python:3.11  
WORKDIR /app  
COPY requirements.txt .  
RUN pip install \-r requirements.txt  
COPY . .

CMD \["python", "mcp\_advanced\_server.py"\]

## **Learning Resources**

* [Official MCP Documentation](https://modelcontextprotocol.io/)  
* [MCP Python SDK GitHub](https://github.com/modelcontextprotocol/python-sdk)  
* [MCP Specification](https://spec.modelcontextprotocol.io/)

## **Contributing**

This implementation demonstrates MCP best practices. Feel free to:

1. Extend the protein database with new entries  
2. Add more advanced tools and resources  
3. Implement additional transport layers  
4. Create integration tests

## **Troubleshooting**

### **Common Issues**

1. Port already in use: Change port in server or use lsof \-ti:8501 | xargs kill  
2. OpenAI API errors: Verify API key and quota  
3. Import errors: Ensure MCP SDK is installed: pip install mcp

### **Getting Help**

* Check the official MCP Discord  
* Review SDK documentation  
* Examine debug output in clients

---

Happy Building with MCP\!
