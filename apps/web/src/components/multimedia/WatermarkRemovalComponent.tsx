'use client'

import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Loader2, Upload, Download, RotateCcw, Droplets, EyeOff, Wand2 } from 'lucide-react';
import { multimediaApi } from '@/lib/api';

export default function WatermarkRemovalComponent() {
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [maskImage, setMaskImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [resultImage, setResultImage] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [technique, setTechnique] = useState('auto');
  const [techniques, setTechniques] = useState<any[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const maskInputRef = useRef<HTMLInputElement>(null);

  // 获取可用的去水印技术
  useEffect(() => {
    const fetchTechniques = async () => {
      try {
        const response = await multimediaApi.getWatermarkRemovalTechniques();
        setTechniques(response.data.techniques);
        if (response.data.techniques.length > 0) {
          setTechnique(response.data.techniques[0].id);
        }
      } catch (error) {
        console.error('获取去水印技术失败:', error);
      }
    };

    fetchTechniques();
  }, []);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>, type: 'image' | 'mask') => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          if (type === 'image') {
            setOriginalImage(event.target.result as string);
          } else {
            setMaskImage(event.target.result as string);
          }
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
    if (!originalImage) {
      alert('请上传需要去水印的图片');
      return;
    }

    setIsLoading(true);

    try {
      const requestData = {
        image_url: originalImage, // 实际应用中应为服务器URL
        mask_url: maskImage || undefined, // 可选参数
        technique
      };

      const response = await multimediaApi.removeWatermark(requestData);
      // 直接使用返回的base64图像数据
      setResultImage(response.data.result_image);
    } catch (error) {
      console.error('去水印失败:', error);
      alert('去水印失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = () => {
    if (originalImage) {
      handleSubmit(new Event('submit') as any);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Droplets className="h-5 w-5" />
          图像去水印
        </CardTitle>
        <CardDescription>使用AI技术智能去除图片中的水印</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label>上传带水印的图片</Label>
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
                    alt="To remove watermark from"
                    className="mx-auto max-h-60 rounded-md object-contain"
                  />
                  <p className="mt-2 text-sm text-gray-500">点击更换图片</p>
                </div>
              ) : (
                <div className="space-y-2">
                  <EyeOff className="mx-auto h-10 w-10 text-gray-400" />
                  <p className="text-sm text-gray-500">拖拽图片到这里或点击上传</p>
                  <p className="text-xs text-gray-400">支持 JPG, PNG, WEBP 格式</p>
                </div>
              )}
              <input
                type="file"
                ref={fileInputRef}
                onChange={(e) => handleFileUpload(e, 'image')}
                accept="image/*"
                className="hidden"
              />
            </div>
          </div>

          {originalImage && (
            <div className="space-y-2">
              <Label>水印区域蒙版 (可选)</Label>
              <div
                className="border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors border-gray-300 hover:border-gray-400"
                onClick={() => maskInputRef.current?.click()}
              >
                {maskImage ? (
                  <div className="relative">
                    <img
                      src={maskImage}
                      alt="Mask"
                      className="mx-auto max-h-40 rounded-md object-contain"
                    />
                    <p className="mt-2 text-sm text-gray-500">点击更换蒙版</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <Wand2 className="mx-auto h-8 w-8 text-gray-400" />
                    <p className="text-sm text-gray-500">点击上传蒙版图片</p>
                    <p className="text-xs text-gray-400">用于指定水印位置（白色区域为水印）</p>
                  </div>
                )}
                <input
                  type="file"
                  ref={maskInputRef}
                  onChange={(e) => handleFileUpload(e, 'mask')}
                  accept="image/*"
                  className="hidden"
                />
              </div>
            </div>
          )}

          {originalImage && techniques.length > 0 && (
            <div className="space-y-2">
              <Label htmlFor="technique">去水印技术</Label>
              <Select value={technique} onValueChange={setTechnique}>
                <SelectTrigger id="technique">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {techniques.map((tech) => (
                    <SelectItem key={tech.id} value={tech.id}>
                      {tech.name} {tech.recommended && '(推荐)'}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-sm text-gray-500">
                {techniques.find(t => t.id === technique)?.description}
              </p>
            </div>
          )}

          <div className="flex flex-col sm:flex-row gap-3">
            <Button type="submit" disabled={isLoading || !originalImage} className="flex-1">
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  去除水印中...
                </>
              ) : (
                '开始去水印'
              )}
            </Button>

            {resultImage && (
              <Button type="button" variant="secondary" onClick={handleRegenerate} disabled={isLoading}>
                <RotateCcw className="mr-2 h-4 w-4" />
                重新处理
              </Button>
            )}
          </div>
        </form>

        {resultImage && (
          <div className="mt-8">
            <h3 className="text-lg font-medium mb-4">去水印后的图片</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">原图</h4>
                <div className="border rounded-lg overflow-hidden">
                  <img
                    src={originalImage!}
                    alt="Original"
                    className="w-full h-auto max-h-80 object-contain"
                  />
                </div>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">去水印后</h4>
                <div className="border rounded-lg overflow-hidden relative group">
                  <img
                    src={resultImage}
                    alt="Result"
                    className="w-full h-auto max-h-80 object-contain"
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
          </div>
        )}
      </CardContent>
    </Card>
  );
}