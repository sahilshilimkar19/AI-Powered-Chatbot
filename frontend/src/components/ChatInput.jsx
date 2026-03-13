import { useState, useRef, useEffect } from 'react'
import './ChatInput.css'

function ChatInput({ onSend, disabled }) {
  const [input, setInput] = useState('')
  const textareaRef = useRef(null)

  // Auto-resize textarea
  useEffect(() => {
    const el = textareaRef.current
    if (el) {
      el.style.height = 'auto'
      el.style.height = Math.min(el.scrollHeight, 150) + 'px'
    }
  }, [input])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!input.trim() || disabled) return
    onSend(input)
    setInput('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <div className={`input-wrapper ${disabled ? 'is-loading' : ''} ${input.trim() ? 'has-text' : ''}`}>
        <div className="input-glow" />
        <textarea
          ref={textareaRef}
          rows="1"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={disabled ? 'AI is thinking...' : 'Ask me anything...'}
          disabled={disabled}
          className="input-field"
        />
        <button type="submit" disabled={disabled || !input.trim()} className="send-btn" title="Send message">
          {disabled ? (
            <div className="spinner" />
          ) : (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 2L11 13" />
              <path d="M22 2L15 22L11 13L2 9L22 2Z" />
            </svg>
          )}
        </button>
      </div>
      <div className="input-footer">
        <kbd>Enter</kbd> to send &nbsp;·&nbsp; <kbd>Shift + Enter</kbd> for new line
      </div>
    </form>
  )
}

export default ChatInput
