'use client'

import { useParams, useRouter } from 'next/navigation'
import { useQuery, useMutation } from '@tanstack/react-query'
import { ArrowLeft, CheckCircle, Circle, Play, BookOpen, Clock, Target, Award } from 'lucide-react'
import Link from 'next/link'
import { pathsApi, progressApi } from '@/lib/api'

export default function PathDetailPage() {
  const params = useParams()
  const router = useRouter()
  const pathId = parseInt(params.id as string)

  const { data: path, isLoading } = useQuery({
    queryKey: ['path', pathId],
    queryFn: async () => {
      // 模拟数据
      return {
        id: pathId,
        path_name: '机器学习入门',
        description: '从零开始掌握机器学习基础，能够独立完成 ML 项目',
        target_goal: '掌握机器学习基础',
        total_duration: '12 周',
        progress: 45,
        status: 'active',
        created_at: '2026-01-01',
        path_data: {
          pathName: '机器学习入门',
          description: '从零开始掌握机器学习',
          totalDuration: '12 周',
          phases: [
            {
              phaseNumber: 1,
              phaseName: 'Python 基础',
              duration: '2 周',
              objectives: ['掌握 Python 语法', '熟悉 NumPy 和 Pandas'],
              topics: ['变量和数据类型', '函数和类', 'NumPy 数组', 'Pandas DataFrame'],
              milestone: '完成数据分析小项目',
              status: 'completed'
            },
            {
              phaseNumber: 2,
              phaseName: '机器学习基础',
              duration: '4 周',
              objectives: ['理解 ML 基本概念', '掌握 sklearn 库'],
              topics: ['线性回归', '逻辑回归', '决策树', '随机森林'],
              milestone: '完成 Kaggle 入门比赛',
              status: 'in_progress'
            },
            {
              phaseNumber: 3,
              phaseName: '深度学习入门',
              duration: '4 周',
              objectives: ['理解神经网络', '掌握 PyTorch 基础'],
              topics: ['感知机', '反向传播', 'CNN', 'RNN'],
              milestone: '实现图像分类模型',
              status: 'pending'
            },
            {
              phaseNumber: 4,
              phaseName: '实战项目',
              duration: '2 周',
              objectives: ['完成综合项目'],
              topics: ['项目选题', '数据收集', '模型训练', '部署上线'],
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
    }
  })

  const completePhase = useMutation({
    mutationFn: async (phaseNumber: number) => {
      return await progressApi.track({
        userId: 1,
        pathId: pathId,
        action: 'complete',
        itemType: 'phase',
        itemId: `phase_${phaseNumber}`
      })
    },
    onSuccess: () => {
      // 刷新数据
    }
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="text-gray-500 mt-4">加载中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => router.back()}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft className="h-6 w-6" />
        </button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold text-gray-900">{path?.path_name}</h1>
          <p className="text-gray-500 mt-1">{path?.description}</p>
        </div>
      </div>

      {/* Progress Overview */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between mb-4">
          <div>
            <p className="text-blue-100">总进度</p>
            <p className="text-4xl font-bold mt-2">{path?.progress}%</p>
          </div>
          <Award className="h-20 w-20 text-blue-200" />
        </div>
        <div className="w-full bg-blue-800 rounded-full h-3">
          <div
            className="bg-white h-3 rounded-full transition-all"
            style={{ width: `${path?.progress}%` }}
          />
        </div>
        <div className="flex items-center justify-between mt-4 text-sm text-blue-100">
          <span className="flex items-center gap-2">
            <Clock className="h-4 w-4" />
            {path?.total_duration}
          </span>
          <span className="flex items-center gap-2">
            <Target className="h-4 w-4" />
            {path?.target_goal}
          </span>
        </div>
      </div>

      {/* Phases */}
      <div className="space-y-6">
        <h2 className="text-xl font-bold text-gray-900">学习阶段</h2>
        {path?.path_data?.phases?.map((phase: any, idx: number) => (
          <PhaseCard
            key={phase.phaseNumber}
            phase={phase}
            isCompleted={phase.status === 'completed'}
            isCurrent={phase.status === 'in_progress'}
            onComplete={() => completePhase.mutate(phase.phaseNumber)}
          />
        ))}
      </div>

      {/* Weekly Schedule */}
      <div className="bg-white rounded-xl shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <BookOpen className="h-5 w-5" />
          每周学习安排
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(path?.path_data?.weeklySchedule || {}).map(([day, schedule]: [string, any]) => (
            <div key={day} className="bg-gray-50 rounded-lg p-4">
              <p className="font-medium text-gray-900 capitalize">
                {day === 'monday' ? '周一' : day === 'wednesday' ? '周三' : '周末'}
              </p>
              <p className="text-gray-600 mt-1">{schedule}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Tips */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-yellow-900 mb-4">💡 学习建议</h3>
        <ul className="space-y-2">
          {path?.path_data?.tips?.map((tip: string, idx: number) => (
            <li key={idx} className="flex items-start gap-2 text-yellow-800">
              <span className="text-yellow-500 mt-1">•</span>
              {tip}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

function PhaseCard({ phase, isCompleted, isCurrent, onComplete }: {
  phase: any
  isCompleted: boolean
  isCurrent: boolean
  onComplete: () => void
}) {
  return (
    <div className={`bg-white rounded-xl shadow-sm border p-6 ${isCurrent ? 'border-blue-300 ring-2 ring-blue-100' : ''}`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-4">
          <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
            isCompleted ? 'bg-green-500 text-white' : isCurrent ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-500'
          }`}>
            {isCompleted ? <CheckCircle className="h-6 w-6" /> : <span className="text-lg font-bold">{phase.phaseNumber}</span>}
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{phase.phaseName}</h3>
            <p className="text-sm text-gray-500 mt-1">{phase.duration}</p>
          </div>
        </div>
        {isCurrent && (
          <button
            onClick={onComplete}
            disabled={isCompleted}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              isCompleted
                ? 'bg-green-100 text-green-700'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {isCompleted ? '已完成' : '标记完成'}
          </button>
        )}
      </div>

      {/* Objectives */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">学习目标</h4>
        <ul className="space-y-1">
          {phase.objectives?.map((obj: string, idx: number) => (
            <li key={idx} className="flex items-center gap-2 text-sm text-gray-600">
              <CheckCircle className={`h-4 w-4 ${isCompleted ? 'text-green-500' : 'text-gray-300'}`} />
              {obj}
            </li>
          ))}
        </ul>
      </div>

      {/* Topics */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">学习内容</h4>
        <div className="flex flex-wrap gap-2">
          {phase.topics?.map((topic: string, idx: number) => (
            <span
              key={idx}
              className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-medium"
            >
              {topic}
            </span>
          ))}
        </div>
      </div>

      {/* Milestone */}
      <div className="flex items-center gap-2 text-sm text-gray-600 bg-gray-50 rounded-lg p-3">
        <Award className="h-4 w-4 text-yellow-500" />
        <span>里程碑：{phase.milestone}</span>
      </div>
    </div>
  )
}
