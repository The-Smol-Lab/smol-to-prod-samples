from strands import Agent
from strands_tools import calculator
from strands.models import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from tools import eligibility_scoring_model


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
        system_prompt="You're a helpful assistant. You can do simple math calculations and run the Car4Cash eligibility scoring model.",
    )

# Instantiate agent globally once for performance
agent = create_agent()

@app.entrypoint
async def agent_invocation(payload: dict):
    """Stream model output back to the caller."""
    prompt = payload.get(
        "prompt",
        "No prompt found in input, please guide customer to create a json payload with prompt key",
    )
    stream = agent.stream_async(prompt)
    async for event in stream:
        print(event)
        yield event

if __name__ == "__main__":
    app.run()
