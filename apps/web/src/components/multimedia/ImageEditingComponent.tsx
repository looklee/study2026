'use client'

import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, Upload, Download, RotateCcw, Scissors } from 'lucide-react';
import { multimediaApi } from '@/lib/api';

export default function ImageEditingComponent() {
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [instruction, setInstruction] = useState('');
  const [maskImage, setMaskImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [editedImage, setEditedImage] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const maskInputRef = useRef<HTMLInputElement>(null);

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
    if (!originalImage || !instruction) {
      alert('请上传图片并输入编辑指令');
      return;
    }
    
    setIsLoading(true);
    
    try {
      const requestData = {
        image_url: originalImage, // 实际应用中应为服务器URL
        instruction,
        mask_url: maskImage || undefined // 可选参数
      };
      
      const response = await multimediaApi.editImage(requestData);
      setEditedImage(response.data.image);
    } catch (error) {
      console.error('图片编辑失败:', error);
      alert('图片编辑失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = () => {
    if (originalImage && instruction) {
      handleSubmit(new Event('submit') as any);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>图片编辑</CardTitle>
        <CardDescription>使用AI编辑或修复图片内容</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label>上传待编辑图片</Label>
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
                    alt="To edit" 
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
                onChange={(e) => handleFileUpload(e, 'image')}
                accept="image/*"
                className="hidden"
              />
            </div>
          </div>
          
          {originalImage && (
            <div className="space-y-2">
              <Label>蒙版图片 (可选)</Label>
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
                    <Scissors className="mx-auto h-8 w-8 text-gray-400" />
                    <p className="text-sm text-gray-500">点击上传蒙版图片</p>
                    <p className="text-xs text-gray-400">用于指定编辑区域</p>
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
          
          <div className="space-y-2">
            <Label htmlFor="instruction">编辑指令</Label>
            <Textarea
              id="instruction"
              value={instruction}
              onChange={(e) => setInstruction(e.target.value)}
              placeholder="描述您希望对图片进行的编辑..."
              rows={3}
              required
            />
          </div>
          
          <div className="flex flex-col sm:flex-row gap-3">
            <Button type="submit" disabled={isLoading || !originalImage || !instruction} className="flex-1">
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  编辑中...
                </>
              ) : (
                '编辑图片'
              )}
            </Button>
            
            {editedImage && (
              <Button type="button" variant="secondary" onClick={handleRegenerate} disabled={isLoading}>
                <RotateCcw className="mr-2 h-4 w-4" />
                重新编辑
              </Button>
            )}
          </div>
        </form>
        
        {editedImage && (
          <div className="mt-8">
            <h3 className="text-lg font-medium mb-4">编辑后的图片</h3>
            <div className="flex justify-center">
              <div className="relative group">
                <img 
                  src={editedImage} 
                  alt="Edited" 
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