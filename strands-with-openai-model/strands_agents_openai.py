import os
import json
import boto3
from strands import Agent, tool
from strands_tools import calculator
from strands.models.litellm import LiteLLMModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp


# Initialize Bedrock AgentCore app
app = BedrockAgentCoreApp()


def get_openrouter_api_key(param_name="/llm-provider/openrouter/api-key", region="ap-southeast-1") -> str:
    """Fetch OpenRouter API key securely from AWS SSM Parameter Store."""
    ssm = boto3.client("ssm", region_name=region)
    response = ssm.get_parameter(Name=param_name, WithDecryption=True)
    return response["Parameter"]["Value"]


def setup_environment(api_key: str) -> None:
    """Set required environment variables for LiteLLM."""
    os.environ["OPENROUTER_API_KEY"] = api_key
    os.environ["OPENROUTER_API_BASE"] = "https://openrouter.ai/api/v1"


# Initialize environment (only once at startup)
setup_environment(get_openrouter_api_key())


@tool
def weather() -> str:
    """Return dummy weather info."""
    return "sunny"


def create_agent() -> Agent:
    """Configure and return a Strands agent instance."""
    model = LiteLLMModel(
        model_id="openrouter/qwen/qwen3-30b-a3b-instruct-2507",
        params={"max_tokens": 32000, "temperature": 0.3},
    )
    return Agent(
        model=model,
        tools=[calculator, weather],
        system_prompt="You're a helpful assistant. You can do simple math calculations and tell the weather.",
    )


# Instantiate agent globally once for performance
agent = create_agent()


@app.entrypoint
def strands_agent_open_ai(payload: dict) -> str:
    """Handle incoming payload and return model output."""
    prompt = payload.get("prompt", "")
    response = agent(prompt)
    return response.message["content"][0]["text"]


if __name__ == "__main__":
    app.run()
