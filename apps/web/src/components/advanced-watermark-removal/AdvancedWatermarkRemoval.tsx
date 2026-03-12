'use client';

import { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Upload, 
  Download, 
  MousePointer, 
  Square, 
  Droplets, 
  ScanEye, 
  Wand2,
  Eye,
  EyeOff
} from 'lucide-react';
import api from '@/lib/api';

const AdvancedWatermarkRemoval = () => {
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [processedImage, setProcessedImage] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [brushSize, setBrushSize] = useState(20);
  const [mode, setMode] = useState<'brush' | 'rectangle' | 'auto'>('brush');
  const [showMask, setShowMask] = useState(false);
  const [clickPositions, setClickPositions] = useState<{x: number, y: number}[]>([]);
  const [rectangles, setRectangles] = useState<{x: number, y: number, width: number, height: number}[]>([]);
  const [currentRect, setCurrentRect] = useState<{x: number, y: number, width: number, height: number} | null>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imageRef = useRef<HTMLImageElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // 处理文件上传
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setOriginalImage(e.target?.result as string);
        setProcessedImage(null);
        setClickPositions([]);
        setRectangles([]);
        setCurrentRect(null);
      };
      reader.readAsDataURL(file);
    }
  };

  // 在图像上绘制遮罩
  useEffect(() => {
    if (!originalImage || !imageRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const img = imageRef.current;

    if (!ctx) return;

    // 设置画布尺寸为图像尺寸
    canvas.width = img.width;
    canvas.height = img.height;

    // 清除画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 绘制点击位置的圆圈
    if (mode === 'brush' && clickPositions.length > 0) {
      ctx.fillStyle = 'rgba(255, 0, 0, 0.5)';
      clickPositions.forEach(pos => {
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, brushSize, 0, Math.PI * 2);
        ctx.fill();
      });
    }

    // 绘制矩形区域
    if (mode === 'rectangle') {
      ctx.fillStyle = 'rgba(0, 255, 0, 0.5)';
      rectangles.forEach(rect => {
        ctx.fillRect(rect.x, rect.y, rect.width, rect.height);
      });

      // 绘制当前正在绘制的矩形
      if (currentRect) {
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 2;
        ctx.strokeRect(currentRect.x, currentRect.y, currentRect.width, currentRect.height);
      }
    }
  }, [originalImage, clickPositions, rectangles, currentRect, mode, brushSize]);

  // 处理图像上的点击事件（涂抹模式）
  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (mode !== 'brush' || !imageRef.current) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    setClickPositions(prev => [...prev, { x, y }]);
  };

  // 处理鼠标按下事件（矩形模式）
  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (mode !== 'rectangle' || !imageRef.current) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    const startX = (e.clientX - rect.left) * scaleX;
    const startY = (e.clientY - rect.top) * scaleY;

    setIsDrawing(true);
    setCurrentRect({ x: startX, y: startY, width: 0, height: 0 });
  };

  // 处理鼠标移动事件（矩形模式）
  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing || mode !== 'rectangle' || !currentRect || !imageRef.current) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    const currentX = (e.clientX - rect.left) * scaleX;
    const currentY = (e.clientY - rect.top) * scaleY;

    const width = currentX - currentRect.x;
    const height = currentY - currentRect.y;

    setCurrentRect({
      x: currentRect.x,
      y: currentRect.y,
      width,
      height
    });
  };

  // 处理鼠标释放事件（矩形模式）
  const handleMouseUp = () => {
    if (!isDrawing || mode !== 'rectangle' || !currentRect) return;

    // 只有当矩形足够大时才添加到列表中
    if (Math.abs(currentRect.width) > 10 && Math.abs(currentRect.height) > 10) {
      setRectangles(prev => [...prev, { ...currentRect }]);
    }

    setIsDrawing(false);
    setCurrentRect(null);
  };

  // 清除所有标记
  const clearAllMarks = () => {
    setClickPositions([]);
    setRectangles([]);
    setCurrentRect(null);
  };

  // 执行去水印处理
  const handleRemoveWatermark = async () => {
    if (!originalImage) return;

    setIsProcessing(true);
    setProgress(10);

    try {
      // 创建临时文件
      const response = await fetch(originalImage);
      const blob = await response.blob();
      const file = new File([blob], 'input_image.jpg', { type: 'image/jpeg' });

      const formData = new FormData();
      formData.append('file', file);

      // 根据模式选择不同的API端点
      let result;
      
      if (mode === 'brush' && clickPositions.length > 0) {
        // 涂抹模式：通过点击位置去除水印
        setProgress(30);
        
        result = await api.post('/advanced-watermark-removal/by-clicks', {
          clicks: clickPositions.map(pos => [pos.x, pos.y]),
          brush_radius: brushSize
        });
      } else if (mode === 'rectangle' && rectangles.length > 0) {
        // 矩形模式：通过坐标去除水印
        setProgress(30);
        
        const coords = rectangles.map(rect => [
          Math.min(rect.x, rect.x + rect.width),
          Math.min(rect.y, rect.y + rect.height),
          Math.abs(rect.width),
          Math.abs(rect.height)
        ]);
        
        result = await api.post('/advanced-watermark-removal/by-coordinates', {
          coordinates: coords
        });
      } else if (mode === 'auto') {
        // 自动检测模式
        setProgress(30);
        
        result = await api.post('/advanced-watermark-removal/by-segmentation');
      } else {
        throw new Error('请至少标记一个要去除的区域');
      }

      setProgress(80);
      
      // 更新处理后的图像
      // 这里应该从API响应中获取处理后的图像URL
      // 为了演示目的，我们暂时使用原图
      setProcessedImage(originalImage);
      
      setProgress(100);
      setTimeout(() => setProgress(0), 1000);
    } catch (error) {
      console.error('去水印处理失败:', error);
      alert(`去水印处理失败: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // 自动检测水印区域
  const handleDetectWatermarks = async () => {
    if (!originalImage) return;

    try {
      const response = await fetch(originalImage);
      const blob = await response.blob();
      const file = new File([blob], 'input_image.jpg', { type: 'image/jpeg' });

      const formData = new FormData();
      formData.append('file', file);

      const result = await api.post('/advanced-watermark-removal/detect-areas', formData);
      
      // 在实际应用中，这里应该根据检测结果在图像上标记区域
      alert(`检测到 ${result.data.total_detected} 个潜在水印区域`);
    } catch (error) {
      console.error('水印检测失败:', error);
      alert(`水印检测失败: ${error.message}`);
    }
  };

  return (
    <div className="container mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">🎨 高级去水印工具</h1>
        <p className="text-gray-600">使用多种技术去除图像中的水印，支持涂抹选择和智能检测</p>
      </div>

      {/* 控制面板 */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>处理控制</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex flex-wrap gap-4 items-center">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              accept="image/*"
              className="hidden"
            />
            <Button onClick={() => fileInputRef.current?.click()}>
              <Upload className="h-4 w-4 mr-2" />
              上传图像
            </Button>
            
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium">模式:</span>
              <div className="flex bg-gray-100 rounded-lg p-1">
                <Button
                  variant={mode === 'brush' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setMode('brush')}
                  className="flex items-center gap-1"
                >
                  <MousePointer className="h-4 w-4" />
                  涂抹
                </Button>
                <Button
                  variant={mode === 'rectangle' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setMode('rectangle')}
                  className="flex items-center gap-1"
                >
                  <Square className="h-4 w-4" />
                  矩形
                </Button>
                <Button
                  variant={mode === 'auto' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setMode('auto')}
                  className="flex items-center gap-1"
                >
                  <Wand2 className="h-4 w-4" />
                  自动
                </Button>
              </div>
            </div>
            
            {mode === 'brush' && (
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium">笔刷大小:</span>
                <Slider
                  value={[brushSize]}
                  onValueChange={(value) => setBrushSize(value[0])}
                  max={50}
                  min={5}
                  step={1}
                  className="w-32"
                />
                <span className="text-sm w-8">{brushSize}px</span>
              </div>
            )}
            
            <Button onClick={clearAllMarks} variant="outline">
              清除标记
            </Button>
            
            <Button onClick={handleDetectWatermarks} variant="outline">
              <ScanEye className="h-4 w-4 mr-2" />
              检测水印
            </Button>
            
            <Button 
              onClick={handleRemoveWatermark} 
              disabled={!originalImage || isProcessing}
              className="bg-blue-600 hover:bg-blue-700"
            >
              {isProcessing ? (
                <>
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent mr-2"></div>
                  处理中...
                </>
              ) : (
                <>
                  <Droplets className="h-4 w-4 mr-2" />
                  去除水印
                </>
              )}
            </Button>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowMask(!showMask)}
              >
                {showMask ? <EyeOff className="h-4 w-4 mr-2" /> : <Eye className="h-4 w-4 mr-2" />}
                {showMask ? '隐藏遮罩' : '显示遮罩'}
              </Button>
            </div>
            
            {clickPositions.length > 0 && (
              <Badge variant="secondary">
                已标记 {clickPositions.length} 个点
              </Badge>
            )}
            
            {rectangles.length > 0 && (
              <Badge variant="secondary">
                已标记 {rectangles.length} 个区域
              </Badge>
            )}
          </div>
          
          {isProcessing && (
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>处理进度</span>
                <span>{progress}%</span>
              </div>
              <Progress value={progress} className="w-full" />
            </div>
          )}
        </CardContent>
      </Card>

      {/* 图像处理区域 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* 原图 */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              原始图像
              {originalImage && <Badge variant="outline">已上传</Badge>}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {originalImage ? (
              <div className="relative inline-block">
                <img
                  ref={imageRef}
                  src={originalImage}
                  alt="Original"
                  className="max-w-full h-auto rounded-lg border"
                />
                <canvas
                  ref={canvasRef}
                  className={`absolute top-0 left-0 pointer-events-none ${showMask ? 'opacity-100' : 'opacity-0'} transition-opacity`}
                  onClick={handleCanvasClick}
                  onMouseDown={handleMouseDown}
                  onMouseMove={handleMouseMove}
                  onMouseUp={handleMouseUp}
                  onMouseLeave={handleMouseUp}
                />
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-96 border-2 border-dashed border-gray-300 rounded-lg">
                <Upload className="h-12 w-12 text-gray-400 mb-4" />
                <p className="text-gray-500 mb-4">点击上传按钮选择图像</p>
                <p className="text-sm text-gray-400">支持 JPG, PNG, WEBP 格式</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* 处理后图像 */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              处理后图像
              {processedImage && <Badge variant="default">已完成</Badge>}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {processedImage ? (
              <div className="flex flex-col items-center">
                <img
                  src={processedImage}
                  alt="Processed"
                  className="max-w-full h-auto rounded-lg border"
                />
                <Button className="mt-4">
                  <Download className="h-4 w-4 mr-2" />
                  下载图像
                </Button>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-96 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50">
                <Droplets className="h-12 w-12 text-gray-400 mb-4" />
                <p className="text-gray-500 mb-2">处理后的图像将在此显示</p>
                <p className="text-sm text-gray-400">点击"去除水印"按钮开始处理</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* 说明 */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>使用说明</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <h3 className="font-semibold flex items-center gap-2">
                <MousePointer className="h-4 w-4 text-blue-500" />
                涂抹模式
              </h3>
              <p className="text-sm text-gray-600">
                点击要移除的水印区域，系统将使用AI算法进行智能修复
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold flex items-center gap-2">
                <Square className="h-4 w-4 text-green-500" />
                矩形模式
              </h3>
              <p className="text-sm text-gray-600">
                拖拽选择水印区域，精确控制要去除的范围
              </p>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold flex items-center gap-2">
                <Wand2 className="h-4 w-4 text-purple-500" />
                自动模式
              </h3>
              <p className="text-sm text-gray-600">
                智能检测图像中的水印区域并自动处理
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AdvancedWatermarkRemoval;