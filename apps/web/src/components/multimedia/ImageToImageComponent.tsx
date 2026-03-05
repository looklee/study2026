'use client'

import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Slider } from '@/components/ui/slider';
import { Loader2, Upload, Download, RotateCcw } from 'lucide-react';
import { multimediaApi } from '@/lib/api';

export default function ImageToImageComponent() {
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [prompt, setPrompt] = useState('');
  const [strength, setStrength] = useState(0.7);
  const [style, setStyle] = useState('realistic');
  const [isLoading, setIsLoading] = useState(false);
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          setOriginalImage(event.target.result as string);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (event) => {
          if (event.target?.result) {
            setOriginalImage(event.target.result as string);
          }
        };
        reader.readAsDataURL(file);
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!originalImage || !prompt) {
      alert('请上传图片并输入提示词');
      return;
    }
    
    setIsLoading(true);
    
    try {
      // 实际应用中，这里需要上传原始图片到服务器获取URL
      // 目前使用模拟数据
      const requestData = {
        image_url: originalImage, // 实际应用中应为服务器URL
        prompt,
        strength,
        style
      };
      
      const response = await multimediaApi.imageToImage(requestData);
      setGeneratedImage(response.data.image);
    } catch (error) {
      console.error('图像转换失败:', error);
      alert('图像转换失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = () => {
    if (originalImage && prompt) {
      handleSubmit(new Event('submit') as any);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>图生图</CardTitle>
        <CardDescription>基于参考图像和文本描述生成新图像</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label>上传参考图片</Label>
            <div
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
              }`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              {originalImage ? (
                <div className="relative">
                  <img 
                    src={originalImage} 
                    alt="Reference" 
                    className="mx-auto max-h-60 rounded-md object-contain"
                  />
                  <p className="mt-2 text-sm text-gray-500">点击更换图片</p>
                </div>
              ) : (
                <div className="space-y-2">
                  <Upload className="mx-auto h-10 w-10 text-gray-400" />
                  <p className="text-sm text-gray-500">拖拽图片到这里或点击上传</p>
                  <p className="text-xs text-gray-400">支持 JPG, PNG, WEBP 格式</p>
                </div>
              )}
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileUpload}
                accept="image/*"
                className="hidden"
              />
            </div>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="prompt">提示词</Label>
            <Textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="描述您希望如何转换这张图片..."
              rows={3}
              required
            />
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between">
              <Label>变换强度: {(strength * 100).toFixed(0)}%</Label>
            </div>
            <Slider
              value={[strength]}
              onValueChange={(value) => setStrength(value[0])}
              max={1}
              min={0.1}
              step={0.1}
              className="w-full"
            />
            <p className="text-xs text-gray-500">
              控制原始图像特征保留程度，数值越低变化越大
            </p>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="style">目标风格</Label>
            <Input
              id="style"
              value={style}
              onChange={(e) => setStyle(e.target.value)}
              placeholder="例如：动漫、油画、素描等"
            />
          </div>
          
          <div className="flex flex-col sm:flex-row gap-3">
            <Button type="submit" disabled={isLoading || !originalImage || !prompt} className="flex-1">
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  生成中...
                </>
              ) : (
                '生成图像'
              )}
            </Button>
            
            {generatedImage && (
              <Button type="button" variant="secondary" onClick={handleRegenerate} disabled={isLoading}>
                <RotateCcw className="mr-2 h-4 w-4" />
                重新生成
              </Button>
            )}
          </div>
        </form>
        
        {generatedImage && (
          <div className="mt-8">
            <h3 className="text-lg font-medium mb-4">生成的图像</h3>
            <div className="flex justify-center">
              <div className="relative group">
                <img 
                  src={generatedImage} 
                  alt="Generated" 
                  className="max-h-96 rounded-lg object-contain"
                />
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <Button size="sm" variant="secondary">
                    <Download className="h-4 w-4 mr-1" />
                    下载
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}