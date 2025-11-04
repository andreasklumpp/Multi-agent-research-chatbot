from langfuse import observe
from src.custom_agents.report_agent import ReportAgent
from src.custom_agents.research_assistant_agent import ResearchAssistantAgent
from src.custom_agents.researcher_agent import ResearcherAgent
from src.mcp_servers.search_mcp import get_search_mcp_server
from src.models.research_result import ResearchResult


class DeepResearch:
    def __init__(self):
        self.researchAssistant = ResearchAssistantAgent()
        self.reportAgent = ReportAgent()
        self.searchMcpServer = get_search_mcp_server()
        self.researchAgent = None

    @observe(name="Deep Research")
    async def run(self, query: str) -> str:
        # Use async context manager to ensure proper MCP server connection
        research_queries = await self.prepare_research(query)
        print("Research Queries:", research_queries)

        results = await self.conduct_research(research_queries)
        print("Results:", results, type(results))
        report = await self.report(query, results)

        return report

    async def prepare_research(self, query: str) -> list[str]:
        research_queries = await self.researchAssistant.run(query)
        return research_queries

    async def conduct_research(self, research_queries: list[str]) -> list[ResearchResult]:
        combined_results = []

        async with self.searchMcpServer as server:
            self.researchAgent = ResearcherAgent(mcp_servers=[server])
            
            for rq in research_queries:
                result = await self.researchAgent.run(rq)
                combined_results.append(result)

        return combined_results
    
    async def report(self, initial_query: str, research_results: list[ResearchResult]) -> str:
        report = await self.reportAgent.run(initial_query, research_results)
        return report