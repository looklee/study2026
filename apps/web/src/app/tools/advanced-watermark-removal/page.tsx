'use client';

import dynamic from 'next/dynamic';
import { Suspense } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { RefreshCw, Droplets, ScanEye, MousePointer, Square, Wand2 } from 'lucide-react';

// 动态导入去水印组件，避免服务端渲染问题
const AdvancedWatermarkRemoval = dynamic(
  () => import('@/components/advanced-watermark-removal/AdvancedWatermarkRemoval'),
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

export default function AdvancedWatermarkRemovalPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        {/* 页面头部 */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">🎨 高级去水印工具</h1>
              <p className="text-gray-600">使用多种AI技术去除图像中的水印，支持涂抹选择和智能检测</p>
            </div>
            <Badge variant="secondary" className="text-sm">
              AI增强
            </Badge>
          </div>
          
          <div className="mt-4 flex flex-wrap gap-2">
            <Badge>图像处理</Badge>
            <Badge variant="secondary">AI修复</Badge>
            <Badge variant="outline">涂抹选择</Badge>
          </div>
        </div>

        {/* 功能特性卡片 */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>功能特性</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg text-center">
                <MousePointer className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                <h3 className="font-semibold text-blue-800 mb-1">涂抹选择</h3>
                <p className="text-sm text-blue-600">点击涂抹要去除的水印区域</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg text-center">
                <Square className="h-8 w-8 text-green-600 mx-auto mb-2" />
                <h3 className="font-semibold text-green-800 mb-1">矩形选择</h3>
                <p className="text-sm text-green-600">拖拽选择精确的水印区域</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg text-center">
                <Wand2 className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                <h3 className="font-semibold text-purple-800 mb-1">智能检测</h3>
                <p className="text-sm text-purple-600">自动识别常见的水印位置</p>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg text-center">
                <Droplets className="h-8 w-8 text-orange-600 mx-auto mb-2" />
                <h3 className="font-semibold text-orange-800 mb-1">AI修复</h3>
                <p className="text-sm text-orange-600">使用AI算法智能修复图像</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 去水印工具组件 */}
        <Suspense fallback={
          <div className="flex items-center justify-center h-64">
            <RefreshCw className="h-8 w-8 animate-spin text-blue-500" />
            <span className="ml-2">加载去水印工具...</span>
          </div>
        }>
          <AdvancedWatermarkRemoval />
        </Suspense>
      </div>
    </div>
  );
}