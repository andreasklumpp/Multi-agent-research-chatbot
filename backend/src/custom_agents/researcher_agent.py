from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from langfuse import observe

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
        )

    @observe(name="Researcher Agent - run")
    async def run(self, research_input: str) -> str:
        response = await Runner.run(self.agent, research_input)
        return response.final_output