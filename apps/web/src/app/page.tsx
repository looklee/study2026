import { redirect } from 'next/navigation'

export default function HomePage() {
  // 服务器端重定向到仪表板
  redirect('/dashboard')
}
