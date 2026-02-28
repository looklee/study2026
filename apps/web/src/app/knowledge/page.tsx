'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Search, Upload, FileText, Tag, Trash2, Eye, Plus, X, CheckCircle, Clock, XCircle, Folder, BarChart3 } from 'lucide-react'

export default function KnowledgePage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [showUploadModal, setShowUploadModal] = useState(false)
  const [selectedDoc, setSelectedDoc] = useState<any>(null)

  const queryClient = useQueryClient()

  // 获取统计信息
  const { data: stats } = useQuery({
    queryKey: ['knowledge-stats'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8001/api/v1/knowledge/stats')
      return response.json()
    }
  })

  // 获取分类
  const { data: categories } = useQuery({
    queryKey: ['knowledge-categories'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8001/api/v1/knowledge/categories')
      return response.json()
    }
  })

  // 获取文档列表
  const { data: documents, isLoading } = useQuery({
    queryKey: ['knowledge-documents', selectedCategory],
    queryFn: async () => {
      const url = selectedCategory !== 'all' 
        ? `http://localhost:8001/api/v1/knowledge/documents?category=${selectedCategory}`
        : 'http://localhost:8001/api/v1/knowledge/documents'
      const response = await fetch(url)
      return response.json()
    }
  })

  // 搜索知识库
  const searchMutation = useMutation({
    mutationFn: async (query: string) => {
      const response = await fetch('http://localhost:8001/api/v1/knowledge/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, limit: 20 })
      })
      return response.json()
    }
  })

  // 上传文档
  const uploadMutation = useMutation({
    mutationFn: async (docData: any) => {
      const response = await fetch('http://localhost:8001/api/v1/knowledge/documents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(docData)
      })
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['knowledge-documents'] })
      queryClient.invalidateQueries({ queryKey: ['knowledge-stats'] })
      setShowUploadModal(false)
      alert('文档上传成功！')
    }
  })

  // 删除文档
  const deleteMutation = useMutation({
    mutationFn: async (docId: string) => {
      const response = await fetch(`http://localhost:8001/api/v1/knowledge/documents/${docId}`, {
        method: 'DELETE'
      })
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['knowledge-documents'] })
      queryClient.invalidateQueries({ queryKey: ['knowledge-stats'] })
      alert('文档已删除')
    }
  })

  const handleSearch = () => {
    if (searchQuery.trim()) {
      searchMutation.mutate(searchQuery)
    }
  }

  const categoryList = ['all', ...(categories?.categories || [])]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">📚 知识库</h1>
          <p className="text-gray-600 mt-1">管理和检索学习文档，支持 RAG 检索增强</p>
        </div>
        <button
          onClick={() => setShowUploadModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Upload className="h-4 w-4" />
          上传文档
        </button>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard 
          label="总文档数" 
          value={stats?.stats?.total_documents || 0} 
          icon={<FileText className="h-6 w-6" />}
          color="blue"
        />
        <StatCard 
          label="文本块数" 
          value={stats?.stats?.total_chunks || 0} 
          icon={<BarChart3 className="h-6 w-6" />}
          color="green"
        />
        <StatCard 
          label="分类数" 
          value={Object.keys(stats?.stats?.by_category || {}).length} 
          icon={<Folder className="h-6 w-6" />}
          color="purple"
        />
        <StatCard 
          label="已处理" 
          value={stats?.stats?.by_status?.processed || 0} 
          icon={<CheckCircle className="h-6 w-6" />}
          color="green"
        />
      </div>

      {/* 搜索栏 */}
      <div className="relative max-w-3xl mx-auto">
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
        <input
          type="text"
          placeholder="搜索知识库内容..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg"
        />
        <button
          onClick={handleSearch}
          disabled={searchMutation.isPending}
          className="absolute right-2 top-1/2 transform -translate-y-1/2 px-6 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          {searchMutation.isPending ? '搜索中...' : '搜索'}
        </button>
      </div>

      {/* 分类筛选 */}
      <div className="flex flex-wrap gap-3">
        {categoryList.map((category) => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              selectedCategory === category
                ? 'bg-blue-600 text-white shadow-lg scale-105'
                : 'bg-white border hover:bg-gray-50'
            }`}
          >
            {category === 'all' ? '全部' : category}
          </button>
        ))}
      </div>

      {/* 搜索结果 */}
      {searchMutation.data && (
        <div className="bg-white rounded-xl border p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900">
              搜索结果 ({searchMutation.data.results?.length || 0})
            </h2>
            <button onClick={() => searchMutation.reset()} className="text-gray-500 hover:text-gray-700">
              <X className="h-5 w-5" />
            </button>
          </div>
          <div className="space-y-4">
            {searchMutation.data.results?.map((result: any) => (
              <div key={result.doc_id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">{result.file_name}</h3>
                    <p className="text-sm text-gray-600 mt-1">{result.snippet}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">
                        {result.category}
                      </span>
                      <span className="text-xs text-gray-500">相关性：{(result.score || 0).toFixed(1)}</span>
                    </div>
                  </div>
                  <button
                    onClick={() => setSelectedDoc(result)}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    <Eye className="h-5 w-5 text-gray-500" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 文档列表 */}
      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          文档列表
          {selectedCategory !== 'all' && <span className="ml-2 text-sm font-normal text-gray-500">({selectedCategory})</span>}
        </h2>
        <div className="bg-white rounded-xl border overflow-hidden">
          {isLoading ? (
            <div className="p-8 text-center text-gray-500">加载中...</div>
          ) : documents?.documents?.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              暂无文档，点击上方"上传文档"按钮添加
            </div>
          ) : (
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">文档名</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">分类</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">标签</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">状态</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">块数</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {documents?.documents?.map((doc: any) => (
                  <tr key={doc.doc_id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">{doc.file_name}</td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">{doc.category}</span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      <div className="flex flex-wrap gap-1">
                        {doc.tags?.slice(0, 3).map((tag: string, i: number) => (
                          <span key={i} className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                            #{tag}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        doc.status === 'processed' ? 'bg-green-100 text-green-700' :
                        doc.status === 'processing' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-gray-100 text-gray-700'
                      }`}>
                        {doc.status === 'processed' ? '✓ 已处理' : doc.status === 'processing' ? '⋯ 处理中' : '○ 待处理'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">{doc.chunks_count || 0}</td>
                    <td className="px-6 py-4 text-sm">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => setSelectedDoc(doc)}
                          className="p-1 hover:bg-blue-50 rounded transition-colors"
                          title="查看"
                        >
                          <Eye className="h-4 w-4 text-blue-600" />
                        </button>
                        <button
                          onClick={() => deleteMutation.mutate(doc.doc_id)}
                          className="p-1 hover:bg-red-50 rounded transition-colors"
                          title="删除"
                        >
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* 上传文档模态框 */}
      {showUploadModal && (
        <UploadModal
          onClose={() => setShowUploadModal(false)}
          onUpload={(data) => uploadMutation.mutate(data)}
        />
      )}

      {/* 文档详情模态框 */}
      {selectedDoc && (
        <DocumentDetail
          doc={selectedDoc}
          onClose={() => setSelectedDoc(null)}
        />
      )}
    </div>
  )
}

function StatCard({ label, value, icon, color }: { label: string; value: number; icon: any; color: string }) {
  const colors: Record<string, string> = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600'
  }

  return (
    <div className="bg-white rounded-xl border p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{label}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
        <div className={`${colors[color]} p-3 rounded-lg`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

function UploadModal({ onClose, onUpload }: { onClose: () => void; onUpload: (data: any) => void }) {
  const [formData, setFormData] = useState({
    file_name: '',
    content: '',
    category: 'general',
    tags: ''
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onUpload({
      ...formData,
      tags: formData.tags.split(',').map((t: string) => t.trim()).filter(Boolean)
    })
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">上传文档</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="h-6 w-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">文档名称</label>
            <input
              type="text"
              value={formData.file_name}
              onChange={(e) => setFormData({ ...formData, file_name: e.target.value })}
              className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="例如：机器学习笔记"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">文档内容</label>
            <textarea
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
              className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={8}
              placeholder="粘贴文档内容..."
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">分类</label>
            <select
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="general">通用</option>
              <option value="course-material">课程资料</option>
              <option value="tutorial">教程</option>
              <option value="article">文章</option>
              <option value="book">书籍</option>
              <option value="notes">笔记</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">标签（用逗号分隔）</label>
            <input
              type="text"
              value={formData.tags}
              onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
              className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="例如：机器学习，AI，深度学习"
            />
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border rounded-lg hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              上传
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

function DocumentDetail({ doc, onClose }: { doc: any; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 max-w-3xl w-full mx-4 max-h-[80vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">文档详情</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="h-6 w-6" />
          </button>
        </div>

        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{doc.file_name || doc.doc_id}</h3>
          </div>

          <div className="flex items-center gap-4">
            <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
              {doc.category}
            </span>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              doc.status === 'processed' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
            }`}>
              {doc.status}
            </span>
          </div>

          {doc.tags && doc.tags.length > 0 && (
            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">标签</p>
              <div className="flex flex-wrap gap-2">
                {doc.tags.map((tag: string, i: number) => (
                  <span key={i} className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-sm">
                    #{tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          {doc.snippet && (
            <div>
              <p className="text-sm font-medium text-gray-700 mb-2">内容预览</p>
              <div className="bg-gray-50 rounded-lg p-4 text-sm text-gray-600">
                {doc.snippet}
              </div>
            </div>
          )}

          {doc.created_at && (
            <div className="text-sm text-gray-500">
              创建时间：{new Date(doc.created_at).toLocaleString('zh-CN')}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
