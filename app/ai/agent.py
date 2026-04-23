from langchain_groq import ChatGroq
from typing import List, Dict
import re

from app.ai.tools import search_perfumes

# -----------------------------
# LLM
# -----------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7
)

# -----------------------------
# LANGUAGE DETECTION
# -----------------------------
def detect_language(text: str) -> str:
    text = text.lower()

    spanish_keywords = [
        "hola", "quiero", "busco", "fragancia", "buscando",
        "dulce", "fresco", "amaderado", "recomenda"
    ]

    if any(word in text for word in spanish_keywords):
        return "es"

    return "en"


# -----------------------------
# INTENT DETECTION
# -----------------------------
def is_recommendation_query(message: str) -> bool:
    msg = message.lower()

    keywords = [
        "recommend", "suggest", "show me", "looking for",
        "sweet", "fresh", "woody",
        "recomendar", "recomendame", "busco", "quiero",
        "dulce", "fresco", "amaderado"
    ]

    return any(k in msg for k in keywords)


def is_perfume_info_query(message: str) -> bool:
    msg = message.lower()

    patterns = [
        "tell me about",
        "what is",
        "info about",
        "information about",
        "hablame de",
        "qué tal es",
        "que tal es",
        "informacion de"
    ]

    return any(p in msg for p in patterns)


# -----------------------------
# RESPONSE FORMATTER
# -----------------------------
def format_response(results: List[Dict], lang: str) -> str:

    if not results:
        return (
            "No encontré perfumes 😔 ¿Querés que busque algo diferente?"
            if lang == "es"
            else "I couldn't find perfumes 😔 Want me to try something else?"
        )

    intro = (
        "Encontré estos perfumes para vos:\n\n"
        if lang == "es"
        else "Here are some perfumes you might like:\n\n"
    )

    emojis = ["🌸", "🔥", "💎"]

    text = intro

    for i, p in enumerate(results[:3]):
        desc = p.get("short_description", "")

        if lang == "es":
            desc = (
                desc
                .replace("sweet", "dulce")
                .replace("warm", "cálido")
                .replace("fresh", "fresco")
                .replace("woody", "amaderado")
                .replace("fragrance", "fragancia")
            )

        text += f"{emojis[i]} {p['name']}\n"
        text += f"{desc}\n"
        text += f"{p['url']}\n\n"

    text += "¿Querés algo más?" if lang == "es" else "Want more recommendations?"

    return text


# -----------------------------
# PERFUME INFO MODE (LLM)
# -----------------------------
def generate_perfume_info(message: str, lang: str) -> str:

    prompt = f"""
You are Perfumina, a premium perfume sales assistant.

User message:
{message}

Your job:
Explain the perfume in a persuasive, premium, and natural way.

You MUST include:
- How it smells
- Who it's for
- Best season or occasion
- Why it's special

Rules:
- Keep it concise (max 120 words)
- Be natural, not robotic
- Be slightly sales-driven
- Respond in {"Spanish" if lang == "es" else "English"}

DO NOT say you couldn't find the perfume.
"""

    try:
        response = llm.invoke(prompt)
        return response.content.strip()

    except Exception as e:
        print("AI INFO MODE ERROR:", e)

        return (
            "No pude obtener la información ahora 😔"
            if lang == "es"
            else "I couldn't get the info right now 😔"
        )


# -----------------------------
# MAIN AGENT
# -----------------------------
def run_agent(message: str) -> str:

    try:

        lang = detect_language(message)

        print("🧠 USER MESSAGE:", message)
        print("🌎 DETECTED LANG:", lang)

        # -------------------------
        # 1. PERFUME INFO MODE
        # -------------------------
        if is_perfume_info_query(message):
            print("📌 MODE: INFO")
            return generate_perfume_info(message, lang)

        # -------------------------
        # 2. RECOMMENDATION MODE
        # -------------------------
        if is_recommendation_query(message):
            print("📌 MODE: RECOMMENDATION")

            try:
                results = search_perfumes(message)
                return format_response(results, lang)

            except Exception as e:
                print("❌ TOOL ERROR:", e)

                return (
                    "No pude buscar perfumes ahora 😔 Probá de nuevo en un momento."
                    if lang == "es"
                    else "I couldn't search perfumes right now 😔 Try again in a moment."
                )

        # -------------------------
        # 3. GENERAL CHAT (CONTROLLED)
        # -------------------------
        print("📌 MODE: GENERAL")

        prompt = f"""
You are Perfumina, a perfume expert.

User:
{message}

Rules:
- Keep conversation about perfumes
- Be friendly and natural
- Short response (max 80 words)
- Respond in {"Spanish" if lang == "es" else "English"}
"""

        response = llm.invoke(prompt)

        return response.content.strip()

    except Exception as e:
        print("🔥 CRITICAL AI ERROR:", e)

        return (
            "Ocurrió un error 😔 Intentalo de nuevo."
            if detect_language(message) == "es"
            else "Something went wrong 😔 Please try again."
        )