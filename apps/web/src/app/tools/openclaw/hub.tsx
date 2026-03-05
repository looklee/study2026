import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Brain, Sparkles, Zap, MessageSquare, Code, BookOpen } from 'lucide-react'

export default function OpenClawToolHub() {
  const features = [
    {
      title: "AI 对话",
      description: "与OpenClaw AI助手进行智能对话",
      icon: MessageSquare,
      link: "/openclaw",
      color: "from-blue-500 to-purple-600"
    },
    {
      title: "代码助手",
      description: "获得AI代码编写帮助",
      icon: Code,
      link: "/openclaw",
      color: "from-gray-600 to-purple-700"
    },
    {
      title: "学习助手",
      description: "个性化学习指导",
      icon: BookOpen,
      link: "/openclaw",
      color: "from-orange-500 to-red-600"
    },
    {
      title: "内容生成",
      description: "AI内容创作助手",
      icon: Sparkles,
      link: "/openclaw",
      color: "from-pink-500 to-rose-600"
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-12">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-3 bg-gradient-to-r from-red-500 to-orange-500 text-white px-6 py-3 rounded-full mb-4">
            <span className="text-2xl">🦞</span>
            <h1 className="text-4xl font-bold">OpenClaw AI 助手</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            您的个人AI助手，支持多模型和技能扩展，提供智能化的学习和工作效率提升
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {features.map((feature, index) => (
            <Card key={index} className="hover:shadow-xl transition-all duration-300 hover:-translate-y-1 overflow-hidden">
              <div className={`h-2 bg-gradient-to-r ${feature.color}`}></div>
              <CardHeader>
                <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${feature.color} flex items-center justify-center text-white mb-4`}>
                  <feature.icon className="h-6 w-6" />
                </div>
                <CardTitle>{feature.title}</CardTitle>
                <CardDescription>{feature.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <Link href={feature.link}>
                  <Button className={`w-full bg-gradient-to-r ${feature.color} hover:from-blue-600 hover:to-purple-700 text-white`}>
                    立即体验
                  </Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-8 mb-12">
          <h2 className="text-2xl font-bold text-center mb-6">为什么选择 OpenClaw AI 助手?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">智能高效</h3>
              <p className="text-gray-600">基于先进的AI模型，提供快速准确的响应和解决方案</p>
            </div>
            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Brain className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">个性化学习</h3>
              <p className="text-gray-600">根据您的需求和偏好，提供定制化的学习和工作建议</p>
            </div>
            <div className="text-center">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Sparkles className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">持续进化</h3>
              <p className="text-gray-600">不断学习和改进，提供越来越智能的服务体验</p>
            </div>
          </div>
        </div>

        <div className="text-center">
          <Link href="/openclaw">
            <Button size="lg" className="bg-gradient-to-r from-red-500 to-orange-500 hover:from-red-600 hover:to-orange-600 text-white px-8 py-6 text-lg">
              开始使用 OpenClaw AI 助手
            </Button>
          </Link>
          <p className="text-gray-500 mt-4">立即体验智能AI助手的强大功能</p>
        </div>
      </div>
    </div>
  )
}