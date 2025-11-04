from agents import Agent, Runner
from langfuse import observe

HOW_MANY_SEARCHES = 2

INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."

class ResearchAssistantAgent:
    def __init__(self):
        self.name = "Research Assistant Agent"
        self.model = "gpt-5-nano"
        self.instructions = INSTRUCTIONS

        self.agent = Agent(
            name=self.name,
            model=self.model,
            instructions=self.instructions,
            output_type=list[str]
        )

    @observe(name="Research Assistant Agent - run")
    async def run(self, research_input: str) -> str:
        response = await Runner.run(self.agent, research_input)
        return response.final_output