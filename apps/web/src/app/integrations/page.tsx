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
  AlertCircle
} from 'lucide-react'

const providers = [
  {
    id: 'qwen',
    name: '通义千问 (Qwen)',
    description: '阿里云通义千问大模型，支持聊天对话、内容生成',
    category: 'AI',
    icon: '🤖',
    color: 'purple',
    configUrl: 'https://dashscope.console.aliyun.com/apiKey',
    defaultBaseUrl: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    envVar: 'QWEN_API_KEY'
  },
  {
    id: 'openai',
    name: 'OpenAI (GPT)',
    description: 'GPT-4、ChatGPT 等 AI 模型',
    category: 'AI',
    icon: '🧠',
    color: 'green',
    configUrl: 'https://platform.openai.com/api-keys',
    defaultBaseUrl: 'https://api.openai.com/v1',
    envVar: 'OPENAI_API_KEY'
  },
  {
    id: 'anthropic',
    name: 'Anthropic (Claude)',
    description: 'Claude AI 助手，擅长长文本理解',
    category: 'AI',
    icon: '🤖',
    color: 'orange',
    configUrl: 'https://console.anthropic.com/settings/keys',
    defaultBaseUrl: 'https://api.anthropic.com',
    envVar: 'ANTHROPIC_API_KEY'
  },
  {
    id: 'openclaw',
    name: 'OpenClaw AI 助手',
    description: '个人AI助手，支持多模型和技能扩展',
    category: 'AI',
    icon: '🦞',
    color: 'red',
    configUrl: 'https://github.com/openclaw/openclaw',
    defaultBaseUrl: 'https://api.openai.com/v1',
    envVar: 'OPENCLAW_API_KEY'
  }
]

export default function IntegrationsPage() {
  const [selectedProvider, setSelectedProvider] = useState<string | null>(null)
  const [showApiKey, setShowApiKey] = useState(false)
  const [apiKey, setApiKey] = useState('')
  const [baseUrl, setBaseUrl] = useState('')

  const queryClient = useQueryClient()

  // 获取 API 密钥配置
  const { data: apiKeys, isLoading } = useQuery({
    queryKey: ['api-keys'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8001/api/v1/api-keys')
      return response.json()
    },
    refetchInterval: 5000
  })

  // 配置 API 密钥
  const configureMutation = useMutation({
    mutationFn: async ({ provider, key, url }: { provider: string; key: string | undefined; url?: string }) => {
      const response = await fetch(`http://localhost:8001/api/v1/api-keys/${provider}/configure`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          api_key: key,
          base_url: url,
          enabled: true
        })
      })
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['api-keys'] })
      setSelectedProvider(null)
      setApiKey('')
      setBaseUrl('')
      alert('配置成功！')
    }
  })

  // 测试 API 密钥
  const testMutation = useMutation({
    mutationFn: async (provider: string) => {
      const response = await fetch(`http://localhost:8001/api/v1/api-keys/${provider}/test`, {
        method: 'POST'
      })
      return response.json()
    }
  })

  // 删除 API 密钥
  const deleteMutation = useMutation({
    mutationFn: async (provider: string) => {
      const response = await fetch(`http://localhost:8001/api/v1/api-keys/${provider}`, {
        method: 'DELETE'
      })
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['api-keys'] })
      alert('已删除配置')
    }
  })

  // 切换启用状态
  const toggleMutation = useMutation({
    mutationFn: async (provider: string) => {
      const response = await fetch(`http://localhost:8001/api/v1/api-keys/${provider}/toggle`, {
        method: 'POST'
      })
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['api-keys'] })
    }
  })

  const openConfigModal = (providerId: string) => {
    setSelectedProvider(providerId)
    const provider = providers.find(p => p.id === providerId)
    if (provider) {
      setBaseUrl(provider.defaultBaseUrl)
    }
    // 如果有已保存的密钥，显示部分
    const savedConfig = apiKeys?.[providerId]
    if (savedConfig?.last_4_digits) {
      // 编辑模式，显示占位符但允许修改
      setApiKey('') // 清空让用户重新输入或保留
    } else {
      setApiKey('')
    }
  }

  const handleSave = () => {
    if (selectedProvider) {
      // 如果有新的 API Key 或者要更新 base_url
      if ((apiKey && !apiKey.startsWith('sk-...')) || baseUrl) {
        configureMutation.mutate({
          provider: selectedProvider,
          key: apiKey?.startsWith('sk-...') ? undefined : apiKey,
          url: baseUrl
        })
      }
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">🔌 API 集成</h1>
        <p className="text-gray-500 mt-1">配置 AI API 密钥，让 AI 导师使用真实的大模型</p>
      </div>

      {/* 状态提示 */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
        <div className="flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5" />
          <div>
            <h3 className="font-medium text-blue-900">配置说明</h3>
            <ul className="mt-2 text-sm text-blue-800 space-y-1">
              <li>• 至少配置一个 AI API 才能使用 AI 导师功能</li>
              <li>• 推荐使用 <strong>通义千问</strong>（国内访问快，有免费额度）</li>
              <li>• 配置后 AI 导师会自动使用已启用的 API 进行对话</li>
              <li>• 可以配置多个 API，系统会按优先级自动切换</li>
            </ul>
          </div>
        </div>
      </div>

      {/* API 列表 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {providers.map((provider) => {
          const config = apiKeys?.[provider.id]
          const isConfigured = config?.configured
          const isEnabled = config?.enabled
          const statusColor = isConfigured && isEnabled ? 'green' : isConfigured ? 'yellow' : 'gray'
          
          return (
            <div
              key={provider.id}
              className={`bg-white rounded-xl shadow-sm border-2 p-6 transition-all ${
                isEnabled ? `border-${provider.color}-200` : 'border-gray-200'
              }`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="text-4xl">{provider.icon}</div>
                  <div>
                    <h3 className="font-semibold text-gray-900">{provider.name}</h3>
                    <span className="text-xs text-gray-500">{provider.category}</span>
                  </div>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  isEnabled
                    ? 'bg-green-100 text-green-700'
                    : isConfigured
                    ? 'bg-yellow-100 text-yellow-700'
                    : 'bg-gray-100 text-gray-700'
                }`}>
                  {isEnabled ? '已启用' : isConfigured ? '已配置' : '未配置'}
                </span>
              </div>

              <p className="text-sm text-gray-600 mb-4">{provider.description}</p>

              {/* 状态信息 */}
              {isConfigured && (
                <div className="mb-4 text-xs text-gray-500">
                  <div className="flex items-center gap-2">
                    <Key className="h-3 w-3" />
                    <span>密钥尾号：{config.last_4_digits}</span>
                  </div>
                  {config.updated_at && (
                    <div className="flex items-center gap-2 mt-1">
                      <RefreshCw className="h-3 w-3" />
                      <span>更新于：{new Date(config.updated_at).toLocaleString('zh-CN')}</span>
                    </div>
                  )}
                </div>
              )}

              {/* 操作按钮 */}
              <div className="flex gap-2">
                <button
                  onClick={() => openConfigModal(provider.id)}
                  className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    provider.color === 'purple'
                      ? 'bg-purple-600 text-white hover:bg-purple-700'
                      : provider.color === 'green'
                      ? 'bg-green-600 text-white hover:bg-green-700'
                      : 'bg-orange-600 text-white hover:bg-orange-700'
                  }`}
                >
                  <Settings className="h-4 w-4" />
                  {isConfigured ? '编辑' : '配置'}
                </button>
                
                {isConfigured && (
                  <>
                    <button
                      onClick={() => testMutation.mutate(provider.id)}
                      disabled={testMutation.isPending}
                      className="p-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50"
                      title="测试连接"
                    >
                      <RefreshCw className={`h-4 w-4 ${testMutation.isPending ? 'animate-spin' : ''}`} />
                    </button>
                    <button
                      onClick={() => toggleMutation.mutate(provider.id)}
                      className="p-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                      title={isEnabled ? '禁用' : '启用'}
                    >
                      {isEnabled ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                    <button
                      onClick={() => deleteMutation.mutate(provider.id)}
                      className="p-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors"
                      title="删除"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </>
                )}
              </div>

              {/* 测试结果 */}
              {testMutation.data && (
                <div className={`mt-3 p-2 rounded-lg text-xs ${
                  testMutation.data.status === 'success'
                    ? 'bg-green-50 text-green-700'
                    : 'bg-red-50 text-red-700'
                }`}>
                  <div className="flex items-center gap-2">
                    {testMutation.data.status === 'success' ? (
                      <CheckCircle className="h-3 w-3" />
                    ) : (
                      <XCircle className="h-3 w-3" />
                    )}
                    <span>{testMutation.data.message}</span>
                  </div>
                </div>
              )}

              {/* 获取密钥链接 */}
              <div className="space-y-2">
                {provider.id !== 'openclaw' ? (
                  <a
                    href={provider.configUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-center gap-2 text-xs text-gray-500 hover:text-gray-700"
                  >
                    <LinkIcon className="h-3 w-3" />
                    获取 API Key
                  </a>
                ) : (
                  <a
                    href="/integrations/openclaw"
                    className="flex items-center justify-center gap-2 text-xs text-blue-600 hover:text-blue-800 font-medium"
                  >
                    <Settings className="h-3 w-3" />
                    配置 OpenClaw
                  </a>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {/* 配置模态框 */}
      {selectedProvider && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold">
                配置 {providers.find(p => p.id === selectedProvider)?.name}
              </h2>
              <button
                onClick={() => setSelectedProvider(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                <XCircle className="h-6 w-6" />
              </button>
            </div>

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
                  你的 API 密钥会安全地存储在本地
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Base URL (可选)
                </label>
                <input
                  type="text"
                  value={baseUrl}
                  onChange={(e) => setBaseUrl(e.target.value)}
                  placeholder="https://api.example.com"
                  className="w-full border rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => setSelectedProvider(null)}
                  className="flex-1 px-4 py-2.5 border rounded-lg hover:bg-gray-50 transition-colors"
                >
                  取消
                </button>
                <button
                  onClick={handleSave}
                  disabled={configureMutation.isPending || !apiKey}
                  className="flex-1 px-4 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {configureMutation.isPending ? '保存中...' : '保存配置'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
