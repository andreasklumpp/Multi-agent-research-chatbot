import asyncio
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from langfuse import get_client
from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor

from src.deep_research import DeepResearch

load_dotenv(override=True)

# Create the FastAPI application instance
app = FastAPI()

origins = [
    'http://localhost:4000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow GET, POST, etc.
    allow_headers=["*"],
)

# Setup Langfuse
OpenAIAgentsInstrumentor().instrument()
langfuse = get_client()
 
# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")

deep_research = DeepResearch();

# Define a path operation (route)
@app.get("/")
async def read_root():
    return {"message": "Hello World with UV and FastAPI!"}


@app.post("/chat")
async def chat_endpoint( request: dict):
    print("Chat endpoint called with request:", request)
    async def event_generator():
        print("Received request:", request['messages'][-1])
        print("Type of request:", type(request))
        # Placeholder: Your agent logic generates and yields events
        research_queries = await deep_research.run(request['messages'][-1]['content'][-1]['text'])

        yield f"data: {json.dumps({'id': '2', 'role': 'assistant', 'content': research_queries})}\n\n"   # ... more events

    # Set media_type to 'text/event-stream' for SSE
    return StreamingResponse(event_generator(), media_type='text/event-stream')
