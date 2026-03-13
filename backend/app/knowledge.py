"""
Knowledge base for the chatbot.
Add domain-specific Q&A pairs here to augment the LLM with custom knowledge.
"""

KNOWLEDGE_BASE = [
    {
        "question": "What is this chatbot?",
        "answer": "This is an AI-powered chatbot built with FastAPI and React. It uses OpenAI's language models to answer questions and can be augmented with a custom knowledge base."
    },
    {
        "question": "What technologies are used?",
        "answer": "The backend uses FastAPI (Python) with streaming support. The frontend uses React with Vite. It integrates with OpenAI's GPT models for intelligent responses."
    },
    {
        "question": "How do I deploy this chatbot?",
        "answer": "You can deploy the frontend on Vercel and the backend on Render. For AWS, use EC2 (free tier) for the backend and S3 + CloudFront for the frontend."
    },
]


def build_knowledge_context(user_message: str) -> str:
    """
    Simple keyword-based knowledge retrieval.
    Returns relevant knowledge base entries as context for the LLM.
    """
    user_lower = user_message.lower()
    relevant = []

    for entry in KNOWLEDGE_BASE:
        keywords = entry["question"].lower().split()
        if any(kw in user_lower for kw in keywords if len(kw) > 3):
            relevant.append(f"Q: {entry['question']}\nA: {entry['answer']}")

    if relevant:
        return "Here is some relevant knowledge:\n\n" + "\n\n".join(relevant)
    return ""
