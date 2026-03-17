from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from app.ai.tools import search_perfumes
from app.ai.prompts import SYSTEM_PROMPT

# -----------------------------
# LLM
# -----------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7
)

# -----------------------------
# Tools
# -----------------------------
tools = [search_perfumes]

# -----------------------------
# Crear agente con nueva API
# -----------------------------
agent = create_agent(
    model=llm,
    tools=tools,
    # checkpointer=memory
)

def run_agent(message: str, session_id: str = "default"):
    """
    Ejecuta el agente con LangGraph / ChatGroq.
    Garantiza que siempre devuelve texto y maneja errores de tool.
    """
    try:
        # Limitar mensajes para evitar errores de memoria corrupta
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]

        config = {
            "configurable": {
                "thread_id": session_id,
                "checkpoint_ns": ""
            }
        }

        print("DEBUG: input enviado al agente:", messages)
        print("DEBUG: config enviado al agente:", config)

        # Llamada al agente
        result = agent.invoke(input={"messages": messages}, config=config)
        print("DEBUG: result devuelto por agent.invoke():", result)
        

        # Siempre devolver algo legible
        if isinstance(result, dict) and "messages" in result and len(result["messages"]) > 0:
            last_msg = result["messages"][-1]

            # Si viene con 'content' lo usamos
            if hasattr(last_msg, "content"):
                return str(last_msg.content)

            elif isinstance(last_msg, dict) and "content" in last_msg:
                return str(last_msg["content"])
        # fallback en caso de tool
        if isinstance(last_msg, dict) and last_msg.get("role") == "tool":
            # simplemente devolver algo seguro
            return "Lo siento, no pude buscar perfumes ahora. 🌸"

        # fallback general
        return str(result)

    except Exception as e:
        print("ERROR ejecutando agente:", e)
        return "Sorry, something went wrong. Por favor, inténtalo de nuevo."