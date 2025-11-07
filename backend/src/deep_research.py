from langfuse import observe
from src.custom_agents.research_readiness_agent import ResearchReadinessAgent, ResearchReadiness
from src.custom_agents.report_agent import ReportAgent
from src.custom_agents.research_assistant_agent import ResearchAssistantAgent, ResearchStructure, ResearchSubject
from src.custom_agents.researcher_agent import ResearcherAgent
from src.mcp_servers.search_mcp import get_search_mcp_server
from src.models.research_result import ResearchOutput
from agents import SQLiteSession


class DeepResearch:
    def __init__(self, thread_id: str):
        self.researchAssistant = ResearchAssistantAgent()
        self.reportAgent = ReportAgent()
        self.clarifierAgent = ResearchReadinessAgent()
        self.searchMcpServer = get_search_mcp_server()
        self.researchAgent = None
        self.session = SQLiteSession(thread_id, "data/assistant_sessions.db")

    @observe(name="Deep Research")
    async def run(self, query: str) -> str:
        readiness = await self.clarify_query(query)

        if readiness.status == "INCOMPLETE":
            return readiness.follow_up_question

        research_subjects = await self.prepare_research(query)
        print("Research Queries:", research_subjects)

        results = await self.conduct_research(research_subjects)

        print("Results:", results, type(results))
        report = await self.report(query, results)

        return report

    async def clarify_query(self, query: str) -> ResearchReadiness:
        clarification = await self.clarifierAgent.run(query, session=self.session)

        return clarification

    async def prepare_research(self, query: str) -> list[ResearchSubject]:
        research_queries = await self.researchAssistant.run(query, self.session)
        return research_queries

    async def conduct_research(self, research_subjects: list[ResearchSubject]) -> list[ResearchOutput]:
        combined_results = []

        async with self.searchMcpServer as server:
            self.researchAgent = ResearcherAgent(mcp_servers=[server])

            for subject in research_subjects:
                result = await self.researchAgent.run(subject)
                combined_results.append(result)

        return combined_results
    
    async def report(self, initial_query: str, research_results: list[ResearchOutput]) -> str:
        report = await self.reportAgent.run(initial_query, research_results)
        return report