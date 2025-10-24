# AI Agents in Life Sciences: Hands-on Session 2 - AI agent collaboration with the Model Context Protocol (MCP)

Welcome! The **`mcp_workshop.ipynb`** Jupyter Notebook provides a complete, hands-on guide to the Model Context Protocol (MCP). It is designed to teach you the fundamentals from first principles, starting with core theory and moving directly into practical, "from-scratch" implementations.

By the end of this notebook, you will have built and tested your own basic and advanced MCP servers and clients using Python, Flask, and REST APIs.

## What You'll Learn

This notebook follows a clear learning path to get you up and running with MCP:

* **Core concepts**: Understand the 3-part architecture (Host, Client, Server) and the two-layer (Data, Transport) design.

* **Basic primitives**: Learn to implement Resources (read-only data) and Tools (executable functions).

* **Full basic implementation**: Combine the primitives to build and run a complete basic_server.py and basic_client.py.

* **Advanced features**: Explore powerful concepts like Prompts, Streaming, Notifications, and Sampling.

* **Full Advanced implementation**: Build an advanced_server.py and advanced_client.py that simulates these advanced features.

## How to Use This Notebook

To help guide you, the notebook is organized into several concise “**parts**.” We want this to be a smooth and enjoyable learning experience, so please don't feel overwhelmed by the amount of material.

### Here’s a friendly tip on how to best navigate the content:

* **For reading & understanding**: Most sections (**Parts 1, 2, and 4**) are there for you to read, explore, and observe. They are designed to help you build a thorough understanding of the core concepts at your own pace.

* **For hands-on action**: Only **Part 3 and Part 5** contain cells that are meant to be run directly within the notebook.

* **Running your code**: These interactive parts will generate a few Python scripts for you. The next action, as guided by the notebook, will be to run these scripts in separate terminals to see the client and server communication live!

* **Finally**, **Part 6 and Part 7** are included as **optional bonus exercises**. Feel free to explore them if you're curious and have extra time, but they are not required.

#### Part 1: Core components & architecture

* Host, Client, Server responsibilities

* Two‑layer view: data layer and protocol layer

#### Part 2: Resources and tools (the MCP primitives)

* **Resources**: list/read resources (e.g., `protein://proteins`)

* **Tools**: list & call tools (e.g., `find_protein`, `get_protein_function`, `get_protein_hypothesis`)

#### Part 3: Putting it together (This will automatically create the scripts you’ll need next)

* Generate a small dataset (e.g., `protein_db.json` with IDs like `P53_HUMAN`, `P53_MOUSE`, `P0DTC2`)

* Stand up a minimal Flask MCP server and a simple client

#### Part 4: Advanced concepts

* **Prompts**: list prompts and get a prompt template (e.g., `protein_analysis`)

* **Streaming & notifications**: simulate progress (e.g., `analyze_protein_stream`) and long‑running tasks

* **Sampling**: demonstrate how an LLM can assist client decisions (**requires API key**)

#### Part 5: Advanced integration test (This will automatically create the scripts you’ll need next)

* Start the advanced server and run a richer client that exercises prompts, tools, streaming, and progress

#### Part 6: Official MCP SDK implementation (Bonus part, completely optional, but fun to explore!)

* How the SDK streamlines transport, typing, and method coverage

#### Part 7: Connect to an existing host (Bonus part, completely optional, but fun to explore!)

* Quick notes for trying MCP against an external host (e.g., via `Postman`)

## Scripts the notebook generates

Running the notebook will write a few helper files to your working directory so you can test outside Jupyter:

| File                 | What it is                                                                                       | How to run                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| `protein_db.json`    | Tiny demo dataset used by the servers (includes IDs like `P53_HUMAN`, `P53_MOUSE`, `P0DTC2`)     | *(created automatically by the notebook)*                                                          |
| `basic_server.py`    | Minimal JSON‑RPC endpoint that exposes **resources** and **tools**                               | `python basic_server.py` → serves at **[http://127.0.0.1:8501/mcp](http://127.0.0.1:8501/mcp)**    |
| `advanced_server.py` | Adds **prompts**, **streaming/progress**, and richer responses                                   | `python advanced_server.py` → serves at **[http://127.0.0.1:8502/mcp](http://127.0.0.1:8502/mcp)** |
| `basic_client.py` | Calls list/read/call methods; uses `OPENAI_API_KEY` if present | `python basic_client.py` (expects advanced server on **8501**)                                  |
| `advanced_client.py` | Calls list/read/call methods, prompts, and simulates streaming; uses `OPENAI_API_KEY` if present | `python advanced_client.py` (expects advanced server on **8502**)                                  |

**Happy learning!**
