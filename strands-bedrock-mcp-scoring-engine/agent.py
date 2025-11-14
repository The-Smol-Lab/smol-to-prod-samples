from strands import Agent
from strands_tools import calculator
from strands.models import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from tools import eligibility_scoring_model
from prompts import SALES_SPECIALIST_PROMPT


# Initialize Bedrock AgentCore app
app = BedrockAgentCoreApp()

# Create a Bedrock model with the custom session
def create_agent() -> Agent:
    """Configure and return a Strands agent instance."""
    model = BedrockModel(
        model_id="global.anthropic.claude-haiku-4-5-20251001-v1:0",
    )
    return Agent(
        model=model,
        tools=[calculator, eligibility_scoring_model],
        system_prompt=SALES_SPECIALIST_PROMPT,
    )

# Instantiate agent globally once for performance
agent = create_agent()

@app.entrypoint
async def agent_invocation(payload):
    """Handler for agent invocation"""
    user_message = payload.get(
        "prompt", "No prompt found in input, please guide customer to create a json payload with prompt key"
    )
    stream = agent.stream_async(user_message)
    async for event in stream:
        print(event)
        yield (event)

if __name__ == "__main__":
    app.run()
