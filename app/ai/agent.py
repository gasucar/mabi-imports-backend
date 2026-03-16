from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from app.ai.tools import search_perfumes
from app.ai.prompts import SYSTEM_PROMPT


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7
)

tools = [search_perfumes]

memory = MemorySaver()

agent = create_react_agent(
    llm,
    tools,
    checkpointer=memory
)


def run_agent(message: str, session_id: str = "default"):

    result = agent.invoke({
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]
    }, config={"configurable": {"thread_id": session_id}})

    return result["messages"][-1].content