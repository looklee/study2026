'use client'

import { createContext, useContext, useState, useEffect, useCallback } from 'react'

interface User {
  user_id: string
  username: string
  email: string
  created_at: string
  last_login: string
  login_count: number
  device_count: number
  preferences: {
    theme: string
    language: string
    notifications: boolean
  }
}

interface AuthContextType {
  user: User | null
  deviceId: string | null
  sessionId: string | null
  isLoading: boolean
  login: () => Promise<void>
  logout: () => void
  updateUserPreferences: (prefs: Partial<User['preferences']>) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [deviceId, setDeviceId] = useState<string | null>(null)
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // 收集设备信息
  const getDeviceInfo = useCallback(() => {
    const nav = navigator as any
    return {
      platform: nav.platform || 'unknown',
      browser: nav.userAgent?.split(' ').pop()?.replace('/', '') || 'unknown',
      language: nav.language || 'zh-CN',
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      screen: `${screen.width}x${screen.height}`,
      cores: nav.hardwareConcurrency || 0,
      memory: (nav as any).deviceMemory || 0
    }
  }, [])

  // 自动登录
  const login = useCallback(async () => {
    try {
      const deviceInfo = getDeviceInfo()

      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 3000)

      const response = await fetch('http://localhost:8001/api/v1/device/identify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: controller.signal,
        body: JSON.stringify(deviceInfo)
      })

      clearTimeout(timeoutId)

      const result = await response.json()

      if (result.status === 'success') {
        setDeviceId(result.device_id)
        setSessionId(result.session_id)
        setUser(result.user)
        
        // 保存到 localStorage
        localStorage.setItem('device_id', result.device_id)
        localStorage.setItem('session_id', result.session_id)
        localStorage.setItem('user', JSON.stringify(result.user))
        setIsLoading(false)
        return
      }
    } catch (error) {
      console.error('自动登录失败:', error)
    }
    
    // API 不可用，使用演示用户
    setDemoUser()
  }, [getDeviceInfo])

  // 设置演示用户
  const setDemoUser = useCallback(() => {
    const demoUser = {
      user_id: 'demo_user',
      username: '演示用户',
      email: 'demo@local.device',
      created_at: new Date().toISOString(),
      last_login: new Date().toISOString(),
      login_count: 1,
      device_count: 1,
      preferences: {
        theme: 'light',
        language: 'zh-CN',
        notifications: true
      }
    }
    setDeviceId('demo_device')
    setSessionId('demo_session')
    setUser(demoUser)
    localStorage.setItem('device_id', 'demo_device')
    localStorage.setItem('session_id', 'demo_session')
    localStorage.setItem('user', JSON.stringify(demoUser))
    setIsLoading(false)
  }, [])

  // 从 localStorage 恢复会话
  const restoreSession = useCallback(async () => {
    const savedSessionId = localStorage.getItem('session_id')
    const savedDeviceId = localStorage.getItem('device_id')
    const savedUser = localStorage.getItem('user')

    if (savedSessionId && savedDeviceId && savedUser) {
      try {
        const response = await fetch(`http://localhost:8001/api/v1/device/verify/${savedSessionId}`)
        const result = await response.json()

        if (result.status === 'success') {
          setSessionId(savedSessionId)
          setDeviceId(savedDeviceId)
          setUser(result.user)
          setIsLoading(false)
          return
        }
      } catch (error) {
        console.error('恢复会话失败:', error)
      }
    }

    // 会话无效或不存在，尝试登录
    await login()
  }, [login])

  // 登出
  const logout = useCallback(() => {
    setUser(null)
    setDeviceId(null)
    setSessionId(null)
    localStorage.removeItem('device_id')
    localStorage.removeItem('session_id')
    localStorage.removeItem('user')
  }, [])

  // 更新用户偏好
  const updateUserPreferences = useCallback(async (prefs: Partial<User['preferences']>) => {
    if (!user) return

    try {
      await fetch(`http://localhost:8001/api/v1/user/${user.user_id}/preferences`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(prefs)
      })

      setUser({
        ...user,
        preferences: { ...user.preferences, ...prefs }
      })
    } catch (error) {
      console.error('更新偏好失败:', error)
    }
  }, [user])

  useEffect(() => {
    restoreSession()
  }, [restoreSession])

  return (
    <AuthContext.Provider value={{ 
      user, 
      deviceId, 
      sessionId, 
      isLoading, 
      login, 
      logout,
      updateUserPreferences 
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
