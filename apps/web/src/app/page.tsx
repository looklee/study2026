'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ArrowRight, Sparkles, Zap, TrendingUp } from 'lucide-react'

export default function HomePage() {
  const router = useRouter()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    // 3 秒后自动跳转到仪表板
    const timer = setTimeout(() => {
      router.push('/dashboard')
    }, 5000)
    return () => clearTimeout(timer)
  }, [router])

  const features = [
    {
      icon: Sparkles,
      title: 'AI 学习路径',
      description: 'AI 驱动的个性化学习计划'
    },
    {
      icon: Zap,
      title: '智能导师',
      description: '24/7 在线答疑'
    },
    {
      icon: TrendingUp,
      title: '进度追踪',
      description: '可视化学习数据'
    }
  ]

  if (!mounted) return null

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center text-white mb-16">
          <h1 className="text-6xl font-bold mb-6 animate-pulse">
            🎯 Study2026
          </h1>
          <p className="text-2xl mb-8 text-white/90">
            AI 驱动的智能学习平台
          </p>
          <p className="text-lg mb-12 text-white/70">
            个性化学习路径 · 智能导师 · 进度追踪
          </p>

          <button
            onClick={() => router.push('/dashboard')}
            className="bg-white text-purple-600 px-8 py-4 rounded-full font-bold text-lg hover:bg-white/90 transition-all transform hover:scale-105 shadow-xl flex items-center gap-3 mx-auto"
          >
            开始学习
            <ArrowRight className="h-6 w-6" />
          </button>

          <p className="mt-4 text-sm text-white/50">
            将在 5 秒后自动跳转...
          </p>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {features.map((feature, idx) => (
            <div
              key={idx}
              className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 text-white hover:bg-white/20 transition-all"
            >
              <feature.icon className="h-12 w-12 mb-4" />
              <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
              <p className="text-white/80">{feature.description}</p>
            </div>
          ))}
        </div>

        {/* Stats */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto text-center text-white">
          <div>
            <p className="text-4xl font-bold mb-2">10+</p>
            <p className="text-white/70">AI 工具集成</p>
          </div>
          <div>
            <p className="text-4xl font-bold mb-2">100+</p>
            <p className="text-white/70">学习资源</p>
          </div>
          <div>
            <p className="text-4xl font-bold mb-2">24/7</p>
            <p className="text-white/70">AI 支持</p>
          </div>
          <div>
            <p className="text-4xl font-bold mb-2">∞</p>
            <p className="text-white/70">学习可能</p>
          </div>
        </div>
      </div>
    </div>
  )
}
