# SciLifeLab Workshop: LangGraph AI Agents for Drug Discovery

A comprehensive hands-on workshop teaching participants how to build AI agents using LangGraph, specifically focused on drug discovery applications.

## Workshop Overview

This 60-minute interactive workshop introduces participants to **LangGraph**, a low-level orchestration framework for constructing stateful AI workflows using graphs. Participants will learn to build AI agents that can perform mathematical calculations, search scientific literature, and query drug databases.

### Learning Objectives

By the end of this workshop, participants will:
- Understand core concepts of LangGraph (tools, nodes, edges, state, and memory)
- Create and integrate custom tools for AI agents
- Build a ReAct-style agent from scratch using LLMs and custom tools
- Implement agent memory to maintain conversational context
- Compare custom agents with prebuilt LangGraph agents
- Explore advanced features like error handling and streaming

## Repository Structure

```
workshop/
├── README.md                 # This comprehensive guide
├── requirements.txt          # Python dependencies
├── .env                     # API keys and configuration
├── agent_demo.py            # Complete working demo implementation
├── lab_1.ipynb             # Main workshop notebook (exercises)
├── answers_1.ipynb         # Solution notebook with completed code
├── images/                 # Workshop assets
```

## Workshop Timeline (70 minutes)

| Part | Duration | Topic | Key Concepts |
|------|----------|-------|--------------|
| **Part 1** | 10 min | Setup & Imports | Environment setup, dependency loading |
| **Part 2** | 20 min | Understanding & Creating Tools | `@tool` decorator, function design, API integration |
| **Part 3** | 10 min | Defining State | TypedDict, state management, reducers |
| **Part 4** | 20 min | Building Agent Graph | Nodes, edges, routing, graph compilation |
| **Part 5** | 10 min | Testing the Agent | Interactive loops, streaming responses |
| **Part 6** | 10 min | Adding Memory | Checkpointers, thread management, persistent state |
| **Part 7** | 10 min | Prebuilt Agents | ReAct pattern, comparison with custom graphs |
| **Part 8** | Optional | Extension Exercises | Advanced features, error handling |


## Detailed Notebook Content

### lab_1.ipynb (Workshop Exercises)

**Structure**: 8 parts with progressive complexity
- **Interactive Design**: TODO sections for hands-on coding
- **Guided Learning**: Step-by-step instructions with code templates
- **Domain Focus**: Drug discovery use cases throughout
- **Progressive Complexity**: From simple tools to complete agent systems

### answers_1.ipynb (Complete Solutions)

**Purpose**: Reference implementation with all exercises completed
- **Full Code**: Working solutions for all TODO sections  
- **Error Handling**: Robust implementations with try-catch blocks
- **Best Practices**: Proper Python coding standards and documentation
- **Testing Ready**: Includes visualization and interaction loops

### agent_demo.py (Production Example)

**Features**:
- **Complete Implementation**: Full ReAct agent with all three tools
- **Production Ready**: Comprehensive error handling and logging
- **Interactive**: Command-line interface with streaming responses
- **Configurable**: Thread-based memory management
- **Extensible**: Easy to add new tools and modify behavior

## API Dependencies & External Services

### LitSense API
- **Purpose**: Semantic search of PubMed literature
- **Technology**: NCBI LitSense2 API with neural embeddings
- **Capabilities**: Context-aware biomedical text retrieval
- **Reference**: [LitSense NAR 2025](https://academic.oup.com/nar/article/53/W1/W361/8133630)

### ChEMBL Web Services
- **Purpose**: Comprehensive drug and bioactivity database
- **Coverage**: 2M+ compounds, extensive bioactivity data
- **Features**: Synonym search, mechanism data, clinical phases
- **Documentation**: [ChEMBL Interface Docs](https://chembl.gitbook.io/chembl-interface-documentation/web-services)

### OpenAI API (Will be replaced by SciLifeLab server)
- **Model**: GPT-4o for tool-calling capabilities
- **Configuration**: Temperature=0 for consistent responses
- **Integration**: LangChain ChatOpenAI wrapper


## Extension Ideas (NEED HELP !!!)

### Advanced Features to Explore

1. **Custom Nodes**: Create specialized processing nodes
2. **Custom Tools**: Create several tools, i.e. Protein Structure Tools, Patent Search, Clinical Trial Tools, Regulatory DB
3. **Multi-Agent Systems**: Coordinate multiple specialized agents
4. **Long-term memoery**: Add long-term memory