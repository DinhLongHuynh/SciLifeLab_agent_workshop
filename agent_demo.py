import json
from tabnanny import check
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Dict,Annotated, List, Sequence, Union

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_core.messages import ToolMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from chembl_webresource_client.new_client import new_client
from langgraph.checkpoint.memory import InMemorySaver
from litsense_wrapper import LitSense_API


load_dotenv() 

# -----------------------------------------------------------------------------
# Tool definitions
#
# Tools are normal Python functions decorated with the @tool decorator.
# The decorator adds metadata so that the chat model knows how to call
# them.  Tools should accept and return JSON‑serialisable values.

@tool
def calculator(expression: str) -> str:
    """Evaluate mathematical expressions and perform calculations.
    
    This tool can handle:
    - Basic arithmetic: addition (+), subtraction (-), multiplication (*), division (/)
    - Exponents and powers: ** or pow()
    - Mathematical functions: sqrt, log, sin, cos, etc. (if imported)
    - Parentheses for order of operations
    - Decimal numbers and scientific notation
    
    Use this tool when you need to:
    - Calculate drug dosages or concentrations
    - Compute molecular weights or ratios
    - Perform statistical calculations
    - Convert units or calculate IC50 values
    
    Args:
        expression (str): A mathematical expression to evaluate
        
    Returns:
        str: The calculated result or an error message if invalid
    
    Examples of valid expressions:
    - "2 + 3 * 4" → 14
    - "(10 - 2) / 4" → 2.0  
    - "2 ** 8" → 256
    - "3.14159 * 2" → 6.28318
    
    
    Warning: Only use with trusted mathematical expressions.
    """
    try:
        # Beware: `eval` is powerful—never expose this to untrusted input in
        # production without proper sandboxing.  Here it is sufficient for a demo.
        result = eval(expression)
        return str(result)
    except Exception as exc:
        return f"Error evaluating expression: {exc}"


@tool
def get_drug_info(drug_name: str) -> str:
    """Retrieve comprehensive pharmaceutical information from the ChEMBL database.
    
    This tool provides detailed drug/compound information. Best for:
    - Drug discovery research and competitive analysis
    - Mechanism of action studies
    - Finding similar compounds or targets
    - Clinical development phase tracking
    - Literature preparation and grant writing

    Args:
        drug_name (str): Name of drug/compound (generic, brand name, or ChEMBL ID)
        
    Returns:
        str: Formatted report with all available drug information
    
        
    **Usage Examples:**
    - get_drug_info("aspirin") - Get info for a common drug
    - get_drug_info("CHEMBL25") - Look up by ChEMBL ID
    - get_drug_info("Humira") - Brand name lookup
    - get_drug_info("adalimumab") - Generic name lookup
    
        
    Note: Searches ChEMBL database which contains 2M+ compounds and extensive bioactivity data.
    """
    try:
        # Use the search endpoint to pick up synonyms/trade names
        search_results = new_client.molecule.search(drug_name)
        search_list = list(search_results)
        if not search_list:
            return f"No information found for '{drug_name}'"
        
        candidate = search_list[0]
        chembl_id = candidate['molecule_chembl_id']
        details = new_client.molecule.get(chembl_id)
        
        # Build base result
        pref_name = details.get('pref_name') or candidate.get('pref_name') or drug_name
        result = f"**{pref_name}** (ChEMBL ID: {chembl_id})\n"
        result += f"Type: {details.get('molecule_type', 'Not specified')}\n"
        

        if details.get('molecule_properties', {}).get('molecular_formula'):
            result += f"Molecular Formula: {details['molecule_properties']['molecular_formula']}\n"
        
        # Include synonyms/trade names if available
        synonyms = details.get('molecule_synonyms', []) or []
        if synonyms:
            result += "\n**Synonyms/Trade names:**\n"
            unique_synonyms = set()
            for syn in synonyms[:15]:  # Increased limit
                name = syn.get('molecule_synonym') or syn.get('synonyms')
                if name and name.lower() != pref_name.lower():
                    unique_synonyms.add(name)
            for name in sorted(unique_synonyms):
                result += f"- {name}\n"
        
        # Mechanism of action (improved error handling)
        try:
            mechanisms = new_client.mechanism.filter(
                molecule_chembl_id=chembl_id
            ).only(['mechanism_of_action', 'target_chembl_id'])
            mechanism_list = list(mechanisms)
            if mechanism_list:
                result += "\n**Mechanism of Action:**\n"
                unique_mechanisms = set()
                for mech in mechanism_list[:5]:  # Increased limit
                    moa = mech.get('mechanism_of_action')
                    if moa:
                        unique_mechanisms.add(moa)
                for moa in sorted(unique_mechanisms):
                    result += f"- {moa}\n"
        except Exception as e:
            result += f"\nMechanism of action data not available (Error: {str(e)[:50]}...)\n"
        
        # Indications (FIXED - using correct field names)
        try:
            indications = new_client.drug_indication.filter(
                molecule_chembl_id=chembl_id
            ).only(['efo_term', 'mesh_heading', 'max_phase_for_ind'])
            indication_list = list(indications)
            if indication_list:
                result += "\n**Indications:**\n"
                unique_indications = set()
                for ind in indication_list[:10]:  # Increased limit
                    # Use efo_term or mesh_heading as the indication name
                    indication_name = ind.get('efo_term') or ind.get('mesh_heading')
                    max_phase = ind.get('max_phase_for_ind')
                    if indication_name:
                        phase_info = f" (Phase {max_phase})" if max_phase else ""
                        unique_indications.add(f"{indication_name}{phase_info}")
                for indication in sorted(unique_indications):
                    result += f"- {indication}\n"
            else:
                result += "\nNo indication data available.\n"
        except Exception as e:
            result += f"\nIndication data not available (Error: {str(e)[:50]}...)\n"
        
        # Add bioactivity summary if available
        try:
            activities = new_client.activity.filter(
                molecule_chembl_id=chembl_id
            ).only(['standard_type', 'standard_value', 'standard_units'])
            activity_list = list(activities)
            if activity_list:
                result += f"\n**Bioactivity Data Available:** {len(activity_list)} records\n"
                # Show most common activity types
                activity_types = {}
                for act in activity_list[:100]:  # Sample first 100
                    act_type = act.get('standard_type')
                    if act_type:
                        activity_types[act_type] = activity_types.get(act_type, 0) + 1
                
                if activity_types:
                    top_types = sorted(activity_types.items(), key=lambda x: x[1], reverse=True)[:5]
                    result += "Most common activity types: " + ", ".join([f"{t[0]} ({t[1]})" for t in top_types]) + "\n"
        except Exception:
            pass  # Bioactivity is optional

        
        return result
        
    except Exception as e:
        return f"Error querying ChEMBL database for '{drug_name}': {str(e)}"



@tool
def lit_search(query, limit=5):
    """Search PubMed literature using advanced semantic search via LitSense API.
    
    This tool performs intelligent, context-aware literature searches that understand 
    scientific concepts and relationships, providing more relevant results than 
    traditional keyword-based searches.
    
    **Key Capabilities:**
    - Semantic understanding of biomedical concepts
    - Retrieves contextually relevant passage snippets
    - Covers all PubMed indexed literature
    - Returns actual text content, not just abstracts
    - Handles complex scientific queries and relationships
    
    
    **Query Formulation Tips:**
    - Use natural language questions rather than just keywords
    - Include specific drug names, diseases, or biological processes
    - Ask about relationships, mechanisms, or outcomes
    - Be specific about the aspect you're interested in
    
    Args:
        query (str): Natural language research question or scientific topic
        limit (int, optional): Maximum number of results to return (default: 5)
        
    Returns:
        str: Formatted passages from relevant PubMed articles with PMIDs
    
    **Example Queries:**
    - "Clinical trial results for donepezil in Alzheimer's disease"
    - "Mechanism of action of SARS-CoV-2 spike protein inhibitors"
    - "Adverse effects of hydroxychloroquine in COVID-19 patients"
    - "Biomarkers for early detection of Alzheimer's disease"
    - "Drug resistance mechanisms in COVID-19 treatment"
        
    Note: Uses NCBI LitSense2 API for semantic search across millions of PubMed records.
    Results include passage text and PubMed ID for further reference.
    """
    try:
        engine = LitSense_API()
        results = engine.retrieve(query, limit=limit)
        
        if not results:
            return f"No relevant literature found for '{query}'. Please try a different or broader search query."
        
        result_str = ""
        for i, result in enumerate(results):
            result_str += (
                f"\n--- Passage #{i+1} ---\n"
                f"PMID: {result.pmid}\n"
                f"Content: {result.text}\n"
            )
        
        return result_str
    
    except Exception as e:
        return f"Error retrieving literature for '{query}': {str(e)}. Please try a different search query."


# Collect all tool instances into a list.  The chat model will know their
# signatures and choose when to call them based on the conversation.
TOOLS = [calculator, get_drug_info, lit_search]


# -----------------------------------------------------------------------------
# LangGraph setup
#
class ChatState(TypedDict):
    """The state schema for our LangGraph.  It contains only a list of messages.

    Messages are appended via the `add_messages` reducer to preserve the full
    conversation history.  Each message is represented as a dict with `role`
    and `content` keys (compatible with the OpenAI API message format).
    """

    messages: Annotated[List[Dict], add_messages]


def build_graph() -> StateGraph:
    """Construct and compile the LangGraph for the demo agent."""
    graph_builder = StateGraph(ChatState)

    # Initialise the chat model.  This example uses OpenAI's gpt‑3.5‑turbo but
    # any tool‑calling LLM supported by LangChain will work.  Make sure
    # OPENAI_API_KEY is set in your environment.
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    # Bind the tools to the LLM so that it knows their schemas and how to
    # construct tool calls in JSON.
    llm_with_tools = llm.bind_tools(TOOLS)

    def chatbot(state: ChatState) -> Dict[str, List]:
        """The main chatbot node.  It invokes the LLM with the current messages."""
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    graph_builder.add_node("chatbot", chatbot)

    # Add the built-in ToolNode to the graph
    tool_node = ToolNode(TOOLS)
    graph_builder.add_node("tools", tool_node)

    # Routing function decides whether to run tools or finish.
    # If the last AI message has tool calls, route to "tools", otherwise END.
    def route_tools(state: ChatState) -> str:
        messages = state.get("messages", [])
        ai_message = messages[-1] if messages else None
        if ai_message and getattr(ai_message, "tool_calls", []):
            return "tools"
        return END

    # Set up the conditional routing and edges
    graph_builder.add_conditional_edges(
        "chatbot",
        route_tools,
        {"tools": "tools", END: END},
    )
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")
    checkpointer = InMemorySaver()
    return graph_builder.compile(checkpointer=checkpointer)


def chat_loop() -> None:
    """Run an interactive chat loop with the compiled graph."""
    graph = build_graph()
    print("Welcome to the LangGraph ReAct demo!  Ask me a question.")
    print(
        "I can perform simple math, look up basic drug information, and search"
        " PubMed via LitSense."
    )
    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break
        if not user_input or user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break
        # Start the conversation with a user message
        state = {"messages": [{"role": "user", "content": user_input}]}
        # Stream events from the graph
        config = {
            "configurable": {
                "thread_id": "1", 
                "recursion_limit": 25
            }
        }
        for event in graph.stream(state, config=config):
            for value in event.values():
                # The last message in the state is the AI response
                msg = value["messages"][-1]
                # Use the built-in pretty_print method for better formatting
                msg.pretty_print()


if __name__ == "__main__":
    chat_loop()