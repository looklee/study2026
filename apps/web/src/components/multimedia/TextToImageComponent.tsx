'use client'

import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Loader2, Upload, Download, RotateCcw } from 'lucide-react';
import { multimediaApi } from '@/lib/api';

export default function TextToImageComponent() {
  const [prompt, setPrompt] = useState('');
  const [negativePrompt, setNegativePrompt] = useState('');
  const [width, setWidth] = useState(1024);
  const [height, setHeight] = useState(1024);
  const [numImages, setNumImages] = useState(1);
  const [style, setStyle] = useState('realistic');
  const [isLoading, setIsLoading] = useState(false);
  const [generatedImages, setGeneratedImages] = useState<string[]>([]);
  const [styles, setStyles] = useState<string[]>([]);

  const canvasRef = useRef<HTMLCanvasElement>(null);

  // 获取支持的样式
  const fetchStyles = async () => {
    try {
      const response = await multimediaApi.getStyles();
      setStyles(response.data.styles);
    } catch (error) {
      console.error('获取样式失败:', error);
    }
  };

  // 组件挂载时获取样式
  useEffect(() => {
    fetchStyles();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const requestData = {
        prompt,
        negative_prompt: negativePrompt,
        width,
        height,
        num_images: numImages,
        style
      };
      
      const response = await multimediaApi.textToImage(requestData);
      setGeneratedImages(response.data.images);
    } catch (error) {
      console.error('生成图像失败:', error);
      alert('生成图像失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = () => {
    if (prompt) {
      handleSubmit(new Event('submit') as any);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>文生图</CardTitle>
        <CardDescription>输入文本描述，生成相应图像</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="prompt">提示词</Label>
            <Textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="描述您想要生成的图像..."
              rows={3}
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="negativePrompt">负面提示词</Label>
            <Textarea
              id="negativePrompt"
              value={negativePrompt}
              onChange={(e) => setNegativePrompt(e.target.value)}
              placeholder="不希望出现的元素..."
              rows={2}
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>宽度: {width}px</Label>
              <Slider
                value={[width]}
                onValueChange={(value) => setWidth(value[0])}
                max={1536}
                min={256}
                step={64}
                className="w-full"
              />
            </div>
            
            <div className="space-y-2">
              <Label>高度: {height}px</Label>
              <Slider
                value={[height]}
                onValueChange={(value) => setHeight(value[0])}
                max={1536}
                min={256}
                step={64}
                className="w-full"
              />
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="numImages">生成数量: {numImages}</Label>
              <Slider
                value={[numImages]}
                onValueChange={(value) => setNumImages(value[0])}
                max={4}
                min={1}
                step={1}
                className="w-full"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="style">风格</Label>
              <Select value={style} onValueChange={setStyle}>
                <SelectTrigger id="style">
                  <SelectValue placeholder="选择风格" />
                </SelectTrigger>
                <SelectContent>
                  {styles.map((s) => (
                    <SelectItem key={s} value={s}>
                      {s}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-3">
            <Button type="submit" disabled={isLoading} className="flex-1">
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  生成中...
                </>
              ) : (
                '生成图像'
              )}
            </Button>
            
            {generatedImages.length > 0 && (
              <Button type="button" variant="secondary" onClick={handleRegenerate} disabled={isLoading}>
                <RotateCcw className="mr-2 h-4 w-4" />
                重新生成
              </Button>
            )}
          </div>
        </form>
        
        {generatedImages.length > 0 && (
          <div className="mt-8">
            <h3 className="text-lg font-medium mb-4">生成的图像</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {generatedImages.map((imageUrl, index) => (
                <div key={index} className="relative group">
                  <img 
                    src={imageUrl} 
                    alt={`Generated ${index + 1}`} 
                    className="w-full h-auto rounded-lg object-cover aspect-square"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100">
                    <Button size="sm" variant="secondary" className="m-2">
                      <Download className="h-4 w-4 mr-1" />
                      下载
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}