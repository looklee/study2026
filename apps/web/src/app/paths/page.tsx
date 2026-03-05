'use client'

import { useQuery } from '@tanstack/react-query'
import { Plus, BookOpen, Clock, TrendingUp, ArrowRight } from 'lucide-react'
import Link from 'next/link'
import { pathsApi } from '@/lib/api'

export default function PathsPage() {
  const { data: paths, isLoading } = useQuery({
    queryKey: ['paths'],
    queryFn: async () => {
      // 调用真实 API 获取学习路径
      const response = await fetch('/api/v1/paths');
      if (!response.ok) {
        throw new Error('Failed to fetch paths');
      }
      return response.json();
    }
  })

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">学习路径</h1>
          <p className="text-gray-500 mt-1">管理你的学习计划</p>
        </div>
        <Link
          href="/paths/new"
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="h-5 w-5" />
          新建路径
        </Link>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          icon={BookOpen}
          label="总路径数"
          value={paths?.length || 0}
          color="blue"
        />
        <StatCard
          icon={Clock}
          label="进行中"
          value={paths?.filter(p => p.status === 'active').length || 0}
          color="green"
        />
        <StatCard
          icon={TrendingUp}
          label="已完成"
          value={paths?.filter(p => p.progress === 100).length || 0}
          color="purple"
        />
      </div>

      {/* Paths List */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="text-gray-500 mt-4">加载中...</p>
          </div>
        ) : (
          paths?.map((path) => (
            <PathCard key={path.id} path={path} />
          ))
        )}
      </div>
    </div>
  )
}

function StatCard({ icon: Icon, label, value, color }: {
  icon: any
  label: string
  value: number
  color: string
}) {
  const colors: Record<string, string> = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600',
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

function PathCard({ path }: { path: any }) {
  const statusColors: Record<string, string> = {
    active: 'bg-green-100 text-green-700',
    not_started: 'bg-gray-100 text-gray-700',
    completed: 'bg-blue-100 text-blue-700',
  }

  const statusText: Record<string, string> = {
    active: '进行中',
    not_started: '未开始',
    completed: '已完成',
  }

  return (
    <Link
      href={`/paths/${path.id}`}
      className="block bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow"
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{path.path_name}</h3>
          <p className="text-gray-500 text-sm mt-1">{path.description}</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[path.status]}`}>
          {statusText[path.status]}
        </span>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between text-sm mb-2">
          <span className="text-gray-500">进度</span>
          <span className="text-gray-900 font-medium">{path.progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all"
            style={{ width: `${path.progress}%` }}
          />
        </div>
      </div>

      {/* Phases */}
      <div className="flex items-center gap-2 mb-4">
        {path.phases?.map((phase: any, idx: number) => (
          <div key={idx} className="flex items-center">
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium ${
                phase.status === 'completed'
                  ? 'bg-green-500 text-white'
                  : phase.status === 'in_progress'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-500'
              }`}
            >
              {idx + 1}
            </div>
            {idx < path.phases.length - 1 && (
              <div
                className={`w-8 h-0.5 ${
                  phase.status === 'completed' ? 'bg-green-500' : 'bg-gray-200'
                }`}
              />
            )}
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4 text-sm text-gray-500">
          <span className="flex items-center gap-1">
            <Clock className="h-4 w-4" />
            {path.total_duration}
          </span>
          <span className="flex items-center gap-1">
            <BookOpen className="h-4 w-4" />
            {path.phases?.length || 0} 个阶段
          </span>
        </div>
        <ArrowRight className="h-5 w-5 text-gray-400" />
      </div>
    </Link>
  )
}
