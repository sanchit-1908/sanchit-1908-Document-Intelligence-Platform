import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center gap-8 p-6">
      <h1 className="text-4xl font-bold mb-6">Welcome to the Document Intelligence Platform</h1>

      <nav className="flex flex-col space-y-4 text-center">
        <Link
          to="/dashboard"
          className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg text-lg font-semibold"
        >
          Go to Dashboard
        </Link>

        <Link
          to="/upload"
          className="bg-green-600 hover:bg-green-700 px-6 py-3 rounded-lg text-lg font-semibold"
        >
          Upload Document
        </Link>

        {/* <Link
          to="/chat/1"  // Example: link to chat with document id 1; adjust as needed
          className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg text-lg font-semibold"
        >
          Chat on Document (Example)
        </Link> */}
      </nav>
    </div>
  )
}
