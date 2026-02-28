'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Star, GitBranch, ExternalLink, Github, TrendingUp, Filter, Search } from 'lucide-react'
import { githubProjects, projectStats, projectTags, topProjects } from '@/lib/github-projects'

export default function RecommendationsPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [showAiOnly, setShowAiOnly] = useState(false)

  const categories = [
    { id: 'all', name: '全部', count: githubProjects.length },
    { id: 'AI/LLM', name: 'AI/LLM', count: projectStats.byCategory['AI/LLM'] },
    { id: '开发工具', name: '开发工具', count: projectStats.byCategory['开发工具'] },
    { id: '效率工具', name: '效率工具', count: projectStats.byCategory['效率工具'] },
    { id: '系统工具', name: '系统工具', count: projectStats.byCategory['系统工具'] }
  ]

  const filteredProjects = githubProjects.filter(project => {
    if (selectedCategory !== 'all' && project.category !== selectedCategory) return false
    if (searchQuery && !project.name.toLowerCase().includes(searchQuery.toLowerCase()) && 
        !project.description.toLowerCase().includes(searchQuery.toLowerCase()) &&
        !project.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))) return false
    if (showAiOnly && !project.aiRelated) return false
    return true
  })

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">🔥 GitHub 热门开源项目</h1>
        <p className="text-gray-600 mt-1">收录 {githubProjects.length} 个近期最火的开源项目，总计 {projectStats.totalStars.toLocaleString()}+ ⭐</p>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard label="总项目数" value={projectStats.total} icon="📦" color="blue" />
        <StatCard label="AI 相关" value={projectStats.aiRelated} icon="🤖" color="purple" />
        <StatCard label="总 Star 数" value={`${(projectStats.totalStars / 1000).toFixed(0)}k`} icon="⭐" color="yellow" />
        <StatCard label=" trending" value={githubProjects.filter(p => p.trending).length} icon="🔥" color="red" />
      </div>

      {/* 搜索栏 */}
      <div className="relative max-w-2xl mx-auto">
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
        <input
          type="text"
          placeholder="搜索项目、标签或描述..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-12 pr-4 py-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* 热门标签 */}
      <div className="flex flex-wrap gap-2">
        {projectTags.map((tag) => (
          <button
            key={tag}
            onClick={() => setSearchQuery(tag)}
            className="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition-colors"
          >
            #{tag}
          </button>
        ))}
      </div>

      {/* 分类筛选 */}
      <div className="flex flex-wrap gap-3">
        {categories.map((category) => (
          <button
            key={category.id}
            onClick={() => setSelectedCategory(category.id)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              selectedCategory === category.id
                ? 'bg-blue-600 text-white shadow-lg scale-105'
                : 'bg-white border hover:bg-gray-50'
            }`}
          >
            {category.name} ({category.count})
          </button>
        ))}
      </div>

      {/* 高级筛选 */}
      <div className="flex items-center gap-4 bg-white p-4 rounded-xl border">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={showAiOnly}
            onChange={(e) => setShowAiOnly(e.target.checked)}
            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <span className="text-sm font-medium">仅看 AI 相关</span>
        </label>
      </div>

      {/* Top 10 项目 */}
      {selectedCategory === 'all' && !searchQuery && (
        <div>
          <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="h-6 w-6 text-red-500" />
            Top 10 热门项目
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
            {topProjects.map((project, index) => (
              <ProjectCard key={project.id} project={project} rank={index + 1} />
            ))}
          </div>
        </div>
      )}

      {/* 全部项目 */}
      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          {selectedCategory === 'all' ? '全部项目' : selectedCategory}
          <span className="ml-2 text-sm font-normal text-gray-500">({filteredProjects.length} 个)</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProjects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      </div>
    </div>
  )
}

function StatCard({ label, value, icon, color }: { label: string; value: string | number; icon: string; color: string }) {
  const colors: Record<string, string> = {
    blue: 'bg-blue-100 text-blue-600',
    purple: 'bg-purple-100 text-purple-600',
    yellow: 'bg-yellow-100 text-yellow-600',
    red: 'bg-red-100 text-red-600'
  }

  return (
    <div className="bg-white rounded-xl border p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{label}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
        <div className={`${colors[color]} w-12 h-12 rounded-lg flex items-center justify-center text-2xl`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

function ProjectCard({ project, rank }: { project: any; rank?: number }) {
  return (
    <div className="bg-white rounded-xl border p-5 hover:shadow-lg hover:-translate-y-1 transition-all group">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-start gap-3 flex-1">
          {rank && (
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm ${
              rank === 1 ? 'bg-yellow-500' : rank === 2 ? 'bg-gray-400' : rank === 3 ? 'bg-amber-600' : 'bg-gray-300'
            }`}>
              {rank}
            </div>
          )}
          <div className="flex-1">
            <a
              href={project.url}
              target="_blank"
              rel="noopener noreferrer"
              className="font-bold text-gray-900 hover:text-blue-600 transition-colors flex items-center gap-2"
            >
              {project.name}
              <ExternalLink className="h-4 w-4 text-gray-400 group-hover:text-blue-500" />
            </a>
            <p className="text-sm text-gray-500 mt-1">{project.repo}</p>
          </div>
        </div>
        <a
          href={project.url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1 text-gray-600 hover:text-yellow-500 transition-colors"
        >
          <Star className="h-4 w-4" />
          <span className="text-sm font-medium">{(project.stars / 1000).toFixed(1)}k</span>
        </a>
      </div>

      <p className="text-sm text-gray-600 mb-4 line-clamp-2">{project.description}</p>

      <div className="flex flex-wrap gap-1.5 mb-4">
        {project.tags.slice(0, 3).map((tag: string, i: number) => (
          <span key={i} className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
            #{tag}
          </span>
        ))}
      </div>

      <div className="flex items-center justify-between pt-4 border-t">
        <div className="flex items-center gap-3 text-sm text-gray-500">
          <span className="flex items-center gap-1">
            <GitBranch className="h-4 w-4" />
            {project.language}
          </span>
          <span className={`px-2 py-1 rounded text-xs font-medium ${
            project.category === 'AI/LLM' ? 'bg-purple-100 text-purple-700' :
            project.category === '开发工具' ? 'bg-blue-100 text-blue-700' :
            project.category === '效率工具' ? 'bg-green-100 text-green-700' :
            'bg-gray-100 text-gray-700'
          }`}>
            {project.category}
          </span>
        </div>
        {project.aiRelated && (
          <span className="text-xs px-2 py-1 bg-purple-100 text-purple-700 rounded font-medium">
            🤖 AI
          </span>
        )}
      </div>
    </div>
  )
}
