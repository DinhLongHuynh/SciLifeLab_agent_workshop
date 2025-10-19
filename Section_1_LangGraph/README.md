# SciLifeLab Workshop: LangGraph AI Agents for Drug Discovery
---

A comprehensive hands-on workshop tutoring participants how to build AI agents using LangGraph, specifically focused on drug discovery applications.

## Workshop Overview

This 70-minute interactive workshop introduces participants to **LangGraph**, a low-level orchestration framework for constructing stateful AI workflows using graphs. Participants will learn to build AI agents that can perform mathematical calculations, search scientific literature, and query drug databases.

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



