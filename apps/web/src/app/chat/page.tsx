'use client'

import { useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { Send, Bot, User, Loader2, AlertCircle } from 'lucide-react'

export default function ChatPage() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState<Array<{ 
    role: string
    content: string
    provider?: string
  }>>([])

  // 获取可用的 AI 提供商
  const { data: providers } = useQuery({
    queryKey: ['chat-providers'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8001/api/v1/chat/providers')
      return response.json()
    },
    refetchInterval: 10000
  })

  const sendMessage = useMutation({
    mutationFn: async (msg: string) => {
      const response = await fetch('http://localhost:8001/api/v1/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: msg,
          userId: 1,
          system_prompt: '你是一位专业、耐心、友善的 AI 导师，专注于帮助学生掌握 AI 和机器学习知识。请用中文回答，解释要清晰易懂，多举例子。'
        })
      })
      return response.json()
    },
    onSuccess: (data) => {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.message,
        provider: data.provider
      }])
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim() || sendMessage.isPending) return
    
    setMessages(prev => [...prev, { role: 'user', content: message }])
    sendMessage.mutate(message)
    setMessage('')
  }

  const hasConfiguredProvider = providers?.providers?.some((p: any) => p.configured && p.enabled)

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col">
      {/* Header */}
      <div className="border-b bg-white px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">🤖 AI 导师</h1>
            <p className="text-sm text-gray-500">随时解答你的学习问题</p>
          </div>
          <div className="flex items-center gap-2">
            {providers?.providers?.filter((p: any) => p.enabled).map((p: any) => (
              <span
                key={p.id}
                className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium"
                title={`${p.name} 已配置`}
              >
                {p.name}
              </span>
            ))}
            {!hasConfiguredProvider && (
              <span className="px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs font-medium">
                未配置 API
              </span>
            )}
          </div>
        </div>
      </div>

      {/* 未配置 API 提示 */}
      {!hasConfiguredProvider && messages.length === 0 && (
        <div className="flex-1 flex items-center justify-center p-6">
          <div className="max-w-md text-center">
            <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6 mb-6">
              <AlertCircle className="h-12 w-12 text-yellow-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-yellow-900 mb-2">
                请先配置 API 密钥
              </h3>
              <p className="text-sm text-yellow-800 mb-4">
                在 <a href="/integrations" className="underline font-medium">API 集成</a> 页面配置至少一个 AI API 才能使用 AI 导师功能。
              </p>
              <a
                href="/integrations"
                className="inline-block px-6 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors font-medium"
              >
                去配置 API
              </a>
            </div>
            <div className="text-gray-500 text-sm">
              <p>支持的 AI 提供商：</p>
              <div className="flex justify-center gap-4 mt-2">
                <span>🤖 通义千问</span>
                <span>🧠 OpenAI</span>
                <span>🤖 Anthropic</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Messages */}
      {(hasConfiguredProvider || messages.length > 0) && (
        <>
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 mt-20">
                <Bot className="h-16 w-16 mx-auto mb-4 text-gray-300" />
                <p>开始与 AI 导师对话吧！</p>
                <p className="text-sm mt-2">问任何问题，比如："什么是机器学习？"</p>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex items-start gap-3 ${
                    msg.role === 'user' ? 'flex-row-reverse' : ''
                  }`}
                >
                  <div
                    className={`p-2 rounded-lg ${
                      msg.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 text-gray-800'
                    }`}
                  >
                    {msg.role === 'user' ? (
                      <User className="h-5 w-5" />
                    ) : (
                      <Bot className="h-5 w-5" />
                    )}
                  </div>
                  <div
                    className={`max-w-[70%] rounded-2xl p-4 ${
                      msg.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white border shadow-sm'
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                    {msg.provider && (
                      <p className="text-xs text-gray-400 mt-2">
                        来自：{msg.provider.toUpperCase()}
                      </p>
                    )}
                  </div>
                </div>
              ))
            )}
            
            {sendMessage.isPending && (
              <div className="flex items-center gap-3">
                <div className="bg-gray-200 p-2 rounded-lg">
                  <Bot className="h-5 w-5 text-gray-600" />
                </div>
                <div className="bg-white border rounded-2xl p-4">
                  <div className="flex items-center gap-2 text-gray-500">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span>AI 思考中...</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <form onSubmit={handleSubmit} className="border-t bg-white p-4">
            <div className="flex gap-4 max-w-4xl mx-auto">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder={hasConfiguredProvider ? "输入你的问题..." : "请先配置 API 密钥"}
                className="flex-1 border rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={!hasConfiguredProvider || sendMessage.isPending}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    handleSubmit(e)
                  }
                }}
              />
              <button
                type="submit"
                disabled={!hasConfiguredProvider || !message.trim() || sendMessage.isPending}
                className="bg-blue-600 text-white px-6 py-3 rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <Send className="h-5 w-5" />
                发送
              </button>
            </div>
          </form>
        </>
      )}
    </div>
  )
}
