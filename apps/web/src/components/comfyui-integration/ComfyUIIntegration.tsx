'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  Upload, 
  Download, 
  Image as ImageIcon, 
  Zap,
  Workflow,
  Settings,
  RefreshCw
} from 'lucide-react';
import api from '@/lib/api';

// 类型定义
interface ComfyUIStatus {
  status: string;
  connected: boolean;
  service: string;
}

interface QueueStatus {
  queue_remaining: number;
}

interface ModelInfo {
  models: string[];
  count: number;
}

interface GenerationResult {
  status: string;
  prompt_id: string;
  images: Array<{
    filename: string;
    subfolder: string;
    type: string;
    url: string;
  }>;
  timestamp: string;
}

interface WorkflowTemplate {
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

const ComfyUIIntegration = () => {
  const [status, setStatus] = useState<ComfyUIStatus | null>(null);
  const [queueStatus, setQueueStatus] = useState<QueueStatus | null>(null);
  const [models, setModels] = useState<ModelInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [generatedImages, setGeneratedImages] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState('text-to-image');
  const [templates, setTemplates] = useState<WorkflowTemplate[]>([]);

  // 表单状态
  const [textToImageForm, setTextToImageForm] = useState({
    prompt: '',
    negativePrompt: '',
    width: 1024,
    height: 1024,
    steps: 20,
    cfg: 8.0,
    seed: -1,
    modelName: 'model.safetensors'
  });

  const [imageToImageForm, setImageToImageForm] = useState({
    image: null as File | null,
    prompt: '',
    negativePrompt: '',
    width: 512,
    height: 512,
    steps: 20,
    cfg: 8.0,
    denoise: 0.7,
    seed: -1,
    modelName: 'model.safetensors'
  });

  const [inpaintingForm, setInpaintingForm] = useState({
    image: null as File | null,
    mask: null as File | null,
    prompt: '',
    negativePrompt: '',
    steps: 20,
    cfg: 8.0,
    denoise: 0.7,
    seed: -1,
    modelName: 'model.safetensors'
  });

  // 加载初始数据
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setIsLoading(true);
    try {
      // 检查服务状态
      const statusRes = await api.get('/comfyui/health');
      setStatus(statusRes.data);

      // 获取队列状态
      const queueRes = await api.get('/comfyui/queue-status');
      setQueueStatus(queueRes.data);

      // 获取模型列表
      const modelsRes = await api.get('/comfyui/models');
      setModels(modelsRes.data);

      // 获取工作流模板
      const templatesRes = await api.get('/comfyui/workflow-templates');
      setTemplates(templatesRes.data.templates);
    } catch (error) {
      console.error('加载初始数据失败:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const refreshStatus = async () => {
    setIsLoading(true);
    await loadInitialData();
    setIsLoading(false);
  };

  const handleGenerate = async () => {
    setIsGenerating(true);
    setProgress(0);

    try {
      let result: GenerationResult;

      if (activeTab === 'text-to-image') {
        result = await api.post('/comfyui/quick/text-to-image', {
          prompt: textToImageForm.prompt,
          negative_prompt: textToImageForm.negativePrompt,
          width: textToImageForm.width,
          height: textToImageForm.height,
          steps: textToImageForm.steps,
          cfg: textToImageForm.cfg,
          seed: textToImageForm.seed,
          model_name: textToImageForm.modelName
        });
      } else if (activeTab === 'image-to-image') {
        // 上传图像
        const formData = new FormData();
        if (imageToImageForm.image) {
          formData.append('file', imageToImageForm.image);
          // 这里需要先上传图像到ComfyUI
          const uploadRes = await api.post('/comfyui/upload-image', formData);
          const imageName = uploadRes.data.filename;

          result = await api.post('/comfyui/quick/image-to-image', {
            image_name: imageName,
            prompt: imageToImageForm.prompt,
            negative_prompt: imageToImageForm.negativePrompt,
            width: imageToImageForm.width,
            height: imageToImageForm.height,
            steps: imageToImageForm.steps,
            cfg: imageToImageForm.cfg,
            denoise: imageToImageForm.denoise,
            seed: imageToImageForm.seed,
            model_name: imageToImageForm.modelName
          });
        } else {
          throw new Error('请选择一张图像');
        }
      } else if (activeTab === 'inpainting') {
        // 上传图像和蒙版
        if (!inpaintingForm.image || !inpaintingForm.mask) {
          throw new Error('请选择图像和蒙版');
        }

        const imageFormData = new FormData();
        imageFormData.append('file', inpaintingForm.image);
        const imageUploadRes = await api.post('/comfyui/upload-image', imageFormData);
        const imageName = imageUploadRes.data.filename;

        const maskFormData = new FormData();
        maskFormData.append('file', inpaintingForm.mask);
        const maskUploadRes = await api.post('/comfyui/upload-image', maskFormData);
        const maskName = maskUploadRes.data.filename;

        result = await api.post('/comfyui/quick/inpainting', {
          image_name: imageName,
          mask_name: maskName,
          prompt: inpaintingForm.prompt,
          negative_prompt: inpaintingForm.negativePrompt,
          steps: inpaintingForm.steps,
          cfg: inpaintingForm.cfg,
          denoise: inpaintingForm.denoise,
          seed: inpaintingForm.seed,
          model_name: inpaintingForm.modelName
        });
      } else {
        throw new Error('未知的操作类型');
      }

      // 更新进度
      setProgress(100);

      // 显示生成的图像
      if (result.images && result.images.length > 0) {
        const imageUrls = result.images.map(img => img.url);
        setGeneratedImages(imageUrls);
      }
    } catch (error) {
      console.error('生成失败:', error);
      alert(`生成失败: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>, setter: React.Dispatch<any>) => {
    if (e.target.files && e.target.files[0]) {
      setter(e.target.files[0]);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="h-8 w-8 animate-spin text-blue-500" />
        <span className="ml-2">加载中...</span>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">🎨 ComfyUI 集成</h1>
        <p className="text-gray-600">与本地 ComfyUI 实例集成，实现高级AI图像生成</p>
      </div>

      {/* 状态卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">服务状态</CardTitle>
            <Zap className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {status?.connected ? '已连接' : '未连接'}
            </div>
            <p className="text-xs text-muted-foreground">
              {status?.status}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">队列状态</CardTitle>
            <Workflow className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {queueStatus?.queue_remaining || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              待处理任务
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">模型数量</CardTitle>
            <Settings className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {models?.count || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              可用模型
            </p>
          </CardContent>
        </Card>
      </div>

      {/* 控制按钮 */}
      <div className="flex flex-wrap gap-4 mb-8">
        <Button onClick={refreshStatus} variant="outline">
          <RefreshCw className="h-4 w-4 mr-2" />
          刷新状态
        </Button>
        <Button variant="outline" disabled>
          <Pause className="h-4 w-4 mr-2" />
          暂停队列
        </Button>
        <Button variant="outline" disabled>
          <RotateCcw className="h-4 w-4 mr-2" />
          清空队列
        </Button>
      </div>

      {/* 生成选项卡 */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="mb-8">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="text-to-image">文生图</TabsTrigger>
          <TabsTrigger value="image-to-image">图生图</TabsTrigger>
          <TabsTrigger value="inpainting">局部重绘</TabsTrigger>
        </TabsList>

        {/* 文生图选项卡 */}
        <TabsContent value="text-to-image">
          <Card>
            <CardHeader>
              <CardTitle>文本到图像生成</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="prompt">正向提示词</Label>
                    <Textarea
                      id="prompt"
                      value={textToImageForm.prompt}
                      onChange={(e) => setTextToImageForm({...textToImageForm, prompt: e.target.value})}
                      placeholder="描述你想要生成的图像..."
                      rows={4}
                    />
                  </div>

                  <div>
                    <Label htmlFor="negativePrompt">负向提示词</Label>
                    <Textarea
                      id="negativePrompt"
                      value={textToImageForm.negativePrompt}
                      onChange={(e) => setTextToImageForm({...textToImageForm, negativePrompt: e.target.value})}
                      placeholder="不希望出现的元素..."
                      rows={2}
                    />
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="width">宽度</Label>
                      <Input
                        id="width"
                        type="number"
                        value={textToImageForm.width}
                        onChange={(e) => setTextToImageForm({...textToImageForm, width: parseInt(e.target.value) || 1024})}
                        min="256"
                        max="2048"
                      />
                    </div>
                    <div>
                      <Label htmlFor="height">高度</Label>
                      <Input
                        id="height"
                        type="number"
                        value={textToImageForm.height}
                        onChange={(e) => setTextToImageForm({...textToImageForm, height: parseInt(e.target.value) || 1024})}
                        min="256"
                        max="2048"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="steps">步数</Label>
                      <Input
                        id="steps"
                        type="number"
                        value={textToImageForm.steps}
                        onChange={(e) => setTextToImageForm({...textToImageForm, steps: parseInt(e.target.value) || 20})}
                        min="1"
                        max="100"
                      />
                    </div>
                    <div>
                      <Label htmlFor="cfg">CFG Scale</Label>
                      <Input
                        id="cfg"
                        type="number"
                        step="0.1"
                        value={textToImageForm.cfg}
                        onChange={(e) => setTextToImageForm({...textToImageForm, cfg: parseFloat(e.target.value) || 8.0})}
                        min="1"
                        max="20"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="seed">种子 (-1为随机)</Label>
                      <Input
                        id="seed"
                        type="number"
                        value={textToImageForm.seed}
                        onChange={(e) => setTextToImageForm({...textToImageForm, seed: parseInt(e.target.value) || -1})}
                      />
                    </div>
                    <div>
                      <Label htmlFor="modelName">模型</Label>
                      <Select
                        value={textToImageForm.modelName}
                        onValueChange={(value) => setTextToImageForm({...textToImageForm, modelName: value})}
                      >
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {models?.models?.map((model, index) => (
                            <SelectItem key={index} value={model}>{model}</SelectItem>
                          )) || (
                            <SelectItem value="model.safetensors">model.safetensors</SelectItem>
                          )}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </div>
              </div>

              <Button 
                onClick={handleGenerate} 
                disabled={isGenerating || !status?.connected}
                className="w-full"
              >
                {isGenerating ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    生成中...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    生成图像
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* 图生图选项卡 */}
        <TabsContent value="image-to-image">
          <Card>
            <CardHeader>
              <CardTitle>图像到图像生成</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="imageUpload">上传图像</Label>
                    <div className="flex items-center gap-2">
                      <Input
                        id="imageUpload"
                        type="file"
                        accept="image/*"
                        onChange={(e) => handleFileChange(e, (file: File) => setImageToImageForm({...imageToImageForm, image: file}))}
                      />
                      {imageToImageForm.image && (
                        <Badge variant="secondary">{imageToImageForm.image.name}</Badge>
                      )}
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="i2iPrompt">正向提示词</Label>
                    <Textarea
                      id="i2iPrompt"
                      value={imageToImageForm.prompt}
                      onChange={(e) => setImageToImageForm({...imageToImageForm, prompt: e.target.value})}
                      placeholder="描述你想要生成的图像..."
                      rows={4}
                    />
                  </div>

                  <div>
                    <Label htmlFor="i2iNegativePrompt">负向提示词</Label>
                    <Textarea
                      id="i2iNegativePrompt"
                      value={imageToImageForm.negativePrompt}
                      onChange={(e) => setImageToImageForm({...imageToImageForm, negativePrompt: e.target.value})}
                      placeholder="不希望出现的元素..."
                      rows={2}
                    />
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="i2iWidth">宽度</Label>
                      <Input
                        id="i2iWidth"
                        type="number"
                        value={imageToImageForm.width}
                        onChange={(e) => setImageToImageForm({...imageToImageForm, width: parseInt(e.target.value) || 512})}
                        min="256"
                        max="2048"
                      />
                    </div>
                    <div>
                      <Label htmlFor="i2iHeight">高度</Label>
                      <Input
                        id="i2iHeight"
                        type="number"
                        value={imageToImageForm.height}
                        onChange={(e) => setImageToImageForm({...imageToImageForm, height: parseInt(e.target.value) || 512})}
                        min="256"
                        max="2048"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="i2iSteps">步数</Label>
                      <Input
                        id="i2iSteps"
                        type="number"
                        value={imageToImageForm.steps}
                        onChange={(e) => setImageToImageForm({...imageToImageForm, steps: parseInt(e.target.value) || 20})}
                        min="1"
                        max="100"
                      />
                    </div>
                    <div>
                      <Label htmlFor="i2iCfg">CFG Scale</Label>
                      <Input
                        id="i2iCfg"
                        type="number"
                        step="0.1"
                        value={imageToImageForm.cfg}
                        onChange={(e) => setImageToImageForm({...imageToImageForm, cfg: parseFloat(e.target.value) || 8.0})}
                        min="1"
                        max="20"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="i2iDenoise">去噪强度</Label>
                      <Input
                        id="i2iDenoise"
                        type="number"
                        step="0.01"
                        value={imageToImageForm.denoise}
                        onChange={(e) => setImageToImageForm({...imageToImageForm, denoise: parseFloat(e.target.value) || 0.7})}
                        min="0"
                        max="1"
                      />
                    </div>
                    <div>
                      <Label htmlFor="i2iSeed">种子 (-1为随机)</Label>
                      <Input
                        id="i2iSeed"
                        type="number"
                        value={imageToImageForm.seed}
                        onChange={(e) => setImageToImageForm({...imageToImageForm, seed: parseInt(e.target.value) || -1})}
                      />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="i2iModelName">模型</Label>
                    <Select
                      value={imageToImageForm.modelName}
                      onValueChange={(value) => setImageToImageForm({...imageToImageForm, modelName: value})}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {models?.models?.map((model, index) => (
                          <SelectItem key={index} value={model}>{model}</SelectItem>
                        )) || (
                          <SelectItem value="model.safetensors">model.safetensors</SelectItem>
                        )}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>

              <Button 
                onClick={handleGenerate} 
                disabled={isGenerating || !status?.connected || !imageToImageForm.image}
                className="w-full"
              >
                {isGenerating ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    生成中...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    生成图像
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* 局部重绘选项卡 */}
        <TabsContent value="inpainting">
          <Card>
            <CardHeader>
              <CardTitle>局部重绘</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="inpImageUpload">上传图像</Label>
                    <div className="flex items-center gap-2">
                      <Input
                        id="inpImageUpload"
                        type="file"
                        accept="image/*"
                        onChange={(e) => handleFileChange(e, (file: File) => setInpaintingForm({...inpaintingForm, image: file}))}
                      />
                      {inpaintingForm.image && (
                        <Badge variant="secondary">{inpaintingForm.image.name}</Badge>
                      )}
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="inpMaskUpload">上传蒙版</Label>
                    <div className="flex items-center gap-2">
                      <Input
                        id="inpMaskUpload"
                        type="file"
                        accept="image/*"
                        onChange={(e) => handleFileChange(e, (file: File) => setInpaintingForm({...inpaintingForm, mask: file}))}
                      />
                      {inpaintingForm.mask && (
                        <Badge variant="secondary">{inpaintingForm.mask.name}</Badge>
                      )}
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="inpPrompt">正向提示词</Label>
                    <Textarea
                      id="inpPrompt"
                      value={inpaintingForm.prompt}
                      onChange={(e) => setInpaintingForm({...inpaintingForm, prompt: e.target.value})}
                      placeholder="描述你想要生成的图像..."
                      rows={4}
                    />
                  </div>

                  <div>
                    <Label htmlFor="inpNegativePrompt">负向提示词</Label>
                    <Textarea
                      id="inpNegativePrompt"
                      value={inpaintingForm.negativePrompt}
                      onChange={(e) => setInpaintingForm({...inpaintingForm, negativePrompt: e.target.value})}
                      placeholder="不希望出现的元素..."
                      rows={2}
                    />
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="inpSteps">步数</Label>
                      <Input
                        id="inpSteps"
                        type="number"
                        value={inpaintingForm.steps}
                        onChange={(e) => setInpaintingForm({...inpaintingForm, steps: parseInt(e.target.value) || 20})}
                        min="1"
                        max="100"
                      />
                    </div>
                    <div>
                      <Label htmlFor="inpCfg">CFG Scale</Label>
                      <Input
                        id="inpCfg"
                        type="number"
                        step="0.1"
                        value={inpaintingForm.cfg}
                        onChange={(e) => setInpaintingForm({...inpaintingForm, cfg: parseFloat(e.target.value) || 8.0})}
                        min="1"
                        max="20"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="inpDenoise">去噪强度</Label>
                      <Input
                        id="inpDenoise"
                        type="number"
                        step="0.01"
                        value={inpaintingForm.denoise}
                        onChange={(e) => setInpaintingForm({...inpaintingForm, denoise: parseFloat(e.target.value) || 0.7})}
                        min="0"
                        max="1"
                      />
                    </div>
                    <div>
                      <Label htmlFor="inpSeed">种子 (-1为随机)</Label>
                      <Input
                        id="inpSeed"
                        type="number"
                        value={inpaintingForm.seed}
                        onChange={(e) => setInpaintingForm({...inpaintingForm, seed: parseInt(e.target.value) || -1})}
                      />
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="inpModelName">模型</Label>
                    <Select
                      value={inpaintingForm.modelName}
                      onValueChange={(value) => setInpaintingForm({...inpaintingForm, modelName: value})}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {models?.models?.map((model, index) => (
                          <SelectItem key={index} value={model}>{model}</SelectItem>
                        )) || (
                          <SelectItem value="model.safetensors">model.safetensors</SelectItem>
                        )}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>

              <Button 
                onClick={handleGenerate} 
                disabled={isGenerating || !status?.connected || !inpaintingForm.image || !inpaintingForm.mask}
                className="w-full"
              >
                {isGenerating ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    生成中...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    生成图像
                  </>
                )}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* 生成进度 */}
      {isGenerating && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>生成进度</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <Progress value={progress} className="w-full" />
              <p className="text-sm text-gray-600">正在生成图像，请稍候...</p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* 生成结果 */}
      {generatedImages.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>生成结果</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {generatedImages.map((url, index) => (
                <div key={index} className="overflow-hidden rounded-lg border">
                  <img 
                    src={url} 
                    alt={`Generated ${index + 1}`} 
                    className="w-full h-auto object-cover aspect-square"
                  />
                  <div className="p-2 bg-gray-50">
                    <Button variant="outline" size="sm" className="w-full">
                      <Download className="h-4 w-4 mr-2" />
                      下载
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ComfyUIIntegration;