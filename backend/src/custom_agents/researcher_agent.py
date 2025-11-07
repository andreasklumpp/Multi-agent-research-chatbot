from agents import Agent, ModelSettings, Runner
from agents.mcp import MCPServerStdio
from langfuse import observe

from src.custom_agents.research_assistant_agent import ResearchSubject
from src.models.research_result import ResearchOutput

INSTRUCTIONS = """
    You are a senior reseacher. Given a research subject with multiple search terms, you use your tools to perform web searches
    and gather relevant information. For each search term, you should:
    1. Perform the web search using the provided MCP server.
    2. Analyze the search results and extract the most relevant information.
    3. Synthesize the findings into a coherent summary for the research subject.
    Your final output should be a comprehensive research result that addresses the research subject based on the gathered information.
"""

class ResearcherAgent:
    def __init__(self, mcp_servers: MCPServerStdio):
        self.name = "Researcher Agent"
        self.model = "gpt-5-nano"
        self.instructions = INSTRUCTIONS
        self.mcp_servers = mcp_servers or []

        self.agent = Agent(
            name=self.name,
            model=self.model,
            instructions=self.instructions,
            mcp_servers=self.mcp_servers,
            model_settings=ModelSettings(tool_choice="required")
        )

    @observe(name="Researcher Agent - run")
    async def run(self, research_input: ResearchSubject) -> ResearchOutput:
        prompt = f"Research Subject: {research_input.topic}\nSearch Terms: {', '.join(research_input.search_terms)}"
        response = await Runner.run(self.agent, prompt)

        output = ResearchOutput(
            research_subject=research_input,
            research_output=response.final_output
        )
        return output