from strands import Agent, tool
from strands_tools import calculator # Import the calculator tool
import argparse
import json
from strands.models.litellm import LiteLLMModel
import os
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import boto3

app = BedrockAgentCoreApp()

def get_openrouter_api_key(param_name="/llm-provider/openrouter/api-key", region="ap-southeast-1"):
    """Fetch OpenRouter API key securely from AWS SSM."""
    ssm = boto3.client("ssm", region_name=region)
    param = ssm.get_parameter(Name=param_name, WithDecryption=True)
    return param["Parameter"]["Value"]


def setup_environment(api_key: str):
    """Set environment variables for LiteLLM."""
    os.environ["OPENROUTER_API_KEY"] = api_key
    os.environ["OPENROUTER_API_BASE"] = "https://openrouter.ai/api/v1"

api_key = get_openrouter_api_key()
setup_environment(api_key)

# Create a custom tool 
@tool
def weather():
    """ Get weather """ # Dummy implementation
    return "sunny"

model = "openrouter/qwen/qwen3-30b-a3b-instruct-2507"
litellm_model = LiteLLMModel(
    model_id=model, params={"max_tokens": 32000, "temperature": 0.3}
)


agent = Agent(
    model=litellm_model,
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculation, and tell the weather."
)


@app.entrypoint
def strands_agent_open_ai(payload):
    """
    Invoke the agent with a payload
    """
    user_input = payload.get("prompt")
    response = agent(user_input)
    return response.message['content'][0]['text']

if __name__ == "__main__":
    app.run()
