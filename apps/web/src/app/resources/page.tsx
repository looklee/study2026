'use client'

import { useState } from 'react'
import { Search, Play, Clock, User, Eye, Calendar, Star, Grid, List } from 'lucide-react'
import { bilibiliResources, categoryStats, popularTags } from '@/lib/bilibili-resources'

export default function ResourcesPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [showSeriesOnly, setShowSeriesOnly] = useState(false)

  const categories = [
    { id: 'all', name: '全部', count: bilibiliResources.length },
    { id: 'AI 基础', name: 'AI 基础', count: categoryStats['AI 基础'] },
    { id: 'Claude', name: 'Claude', count: categoryStats['Claude'] },
    { id: 'Agent', name: 'Agent', count: categoryStats['Agent'] },
    { id: '工作流', name: '工作流', count: categoryStats['工作流'] },
    { id: 'UP 主', name: 'UP 主推荐', count: categoryStats['UP 主'] }
  ]

  const filteredResources = bilibiliResources.filter(resource => {
    if (selectedCategory !== 'all' && resource.category !== selectedCategory) return false
    if (searchQuery && !resource.title.toLowerCase().includes(searchQuery.toLowerCase()) && 
        !resource.description.toLowerCase().includes(searchQuery.toLowerCase()) &&
        !resource.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))) return false
    if (showSeriesOnly && !resource.series) return false
    return true
  })

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">📺 B 站 AI 学习资源</h1>
        <p className="text-gray-600 mt-1">收录 {bilibiliResources.length}+ 个优质 AI 学习视频</p>
      </div>

      {/* 搜索栏 */}
      <div className="relative max-w-3xl mx-auto">
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
        <input
          type="text"
          placeholder="搜索视频、UP 主或标签..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg"
        />
      </div>

      {/* 热门标签 */}
      <div className="flex flex-wrap gap-2">
        {popularTags.map((tag) => (
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
      <div className="flex items-center justify-between bg-white p-4 rounded-xl border">
        <div className="flex items-center gap-4">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showSeriesOnly}
              onChange={(e) => setShowSeriesOnly(e.target.checked)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-sm font-medium">仅看系列课</span>
          </label>
        </div>

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

      {/* 结果统计 */}
      <div className="text-sm text-gray-600">
        找到 <span className="font-semibold text-blue-600">{filteredResources.length}</span> 个资源
      </div>

      {/* 资源列表 */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredResources.map((resource) => (
            <VideoCard key={resource.id} resource={resource} />
          ))}
        </div>
      ) : (
        <div className="space-y-4">
          {filteredResources.map((resource) => (
            <VideoCard key={resource.id} resource={resource} viewMode="list" />
          ))}
        </div>
      )}
    </div>
  )
}

function VideoCard({ resource, viewMode = 'grid' }: { resource: any; viewMode?: 'grid' | 'list' }) {
  if (viewMode === 'list') {
    return (
      <a
        href={resource.url}
        target="_blank"
        rel="noopener noreferrer"
        className="block bg-white rounded-xl border p-6 hover:shadow-lg transition-all"
      >
        <div className="flex items-start gap-4">
          <div className="bg-blue-100 p-4 rounded-xl">
            <Play className="h-8 w-8 text-blue-600" />
          </div>
          <div className="flex-1">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h3 className="text-xl font-bold text-gray-900">{resource.title}</h3>
                <p className="text-gray-600 mt-1">{resource.description}</p>
              </div>
              <div className="flex items-center gap-1 text-yellow-500">
                <Star className="h-5 w-5 fill-yellow-500" />
                <span className="font-medium">{resource.rating}</span>
              </div>
            </div>
            <div className="flex items-center gap-4 mt-3 flex-wrap">
              <span className="flex items-center gap-1 text-sm text-gray-500">
                <User className="h-4 w-4" />
                {resource.author}
              </span>
              <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
                {resource.category}
              </span>
              {resource.series && (
                <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                  系列课 ({resource.episodes}集)
                </span>
              )}
            </div>
          </div>
        </div>
      </a>
    )
  }

  return (
    <a
      href={resource.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block bg-white rounded-xl border overflow-hidden hover:shadow-xl hover:-translate-y-1 transition-all group"
    >
      {/* 封面 */}
      <div className="relative aspect-video bg-gradient-to-br from-blue-500 to-purple-600">
        <div className="absolute inset-0 flex items-center justify-center">
          <Play className="h-16 w-16 text-white/80 group-hover:scale-110 transition-transform" />
        </div>
        {resource.series && (
          <div className="absolute top-2 right-2 bg-green-500 text-white px-2 py-1 rounded text-xs font-medium">
            系列 {resource.episodes}集
          </div>
        )}
        <div className="absolute bottom-2 left-2 bg-black/80 text-white px-2 py-1 rounded text-xs">
          {resource.category}
        </div>
      </div>

      {/* 内容 */}
      <div className="p-4">
        <h3 className="font-bold text-gray-900 line-clamp-2">{resource.title}</h3>
        <p className="text-sm text-gray-600 mt-2 line-clamp-2">{resource.description}</p>
        
        <div className="flex items-center gap-2 mt-3 flex-wrap">
          {resource.tags.slice(0, 3).map((tag: string, i: number) => (
            <span key={i} className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
              #{tag}
            </span>
          ))}
        </div>

        <div className="flex items-center justify-between mt-4 pt-4 border-t">
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <User className="h-4 w-4" />
            <span className="truncate max-w-[100px]">{resource.author}</span>
          </div>
          <div className="flex items-center gap-1 text-yellow-500">
            <Star className="h-4 w-4 fill-yellow-500" />
            <span className="text-sm font-medium">{resource.rating}</span>
          </div>
        </div>
      </div>
    </a>
  )
}
