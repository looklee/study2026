'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  BookOpen,
  MessageSquare,
  BarChart3,
  Sparkles,
  Video,
  Plug,
  Lightbulb,
  Library,
  Workflow,
  Home,
  Settings,
  LogOut,
  Calendar,
  Heart
} from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

const navigation = [
  { name: '首页', href: '/', icon: Home },
  { name: '仪表板', href: '/dashboard', icon: BarChart3 },
  { name: '学习路径', href: '/paths', icon: BookOpen },
  { name: 'AI 导师', href: '/chat', icon: MessageSquare },
  { name: 'OpenClaw 助手', href: '/openclaw', icon: Sparkles },
  { name: 'AI 创作', href: '/multimedia', icon: Sparkles },
  { name: '学习进度', href: '/progress', icon: BarChart3 },
  { name: '每日签到', href: '/checkin', icon: Calendar },
  { name: '学习伴侣', href: '/pet', icon: Heart },
  { name: 'AI 工具库', href: '/tools', icon: Sparkles },
  { name: '学习资源', href: '/resources', icon: Video },
  { name: 'API 集成', href: '/integrations', icon: Plug },
  { name: '内容推荐', href: '/recommendations', icon: Lightbulb },
  { name: '知识库', href: '/knowledge', icon: Library },
  { name: '工作流', href: '/workflows', icon: Workflow },
]

const features = [
  { name: '每日签到', href: '/checkin', icon: Calendar, color: 'from-purple-500 to-pink-500' },
  { name: '学习伴侣', href: '/pet', icon: Heart, color: 'from-red-500 to-orange-500' },
]

export function Sidebar() {
  const pathname = usePathname()
  const { user, logout } = useAuth()

  return (
    <div className="fixed inset-y-0 left-0 w-64 bg-gray-900 text-white flex flex-col">
      {/* Logo */}
      <div className="flex h-16 items-center px-6 border-b border-gray-800">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-2xl">🎯</span>
          <h1 className="text-xl font-bold">Study2026</h1>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4 px-3">
        <div className="space-y-1">
          {navigation.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`group flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`}
              >
                <item.icon className={`h-5 w-5 ${isActive ? 'text-white' : 'text-gray-400 group-hover:text-white'}`} />
                {item.name}
              </Link>
            )
          })}
        </div>

        {/* 分隔线 */}
        <div className="mt-8 pt-4 border-t border-gray-800">
          <p className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
            设置
          </p>
          <div className="mt-2 space-y-1">
            <Link
              href="/profile"
              className={`group flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                pathname === '/profile'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <Settings className="h-5 w-5 text-gray-400 group-hover:text-white" />
              个人设置
            </Link>
          </div>
        </div>
      </nav>

      {/* 特色功能卡片 */}
      <div className="px-3 pb-4">
        <div className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl p-3 text-center">
          <p className="text-xs font-bold text-white mb-2">✨ 新功能</p>
          <div className="grid grid-cols-2 gap-2">
            {features.map((feature) => (
              <Link
                key={feature.name}
                href={feature.href}
                className={`bg-white/20 hover:bg-white/30 rounded-lg p-2 transition-colors`}
              >
                <feature.icon className="h-5 w-5 text-white mx-auto mb-1" />
                <p className="text-xs text-white">{feature.name}</p>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* User Profile */}
      <div className="border-t border-gray-800 p-4">
        {user ? (
          <>
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                {user.username?.[0] || 'U'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">{user.username}</p>
                <p className="text-xs text-gray-400 truncate">{user.user_id}</p>
              </div>
            </div>
            <button
              onClick={logout}
              className="w-full flex items-center justify-center gap-2 px-3 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-sm"
            >
              <LogOut className="h-4 w-4" />
              切换设备
            </button>
          </>
        ) : (
          <div className="text-center text-gray-400 text-sm">
            识别中...
          </div>
        )}
      </div>
    </div>
  )
}
