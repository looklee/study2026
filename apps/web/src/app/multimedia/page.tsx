'use client'

import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Sparkles, Image, Video, Scissors, Palette, Droplets } from 'lucide-react';
import TextToImageComponent from '@/components/multimedia/TextToImageComponent';
import ImageToImageComponent from '@/components/multimedia/ImageToImageComponent';
import VideoGenerationComponent from '@/components/multimedia/VideoGenerationComponent';
import ImageEditingComponent from '@/components/multimedia/ImageEditingComponent';
import WatermarkRemovalComponent from '@/components/multimedia/WatermarkRemovalComponent';

export default function MultimediaAIPage() {
  const [activeTab, setActiveTab] = useState('text-to-image');

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Header */}
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-full mb-4">
          <Sparkles className="h-6 w-6" />
          <h1 className="text-3xl font-bold">AI 多媒体创作</h1>
        </div>
        <p className="text-gray-600 text-lg max-w-2xl mx-auto">
          利用先进的人工智能技术，轻松创建图像、视频和编辑内容
        </p>
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 border-purple-200">
          <CardContent className="p-6 text-center">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Image className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">文生图</h3>
            <p className="text-sm text-gray-600">从文本描述生成图像</p>
            <Badge variant="secondary" className="mt-2">AI生成</Badge>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 border-blue-200">
          <CardContent className="p-6 text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Palette className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">图生图</h3>
            <p className="text-sm text-gray-600">基于参考图生成新图像</p>
            <Badge variant="secondary" className="mt-2">AI转换</Badge>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 border-green-200">
          <CardContent className="p-6 text-center">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Video className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">视频生成</h3>
            <p className="text-sm text-gray-600">从文本生成视频内容</p>
            <Badge variant="secondary" className="mt-2">AI创作</Badge>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 border-orange-200">
          <CardContent className="p-6 text-center">
            <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Droplets className="h-6 w-6 text-orange-600" />
            </div>
            <h3 className="font-semibold text-gray-900 mb-1">去水印</h3>
            <p className="text-sm text-gray-600">智能去除图片水印</p>
            <Badge variant="secondary" className="mt-2">AI修复</Badge>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="text-to-image" onClick={() => setActiveTab('text-to-image')}>
            文生图
          </TabsTrigger>
          <TabsTrigger value="image-to-image" onClick={() => setActiveTab('image-to-image')}>
            图生图
          </TabsTrigger>
          <TabsTrigger value="video-generation" onClick={() => setActiveTab('video-generation')}>
            视频生成
          </TabsTrigger>
          <TabsTrigger value="image-editing" onClick={() => setActiveTab('image-editing')}>
            图片编辑
          </TabsTrigger>
          <TabsTrigger value="watermark-removal" onClick={() => setActiveTab('watermark-removal')}>
            去水印
          </TabsTrigger>
        </TabsList>

        <TabsContent value="text-to-image" className="mt-6">
          <TextToImageComponent />
        </TabsContent>

        <TabsContent value="image-to-image" className="mt-6">
          <ImageToImageComponent />
        </TabsContent>

        <TabsContent value="video-generation" className="mt-6">
          <VideoGenerationComponent />
        </TabsContent>

        <TabsContent value="image-editing" className="mt-6">
          <ImageEditingComponent />
        </TabsContent>

        <TabsContent value="watermark-removal" className="mt-6">
          <WatermarkRemovalComponent />
        </TabsContent>
      </Tabs>

      {/* Info Section */}
      <div className="mt-12 bg-gradient-to-r from-gray-50 to-blue-50 rounded-2xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">AI 多媒体创作工具集</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h3 className="font-semibold text-lg mb-2">文生图</h3>
            <p className="text-gray-600">
              通过自然语言描述生成高质量图像，支持多种艺术风格和自定义参数。
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-lg mb-2">图生图</h3>
            <p className="text-gray-600">
              基于参考图像和文本描述，生成具有相似风格的新图像。
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-lg mb-2">视频生成</h3>
            <p className="text-gray-600">
              根据文本描述自动生成视频内容，适用于创意视频制作。
            </p>
          </div>
        </div>
        <p className="text-gray-700 mt-6 italic">
          所有功能均由AI驱动，创作过程完全自动化，只需输入您的创意即可获得专业级结果。
        </p>
      </div>
    </div>
  );
}