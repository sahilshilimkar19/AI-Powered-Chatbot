import json
from typing import AsyncGenerator

from openai import AsyncOpenAI

from app.config import settings
from app.knowledge import build_knowledge_context

# Provider base URLs (Groq and OpenAI use the same client with different base_url)
PROVIDER_URLS = {
    "groq": "https://api.groq.com/openai/v1",
    "openai": "https://api.openai.com/v1",
}

SYSTEM_PROMPT = """You are a helpful, friendly AI assistant. You answer user questions clearly and concisely.
If provided with knowledge base context, use it to inform your answers.
If you don't know the answer, say so honestly rather than making something up."""


def _get_openai_client() -> AsyncOpenAI:
    """Get an OpenAI-compatible client for the active provider."""
    base_url = PROVIDER_URLS.get(settings.llm_provider, PROVIDER_URLS["openai"])
    return AsyncOpenAI(api_key=settings.active_api_key, base_url=base_url)


# ──── Gemini-specific helpers ────

async def _gemini_chat(messages: list[dict]) -> str:
    import google.generativeai as genai
    genai.configure(api_key=settings.active_api_key)
    model = genai.GenerativeModel(settings.active_model)

    # Convert messages to Gemini format
    history, last_msg = _to_gemini_format(messages)
    chat = model.start_chat(history=history)
    response = await chat.send_message_async(last_msg)
    return response.text


async def _gemini_stream(messages: list[dict]) -> AsyncGenerator[str, None]:
    import google.generativeai as genai
    genai.configure(api_key=settings.active_api_key)
    model = genai.GenerativeModel(settings.active_model)

    history, last_msg = _to_gemini_format(messages)
    chat = model.start_chat(history=history)
    response = await chat.send_message_async(last_msg, stream=True)

    async for chunk in response:
        if chunk.text:
            yield f"data: {json.dumps({'content': chunk.text})}\n\n"

    yield "data: [DONE]\n\n"


def _to_gemini_format(messages: list[dict]):
    """Convert OpenAI-style messages to Gemini history + last message."""
    gemini_history = []
    for msg in messages:
        role = "user" if msg["role"] in ("user", "system") else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    last_msg = gemini_history.pop()["parts"][0] if gemini_history else ""
    return gemini_history, last_msg


# ──── Public API ────

async def get_chat_response(messages: list[dict]) -> str:
    """Non-streaming chat completion."""
    prepared = _prepare_messages(messages)

    if settings.llm_provider == "gemini":
        return await _gemini_chat(prepared)

    client = _get_openai_client()
    response = await client.chat.completions.create(
        model=settings.active_model,
        messages=prepared,
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content


async def stream_chat_response(messages: list[dict]) -> AsyncGenerator[str, None]:
    """Streaming chat completion using Server-Sent Events format."""
    prepared = _prepare_messages(messages)

    if settings.llm_provider == "gemini":
        async for chunk in _gemini_stream(prepared):
            yield chunk
        return

    client = _get_openai_client()
    stream = await client.chat.completions.create(
        model=settings.active_model,
        messages=prepared,
        temperature=0.7,
        max_tokens=1024,
        stream=True,
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            yield f"data: {json.dumps({'content': delta.content})}\n\n"

    yield "data: [DONE]\n\n"


def _prepare_messages(messages: list[dict]) -> list[dict]:
    """Inject system prompt and knowledge base context into the message list."""
    prepared = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Find the latest user message for knowledge retrieval
    last_user_msg = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            last_user_msg = msg.get("content", "")
            break

    # Add knowledge context if relevant
    knowledge_ctx = build_knowledge_context(last_user_msg)
    if knowledge_ctx:
        prepared.append({"role": "system", "content": knowledge_ctx})

    # Add conversation history
    for msg in messages:
        prepared.append({"role": msg["role"], "content": msg["content"]})

    return prepared
