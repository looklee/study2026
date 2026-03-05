'use client'

import { useState, useEffect } from 'react'
import { Heart, Zap, Coffee, Book, Gamepad, Sparkles, TrendingUp, Clock, Trophy } from 'lucide-react'

interface Pet {
  pet_type: string
  pet_name: string
  icon: string
  level: number
  level_name: string
  exp: number
  exp_to_next: number
  happiness: number
  energy: number
  total_study_time: number
  checkin_days: number
  message: string
  created_at: string
  last_interaction: string
}

interface InteractionResult {
  status: string
  message: string
  happiness: number
  energy: number
  exp_gain: number
  pet: Pet
}

export default function PetPage() {
  const [pet, setPet] = useState<Pet | null>(null)
  const [loading, setLoading] = useState(true)
  const [interacting, setInteracting] = useState<string | null>(null)
  const [showLevelUp, setShowLevelUp] = useState(false)
  const [levelUpData, setLevelUpData] = useState({ level: 0, name: '', icon: '' })

  useEffect(() => {
    fetchPet()
  }, [])

  const fetchPet = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/pet?user_id=demo_user`)
      const data = await response.json()
      setPet(data)
    } catch (error) {
      console.error('获取宠物信息失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleInteract = async (action: string) => {
    setInteracting(action)
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/pet/interact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'demo_user', action })
      })
      const result: InteractionResult = await res.json()

      if (result.status === 'success') {
        setPet(result.pet)
        // 检查是否升级
        if (result.pet && result.pet.level > (pet?.level || 1)) {
          setLevelUpData({
            level: result.pet.level,
            name: result.pet.level_name,
            icon: result.pet.icon
          })
          setShowLevelUp(true)
          setTimeout(() => setShowLevelUp(false), 3000)
        }
      }
    } catch (error) {
      console.error('互动失败:', error)
    } finally {
      setInteracting(null)
    }
  }

  const handleAddExp = async () => {
    setInteracting('study')
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/pet/exp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'demo_user', exp: 20, reason: '学习' })
      })
      const result = await res.json()
      if (result.status === 'success') {
        setPet(result.pet)
        if (result.pet && result.pet.level > (pet?.level || 1)) {
          setLevelUpData({
            level: result.pet.level,
            name: result.pet.level_name,
            icon: result.pet.icon
          })
          setShowLevelUp(true)
          setTimeout(() => setShowLevelUp(false), 3000)
        }
      }
    } catch (error) {
      console.error('添加经验失败:', error)
    } finally {
      setInteracting(null)
    }
  }

  const getExpProgress = () => {
    if (!pet) return 0
    return Math.min(100, (pet.exp / pet.exp_to_next) * 100)
  }

  const getStatusColor = (value: number) => {
    if (value >= 80) return 'text-green-500'
    if (value >= 50) return 'text-yellow-500'
    return 'text-red-500'
  }

  const getStatusBg = (value: number) => {
    if (value >= 80) return 'bg-green-500'
    if (value >= 50) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">召唤宠物中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* 标题 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            🐾 学习伴侣
          </h1>
          <p className="text-gray-600 mt-2">陪伴你学习的虚拟宠物，一起成长！</p>
        </div>

        {/* 升级动画 */}
        {showLevelUp && (
          <div className="fixed inset-0 flex items-center justify-center z-50 pointer-events-none">
            <div className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-8 py-4 rounded-2xl shadow-2xl animate-bounce">
              <div className="text-center">
                <Sparkles className="h-12 w-12 mx-auto mb-2 animate-spin" />
                <div className="text-2xl font-bold">升级了！</div>
                <div className="text-xl">
                  {levelUpData.icon} Lv.{levelUpData.level} {levelUpData.name}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* 宠物展示区 */}
        <div className="bg-white rounded-3xl shadow-xl p-8 mb-6">
          <div className="flex flex-col items-center">
            {/* 宠物形象 */}
            <div className="relative">
              <div className="w-48 h-48 rounded-full bg-gradient-to-br from-purple-100 to-pink-100 flex items-center justify-center mb-4 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-t from-purple-200/50 to-transparent animate-pulse"></div>
                <span className="text-8xl relative z-10">{pet?.icon}</span>
              </div>
              {/* 等级徽章 */}
              <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-1 rounded-full text-sm font-bold shadow-lg">
                Lv.{pet?.level} {pet?.level_name}
              </div>
            </div>

            {/* 宠物名字 */}
            <h2 className="text-2xl font-bold text-gray-800 mt-4">{pet?.pet_name}</h2>

            {/* 宠物消息 */}
            <div className="bg-purple-50 rounded-xl p-4 mt-4 max-w-md">
              <p className="text-gray-700 text-center">{pet?.message}</p>
            </div>

            {/* 经验条 */}
            <div className="w-full max-w-md mt-6">
              <div className="flex justify-between text-sm text-gray-600 mb-2">
                <span>经验值</span>
                <span>{pet?.exp} / {pet?.exp_to_next}</span>
              </div>
              <div className="h-4 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500"
                  style={{ width: `${getExpProgress()}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* 状态面板 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          {/* 心情 */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-3 rounded-full bg-pink-100">
                <Heart className={`h-6 w-6 ${getStatusColor(pet?.happiness || 0)}`} />
              </div>
              <div>
                <div className="text-gray-600">心情</div>
                <div className={`text-2xl font-bold ${getStatusColor(pet?.happiness || 0)}`}>
                  {pet?.happiness || 0}
                </div>
              </div>
            </div>
            <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className={`h-full ${getStatusBg(pet?.happiness || 0)} transition-all duration-500`}
                style={{ width: `${pet?.happiness || 0}%` }}
              ></div>
            </div>
          </div>

          {/* 精力 */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="p-3 rounded-full bg-yellow-100">
                <Zap className={`h-6 w-6 ${getStatusColor(pet?.energy || 0)}`} />
              </div>
              <div>
                <div className="text-gray-600">精力</div>
                <div className={`text-2xl font-bold ${getStatusColor(pet?.energy || 0)}`}>
                  {pet?.energy || 0}
                </div>
              </div>
            </div>
            <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
              <div 
                className={`h-full ${getStatusBg(pet?.energy || 0)} transition-all duration-500`}
                style={{ width: `${pet?.energy || 0}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* 互动按钮 */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">与宠物互动</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button
              onClick={() => handleInteract('feed')}
              disabled={interacting === 'feed'}
              className="flex flex-col items-center gap-2 p-4 rounded-xl bg-gradient-to-br from-green-50 to-emerald-50 
                       hover:from-green-100 hover:to-emerald-100 transition-all disabled:opacity-50"
            >
              <Coffee className="h-8 w-8 text-green-600" />
              <span className="text-sm font-medium text-gray-700">喂食</span>
              <span className="text-xs text-gray-500">+15 心情</span>
            </button>

            <button
              onClick={() => handleInteract('play')}
              disabled={interacting === 'play'}
              className="flex flex-col items-center gap-2 p-4 rounded-xl bg-gradient-to-br from-blue-50 to-cyan-50 
                       hover:from-blue-100 hover:to-cyan-100 transition-all disabled:opacity-50"
            >
              <Gamepad className="h-8 w-8 text-blue-600" />
              <span className="text-sm font-medium text-gray-700">玩耍</span>
              <span className="text-xs text-gray-500">+20 心情</span>
            </button>

            <button
              onClick={() => handleInteract('rest')}
              disabled={interacting === 'rest'}
              className="flex flex-col items-center gap-2 p-4 rounded-xl bg-gradient-to-br from-purple-50 to-pink-50 
                       hover:from-purple-100 hover:to-pink-100 transition-all disabled:opacity-50"
            >
              <Coffee className="h-8 w-8 text-purple-600" />
              <span className="text-sm font-medium text-gray-700">休息</span>
              <span className="text-xs text-gray-500">+30 精力</span>
            </button>

            <button
              onClick={handleAddExp}
              disabled={interacting === 'study'}
              className="flex flex-col items-center gap-2 p-4 rounded-xl bg-gradient-to-br from-orange-50 to-red-50 
                       hover:from-orange-100 hover:to-red-100 transition-all disabled:opacity-50"
            >
              <Book className="h-8 w-8 text-orange-600" />
              <span className="text-sm font-medium text-gray-700">学习</span>
              <span className="text-xs text-gray-500">+20 经验</span>
            </button>
          </div>
        </div>

        {/* 统计信息 */}
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-purple-600" />
            成长统计
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-xl p-4 text-center">
              <Clock className="h-6 w-6 text-purple-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-800">{pet?.total_study_time || 0}</div>
              <div className="text-sm text-gray-500">学习时长 (分钟)</div>
            </div>
            <div className="bg-white rounded-xl p-4 text-center">
              <Sparkles className="h-6 w-6 text-pink-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-800">{pet?.checkin_days || 0}</div>
              <div className="text-sm text-gray-500">签到天数</div>
            </div>
            <div className="bg-white rounded-xl p-4 text-center">
              <Trophy className="h-6 w-6 text-yellow-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-800">{pet?.level || 1}</div>
              <div className="text-sm text-gray-500">当前等级</div>
            </div>
            <div className="bg-white rounded-xl p-4 text-center">
              <Heart className="h-6 w-6 text-red-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-800">{pet?.level_name}</div>
              <div className="text-sm text-gray-500">宠物称号</div>
            </div>
          </div>
        </div>

        {/* 等级说明 */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mt-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">宠物等级</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { level: 1, name: '蛋蛋', icon: '🥚', exp: 0 },
              { level: 2, name: '小雏', icon: '🐣', exp: 100 },
              { level: 3, name: '学童', icon: '🐤', exp: 300 },
              { level: 4, name: '学子', icon: '🐥', exp: 600 },
              { level: 5, name: '学师', icon: '🦅', exp: 1000 },
              { level: 6, name: '学尊', icon: '🦉', exp: 1600 },
              { level: 7, name: '学圣', icon: '🐉', exp: 2500 },
              { level: 8, name: '学神', icon: '✨', exp: 4000 },
            ].map((tier) => (
              <div
                key={tier.level}
                className={`p-3 rounded-xl text-center transition-all ${
                  pet && pet.level >= tier.level
                    ? 'bg-gradient-to-br from-purple-100 to-pink-100 border-2 border-purple-400'
                    : 'bg-gray-100 opacity-50'
                }`}
              >
                <div className="text-2xl mb-1">{tier.icon}</div>
                <div className="text-sm font-medium text-gray-700">Lv.{tier.level} {tier.name}</div>
                <div className="text-xs text-gray-500">{tier.exp} 经验</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
