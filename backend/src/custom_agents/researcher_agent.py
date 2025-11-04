from agents import Agent, ModelSettings, Runner
from agents.mcp import MCPServerStdio
from langfuse import observe

from src.models.research_result import ResearchResult

# Add websearch tool
class ResearcherAgent:
    def __init__(self, mcp_servers: MCPServerStdio):
        self.name = "Researcher Agent"
        self.model = "gpt-5-nano"
        self.instructions = f"You are an expert researcher specialized in gathering and summarizing information."
        self.mcp_servers = mcp_servers or []

        self.agent = Agent(
            name=self.name,
            model=self.model,
            instructions=self.instructions,
            mcp_servers=self.mcp_servers,
            model_settings=ModelSettings(tool_choice="required")
        )

    @observe(name="Researcher Agent - run")
    async def run(self, research_input: str) -> ResearchResult:
        response = await Runner.run(self.agent, research_input)
        return ResearchResult(query=research_input, result=response.final_output)