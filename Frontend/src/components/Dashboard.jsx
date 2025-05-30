import { useEffect, useState } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const [documents, setDocuments] = useState([])
  const [search, setSearch] = useState("")
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  useEffect(() => {
    fetchDocuments()
  }, [search, page])

  const fetchDocuments = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/documents/`, {
        params: { search, page }
      })
      setDocuments(res.data.results)
      setTotalPages(Math.ceil(res.data.count / 10))  // Adjust page size if changed in backend
    } catch (error) {
      console.error("Error fetching documents:", error)
    }
  }

  const handleDelete = async (id) => {
    const confirm = window.confirm("Are you sure you want to delete this document?")
    if (!confirm) return

    try {
      await axios.delete(`http://localhost:8000/api/documents/${id}/delete/`)
      setDocuments(prev => prev.filter(doc => doc.id !== id))
    } catch (error) {
      alert("Failed to delete: " + (error.response?.data?.detail || error.message))
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">📚 Document Library</h1>

      <input
        type="text"
        value={search}
        onChange={(e) => {
          setSearch(e.target.value)
          setPage(1) // Reset to page 1 on new search
        }}
        placeholder="Search documents..."
        className="bg-gray-800 text-white border border-gray-700 rounded px-4 py-2 mb-6 w-full max-w-md"
      />

      <div className="grid md:grid-cols-2 gap-4">
        {documents.length === 0 && (
          <p className="text-gray-400">No documents found.</p>
        )}

        {documents.map((doc) => (
          <div key={doc.id} className="bg-gray-800 p-4 rounded-xl shadow-md">
            <h2 className="text-xl font-semibold">{doc.title}</h2>
            <p className="text-sm text-gray-400">
              {doc.file_type?.toUpperCase() || "N/A"} • {doc.pages || "?"} pages
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Uploaded: {new Date(doc.created_at).toLocaleString()}
            </p>

            <div className="mt-4 flex justify-between items-center">
              <Link
                to={`/chat/${doc.id}`}
                className="text-blue-500 hover:underline font-medium"
              >
                Chat →
              </Link>

              {doc.file ? (
                <a
                  href={`http://localhost:8000${doc.file}`}
                  download
                  className="text-gray-400 hover:text-white text-sm"
                >
                  Download
                </a>
              ) : (
                <span className="text-gray-600 text-sm">No file</span>
              )}
            </div>

            <button
              onClick={() => handleDelete(doc.id)}
              className="mt-3 text-red-500 hover:text-red-700 text-sm"
            >
              Delete
            </button>
          </div>
        ))}
      </div>

      {/* Pagination */}
      <div className="mt-8 flex gap-2 justify-center">
        {Array.from({ length: totalPages }, (_, i) => (
          <button
            key={i}
            onClick={() => setPage(i + 1)}
            className={`px-3 py-1 rounded-lg ${
              page === i + 1 ? 'bg-blue-600' : 'bg-gray-700'
            } hover:bg-blue-700`}
          >
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  )
}
