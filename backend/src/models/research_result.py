from pydantic import BaseModel

from src.custom_agents.research_assistant_agent import ResearchSubject

class ResearchOutput(BaseModel):
    research_subject: ResearchSubject
    research_output: str