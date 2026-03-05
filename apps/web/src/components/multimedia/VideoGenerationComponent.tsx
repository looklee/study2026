'use client'

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Slider } from '@/components/ui/slider';
import { Loader2, Play, Download, RotateCcw } from 'lucide-react';
import { multimediaApi } from '@/lib/api';

export default function VideoGenerationComponent() {
  const [prompt, setPrompt] = useState('');
  const [duration, setDuration] = useState(5);
  const [width, setWidth] = useState(1024);
  const [height, setHeight] = useState(576);
  const [fps, setFps] = useState(8);
  const [isLoading, setIsLoading] = useState(false);
  const [generatedVideo, setGeneratedVideo] = useState<string | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const requestData = {
        prompt,
        duration,
        width,
        height,
        frames_per_second: fps
      };
      
      const response = await multimediaApi.generateVideo(requestData);
      setGeneratedVideo(response.data.video);
      setJobId(response.data.job_id);
    } catch (error) {
      console.error('视频生成失败:', error);
      alert('视频生成失败，请重试');
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
        <CardTitle>视频生成</CardTitle>
        <CardDescription>根据文本描述生成视频内容</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="prompt">视频描述</Label>
            <Textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="描述您想要生成的视频内容..."
              rows={3}
              required
            />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>时长: {duration}秒</Label>
              </div>
              <Slider
                value={[duration]}
                onValueChange={(value) => setDuration(value[0])}
                max={30}
                min={1}
                step={1}
                className="w-full"
              />
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between">
                <Label>FPS: {fps}帧/秒</Label>
              </div>
              <Slider
                value={[fps]}
                onValueChange={(value) => setFps(value[0])}
                max={24}
                min={4}
                step={1}
                className="w-full"
              />
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>宽度: {width}px</Label>
              <Slider
                value={[width]}
                onValueChange={(value) => setWidth(value[0])}
                max={1920}
                min={640}
                step={64}
                className="w-full"
              />
            </div>
            
            <div className="space-y-2">
              <Label>高度: {height}px</Label>
              <Slider
                value={[height]}
                onValueChange={(value) => setHeight(value[0])}
                max={1080}
                min={480}
                step={64}
                className="w-full"
              />
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
                '生成视频'
              )}
            </Button>
            
            {generatedVideo && (
              <Button type="button" variant="secondary" onClick={handleRegenerate} disabled={isLoading}>
                <RotateCcw className="mr-2 h-4 w-4" />
                重新生成
              </Button>
            )}
          </div>
        </form>
        
        {generatedVideo && (
          <div className="mt-8">
            <h3 className="text-lg font-medium mb-4">生成的视频</h3>
            <div className="flex justify-center">
              <div className="relative group">
                {generatedVideo ? (
                  <video 
                    src={generatedVideo} 
                    controls 
                    className="max-w-full max-h-96 rounded-lg"
                  >
                    您的浏览器不支持视频播放
                  </video>
                ) : (
                  <div className="bg-gray-200 border-2 border-dashed rounded-xl w-full h-64 flex items-center justify-center">
                    <p className="text-gray-500">视频渲染中...</p>
                  </div>
                )}
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