'use client'

import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { 
  TrendingUp, Award, Calendar, Clock, Target, Activity, 
  Flame, BookOpen, CheckCircle, Star, Zap, Trophy
} from 'lucide-react'

export default function ProgressPage() {
  const [selectedPath, setSelectedPath] = useState<string>('all')
  const userId = 'demo_user'

  // 获取统计信息
  const { data: stats } = useQuery({
    queryKey: ['progress-stats', userId],
    queryFn: async () => {
      const response = await fetch(`http://localhost:8001/api/v1/progress/stats/${userId}`)
      return response.json()
    },
    refetchInterval: 5000
  })

  // 获取进度详情
  const { data: progress } = useQuery({
    queryKey: ['progress-detail', userId, selectedPath],
    queryFn: async () => {
      const url = selectedPath !== 'all'
        ? `http://localhost:8001/api/v1/progress/${userId}?path_id=${selectedPath}`
        : `http://localhost:8001/api/v1/progress/${userId}`
      const response = await fetch(url)
      return response.json()
    }
  })

  // 获取成就
  const { data: achievements } = useQuery({
    queryKey: ['achievements', userId],
    queryFn: async () => {
      const response = await fetch(`http://localhost:8001/api/v1/progress/${userId}/achievements`)
      return response.json()
    }
  })

  // 获取时间线
  const { data: timeline } = useQuery({
    queryKey: ['timeline', userId],
    queryFn: async () => {
      const response = await fetch(`http://localhost:8001/api/v1/progress/${userId}/timeline?days=7`)
      return response.json()
    }
  })

  // 模拟学习路径
  const learningPaths = [
    { id: '1', name: '机器学习入门', progress: 45 },
    { id: '2', name: '深度学习进阶', progress: 20 },
    { id: '3', name: 'LLM 应用开发', progress: 0 }
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">📈 学习进度</h1>
        <p className="text-gray-600 mt-1">追踪你的学习旅程，见证每一步成长</p>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          label="总体进度"
          value={`${stats?.stats?.overallProgress || 0}%`}
          icon={<TrendingUp className="h-6 w-6" />}
          color="blue"
          trend="+5% 本周"
        />
        <StatCard
          label="已完成项目"
          value={stats?.stats?.totalItemsCompleted || 0}
          icon={<CheckCircle className="h-6 w-6" />}
          color="green"
          trend={`${stats?.stats?.totalItemsCompleted || 0} 个成就`}
        />
        <StatCard
          label="连续学习"
          value={`${stats?.stats?.studyStreak || 0} 天`}
          icon={<Flame className="h-6 w-6" />}
          color="orange"
          trend={`历史最长：${stats?.stats?.longestStreak || 0} 天`}
        />
        <StatCard
          label="学习时长"
          value={`${stats?.stats?.totalStudyTime || 0} 小时`}
          icon={<Clock className="h-6 w-6" />}
          color="purple"
          trend={`经验值：${stats?.stats?.experiencePoints || 0}`}
        />
      </div>

      {/* 成就进度 */}
      <div className="bg-gradient-to-r from-yellow-500 to-orange-500 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold flex items-center gap-2">
              <Award className="h-6 w-6" />
              成就系统
            </h2>
            <p className="text-white/80 mt-1">
              已解锁 {achievements?.unlocked_ids?.length || 0} / {achievements?.achievements?.length || 0} 个成就
            </p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold">
              {Math.round(((achievements?.unlocked_ids?.length || 0) / (achievements?.achievements?.length || 1)) * 100)}%
            </div>
            <div className="text-sm text-white/80">完成度</div>
          </div>
        </div>
        <div className="mt-4 bg-white/20 rounded-full h-3">
          <div 
            className="bg-white h-3 rounded-full transition-all"
            style={{ 
              width: `${((achievements?.unlocked_ids?.length || 0) / (achievements?.achievements?.length || 1)) * 100}%` 
            }}
          />
        </div>
      </div>

      {/* 学习路径选择 */}
      <div className="flex flex-wrap gap-3">
        <button
          onClick={() => setSelectedPath('all')}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
            selectedPath === 'all'
              ? 'bg-blue-600 text-white shadow-lg scale-105'
              : 'bg-white border hover:bg-gray-50'
          }`}
        >
          全部路径
        </button>
        {learningPaths.map((path) => (
          <button
            key={path.id}
            onClick={() => setSelectedPath(path.id)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              selectedPath === path.id
                ? 'bg-blue-600 text-white shadow-lg scale-105'
                : 'bg-white border hover:bg-gray-50'
            }`}
          >
            {path.name}
          </button>
        ))}
      </div>

      {/* 进度详情 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 进度分析 */}
        <div className="bg-white rounded-xl border p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Activity className="h-5 w-5 text-blue-600" />
            进度分析
          </h3>
          <div className="space-y-4">
            <ProgressBar
              label="总体进度"
              value={progress?.progress?.overall || 0}
              total={100}
              color="blue"
            />
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">已完成</p>
                <p className="text-2xl font-bold text-green-600">
                  {progress?.progress?.completedItems || 0}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">总项目</p>
                <p className="text-2xl font-bold text-gray-900">
                  {progress?.progress?.totalItems || 0}
                </p>
              </div>
            </div>
            <div className="pt-4 border-t">
              <p className="text-sm text-gray-500">按类型分布</p>
              <div className="mt-2 space-y-2">
                {Object.entries(progress?.progress?.byType || {}).map(([type, data]: [string, any]) => (
                  <div key={type} className="flex items-center justify-between text-sm">
                    <span className="text-gray-600 capitalize">{type}</span>
                    <span className="text-gray-900 font-medium">
                      {data.completed}/{data.total}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* 学习统计 */}
        <div className="bg-white rounded-xl border p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-purple-600" />
            学习统计
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-500">开始日期</span>
              <span className="text-gray-900 font-medium">
                {progress?.statistics?.startDate ? new Date(progress.statistics.startDate).toLocaleDateString('zh-CN') : '-'}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-500">学习天数</span>
              <span className="text-gray-900 font-medium">
                {progress?.statistics?.totalDays || 0} 天
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-500">平均每周</span>
              <span className="text-gray-900 font-medium">
                {progress?.statistics?.averagePerWeek || 0} 项
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-500">总学习时长</span>
              <span className="text-gray-900 font-medium">
                {progress?.statistics?.totalTimeMinutes ? Math.round(progress.statistics.totalTimeMinutes / 60) : 0} 小时
              </span>
            </div>
            <div className="flex items-center justify-between pt-4 border-t">
              <span className="text-gray-500">预计完成</span>
              <span className="text-blue-600 font-medium">
                {progress?.statistics?.estimatedCompletionDate 
                  ? new Date(progress.statistics.estimatedCompletionDate).toLocaleDateString('zh-CN')
                  : '计算中...'
                }
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* 成就展示 */}
      <div className="bg-white rounded-xl border p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Trophy className="h-5 w-5 text-yellow-600" />
          成就徽章
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {achievements?.achievements?.map((achievement: any) => (
            <AchievementCard key={achievement.id} achievement={achievement} />
          ))}
        </div>
      </div>

      {/* 活动时间线 */}
      <div className="bg-white rounded-xl border p-6">
        <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Calendar className="h-5 w-5 text-green-600" />
          最近活动
        </h3>
        <div className="space-y-3">
          {timeline?.timeline?.slice(0, 7).map((day: any) => (
            <TimelineItem key={day.date} day={day} />
          ))}
          {!timeline?.timeline || timeline.timeline.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              暂无活动记录，开始学习吧！
            </div>
          ) : null}
        </div>
      </div>
    </div>
  )
}

function StatCard({ label, value, icon, color, trend }: { 
  label: string; 
  value: string | number; 
  icon: any; 
  color: string;
  trend?: string;
}) {
  const colors: Record<string, string> = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    orange: 'bg-orange-100 text-orange-600',
    purple: 'bg-purple-100 text-purple-600'
  }

  return (
    <div className="bg-white rounded-xl border p-4">
      <div className="flex items-center justify-between mb-2">
        <div className={`${colors[color]} p-2.5 rounded-lg`}>
          {icon}
        </div>
        {trend && <span className="text-xs text-green-600 font-medium">{trend}</span>}
      </div>
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
    </div>
  )
}

function ProgressBar({ label, value, total, color }: { 
  label: string; 
  value: number; 
  total: number; 
  color: string;
}) {
  const percentage = Math.min(100, Math.round((value / total) * 100))
  
  const colors: Record<string, string> = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    purple: 'bg-purple-500'
  }

  return (
    <div>
      <div className="flex items-center justify-between text-sm mb-1">
        <span className="text-gray-600">{label}</span>
        <span className="text-gray-900 font-medium">{percentage}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div
          className={`${colors[color]} h-2.5 rounded-full transition-all duration-500`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

function AchievementCard({ achievement }: { achievement: any }) {
  return (
    <div className={`text-center p-4 rounded-xl border-2 transition-all ${
      achievement.unlocked
        ? 'border-yellow-200 bg-yellow-50'
        : 'border-gray-200 bg-gray-50 opacity-50'
    }`}>
      <div className="text-4xl mb-2">{achievement.icon}</div>
      <p className="text-sm font-bold text-gray-900">{achievement.name}</p>
      <p className="text-xs text-gray-500 mt-1">{achievement.description}</p>
      {achievement.unlocked && (
        <div className="mt-2 flex items-center justify-center gap-1 text-xs text-green-600">
          <CheckCircle className="h-3 w-3" />
          已解锁
        </div>
      )}
    </div>
  )
}

function TimelineItem({ day }: { day: any }) {
  return (
    <div className="flex items-start gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
      <div className="bg-blue-100 p-2 rounded-lg">
        <Activity className="h-5 w-5 text-blue-600" />
      </div>
      <div className="flex-1">
        <div className="flex items-center justify-between">
          <p className="font-medium text-gray-900">
            {new Date(day.date).toLocaleDateString('zh-CN', { 
              month: 'long', 
              day: 'numeric',
              weekday: 'short'
            })}
          </p>
          <span className="text-sm text-gray-500">
            {day.items_completed} 项完成
          </span>
        </div>
        <div className="flex items-center gap-4 mt-1 text-sm text-gray-500">
          <span className="flex items-center gap-1">
            <Clock className="h-3 w-3" />
            {Math.round(day.time_spent)} 分钟
          </span>
          <span className="flex items-center gap-1">
            <CheckCircle className="h-3 w-3" />
            {day.activities.length} 个活动
          </span>
        </div>
      </div>
    </div>
  )
}
