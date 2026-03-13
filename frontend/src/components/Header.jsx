import { useState, useEffect } from 'react'
import './Header.css'

function Header({ onClear, messageCount }) {
  const [statusDot, setStatusDot] = useState(false)

  useEffect(() => {
    const interval = setInterval(() => setStatusDot((v) => !v), 2000)
    return () => clearInterval(interval)
  }, [])

  return (
    <header className="header">
      <div className="header-glow" />
      <div className="header-content">
        <div className="header-left">
          <div className="header-logo-wrap">
            <div className="header-logo-ring" />
            <span className="header-logo">🤖</span>
          </div>
          <div>
            <h1 className="header-title">
              AI Chatbot
              <span className={`status-dot ${statusDot ? 'pulse' : ''}`} />
            </h1>
            <span className="header-subtitle">
              <span className="subtitle-icon">⚡</span> Powered by AI
            </span>
          </div>
        </div>
        <div className="header-right">
          {messageCount > 0 && (
            <button className="clear-btn" onClick={onClear} title="Clear chat">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="3 6 5 6 21 6" />
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
              </svg>
              New Chat
            </button>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header
