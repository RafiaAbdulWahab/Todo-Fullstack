// frontend/src/app/chat/page.tsx
"use client";

import { useState, useEffect, useRef, FormEvent } from 'react';
import fetchWithAuth from '../../../src/lib/api'; // Adjust path as necessary
import { useRouter } from 'next/navigation'; // For redirection if needed

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatResponse {
  conversation_id: number;
  ai_response: string;
  tool_outputs?: Array<Record<string, any>>; // Adjust type if more specific schema is known
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Optionally, load initial conversation history if navigating to an existing chat
  // For simplicity, we start fresh or continue the last one if conversationId is persisted.
  useEffect(() => {
    const savedConversationId = localStorage.getItem('lastConversationId');
    if (savedConversationId) {
      setConversationId(parseInt(savedConversationId, 10));
      // In a real app, you would fetch the history for this conversationId
      // For this implementation, we assume starting fresh if not explicitly fetched.
    }
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: inputMessage };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const requestBody = {
        conversation_id: conversationId,
        message: inputMessage,
      };

      const response = await fetchWithAuth('/api/chat', {
        method: 'POST',
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        // Handle API errors, e.g., redirect to login if unauthorized
        if (response.status === 401) {
          router.push('/login');
        }
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get AI response');
      }

      const data: ChatResponse = await response.json();
      
      // Update conversationId if it's a new conversation
      if (conversationId === null && data.conversation_id) {
        setConversationId(data.conversation_id);
        localStorage.setItem('lastConversationId', data.conversation_id.toString());
      }

      const assistantMessage: Message = { role: 'assistant', content: data.ai_response };
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);

    } catch (error: any) {
      console.error('Chat API Error:', error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'assistant', content: `Error: ${error.message}. Please try again.` },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 text-gray-800">
      <header className="bg-white shadow p-4 text-center text-2xl font-bold">
        AI Chatbot
      </header>

      <main className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex justify-center items-center h-full text-gray-500">
            Start a conversation with the AI!
          </div>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg shadow ${
                  msg.role === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white text-gray-800'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </main>

      <form onSubmit={handleSubmit} className="bg-white shadow-md p-4 flex items-center">
        <textarea
          className="flex-1 resize-none border rounded-lg p-2 mr-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={1}
          placeholder="Type your message..."
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          disabled={isLoading}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
}
