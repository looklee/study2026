'use client'

import { useState, useRef, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Send, Bot, User, Sparkles, Zap, Brain, Loader2 } from 'lucide-react'
import { openclawApi } from '@/lib/api'

export default function OpenClawPage() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Array<{
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
  }>>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const queryClient = useQueryClient()

  // 获取可用技能
  const { data: skillsData, isLoading: skillsLoading } = useQuery({
    queryKey: ['openclaw-skills'],
    queryFn: async () => {
      const response = await openclawApi.getSkills()
      return response.data
    },
    refetchInterval: 30000 // 每30秒刷新一次
  })

  // 发送消息到OpenClaw
  const sendMessageMutation = useMutation({
    mutationFn: async (message: string) => {
      const response = await openclawApi.chat({
        message,
        conversation_id: 'web-conversation'
      })
      return response.data
    },
    onSuccess: (data) => {
      const newMessage = {
        id: Date.now().toString(),
        role: 'assistant' as const,
        content: data.reply,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, newMessage])
      setInput('')
    },
    onError: (error) => {
      console.error('发送消息失败:', error)
      const errorMessage = {
        id: Date.now().toString(),
        role: 'assistant' as const,
        content: '抱歉，发生了一些错误，请稍后再试。',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    }
  })

  // 处理发送消息
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || sendMessageMutation.isPending) return

    // 添加用户消息
    const userMessage = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: input.trim(),
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])

    // 发送消息到API
    sendMessageMutation.mutate(input.trim())
  }

  // 滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // 快捷操作
  const quickActions = [
    { icon: Brain, label: '解释概念', prompt: '请解释什么是人工智能？' },
    { icon: Zap, label: '生成想法', prompt: '给我一些关于学习编程的建议' },
    { icon: Sparkles, label: '创意写作', prompt: '帮我写一段关于未来学习的文章' },
  ]

  const handleQuickAction = (prompt: string) => {
    setInput(prompt)
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* 标题区域 */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-3 bg-gradient-to-r from-red-500 to-orange-500 text-white px-6 py-3 rounded-full mb-4">
          <span className="text-2xl">🦞</span>
          <h1 className="text-2xl font-bold">OpenClaw AI 助手</h1>
        </div>
        <p className="text-gray-600">您的个人AI助手，支持多模型和技能扩展</p>
      </div>

      {/* 快捷操作 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
        {quickActions.map((action, index) => (
          <button
            key={index}
            onClick={() => handleQuickAction(action.prompt)}
            className="flex items-center justify-center gap-2 bg-white border border-gray-200 rounded-lg p-3 hover:bg-gray-50 transition-colors"
          >
            <action.icon className="h-4 w-4 text-blue-600" />
            <span className="text-sm font-medium">{action.label}</span>
          </button>
        ))}
      </div>

      {/* 技能面板 */}
      <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Zap className="h-5 w-5 text-yellow-600" />
          <h2 className="text-lg font-semibold">可用技能</h2>
          {skillsLoading && <Loader2 className="h-4 w-4 animate-spin ml-2" />}
        </div>
        {skillsData?.skills ? (
          <div className="flex flex-wrap gap-2">
            {skillsData.skills.slice(0, 6).map((skill: string, index: number) => (
              <span 
                key={index}
                className="bg-blue-100 text-blue-800 text-xs font-medium px-3 py-1 rounded-full"
              >
                {skill}
              </span>
            ))}
            {skillsData.skills.length > 6 && (
              <span className="bg-gray-100 text-gray-800 text-xs font-medium px-3 py-1 rounded-full">
                +{skillsData.skills.length - 6} 更多
              </span>
            )}
          </div>
        ) : (
          <p className="text-gray-500 text-sm">暂无可用技能</p>
        )}
      </div>

      {/* 聊天区域 */}
      <div className="bg-white rounded-xl shadow-sm border h-[500px] flex flex-col">
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center text-gray-500">
              <Bot className="h-12 w-12 mb-4 text-gray-300" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">欢迎使用 OpenClaw AI 助手</h3>
              <p className="max-w-md">我是您的个人AI助手，可以帮助您解答问题、生成内容、执行任务等。</p>
              <p className="max-w-md mt-2">在下方输入框中提问，开始与我交流吧！</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-gray-100 text-gray-800 rounded-bl-none'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    {message.role === 'assistant' && (
                      <Bot className="h-4 w-4 mt-0.5 flex-shrink-0" />
                    )}
                    <div className="whitespace-pre-wrap break-words">
                      {message.content}
                    </div>
                    {message.role === 'user' && (
                      <User className="h-4 w-4 mt-0.5 flex-shrink-0" />
                    )}
                  </div>
                  <div
                    className={`text-xs mt-1 ${
                      message.role === 'user' ? 'text-blue-200' : 'text-gray-500'
                    }`}
                  >
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              </div>
            ))
          )}
          {sendMessageMutation.isPending && (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-800 rounded-2xl rounded-bl-none px-4 py-3">
                <div className="flex items-center gap-2">
                  <Bot className="h-4 w-4" />
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>AI 正在思考...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* 输入区域 */}
        <form onSubmit={handleSubmit} className="border-t p-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="输入您的问题..."
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={sendMessageMutation.isPending}
            />
            <button
              type="submit"
              disabled={!input.trim() || sendMessageMutation.isPending}
              className="bg-blue-600 text-white rounded-lg px-6 py-3 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {sendMessageMutation.isPending ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
              发送
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            OpenClaw AI 助手 • 支持多模型和技能扩展
          </p>
        </form>
      </div>
    </div>
  )
}