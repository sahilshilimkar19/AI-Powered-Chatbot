# AI-Powered Chatbot

A real-time AI chatbot with streaming responses, built with **FastAPI** + **React (Vite)**. Supports **free** LLM providers (Groq, Google Gemini) out of the box, with optional OpenAI support. Includes a customizable knowledge base.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![React](https://img.shields.io/badge/React-18-61dafb) ![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688) ![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- **Real-time streaming** — AI responses stream token-by-token via Server-Sent Events (SSE)
- **Knowledge base** — Augment the LLM with domain-specific Q&A pairs
- **Markdown rendering** — Responses render with code blocks, lists, links
- **Responsive UI** — Clean dark-themed interface that works on desktop and mobile
- **Conversation history** — Full context maintained across messages
- **Deployment ready** — Configs for Vercel, Render, Docker, and AWS

---

## Project Structure

```
AI-Powered Chatbot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── chat.py          # OpenAI integration & streaming
│   │   ├── config.py        # Settings from environment
│   │   ├── knowledge.py     # Knowledge base & retrieval
│   │   └── models.py        # Pydantic schemas
│   ├── main.py              # FastAPI app & routes
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── public/
│   │   └── chatbot.svg
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInput.jsx / .css
│   │   │   ├── ChatMessage.jsx / .css
│   │   │   └── Header.jsx / .css
│   │   ├── api.js            # API client with SSE parsing
│   │   ├── App.jsx / .css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .gitignore
├── aws/
│   ├── setup-ec2.sh          # EC2 provisioning script
│   └── nginx.conf            # Nginx reverse proxy config
├── Dockerfile                # Docker image for backend
├── render.yaml               # Render deployment config
├── vercel.json               # Vercel deployment config
├── DEPLOY_AWS.md             # Full AWS deployment guide
└── README.md
```

---

## Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **OpenAI API key** ([get one here](https://platform.openai.com/api-keys))

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — set LLM_PROVIDER and the matching API key
# Default is Groq (free): get a key at https://console.groq.com/keys

# Start the server
uvicorn main:app --reload --port 8000
```

The API is now running at `http://localhost:8000`. Check `http://localhost:8000/docs` for interactive Swagger docs.

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Open `http://localhost:5173` — the frontend proxies API requests to the backend automatically.

---

## API Endpoints

| Method | Endpoint  | Description                    |
|--------|-----------|--------------------------------|
| GET    | `/health` | Health check + model info      |
| POST   | `/chat`   | Send messages, get AI response |

### POST `/chat` — Request Body

```json
{
  "messages": [
    { "role": "user", "content": "Hello!" }
  ],
  "stream": true
}
```

- `stream: true` → returns Server-Sent Events (text/event-stream)
- `stream: false` → returns JSON `{ "role": "assistant", "content": "..." }`

---

## Knowledge Base

Edit [backend/app/knowledge.py](backend/app/knowledge.py) to add custom Q&A pairs:

```python
KNOWLEDGE_BASE = [
    {
        "question": "What are your business hours?",
        "answer": "We're open Monday-Friday, 9 AM to 5 PM EST."
    },
    # Add more entries...
]
```

The system automatically retrieves relevant entries based on keyword matching and injects them as context for the LLM.

---

## Deployment

### Option A: Vercel (Frontend) + Render (Backend)

**Backend on Render:**
1. Push to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo, select Python runtime
4. Build command: `pip install -r backend/requirements.txt`
5. Start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables: `LLM_PROVIDER=groq`, `GROQ_API_KEY=your-key`

**Frontend on Vercel:**
1. Go to [vercel.com](https://vercel.com) → Import Project
2. Set root directory to `frontend`
3. Add environment variable: `VITE_API_URL=https://your-app.onrender.com`
4. Deploy

### Option B: AWS Free Tier

See the full guide: [DEPLOY_AWS.md](DEPLOY_AWS.md)

### Option C: Docker

```bash
docker build -t chatbot-api .
docker run -p 8000:8000 -e LLM_PROVIDER=groq -e GROQ_API_KEY=gsk_... chatbot-api
```

---

## Environment Variables

| Variable        | Required | Default                      | Description                          |
|----------------|----------|------------------------------|--------------------------------------|
| `LLM_PROVIDER`   | No       | `groq`                       | `groq` (free), `gemini` (free), or `openai` (paid) |
| `GROQ_API_KEY`   | If groq  | —                            | Free key from console.groq.com       |
| `GROQ_MODEL`     | No       | `llama-3.3-70b-versatile`    | Groq model name                      |
| `GEMINI_API_KEY`  | If gemini| —                            | Free key from aistudio.google.com    |
| `GEMINI_MODEL`   | No       | `gemini-1.5-flash`           | Gemini model name                    |
| `OPENAI_API_KEY` | If openai| —                            | Paid key from platform.openai.com    |
| `OPENAI_MODEL`   | No       | `gpt-3.5-turbo`              | OpenAI model name                    |
| `CORS_ORIGINS`   | No       | `localhost:5173`             | Allowed CORS origins                 |
| `VITE_API_URL`   | No       | `/api` (proxy)               | Backend URL for frontend             |

---

## License

MIT
