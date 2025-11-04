from typing_extensions import Literal
from agents import Agent, Runner, SQLiteSession
from langfuse import observe
from pydantic import BaseModel


instructions = """
You are talking to a user who is asking for a research task to be conducted. Your task is to analyze the complete transcript of the user's conversation with the assistant up to the present moment. The user's ultimate goal is to perform a detailed research task.
Follow these steps rigorously:

### 1. Identify Core Intent
Determine the user's **primary research topic and goal** from the conversation. (e.g., "Find the top 5 competitors for a new coffee brand in Seattle").

### 2. Define Necessary Information
Based on the Core Intent, list the 3-5 **essential, non-negotiable data points** required for a successful, actionable research report. (e.g., "Target City", "Product/Service Type", "Target Audience", "Timeframe/Year").

### 3. Audit Conversation History
Go through the entire conversation history. For each necessary data point identified in Step 2, determine if it has been provided and is **unambiguous**.

### 4. Determine Outcome
* **If all necessary information is present and clear:** Conclude that the information is **COMPLETE**.
* **If any necessary information is missing or ambiguous:** Conclude that the information is **INCOMPLETE**.

### 5. Formulate Response
If the information is **INCOMPLETE**, you must generate a **single, clear, and focused follow-up question** that targets the **most critical missing data point**. Do not ask multiple questions.
If the information is **COMPLETE**, return the status: "COMPLETE".

ALWAYS respond using the required JSON format. DO NOT include any explanatory text outside of the JSON block.
IMPORTANT: Do NOT conduct any research yourself, just gather information that will be given to a researcher to conduct the research task.
"""

class MissingDetail(BaseModel):
    key: str
    reasoning: str


class ResearchReadiness(BaseModel):
    status: Literal["COMPLETE", "INCOMPLETE"]
    missing_details: list[MissingDetail]
    follow_up_question: str | None
    
class ResearchReadinessAgent:
    def __init__(self): 
        self.name = "Research Readiness Agent"
        self.model = "gpt-4o-mini"
        self.instructions = instructions

        self.agent = Agent(
            name=self.name,
            model=self.model,
            instructions=self.instructions,
            output_type=ResearchReadiness
        )

    @observe(name="Research Readiness Agent - run")
    async def run(self, research_input: str, session: SQLiteSession) -> ResearchReadiness:
        response = await Runner.run(self.agent, research_input, session=session)
        return response.final_output