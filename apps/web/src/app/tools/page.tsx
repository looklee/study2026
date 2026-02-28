'use client'

import { useState } from 'react'
import { Search, ExternalLink, Star, Heart, Grid, List } from 'lucide-react'
import { aiToolsDatabase, categories } from '@/lib/ai-tools-database'
import type { AITool } from '@/lib/ai-tools-database'

export default function AIToolsPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [showFreeOnly, setShowFreeOnly] = useState(false)
  const [showChineseOnly, setShowChineseOnly] = useState(false)
  const [sortBy, setSortBy] = useState<'popularity' | 'rating'>('popularity')
  const [favorites, setFavorites] = useState<string[]>([])

  // 过滤和排序工具
  const filteredTools = aiToolsDatabase.filter(tool => {
    if (selectedCategory !== 'all' && tool.category !== selectedCategory) return false
    if (searchQuery && !tool.name.toLowerCase().includes(searchQuery.toLowerCase()) && 
        !tool.description.toLowerCase().includes(searchQuery.toLowerCase()) &&
        !tool.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))) return false
    if (showFreeOnly && tool.pricing === '付费') return false
    if (showChineseOnly && !tool.chinese) return false
    return true
  }).sort((a, b) => {
    if (sortBy === 'popularity') return b.popularity - a.popularity
    if (sortBy === 'rating') return b.rating - a.rating
    return 0
  })

  const toggleFavorite = (id: string) => {
    setFavorites(prev => 
      prev.includes(id) ? prev.filter(f => f !== id) : [...prev, id]
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">🤖 AI 工具集</h1>
        <p className="text-gray-600">收录 {aiToolsDatabase.length}+ 个 AI 工具，发现最适合你的 AI 助手</p>
      </div>

      {/* 搜索栏 */}
      <div className="relative max-w-3xl mx-auto">
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
        <input
          type="text"
          placeholder="搜索 AI 工具、功能或标签..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
        />
      </div>

      {/* 分类筛选 */}
      <div className="flex flex-wrap gap-2">
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
            {category.icon} {category.name}
          </button>
        ))}
      </div>

      {/* 高级筛选 */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-white p-4 rounded-xl border">
        <div className="flex flex-wrap items-center gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showFreeOnly}
              onChange={(e) => setShowFreeOnly(e.target.checked)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-sm font-medium">免费工具</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showChineseOnly}
              onChange={(e) => setShowChineseOnly(e.target.checked)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-sm font-medium">中文工具</span>
          </label>
        </div>

        <div className="flex items-center gap-4">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="popularity">🔥 热度排序</option>
            <option value="rating">⭐ 评分排序</option>
          </select>

          <div className="flex items-center gap-2 border rounded-lg p-1">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 rounded ${viewMode === 'grid' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'}`}
            >
              <Grid className="h-4 w-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded ${viewMode === 'list' ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-100'}`}
            >
              <List className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* 结果统计 */}
      <div className="text-sm text-gray-600">
        找到 <span className="font-semibold text-blue-600">{filteredTools.length}</span> 个工具
      </div>

      {/* 工具列表 */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredTools.map((tool) => (
            <ToolCard 
              key={tool.id} 
              tool={tool} 
              isFavorite={favorites.includes(tool.id)}
              onToggleFavorite={() => toggleFavorite(tool.id)}
            />
          ))}
        </div>
      ) : (
        <div className="space-y-4">
          {filteredTools.map((tool) => (
            <ToolCard 
              key={tool.id} 
              tool={tool} 
              viewMode="list"
              isFavorite={favorites.includes(tool.id)}
              onToggleFavorite={() => toggleFavorite(tool.id)}
            />
          ))}
        </div>
      )}
    </div>
  )
}

function ToolCard({ tool, viewMode = 'grid', isFavorite, onToggleFavorite }: { 
  tool: AITool
  viewMode?: 'grid' | 'list'
  isFavorite: boolean
  onToggleFavorite: () => void
}) {
  const colorClasses: Record<string, string> = {
    green: 'from-green-500 to-emerald-600',
    blue: 'from-blue-500 to-cyan-600',
    purple: 'from-purple-500 to-pink-600',
    orange: 'from-orange-500 to-red-600',
    pink: 'from-pink-500 to-rose-600',
    gray: 'from-gray-500 to-slate-600',
    yellow: 'from-yellow-500 to-orange-600',
    indigo: 'from-indigo-500 to-blue-600',
    cyan: 'from-cyan-500 to-blue-600',
    red: 'from-red-500 to-pink-600',
    black: 'from-gray-800 to-black'
  }

  if (viewMode === 'list') {
    return (
      <div className="bg-white rounded-xl border p-6 hover:shadow-lg transition-all">
        <div className="flex items-start gap-4">
          <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${colorClasses[tool.color]} flex items-center justify-center text-3xl flex-shrink-0`}>
            {tool.icon}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h3 className="text-xl font-bold text-gray-900">{tool.name}</h3>
                <p className="text-gray-600 mt-1 line-clamp-2">{tool.description}</p>
              </div>
              <a
                href={tool.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                访问官网
                <ExternalLink className="h-4 w-4" />
              </a>
            </div>
            <div className="flex items-center gap-4 mt-3 flex-wrap">
              <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
                {tool.category}
              </span>
              <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">
                {tool.pricing}
              </span>
              {tool.chinese && (
                <span className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">
                  中文
                </span>
              )}
              <div className="flex items-center gap-1 text-yellow-500">
                <Star className="h-4 w-4 fill-yellow-500" />
                <span className="font-medium">{tool.rating}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl border p-5 hover:shadow-xl hover:-translate-y-1 transition-all group">
      <div className="flex items-start justify-between mb-3">
        <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${colorClasses[tool.color]} flex items-center justify-center text-2xl`}>
          {tool.icon}
        </div>
        <button
          onClick={onToggleFavorite}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <Heart className={`h-5 w-5 ${isFavorite ? 'fill-red-500 text-red-500' : 'text-gray-400'}`} />
        </button>
      </div>

      <h3 className="font-bold text-gray-900 mb-2 line-clamp-1">{tool.name}</h3>
      <p className="text-sm text-gray-600 mb-3 line-clamp-2">{tool.description}</p>

      <div className="flex flex-wrap gap-1 mb-3">
        {tool.tags.slice(0, 3).map((tag: string, i: number) => (
          <span key={i} className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
            #{tag}
          </span>
        ))}
      </div>

      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
            {tool.category}
          </span>
          <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">
            {tool.pricing}
          </span>
        </div>
        <div className="flex items-center gap-1 text-yellow-500">
          <Star className="h-4 w-4 fill-yellow-500" />
          <span className="text-sm font-medium">{tool.rating}</span>
        </div>
      </div>

      <a
        href={tool.url}
        target="_blank"
        rel="noopener noreferrer"
        className="block w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white text-center py-2.5 rounded-lg hover:from-blue-700 hover:to-blue-800 transition-all font-medium flex items-center justify-center gap-2"
      >
        访问官网
        <ExternalLink className="h-4 w-4" />
      </a>

      {tool.chinese && (
        <div className="mt-2 text-center">
          <span className="text-xs text-red-600 font-medium">🇨🇳 支持中文</span>
        </div>
      )}
    </div>
  )
}
