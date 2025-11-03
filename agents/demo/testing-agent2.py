"""
NEW 02: Use Existing Azure AI Foundry Agent (Interactive Demo)

This demo connects to an EXISTING agent in Azure AI Foundry.
You'll need to update the .env02 file with your agent ID.
"""

import asyncio
import os
import pathlib
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential, ClientSecretCredential
from azure.identity.aio import InteractiveBrowserCredential



# Load environment variables
env_path = pathlib.Path(__file__).parent / '.env'
print(f"Looking for .env file at: {env_path}")
print(f"File exists: {env_path.exists()}")
load_dotenv(env_path)

PROJECT_ENDPOINT = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
AGENT_ID = os.getenv("AZURE_AI_AGENT_ID")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")

async def main():
    """Interactive demo: Connect to existing agent."""
    
    print("\n" + "="*70)
    print("🔗 DEMO: Connect to Existing Azure AI Foundry Agent")
    print("="*70)
    
    print(f"\n📋 Connecting to agent: {AGENT_ID}")
    
    async with (
        InteractiveBrowserCredential(tenant_id=AZURE_TENANT_ID) as credential,
        ChatAgent(
        chat_client=AzureAIAgentClient(
                async_credential=credential,
                project_endpoint=PROJECT_ENDPOINT,
                agent_id=AGENT_ID
            )
        ) as agent
    ):
        print("✅ Connected successfully!")
        
        print("\n" + "="*70)
        print("💬 Interactive Chat (Type 'quit' to exit)")
        print("="*70 + "\n")
        
        while True:
            # Get user input
            user_input = input("You: ")
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not user_input.strip():
                continue
            
            # Get streaming response
            print("Agent: ", end="", flush=True)
            async for chunk in agent.run_stream(user_input):
                if chunk.text:
                    print(chunk.text, end="", flush=True)
            print("\n")


if __name__ == "__main__":
    asyncio.run(main())