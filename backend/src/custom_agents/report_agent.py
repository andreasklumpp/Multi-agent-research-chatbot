from agents import Agent, Runner
from langfuse import observe

from src.models.research_result import ResearchResult


INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query."
    "You will be provided with the original query, and some initial research done by a research agent.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim " 
    "for 4-5 paragraphs of content, at least 400 words."
)

class ReportAgent:

    def __init__(self):
        self.name = "Report Agent"
        self.model = "gpt-5-nano"
        self.instructions = INSTRUCTIONS

        self.agent = Agent(
            name=self.name,
            model=self.model,
            instructions=self.instructions,
        )

    @observe(name="Report Agent - run")
    async def run(self, initial_query: str, research_results: list[ResearchResult]) -> str:
        prompt = f"Initial Query: {initial_query}\n\n"
        prompt += "Research Results:\n"
        for rr in research_results:
            print("Research Result:", rr)
            prompt += f"- {rr.query}: {rr.result}\n"

        response = await Runner.run(self.agent, prompt)
        return response.final_output