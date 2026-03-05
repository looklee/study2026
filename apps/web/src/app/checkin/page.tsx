'use client'

import { useState, useEffect } from 'react'
import { Calendar, Flame, Trophy, Gift, Star, CheckCircle, XCircle } from 'lucide-react'

interface CheckinInfo {
  current_streak: number
  longest_streak: number
  total_checkins: number
  last_checkin: string | null
  today_checked: boolean
  checkin_calendar: Array<{
    date: string
    day: number
    checked: boolean
    is_today: boolean
  }>
}

interface CheckinReward {
  points: number
  badges: string[]
  items: string[]
}

interface CheckinResult {
  status: string
  message: string
  streak: number
  longest_streak: number
  total_checkins: number
  reward?: CheckinReward
  badges_earned?: string[]
}

export default function CheckinPage() {
  const [checkinInfo, setCheckinInfo] = useState<CheckinInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [checkingIn, setCheckingIn] = useState(false)
  const [showReward, setShowReward] = useState(false)
  const [reward, setReward] = useState<CheckinResult | null>(null)

  useEffect(() => {
    fetchCheckinInfo()
  }, [])

  const fetchCheckinInfo = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/checkin/info`)
      const data = await res.json()
      setCheckinInfo(data)
    } catch (error) {
      console.error('获取签到信息失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCheckIn = async () => {
    setCheckingIn(true)
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/checkin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'demo_user', username: '演示用户' })
      })
      const result = await res.json()

      if (result.status === 'success') {
        setReward(result)
        setShowReward(true)
        // 给宠物也发奖励
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/pet/checkin-bonus`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: 'demo_user' })
        })
      }
      fetchCheckinInfo()
    } catch (error) {
      console.error('签到失败:', error)
    } finally {
      setCheckingIn(false)
    }
  }

  const getStreakLevel = (streak: number) => {
    if (streak >= 100) return { color: 'from-yellow-400 to-orange-500', text: '百日传奇' }
    if (streak >= 30) return { color: 'from-purple-400 to-pink-500', text: '月度传奇' }
    if (streak >= 14) return { color: 'from-blue-400 to-cyan-500', text: '半月达人' }
    if (streak >= 7) return { color: 'from-green-400 to-emerald-500', text: '周勤学者' }
    if (streak >= 3) return { color: 'from-orange-400 to-red-500', text: '初露锋芒' }
    return { color: 'from-gray-400 to-gray-500', text: '继续努力' }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">加载中...</p>
        </div>
      </div>
    )
  }

  const streakLevel = getStreakLevel(checkinInfo?.current_streak || 0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* 标题 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            📅 每日签到
          </h1>
          <p className="text-gray-600 mt-2">每日签到，与你的学习伴侣一起成长！</p>
        </div>

        {/* 签到主卡片 */}
        <div className="bg-white rounded-3xl shadow-xl p-8 mb-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            {/* Streak 展示 */}
            <div className="flex items-center gap-4">
              <div className={`p-4 rounded-full bg-gradient-to-r ${streakLevel.color}`}>
                <Flame className="h-12 w-12 text-white" />
              </div>
              <div>
                <div className="text-4xl font-bold text-gray-800">
                  {checkinInfo?.current_streak || 0}
                </div>
                <div className="text-gray-500">连续签到</div>
                <div className={`text-sm font-medium ${streakLevel.color.replace('from-', 'text-').split(' ')[0]}`}>
                  {streakLevel.text}
                </div>
              </div>
            </div>

            {/* 签到按钮 */}
            <div className="text-center">
              {checkinInfo?.today_checked ? (
                <div className="flex items-center gap-2 text-green-600 bg-green-50 px-6 py-4 rounded-xl">
                  <CheckCircle className="h-8 w-8" />
                  <span className="text-lg font-medium">今日已签到</span>
                </div>
              ) : (
                <button
                  onClick={handleCheckIn}
                  disabled={checkingIn}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 
                           text-white px-8 py-4 rounded-xl text-lg font-bold shadow-lg transform hover:scale-105 
                           transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {checkingIn ? '签到中...' : '✍️ 立即签到'}
                </button>
              )}
            </div>

            {/* 统计信息 */}
            <div className="flex gap-6">
              <div className="text-center">
                <div className="flex items-center gap-2 text-gray-600">
                  <Trophy className="h-5 w-5 text-yellow-500" />
                  <span className="text-2xl font-bold">{checkinInfo?.longest_streak || 0}</span>
                </div>
                <div className="text-sm text-gray-500">最长连续</div>
              </div>
              <div className="text-center">
                <div className="flex items-center gap-2 text-gray-600">
                  <Star className="h-5 w-5 text-purple-500" />
                  <span className="text-2xl font-bold">{checkinInfo?.total_checkins || 0}</span>
                </div>
                <div className="text-sm text-gray-500">累计签到</div>
              </div>
            </div>
          </div>
        </div>

        {/* 签到日历 */}
        <div className="bg-white rounded-3xl shadow-xl p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Calendar className="h-6 w-6 text-purple-600" />
            签到日历
          </h2>
          <div className="grid grid-cols-7 gap-2">
            {checkinInfo?.checkin_calendar?.map((day, index) => (
              <div
                key={day.date}
                className={`
                  aspect-square rounded-xl flex flex-col items-center justify-center relative
                  transition-all
                  ${day.is_today ? 'ring-2 ring-purple-600 ring-offset-2' : ''}
                  ${day.checked 
                    ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white' 
                    : 'bg-gray-100 text-gray-400'}
                `}
              >
                <span className="text-xs opacity-70">{index === 0 ? '...' : ''}</span>
                <span className="text-lg font-bold">{day.day}</span>
                {day.checked && <CheckCircle className="h-4 w-4 absolute -bottom-1" />}
              </div>
            ))}
          </div>
          <div className="flex justify-center gap-6 mt-4 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-gradient-to-br from-purple-500 to-pink-500"></div>
              <span>已签到</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-gray-100"></div>
              <span>未签到</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded ring-2 ring-purple-600"></div>
              <span>今天</span>
            </div>
          </div>
        </div>

        {/* 签到奖励说明 */}
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-3xl p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Gift className="h-6 w-6 text-purple-600" />
            签到奖励
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-xl p-4 text-center">
              <div className="text-2xl mb-2">🔥</div>
              <div className="text-sm font-medium text-gray-700">连续 3 天</div>
              <div className="text-xs text-gray-500">初露锋芒</div>
            </div>
            <div className="bg-white rounded-xl p-4 text-center">
              <div className="text-2xl mb-2">🏆</div>
              <div className="text-sm font-medium text-gray-700">连续 7 天</div>
              <div className="text-xs text-gray-500">周勤学者</div>
            </div>
            <div className="bg-white rounded-xl p-4 text-center">
              <div className="text-2xl mb-2">🥈</div>
              <div className="text-sm font-medium text-gray-700">连续 14 天</div>
              <div className="text-xs text-gray-500">半月达人</div>
            </div>
            <div className="bg-white rounded-xl p-4 text-center">
              <div className="text-2xl mb-2">🥇</div>
              <div className="text-sm font-medium text-gray-700">连续 30 天</div>
              <div className="text-xs text-gray-500">月勤学者</div>
            </div>
          </div>
        </div>
      </div>

      {/* 奖励弹窗 */}
      {showReward && reward && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-3xl p-8 max-w-md w-full transform animate-bounce-in">
            <div className="text-center">
              <div className="text-6xl mb-4">🎉</div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">签到成功！</h2>
              <p className="text-gray-600 mb-6">{reward.message}</p>
              
              <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-4 mb-6">
                <div className="flex items-center justify-center gap-2 text-purple-600">
                  <Flame className="h-6 w-6" />
                  <span className="text-2xl font-bold">连续 {reward.streak} 天</span>
                </div>
              </div>

              {reward.badges_earned && reward.badges_earned.length > 0 && (
                <div className="mb-6">
                  <div className="text-sm text-gray-500 mb-2">获得徽章</div>
                  <div className="flex flex-wrap justify-center gap-2">
                    {reward.badges_earned.map((badge, i) => (
                      <span key={i} className="bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-3 py-1 rounded-full text-sm font-medium">
                        🏅 {badge}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <button
                onClick={() => setShowReward(false)}
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-xl font-medium"
              >
                太棒了！
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
