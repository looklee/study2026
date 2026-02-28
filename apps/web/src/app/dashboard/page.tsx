'use client'

import { useQuery } from '@tanstack/react-query'
import { Plus, Target, Clock, TrendingUp } from 'lucide-react'
import Link from 'next/link'

export default function DashboardPage() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['stats'],
    queryFn: async () => {
      // TODO: 实现 API 调用
      return {
        totalPaths: 3,
        activePaths: 2,
        completedItems: 24,
        totalItems: 60,
        streak: 7
      }
    }
  })

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">欢迎回来</h1>
          <p className="text-gray-500 mt-1">继续你的 AI 学习之旅</p>
        </div>
        <Link
          href="/paths/new"
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-5 w-5" />
          新建学习路径
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={Target}
          label="学习路径"
          value={stats?.totalPaths || 0}
          color="blue"
        />
        <StatCard
          icon={Clock}
          label="进行中"
          value={stats?.activePaths || 0}
          color="green"
        />
        <StatCard
          icon={TrendingUp}
          label="完成进度"
          value={`${Math.round((stats?.completedItems || 0) / (stats?.totalItems || 1) * 100)}%`}
          color="purple"
        />
        <StatCard
          icon={Target}
          label="连续学习"
          value={`${stats?.streak || 0} 天`}
          color="orange"
        />
      </div>

      {/* Recent Paths */}
      <div className="bg-white rounded-xl shadow-sm border p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">最近的学习路径</h2>
        <div className="space-y-4">
          <PathCard
            name="机器学习入门"
            progress={45}
            totalDuration="12 周"
            currentPhase="第二阶段：监督学习"
          />
          <PathCard
            name="深度学习进阶"
            progress={20}
            totalDuration="8 周"
            currentPhase="第一阶段：神经网络基础"
          />
          <PathCard
            name="LLM 应用开发"
            progress={0}
            totalDuration="6 周"
            currentPhase="未开始"
          />
        </div>
      </div>
    </div>
  )
}

function StatCard({ icon: Icon, label, value, color }: {
  icon: any
  label: string
  value: string | number
  color: string
}) {
  const colors: Record<string, string> = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600',
    orange: 'bg-orange-100 text-orange-600',
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{label}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
        <div className={`${colors[color]} p-3 rounded-lg`}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </div>
  )
}

function PathCard({ name, progress, totalDuration, currentPhase }: {
  name: string
  progress: number
  totalDuration: string
  currentPhase: string
}) {
  return (
    <Link href={`/paths/1`} className="block">
      <div className="border rounded-lg p-4 hover:shadow-md transition-shadow">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-medium text-gray-900">{name}</h3>
          <span className="text-sm text-gray-500">{totalDuration}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-500">{currentPhase}</span>
          <span className="text-blue-600">{progress}% 完成</span>
        </div>
      </div>
    </Link>
  )
}
