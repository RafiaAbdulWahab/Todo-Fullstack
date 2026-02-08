import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <main className="flex flex-col items-center justify-center flex-1 px-4 sm:px-20 text-center">
        <h1 className="text-4xl sm:text-6xl font-bold mb-8">
          Welcome to Todo Full-Stack App
        </h1>

        <div className="flex flex-wrap items-center justify-center gap-4">
          <Link href="/login" className="p-4 border border-gray-300 rounded-lg hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50 transition ease-in-out duration-150">
            <h2 className="text-xl font-semibold">Login &rarr;</h2>
            <p className="mt-2 text-sm text-gray-700">Access your account.</p>
          </Link>

          <Link href="/signup" className="p-4 border border-gray-300 rounded-lg hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50 transition ease-in-out duration-150">
            <h2 className="text-xl font-semibold">Signup &rarr;</h2>
            <p className="mt-2 text-sm text-gray-700">Create a new account.</p>
          </Link>

          <Link href="/dashboard" className="p-4 border border-gray-300 rounded-lg hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50 transition ease-in-out duration-150">
            <h2 className="text-xl font-semibold">Dashboard &rarr;</h2>
            <p className="mt-2 text-sm text-gray-700">View your tasks.</p>
          </Link>

          <Link href="/chat" className="p-4 border border-blue-300 rounded-lg hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50 transition ease-in-out duration-150">
            <h2 className="text-xl font-semibold">AI Chatbot &rarr;</h2>
            <p className="mt-2 text-sm text-gray-700">Chat with your AI assistant.</p>
          </Link>
        </div>
      </main>
    </div>
  );
}
