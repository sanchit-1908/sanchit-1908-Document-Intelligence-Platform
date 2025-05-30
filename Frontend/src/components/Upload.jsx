import { useState, useRef } from 'react'
import axios from 'axios'

export default function Upload() {
  const [file, setFile] = useState(null)
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [tags, setTags] = useState("")
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState("")
  const [error, setError] = useState(false)

  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file")
      setError(true)
      return
    }

    const tagsArray = tags.split(",").map(tag => tag.trim()).filter(tag => tag)
    const formData = new FormData()
    formData.append("file_path", file)
    formData.append("title", title || file.name)
    formData.append("description", description)
    formData.append("tags", JSON.stringify(tagsArray))

    try {
      setUploading(true)
      setMessage("")
      setError(false)

      const res = await axios.post("http://localhost:8000/api/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      })

      setMessage("Upload successful!")
      setError(false)
      setFile(null)
      setTitle("")
      setDescription("")
      setTags("")
      // Clear the hidden file input's value so label resets
      if (fileInputRef.current) fileInputRef.current.value = null
    } catch (error) {
      setMessage("Upload failed. " + (error.response?.data?.detail || error.message))
      setError(true)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold mb-4">Upload Document</h1>

      <div className="bg-gray-800 p-6 rounded-xl shadow-lg w-full max-w-md text-center space-y-4">
        <div className="relative">
          <input
            type="file"
            accept=".pdf,.doc,.docx,.txt"
            onChange={handleFileChange}
            id="fileInput"
            ref={fileInputRef}
            className="hidden"
          />
          <label
            htmlFor="fileInput"
            className="cursor-pointer bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg inline-block text-white"
          >
            {file ? file.name : "Choose File"}
          </label>
        </div>

        <input
          type="text"
          placeholder="Title (optional)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-3 py-2 rounded bg-gray-700 text-white"
        />

        <textarea
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full px-3 py-2 rounded bg-gray-700 text-white resize-none"
        />

        <input
          type="text"
          placeholder="Tags (comma separated)"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          className="w-full px-3 py-2 rounded bg-gray-700 text-white"
        />

        <button
          onClick={handleUpload}
          disabled={uploading}
          className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg font-medium disabled:opacity-50 w-full"
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>

        {message && (
          <p className={`mt-2 text-sm ${error ? 'text-red-500' : 'text-green-400'}`}>
            {message}
          </p>
        )}
      </div>
    </div>
  )
}