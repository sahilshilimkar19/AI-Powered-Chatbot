from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from app.config import settings
from app.models import ChatRequest, ChatResponse, HealthResponse
from app.chat import get_chat_response, stream_chat_response

app = FastAPI(
    title="AI Chatbot API",
    description="Real-time AI chatbot with streaming responses",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        model=f"{settings.llm_provider}/{settings.active_model}",
    )


@app.post("/chat")
async def chat(request: ChatRequest):
    if not settings.active_api_key:
        raise HTTPException(
            status_code=500,
            detail=f"API key not configured for provider '{settings.llm_provider}'. "
                   f"Set the appropriate key in your .env file.",
        )

    messages = [msg.model_dump() for msg in request.messages]

    if request.stream:
        return StreamingResponse(
            stream_chat_response(messages),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )
    else:
        content = await get_chat_response(messages)
        return ChatResponse(role="assistant", content=content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
