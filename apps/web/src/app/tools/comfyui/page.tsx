'use client';

import dynamic from 'next/dynamic';
import { Suspense } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { RefreshCw } from 'lucide-react';

// 动态导入ComfyUI集成组件，避免服务端渲染问题
const ComfyUIIntegration = dynamic(
  () => import('@/components/comfyui-integration/ComfyUIIntegration'),
  { 
    ssr: false,
    loading: () => (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="h-8 w-8 animate-spin text-blue-500" />
        <span className="ml-2">加载中...</span>
      </div>
    )
  }
);

export default function ComfyUIToolsPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        {/* 页面头部 */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">🎨 ComfyUI 工具</h1>
              <p className="text-gray-600">与本地 ComfyUI 实例集成，实现高级AI图像生成</p>
            </div>
            <Badge variant="secondary" className="text-sm">
              本地部署
            </Badge>
          </div>
          
          <div className="mt-4 flex flex-wrap gap-2">
            <Badge>AI 图像生成</Badge>
            <Badge variant="secondary">工作流</Badge>
            <Badge variant="outline">本地部署</Badge>
          </div>
        </div>

        {/* 说明卡片 */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>关于 ComfyUI 集成</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 mb-4">
              ComfyUI 是一个强大的基于节点的 Stable Diffusion GUI。我们的集成允许您直接从本平台控制本地运行的 ComfyUI 实例，
              实现文生图、图生图、局部重绘等高级图像生成功能。
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h3 className="font-semibold text-blue-800 mb-2">文生图</h3>
                <p className="text-sm text-blue-600">通过文本描述生成高质量图像</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <h3 className="font-semibold text-green-800 mb-2">图生图</h3>
                <p className="text-sm text-green-600">基于参考图像生成新图像</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <h3 className="font-semibold text-purple-800 mb-2">局部重绘</h3>
                <p className="text-sm text-purple-600">对图像特定区域进行修改</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* ComfyUI 集成组件 */}
        <Suspense fallback={
          <div className="flex items-center justify-center h-64">
            <RefreshCw className="h-8 w-8 animate-spin text-blue-500" />
            <span className="ml-2">加载 ComfyUI 集成...</span>
          </div>
        }>
          <ComfyUIIntegration />
        </Suspense>
      </div>
    </div>
  );
}