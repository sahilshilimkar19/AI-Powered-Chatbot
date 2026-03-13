import ReactMarkdown from 'react-markdown'
import './ChatMessage.css'

function ChatMessage({ message }) {
  const isUser = message.role === 'user'
  const isStreaming = !isUser && !message.content && !message.isError

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-assistant'} ${message.isError ? 'message-error' : ''}`}>
      <div className={`message-avatar ${isUser ? 'avatar-user' : 'avatar-assistant'}`}>
        {isUser ? (
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        ) : (
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 8V4H8" />
            <rect width="16" height="12" x="4" y="8" rx="2" />
            <path d="M2 14h2" /><path d="M20 14h2" />
            <path d="M15 13v2" /><path d="M9 13v2" />
          </svg>
        )}
      </div>
      <div className="message-content">
        <span className="message-role">{isUser ? 'You' : 'AI'}</span>
        <div className={`message-bubble ${isStreaming ? 'streaming' : ''}`}>
          {isStreaming ? (
            <div className="typing-indicator">
              <span /><span /><span />
            </div>
          ) : isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown>{message.content}</ReactMarkdown>
          )}
        </div>
      </div>
    </div>
  )
}

export default ChatMessage
