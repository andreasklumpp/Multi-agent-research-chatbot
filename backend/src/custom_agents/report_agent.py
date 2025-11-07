from agents import Agent, Runner
from langfuse import observe

from src.models.research_result import ResearchOutput


INSTRUCTIONS = """
    You are a report generation agent. Given an initial research query and a list of research results,
    your task is to synthesize the information into a coherent and comprehensive report that addresses the initial query.
    The report should be well structured, with clear sections summarizing the key findings from each research output."""

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
    async def run(self, initial_query: str, research_outputs: list[ResearchOutput]) -> str:
        prompt = f"Initial Query: {initial_query}\n\n"
        prompt += "Research Results:\n"
        for ro in research_outputs:
            print("Research Result:", ro)
            prompt += f"- {ro.research_subject.topic}: {ro.research_output}\n"

        response = await Runner.run(self.agent, prompt)
        return response.final_output