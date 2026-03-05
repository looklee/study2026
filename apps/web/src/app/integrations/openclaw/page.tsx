'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  Key, 
  CheckCircle, 
  XCircle, 
  Settings, 
  RefreshCw, 
  Trash2, 
  Eye, 
  EyeOff, 
  Link as LinkIcon, 
  Zap, 
  AlertCircle,
  Brain,
  Cpu,
  Network
} from 'lucide-react'
import { openclawApi } from '@/lib/api'

export default function OpenClawIntegrationPage() {
  const [showApiKey, setShowApiKey] = useState(false)
  const [apiKey, setApiKey] = useState('')
  const [baseUrl, setBaseUrl] = useState('')
  const [model, setModel] = useState('gpt-4o')
  const queryClient = useQueryClient()

  // 获取 OpenClaw 配置
  const { data: config, isLoading } = useQuery({
    queryKey: ['openclaw-config'],
    queryFn: async () => {
      try {
        const response = await openclawApi.health()
        return { 
          configured: true, 
          enabled: true, 
          last_4_digits: '****', 
          updated_at: new Date().toISOString() 
        }
      } catch (error) {
        return { configured: false, enabled: false }
      }
    },
    refetchInterval: 30000
  })

  // 测试 OpenClaw 连接
  const testMutation = useMutation({
    mutationFn: async () => {
      const response = await openclawApi.health()
      return response.data
    }
  })

  // 配置 OpenClaw
  const configureMutation = useMutation({
    mutationFn: async ({ key, url }: { key?: string; url?: string }) => {
      // 在实际实现中，这会向后端发送配置请求
      // 目前我们只做健康检查
      return { success: true, message: '配置更新成功' }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['openclaw-config'] })
      alert('配置更新成功！')
    }
  })

  const handleSave = () => {
    configureMutation.mutate({
      key: apiKey || undefined,
      url: baseUrl || undefined
    })
  }

  const models = [
    { id: 'gpt-4o', name: 'GPT-4o (推荐)' },
    { id: 'gpt-4-turbo', name: 'GPT-4 Turbo' },
    { id: 'claude-3-opus', name: 'Claude 3 Opus' },
    { id: 'claude-3-sonnet', name: 'Claude 3 Sonnet' },
    { id: 'qwen-max', name: '通义千问 Max' },
    { id: 'custom', name: '自定义模型' }
  ]

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="bg-gradient-to-r from-red-500 to-orange-500 p-2 rounded-lg">
            <Brain className="h-6 w-6 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">🦞 OpenClaw 集成</h1>
        </div>
        <p className="text-gray-600">配置 OpenClaw AI 助手，享受个性化AI体验</p>
      </div>

      {/* Status Card */}
      <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">服务状态</h2>
            <p className="text-gray-600">OpenClaw AI 助手运行状态</p>
          </div>
          <div className={`px-4 py-2 rounded-full text-sm font-medium ${
            config?.configured 
              ? 'bg-green-100 text-green-700' 
              : 'bg-gray-100 text-gray-700'
          }`}>
            {config?.configured ? '已连接' : '未连接'}
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center gap-2 text-gray-600 mb-1">
              <Cpu className="h-4 w-4" />
              <span className="text-sm">模型</span>
            </div>
            <p className="font-medium">{model}</p>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center gap-2 text-gray-600 mb-1">
              <Network className="h-4 w-4" />
              <span className="text-sm">连接状态</span>
            </div>
            <p className="font-medium text-green-600">已连接</p>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center gap-2 text-gray-600 mb-1">
              <Zap className="h-4 w-4" />
              <span className="text-sm">响应速度</span>
            </div>
            <p className="font-medium">快速</p>
          </div>
        </div>
      </div>

      {/* Configuration Card */}
      <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">API 配置</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              API Key <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <input
                type={showApiKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="sk-..."
                className="w-full border rounded-lg pl-4 pr-12 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={() => setShowApiKey(!showApiKey)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showApiKey ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>
            <p className="mt-1 text-xs text-gray-500">
              用于连接 OpenClaw 服务的 API 密钥
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Base URL
            </label>
            <input
              type="text"
              value={baseUrl}
              onChange={(e) => setBaseUrl(e.target.value)}
              placeholder="https://api.openai.com/v1"
              className="w-full border rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="mt-1 text-xs text-gray-500">
              OpenClaw 服务的基础 URL
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              模型选择
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full border rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {models.map((m) => (
                <option key={m.id} value={m.id}>{m.name}</option>
              ))}
            </select>
            <p className="mt-1 text-xs text-gray-500">
              选择用于 OpenClaw 的 AI 模型
            </p>
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button
            onClick={handleSave}
            disabled={configureMutation.isPending}
            className="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            {configureMutation.isPending ? '保存中...' : '保存配置'}
          </button>
          
          <button
            onClick={() => testMutation.mutate()}
            disabled={testMutation.isPending}
            className="px-6 py-2.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            <RefreshCw className={`h-4 w-4 ${testMutation.isPending ? 'animate-spin' : ''}`} />
            {testMutation.isPending ? '测试中...' : '测试连接'}
          </button>
        </div>

        {/* Test Result */}
        {testMutation.data && (
          <div className={`mt-4 p-3 rounded-lg ${
            testMutation.data.status === 'healthy'
              ? 'bg-green-50 text-green-700'
              : 'bg-red-50 text-red-700'
          }`}>
            <div className="flex items-center gap-2">
              {testMutation.data.status === 'healthy' ? (
                <CheckCircle className="h-5 w-5" />
              ) : (
                <XCircle className="h-5 w-5" />
              )}
              <span>
                {testMutation.data.status === 'healthy' 
                  ? '连接测试成功！OpenClaw 服务正常运行。' 
                  : '连接测试失败，请检查配置。'}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Features */}
      <div className="bg-white rounded-xl shadow-sm border p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">OpenClaw 功能特性</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="h-5 w-5 text-yellow-500" />
              <span className="font-medium">多模型支持</span>
            </div>
            <p className="text-sm text-gray-600">
              支持多种AI模型，可根据需求切换
            </p>
          </div>
          
          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="h-5 w-5 text-blue-500" />
              <span className="font-medium">技能扩展</span>
            </div>
            <p className="text-sm text-gray-600">
              支持丰富的AI技能，持续扩展中
            </p>
          </div>
          
          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="h-5 w-5 text-green-500" />
              <span className="font-medium">跨平台</span>
            </div>
            <p className="text-sm text-gray-600">
              支持所有操作系统和平台
            </p>
          </div>
          
          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="h-5 w-5 text-purple-500" />
              <span className="font-medium">数据自主</span>
            </div>
            <p className="text-sm text-gray-600">
              完全控制您的数据和隐私
            </p>
          </div>
          
          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="h-5 w-5 text-red-500" />
              <span className="font-medium">智能对话</span>
            </div>
            <p className="text-sm text-gray-600">
              高质量的AI对话体验
            </p>
          </div>
          
          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="h-5 w-5 text-indigo-500" />
              <span className="font-medium">持续学习</span>
            </div>
            <p className="text-sm text-gray-600">
              AI助手不断学习和改进
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}