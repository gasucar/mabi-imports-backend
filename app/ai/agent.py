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

def detect_language(text: str) -> str:
    if any(word in text.lower() for word in ["hola", "quiero", "fresco", "dulce", "fragancia"]):
        return "es"
    return "en"


def format_response(results, lang: str):

    if not results:
        return "No encontré perfumes 😔 ¿Querés que busque algo diferente?" if lang == "es" \
            else "I couldn't find perfumes 😔 Want me to try something else?"

    intro = "Encontré estos perfumes para vos:\n\n" if lang == "es" \
        else "Here are some perfumes you might like:\n\n"

    text = intro

    emojis = ["🌸", "🔥", "💎"]

    for i, p in enumerate(results):
        desc = p["short_description"]

        # traducción simple
        if lang == "es":
            desc = (
                desc
                .replace("sweet", "dulce")
                .replace("warm", "cálido")
                .replace("fresh", "fresco")
                .replace("woody", "maderable")
                .replace("fragance", "fragancia")
                
            )

        text += f"{emojis[i]} {p['name']}\n"
        text += f"{desc}\n"
        text += f"{p['url']}\n\n"

    text += "¿Querés algo más?" if lang == "es" else "Want more recommendations?"

    return text


def run_agent(message: str):

    lang = detect_language(message)

    # 🔥 lógica de decisión (clave)
    if any(word in message.lower() for word in ["perfume", "fragancia", "fragrance", "sweet", "dulce", "fresco", "fresh", "woody"]):

        results = search_perfumes(message)

        return format_response(results, lang)

    # fallback conversacional (LLM)
    response = llm.invoke(message)

    return response.content