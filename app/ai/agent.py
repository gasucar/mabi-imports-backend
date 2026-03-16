from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from app.ai.tools import search_perfumes
from app.ai.prompts import SYSTEM_PROMPT
import os


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=os.getenv("OPENAI_API_KEY")
)


tools = [search_perfumes]


agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    agent_kwargs={
        "system_message": SYSTEM_PROMPT
    }
)


def run_agent(message: str):
    return agent.run(message)