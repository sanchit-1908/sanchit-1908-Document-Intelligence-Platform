import { useParams } from 'react-router-dom'
import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

export default function ChatPage() {
  const { id } = useParams()  // document id
  const [document, setDocument] = useState(null)
  const [messages, setMessages] = useState([])
  const [question, setQuestion] = useState("")
  const [loading, setLoading] = useState(false)

  const messagesEndRef = useRef(null)

  useEffect(() => {
    fetchDocument()
    // Since no GET chat/messages API, optionally clear messages on document change
    setMessages([])
  }, [id])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const fetchDocument = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/documents/${id}/`)
      setDocument(res.data)
    } catch (error) {
      console.error("Error fetching document:", error)
    }
  }

  const handleSend = async () => {
    const trimmedQuestion = question.trim()
    if (!trimmedQuestion) return

    // Show user message immediately
    const userMsg = { sender: 'user', content: trimmedQuestion }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)
    setQuestion("")

    try {
      const res = await axios.post(`http://localhost:8000/api/chat/${id}/`, {
      message: trimmedQuestion,
      sender: "user",
    })

      // Backend response assumed to have user_message and ai_message objects with message text
      const aiMsgContent = res.data.ai_response || "No response"


      const aiMsg = { sender: 'ai', content: aiMsgContent }
      setMessages((prev) => [...prev, aiMsg])
    } catch (error) {
      console.error("Failed to get answer", error)
      setMessages((prev) => [...prev, { sender: 'ai', content: "Sorry, something went wrong." }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 flex flex-col md:flex-row gap-6">
      <div className="md:w-2/3 pr-0 md:pr-4">
        <h1 className="text-3xl font-bold mb-4">📄 {document?.title || "Loading..."}</h1>
        <p className="text-gray-400 mb-2">Type: {document?.file_type?.toUpperCase() || "-"}</p>
        <p className="text-gray-400 mb-2">Pages: {document?.pages ?? "-"}</p>
        <p className="text-gray-500 text-sm mb-6">
          Uploaded: {document?.created_at ? new Date(document.created_at).toLocaleString() : "-"}
        </p>
        <p className="text-gray-300">
          Use the chat on the right to ask questions about this document.
        </p>
      </div>

      <div className="md:w-1/3 bg-gray-800 rounded-xl p-4 flex flex-col max-h-[80vh]">
        <div className="flex-1 overflow-y-auto space-y-3">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`p-3 rounded-xl text-sm ${
                msg.sender === 'user'
                  ? 'bg-blue-600 text-right ml-auto max-w-[80%]'
                  : 'bg-gray-700 text-left mr-auto max-w-[80%]'
              }`}
            >
              {msg.content}
            </div>
          ))}
          <div ref={messagesEndRef} />
          {loading && <div className="text-sm text-gray-400">AI is typing...</div>}
        </div>

        <div className="mt-4 flex items-center gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask a question..."
            className="flex-1 bg-gray-700 border border-gray-600 px-4 py-2 rounded-lg text-white"
            disabled={loading}
          />
          <button
            onClick={handleSend}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
            disabled={loading}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  )
}
