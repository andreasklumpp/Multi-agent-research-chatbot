from agents import Agent, Runner, SQLiteSession
from langfuse import observe
from pydantic import BaseModel

HOW_MANY_SEARCHES = 1

# INSTRUCTIONS = f"You are a helpful research assistant. Given a query, come up with a set of web searches \
# to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."
INSTRUCTIONS = f"You are a research assistant. Given a query, you follow these steps: \
    1. Identify the core intent of the research request. \
    2. Break down the core intent into 4 specific subtopics or aspects that need to be researched. \
    3. For each subtopic, generate {HOW_MANY_SEARCHES} search terms that would yield relevant information."


class ResearchSubject(BaseModel):
    topic: str
    search_terms: list[str]

class ResearchStructure(BaseModel):
    researchOutline: list[ResearchSubject]
    
class ResearchAssistantAgent:
    def __init__(self):
        self.name = "Research Assistant Agent"
        self.model = "gpt-5-nano"
        self.instructions = INSTRUCTIONS

        self.agent = Agent(
            name=self.name,
            model=self.model,
            instructions=self.instructions,
            output_type=list[ResearchSubject]
        )

    @observe(name="Research Assistant Agent - run")
    async def run(self, research_input: str,  session: SQLiteSession) -> list[ResearchSubject]:
        response = await Runner.run(self.agent, research_input, session=session)
        return response.final_output