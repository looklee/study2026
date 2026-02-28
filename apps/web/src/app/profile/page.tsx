'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { User, Mail, BookOpen, Target, Bell, CheckCircle } from 'lucide-react'

export default function ProfilePage() {
  const { user, updateUserPreferences } = useAuth()
  
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    fullName: '',
    currentLevel: 'beginner',
    learningStyle: 'mixed',
    timezone: 'Asia/Shanghai'
  })

  const [notifications, setNotifications] = useState({
    emailEnabled: true,
    dailyReminder: true,
    weeklyReport: true,
    milestoneAlerts: true
  })

  // 从 AuthContext 同步用户信息
  useEffect(() => {
    if (user) {
      setFormData({
        username: user.username || '',
        email: user.email || '',
        fullName: user.username || '用户',
        currentLevel: 'beginner',
        learningStyle: user.preferences?.language === 'zh-CN' ? 'mixed' : 'mixed',
        timezone: user.preferences?.language === 'zh-CN' ? 'Asia/Shanghai' : 'Asia/Shanghai'
      })
      
      setNotifications({
        emailEnabled: user.preferences?.notifications ?? true,
        dailyReminder: true,
        weeklyReport: true,
        milestoneAlerts: true
      })
    }
  }, [user])

  const handleSave = () => {
    // 保存用户信息
    updateUserPreferences({
      language: formData.timezone === 'Asia/Shanghai' ? 'zh-CN' : 'en-US'
    })
    alert('设置已保存！')
  }

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center text-gray-500">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p>加载中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">个人设置</h1>
        <p className="text-gray-500 mt-1">管理你的账户和学习偏好</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* 用户卡片 */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-sm border p-6">
            <div className="text-center">
              <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full mx-auto flex items-center justify-center text-white text-3xl font-bold">
                {user.username?.[0] || 'U'}
              </div>
              <h2 className="text-xl font-bold text-gray-900 mt-4">{user.username}</h2>
              <p className="text-gray-500 text-sm">{user.user_id}</p>
              <div className="mt-4 flex items-center justify-center gap-2 text-sm text-gray-600">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>已激活</span>
              </div>
              <div className="mt-4 text-xs text-gray-500">
                <p>注册时间：{user.created_at ? new Date(user.created_at).toLocaleDateString('zh-CN') : '-'}</p>
                <p>登录次数：{user.login_count || 0}</p>
              </div>
            </div>
          </div>
        </div>

        {/* 设置表单 */}
        <div className="lg:col-span-2 space-y-6">
          {/* 基本信息 */}
          <div className="bg-white rounded-xl shadow-sm border p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
              <User className="h-5 w-5" />
              基本信息
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">用户名</label>
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">显示名称</label>
                <input
                  type="text"
                  value={formData.fullName}
                  onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                  className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          {/* 学习偏好 */}
          <div className="bg-white rounded-xl shadow-sm border p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              学习偏好
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">当前水平</label>
                <select
                  value={formData.currentLevel}
                  onChange={(e) => setFormData({ ...formData, currentLevel: e.target.value })}
                  className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="beginner">初学者 - 从零开始</option>
                  <option value="intermediate">中级 - 有一定基础</option>
                  <option value="advanced">高级 - 想深入学习</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">学习风格</label>
                <select
                  value={formData.learningStyle}
                  onChange={(e) => setFormData({ ...formData, learningStyle: e.target.value })}
                  className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="mixed">混合式（理论 + 实践）</option>
                  <option value="hands-on">动手实践为主</option>
                  <option value="theoretical">理论学习为主</option>
                  <option value="video-based">视频教程为主</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">时区</label>
                <select
                  value={formData.timezone}
                  onChange={(e) => setFormData({ ...formData, timezone: e.target.value })}
                  className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="Asia/Shanghai">中国标准时间 (UTC+8)</option>
                  <option value="Asia/Tokyo">日本标准时间 (UTC+9)</option>
                  <option value="America/New_York">美国东部时间 (UTC-5)</option>
                </select>
              </div>
            </div>
          </div>

          {/* 通知设置 */}
          <div className="bg-white rounded-xl shadow-sm border p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
              <Bell className="h-5 w-5" />
              通知设置
            </h3>
            <div className="space-y-4">
              <Toggle
                label="邮件通知"
                description="接收重要更新的邮件通知"
                checked={notifications.emailEnabled}
                onChange={(checked) => setNotifications({ ...notifications, emailEnabled: checked })}
              />
              <Toggle
                label="每日学习提醒"
                description="每天早上 9 点提醒你学习"
                checked={notifications.dailyReminder}
                onChange={(checked) => setNotifications({ ...notifications, dailyReminder: checked })}
              />
              <Toggle
                label="每周学习报告"
                description="每周日发送学习进度报告"
                checked={notifications.weeklyReport}
                onChange={(checked) => setNotifications({ ...notifications, weeklyReport: checked })}
              />
              <Toggle
                label="里程碑提醒"
                description="达成学习里程碑时发送通知"
                checked={notifications.milestoneAlerts}
                onChange={(checked) => setNotifications({ ...notifications, milestoneAlerts: checked })}
              />
            </div>
          </div>

          {/* 保存按钮 */}
          <div className="flex justify-end gap-4">
            <button className="px-6 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors">
              取消
            </button>
            <button
              onClick={handleSave}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              保存设置
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

function Toggle({ label, description, checked, onChange }: {
  label: string
  description: string
  checked: boolean
  onChange: (checked: boolean) => void
}) {
  return (
    <div className="flex items-center justify-between py-3">
      <div>
        <p className="font-medium text-gray-900">{label}</p>
        <p className="text-sm text-gray-500">{description}</p>
      </div>
      <button
        onClick={() => onChange(!checked)}
        className={`relative w-12 h-6 rounded-full transition-colors ${
          checked ? 'bg-blue-600' : 'bg-gray-200'
        }`}
      >
        <span
          className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${
            checked ? 'left-7' : 'left-1'
          }`}
        />
      </button>
    </div>
  )
}
