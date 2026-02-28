'use client'

import { useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'
import { Sparkles, Clock, BookOpen, Target, AlertCircle } from 'lucide-react'

export default function NewPathPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    currentLevel: 'beginner',
    targetGoal: '',
    availableHoursPerWeek: 10,
    preferredLearningStyle: 'mixed',
    priorExperience: ''
  })

  // 获取可用的 AI 提供商
  const { data: providers } = useQuery({
    queryKey: ['chat-providers'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8001/api/v1/chat/providers')
      return response.json()
    },
    refetchInterval: 10000
  })

  const hasConfiguredProvider = providers?.providers?.some((p: any) => p.configured && p.enabled)

  const generatePath = useMutation({
    mutationFn: async (data: any) => {
      // 调用 Qwen API 生成学习路径
      const qwenConfig = providers?.providers?.find((p: any) => p.id === 'qwen' && p.enabled)
      
      if (!qwenConfig && !providers?.providers?.some((p: any) => p.configured && p.enabled)) {
        throw new Error('请先配置 API 密钥')
      }

      // 使用 AI 生成学习路径
      const systemPrompt = `你是一位专业的 AI 学习路径规划专家。
根据学习者的背景和目标，生成详细的个性化学习路径。

输出 JSON 格式：
{
  "pathName": "路径名称",
  "description": "路径描述",
  "totalDuration": "总时长（如：12 周）",
  "phases": [
    {
      "phaseNumber": 1,
      "phaseName": "阶段名称",
      "duration": "持续时间",
      "objectives": ["目标 1", "目标 2"],
      "topics": ["主题 1", "主题 2"],
      "milestone": "里程碑描述",
      "status": "pending"
    }
  ],
  "weeklySchedule": {
    "monday": "学习内容",
    "wednesday": "学习内容",
    "weekend": "实践项目"
  },
  "tips": ["学习建议 1", "学习建议 2"]
}`

      const userPrompt = `请根据以下学习者信息生成学习路径：

当前水平：${data.currentLevel === 'beginner' ? '初学者' : data.currentLevel === 'intermediate' ? '中级' : '高级'}
学习目标：${data.targetGoal}
每周可用时间：${data.availableHoursPerWeek} 小时
学习风格：${data.preferredLearningStyle === 'mixed' ? '混合式（理论 + 实践）' : data.preferredLearningStyle === 'hands-on' ? '动手实践为主' : '理论学习为主'}
已有经验：${data.priorExperience || '无'}

请生成一份详细的学习路径，返回 JSON 格式。`

      const response = await fetch('http://localhost:8001/api/v1/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: `请生成学习路径 JSON：${userPrompt}`,
          userId: 1,
          system_prompt: systemPrompt
        })
      })

      const result = await response.json()
      
      // 尝试从回复中提取 JSON
      try {
        const jsonMatch = result.message.match(/\{[\s\S]*\}/)
        if (jsonMatch) {
          return JSON.parse(jsonMatch[0])
        }
      } catch (e) {
        console.error('JSON 解析失败', e)
      }
      
      // 返回默认结构
      return generateDefaultPath(data)
    },
    onSuccess: (pathData) => {
      // 保存学习路径到本地存储
      const paths = JSON.parse(localStorage.getItem('learning_paths') || '[]')
      const newPath = {
        id: Date.now(),
        ...pathData,
        progress: 0,
        status: 'active',
        createdAt: new Date().toISOString()
      }
      paths.push(newPath)
      localStorage.setItem('learning_paths', JSON.stringify(paths))
      
      // 跳转到路径列表
      router.push('/paths')
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!hasConfiguredProvider) {
      alert('请先在 API 集成页面配置 AI API 密钥')
      router.push('/integrations')
      return
    }
    generatePath.mutate(formData)
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">✨ AI 生成学习路径</h1>
        <p className="text-gray-500 mt-1">填写你的学习信息，AI 将为你生成个性化学习计划</p>
      </div>

      {/* API 配置提示 */}
      {!hasConfiguredProvider && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-4">
          <div className="flex items-start gap-3">
            <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5" />
            <div className="flex-1">
              <h3 className="font-medium text-yellow-900">需要配置 AI API</h3>
              <p className="text-sm text-yellow-800 mt-1">
                请在 <a href="/integrations" className="underline font-medium">API 集成</a> 页面配置至少一个 AI API 才能使用 AI 生成功能。
              </p>
              <button
                onClick={() => router.push('/integrations')}
                className="mt-3 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors text-sm font-medium"
              >
                去配置 API
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 表单 */}
      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-sm border p-6 space-y-6">
        {/* 当前水平 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            当前水平 <span className="text-red-500">*</span>
          </label>
          <select
            value={formData.currentLevel}
            onChange={(e) => setFormData({ ...formData, currentLevel: e.target.value })}
            className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          >
            <option value="beginner">初学者 - 从零开始</option>
            <option value="intermediate">中级 - 有一定基础</option>
            <option value="advanced">高级 - 想深入学习</option>
          </select>
        </div>

        {/* 学习目标 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            学习目标 <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={formData.targetGoal}
            onChange={(e) => setFormData({ ...formData, targetGoal: e.target.value })}
            placeholder="例如：掌握机器学习基础，能够独立完成 ML 项目"
            className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* 每周时间 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            每周可用时间（小时） <span className="text-red-500">*</span>
          </label>
          <input
            type="number"
            value={formData.availableHoursPerWeek}
            onChange={(e) => setFormData({ ...formData, availableHoursPerWeek: parseInt(e.target.value) })}
            min="1"
            max="168"
            className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        {/* 学习风格 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            学习风格
          </label>
          <select
            value={formData.preferredLearningStyle}
            onChange={(e) => setFormData({ ...formData, preferredLearningStyle: e.target.value })}
            className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="mixed">混合式（理论 + 实践）</option>
            <option value="hands-on">动手实践为主</option>
            <option value="theoretical">理论学习为主</option>
            <option value="video-based">视频教程为主</option>
          </select>
        </div>

        {/* 已有经验 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            已有经验（用逗号分隔）
          </label>
          <input
            type="text"
            value={formData.priorExperience}
            onChange={(e) => setFormData({ ...formData, priorExperience: e.target.value })}
            placeholder="例如：Python 编程，线性代数"
            className="w-full border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* 提交按钮 */}
        <button
          type="submit"
          disabled={generatePath.isPending || !hasConfiguredProvider}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-medium text-lg shadow-lg"
        >
          {generatePath.isPending ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              AI 正在生成学习路径...
            </>
          ) : (
            <>
              <Sparkles className="h-5 w-5" />
              AI 生成学习路径
            </>
          )}
        </button>

        {/* 生成说明 */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-medium text-blue-900 mb-2">AI 将为你生成：</h4>
          <ul className="space-y-1 text-sm text-blue-800">
            <li className="flex items-center gap-2">
              <Target className="h-4 w-4" />
              个性化学习目标和阶段划分
            </li>
            <li className="flex items-center gap-2">
              <Clock className="h-4 w-4" />
              详细的时间规划（基于你的可用时间）
            </li>
            <li className="flex items-center gap-2">
              <BookOpen className="h-4 w-4" />
              每周学习安排和建议
            </li>
          </ul>
        </div>
      </form>
    </div>
  )
}

// 生成默认学习路径（当 AI 不可用时）
function generateDefaultPath(data: any) {
  return {
    pathName: `${data.targetGoal}之路`,
    description: `个性化定制：${data.targetGoal}`,
    totalDuration: '12 周',
    phases: [
      {
        phaseNumber: 1,
        phaseName: '基础准备',
        duration: '2 周',
        objectives: ['掌握基础概念', '熟悉工具和环境'],
        topics: ['入门概念', '环境搭建', 'Hello World'],
        milestone: '完成第一个小项目',
        status: 'pending'
      },
      {
        phaseNumber: 2,
        phaseName: '核心知识',
        duration: '4 周',
        objectives: ['深入理解核心概念', '掌握常用技术'],
        topics: ['核心理论', '常用算法', '最佳实践'],
        milestone: '完成中等难度项目',
        status: 'pending'
      },
      {
        phaseNumber: 3,
        phaseName: '进阶提升',
        duration: '4 周',
        objectives: ['学习高级主题', '实战演练'],
        topics: ['高级特性', '性能优化', '架构设计'],
        milestone: '完成综合项目',
        status: 'pending'
      },
      {
        phaseNumber: 4,
        phaseName: '实战项目',
        duration: '2 周',
        objectives: ['独立完成项目'],
        topics: ['项目选题', '开发实施', '部署上线'],
        milestone: '完成毕业设计',
        status: 'pending'
      }
    ],
    weeklySchedule: {
      monday: '理论学习 2 小时',
      wednesday: '代码练习 2 小时',
      weekend: '项目实践 4 小时'
    },
    tips: ['每天坚持写学习笔记', '多动手实践', '参与社区讨论']
  }
}
