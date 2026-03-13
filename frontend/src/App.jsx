import { useState, useRef, useEffect } from 'react'
import ChatMessage from './components/ChatMessage'
import ChatInput from './components/ChatInput'
import Header from './components/Header'
import { sendMessage } from './api'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async (text) => {
    if (!text.trim() || isLoading) return

    const userMessage = { role: 'user', content: text.trim() }
    const updatedMessages = [...messages, userMessage]
    setMessages(updatedMessages)
    setIsLoading(true)

    // Add empty assistant message for streaming
    const assistantMessage = { role: 'assistant', content: '' }
    setMessages([...updatedMessages, assistantMessage])

    const apiMessages = updatedMessages.map(({ role, content }) => ({ role, content }))

    sendMessage(
      apiMessages,
      (chunk) => {
        setMessages((prev) => {
          const updated = [...prev]
          const last = updated[updated.length - 1]
          if (last.role === 'assistant') {
            updated[updated.length - 1] = { ...last, content: last.content + chunk }
          }
          return updated
        })
      },
      () => setIsLoading(false),
      (error) => {
        setMessages((prev) => {
          const updated = [...prev]
          updated[updated.length - 1] = {
            role: 'assistant',
            content: `⚠️ Error: ${error}. Please check that the backend is running and your API key is configured.`,
            isError: true,
          }
          return updated
        })
        setIsLoading(false)
      }
    )
  }

  const handleClear = () => {
    setMessages([])
  }

  return (
    <div className="app">
      <Header onClear={handleClear} messageCount={messages.length} />
      <main className="chat-container">
        {messages.length === 0 ? (
          <div className="welcome">
            <div className="welcome-glow" />
            <div className="welcome-logo">
              <div className="welcome-logo-ring" />
              <div className="welcome-logo-inner">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 8V4H8" />
                  <rect width="16" height="12" x="4" y="8" rx="2" />
                  <path d="M2 14h2" /><path d="M20 14h2" />
                  <path d="M15 13v2" /><path d="M9 13v2" />
                </svg>
              </div>
            </div>
            <h2 className="welcome-title">How can I help you today?</h2>
            <p className="welcome-desc">I'm your AI assistant — ask me anything about coding, science, writing, or just have a conversation.</p>
            <div className="suggestions">
              {[
                { icon: '💡', text: 'What can you help me with?' },
                { icon: '⚙️', text: 'Explain how this chatbot works' },
                { icon: '🎯', text: 'Tell me a fun fact' },
                { icon: '💻', text: 'Write a Python function' },
              ].map(({ icon, text }) => (
                <button
                  key={text}
                  className="suggestion-btn"
                  onClick={() => handleSend(text)}
                >
                  <span className="suggestion-icon">{icon}</span>
                  <span>{text}</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="messages">
            {messages.map((msg, idx) => (
              <ChatMessage key={idx} message={msg} />
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </main>
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  )
}

export default App
