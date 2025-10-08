# mcp_advanced_client.py
import asyncio
import json
import os
from typing import Any
from openai import OpenAI
from dotenv import load_dotenv

from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

# Load environment variables
load_dotenv()

SERVER_URL = "http://localhost:8501/mcp"

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    llm_client = OpenAI(api_key=openai_api_key)
    print("✅ OpenAI client initialized")
else:
    llm_client = None
    print("❌ OPENAI_API_KEY not found. Sampling demo will be skipped.")

def extract_json_from_result(result: Any) -> str:
    """Extract the actual result text from MCP response."""
    try:
        # If it's a ToolResult with structured_content
        if hasattr(result, 'structured_content') and result.structured_content:
            if 'result' in result.structured_content:
                return result.structured_content['result']
        
        # If it's a ToolResult with content
        if hasattr(result, 'content') and result.content:
            for item in result.content:
                if hasattr(item, 'text') and item.text:
                    return item.text
        
        # Fallback to string representation
        return str(result)
    except Exception as e:
        print(f"Error extracting result: {e}")
        return str(result)

async def handle_elicitation(result) -> str:
    """Handle elicitation responses from the server."""
    result_text = extract_json_from_result(result)
    
    try:
        data = json.loads(result_text)
        if data.get("result_type") == "elicitation":
            print(f"\n🔍 {data['message']}")
            for i, choice in enumerate(data["choices"], 1):
                print(f"  {i}. {choice['label']} ({choice['value']})")
            
            # In a real client, you'd get user input here
            # For demo, auto-select the first option
            selected = data["choices"][0]["value"]
            print(f"Auto-selecting: {selected}")
            return selected
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing elicitation response: {e}")
        print(f"Raw response: {result_text}")
    
    return None

async def handle_sampling(result, session: ClientSession) -> None:
    """Handle sampling responses from the server using real OpenAI API."""
    result_text = extract_json_from_result(result)
    
    try:
        data = json.loads(result_text)
        if data.get("result_type") == "sampling":
            print(f"\n🎯 Sampling Request:")
            print(f"Prompt: {data['prompt']}")
            
            if not llm_client:
                print("❌ Skipping LLM call - OpenAI client not available")
                return
            
            try:
                # Call OpenAI API with the prompt from the server
                print("🔄 Calling OpenAI API...")
                completion = llm_client.chat.completions.create(
                    model="gpt-3.5-turbo",  # or "gpt-4" if you have access
                    messages=[
                        {"role": "system", "content": "You are a helpful scientific research assistant. Generate concise and novel research hypotheses based on protein information."},
                        {"role": "user", "content": data['prompt']}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                
                llm_result = completion.choices[0].message.content
                print(f"🤖 LLM Response: {llm_result}")
                
                # Submit the result back to the server
                print("📤 Submitting result to server...")
                submit_result = await session.call_tool(
                    "submit_sampling_result",
                    arguments={
                        "callback_token": data["callback_token"],
                        "llm_result": llm_result
                    }
                )
                
                submit_text = extract_json_from_result(submit_result)
                submit_data = json.loads(submit_text)
                if submit_data.get("status") == "success":
                    print(f"✅ Sampling result successfully submitted for protein {submit_data.get('protein_id')}")
                else:
                    print(f"❌ Failed to submit sampling result: {submit_text}")
                    
            except Exception as e:
                print(f"❌ Error calling OpenAI API: {e}")
                
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing sampling response: {e}")
        print(f"Raw response: {result_text}")

async def main() -> None:
    print(f"🔗 Connecting to advanced MCP server: {SERVER_URL}")
    
    async with streamablehttp_client(SERVER_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # Demo 1: Register for notifications
            print("\n" + "="*50)
            print("1. CLIENT REGISTRATION")
            print("="*50)
            
            try:
                reg_result = await session.call_tool(
                    "register_client",
                    arguments={
                        "client_id": "advanced_sdk_client",
                        "callback_url": "http://localhost:8505/mcp_callback"
                    }
                )
                reg_text = extract_json_from_result(reg_result)
                print(f"Registration: {reg_text}")
            except Exception as e:
                print(f"Registration failed (expected in demo): {e}")
            
            # Demo 2: Elicitation example
            print("\n" + "="*50)
            print("2. ELICITATION DEMO")
            print("="*50)
            
            elicitation_result = await session.call_tool(
                "find_protein",
                arguments={"protein_name": "p53"}
            )
            
            # Handle elicitation response
            selected_protein = await handle_elicitation(elicitation_result)
            if selected_protein:
                # Get the selected protein details
                protein_result = await session.call_tool(
                    "get_protein_function",
                    arguments={"protein_id": selected_protein}
                )
                protein_text = extract_json_from_result(protein_result)
                print(f"Selected protein function: {protein_text}")
            
            # Demo 3: Sampling example with real LLM
            print("\n" + "="*50)
            print("3. SAMPLING DEMO (with real OpenAI API)")
            print("="*50)
            
            if llm_client:
                sampling_result = await session.call_tool(
                    "generate_hypothesis",
                    arguments={"protein_id": "P0DTC2"}  # Using a different protein for variety
                )
                
                await handle_sampling(sampling_result, session)
            else:
                print("❌ Skipping sampling demo - OpenAI API key not configured")
                print("💡 Set OPENAI_API_KEY in your .env file to enable this feature")
            
            # Demo 4: Streaming example
            print("\n" + "="*50)
            print("4. STREAMING DEMO")
            print("="*50)
            
            print("Starting streaming analysis...")
            try:
                stream_result = await session.call_tool(
                    "stream_analysis_log",
                    arguments={"protein_id": "P53_HUMAN"}
                )
                stream_text = extract_json_from_result(stream_result)
                print(f"Streaming complete. Final result:\n{stream_text}")
            except Exception as e:
                print(f"Streaming demo completed: {e}")
            
            # Demo 5: Trigger notification
            print("\n" + "="*50)
            print("5. NOTIFICATION DEMO")
            print("="*50)
            
            try:
                trigger_result = await session.call_tool(
                    "trigger_notification",
                    arguments={}
                )
                trigger_text = extract_json_from_result(trigger_result)
                print(f"Notification trigger: {trigger_text}")
            except Exception as e:
                print(f"Notification trigger failed (expected in demo): {e}")
            
            print("\n" + "="*50)
            print("ADVANCED CLIENT DEMO COMPLETE")
            print("="*50)

if __name__ == "__main__":
    asyncio.run(main())