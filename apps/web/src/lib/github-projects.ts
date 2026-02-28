// GitHub 热门开源项目数据库

export interface GitHubProject {
  id: string
  name: string
  repo: string
  url: string
  description: string
  category: string
  tags: string[]
  stars: number
  language: string
  trending: boolean
  aiRelated: boolean
}

export const githubProjects: GitHubProject[] = [
  // ============== AI/LLM 相关 (8 个) ==============
  {
    id: 'gh001',
    name: 'ChatGPT-Next-Web',
    repo: 'ChatGPTNextWeb/ChatGPT-Next-Web',
    url: 'https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web',
    description: '一键免费部署你的私人 ChatGPT 网页应用，支持 GPT4、GPT3.5 和 Claude',
    category: 'AI/LLM',
    tags: ['ChatGPT', 'Web 应用', '部署'],
    stars: 68000,
    language: 'TypeScript',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh002',
    name: 'LangChain',
    repo: 'langchain-ai/langchain',
    url: 'https://github.com/langchain-ai/langchain',
    description: '构建 LLM 应用的框架，支持链式调用、Agent、RAG 等',
    category: 'AI/LLM',
    tags: ['LLM', '框架', 'Agent'],
    stars: 82000,
    language: 'Python',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh003',
    name: 'LlamaFactory',
    repo: 'hiyouga/LLaMA-Factory',
    url: 'https://github.com/hiyouga/LLaMA-Factory',
    description: '一站式大模型微调平台，支持 LLaMA、Qwen、ChatGLM 等',
    category: 'AI/LLM',
    tags: ['微调', 'LLM', '训练'],
    stars: 28000,
    language: 'Python',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh004',
    name: 'Ollama',
    repo: 'ollama/ollama',
    url: 'https://github.com/ollama/ollama',
    description: '本地运行大模型的工具，支持 Llama2、Mistral 等开源模型',
    category: 'AI/LLM',
    tags: ['本地部署', 'LLM', '推理'],
    stars: 72000,
    language: 'Go',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh005',
    name: 'AnythingLLM',
    repo: 'Mintplex-Labs/anything-llm',
    url: 'https://github.com/Mintplex-Labs/anything-llm',
    description: '全栈 RAG 应用，支持文档问答、知识库管理',
    category: 'AI/LLM',
    tags: ['RAG', '知识库', '问答'],
    stars: 35000,
    language: 'TypeScript',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh006',
    name: 'AutoGPT',
    repo: 'Significant-Gravitas/AutoGPT',
    url: 'https://github.com/Significant-Gravitas/AutoGPT',
    description: '自主 AI Agent，能够自动完成任务',
    category: 'AI/LLM',
    tags: ['Agent', '自主 AI', '自动化'],
    stars: 158000,
    language: 'Python',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh007',
    name: 'ComfyUI',
    repo: 'comfyanonymous/ComfyUI',
    url: 'https://github.com/comfyanonymous/ComfyUI',
    description: 'Stable Diffusion 图形化界面，节点式工作流',
    category: 'AI/LLM',
    tags: ['Stable Diffusion', 'AI 绘画', '工作流'],
    stars: 42000,
    language: 'Python',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh008',
    name: 'Dify',
    repo: 'langgenius/dify',
    url: 'https://github.com/langgenius/dify',
    description: 'LLM 应用开发平台，支持可视化编排和部署',
    category: 'AI/LLM',
    tags: ['LLM', '应用开发', '平台'],
    stars: 38000,
    language: 'TypeScript',
    trending: true,
    aiRelated: true
  },

  // ============== 开发工具 (5 个) ==============
  {
    id: 'gh009',
    name: 'Cursor',
    repo: 'getcursor/cursor',
    url: 'https://github.com/getcursor/cursor',
    description: 'AI 驱动的代码编辑器，支持 AI 对话和代码生成',
    category: '开发工具',
    tags: ['编辑器', 'AI', '编程'],
    stars: 25000,
    language: 'TypeScript',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh010',
    name: 'Continue',
    repo: 'continuedev/continue',
    url: 'https://github.com/continuedev/continue',
    description: '开源的 VS Code AI 编程助手',
    category: '开发工具',
    tags: ['VS Code', 'AI 编程', '插件'],
    stars: 18000,
    language: 'TypeScript',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh011',
    name: 'Trae',
    repo: 'trae-project/trae',
    url: 'https://github.com/trae-project/trae',
    description: '新一代 AI 原生 IDE',
    category: '开发工具',
    tags: ['IDE', 'AI', '开发环境'],
    stars: 12000,
    language: 'Rust',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh012',
    name: 'Devika',
    repo: 'stitionai/devika',
    url: 'https://github.com/stitionai/devika',
    description: 'AI 软件工程师，能够理解任务并编写代码',
    category: '开发工具',
    tags: ['AI Agent', '编程', '自动化'],
    stars: 32000,
    language: 'Python',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh013',
    name: 'Open Interpreter',
    repo: 'OpenInterpreter/open-interpreter',
    url: 'https://github.com/OpenInterpreter/open-interpreter',
    description: '用自然语言让 AI 执行代码',
    category: '开发工具',
    tags: ['AI', '代码执行', '自动化'],
    stars: 45000,
    language: 'Python',
    trending: true,
    aiRelated: true
  },

  // ============== 效率工具 (4 个) ==============
  {
    id: 'gh014',
    name: 'n8n',
    repo: 'n8n-io/n8n',
    url: 'https://github.com/n8n-io/n8n',
    description: '工作流自动化工具，支持 350+ 应用集成',
    category: '效率工具',
    tags: ['工作流', '自动化', '集成'],
    stars: 42000,
    language: 'TypeScript',
    trending: true,
    aiRelated: false
  },
  {
    id: 'gh015',
    name: 'Flowise',
    repo: 'FlowiseAI/Flowise',
    url: 'https://github.com/FlowiseAI/Flowise',
    description: '拖拽式构建 LangChain 应用',
    category: '效率工具',
    tags: ['LangChain', '可视化', '低代码'],
    stars: 28000,
    language: 'TypeScript',
    trending: true,
    aiRelated: true
  },
  {
    id: 'gh016',
    name: 'Appsmith',
    repo: 'appsmithorg/appsmith',
    url: 'https://github.com/appsmithorg/appsmith',
    description: '低代码内部工具开发平台',
    category: '效率工具',
    tags: ['低代码', '内部工具', '快速开发'],
    stars: 32000,
    language: 'TypeScript',
    trending: true,
    aiRelated: false
  },
  {
    id: 'gh017',
    name: 'Affine',
    repo: 'toeverything/AFFiNE',
    url: 'https://github.com/toeverything/AFFiNE',
    description: '开源的 Notion 替代品，支持文档和知识库',
    category: '效率工具',
    tags: ['笔记', '知识库', '协作'],
    stars: 35000,
    language: 'TypeScript',
    trending: true,
    aiRelated: false
  },

  // ============== 系统工具 (3 个) ==============
  {
    id: 'gh018',
    name: '1Panel',
    repo: '1Panel-dev/1Panel',
    url: 'https://github.com/1Panel-dev/1Panel',
    description: '现代化的 Linux 服务器管理面板',
    category: '系统工具',
    tags: ['服务器', '管理面板', '运维'],
    stars: 22000,
    language: 'Go',
    trending: true,
    aiRelated: false
  },
  {
    id: 'gh019',
    name: 'RustDesk',
    repo: 'rustdesk/rustdesk',
    url: 'https://github.com/rustdesk/rustdesk',
    description: '开源的远程桌面软件，TeamViewer 替代品',
    category: '系统工具',
    tags: ['远程桌面', '开源', '跨平台'],
    stars: 68000,
    language: 'Rust',
    trending: true,
    aiRelated: false
  },
  {
    id: 'gh020',
    name: 'Uptime Kuma',
    repo: 'louislam/uptime-kuma',
    url: 'https://github.com/louislam/uptime-kuma',
    description: '自托管的网站监控工具',
    category: '系统工具',
    tags: ['监控', '运维', '自托管'],
    stars: 48000,
    language: 'JavaScript',
    trending: true,
    aiRelated: false
  }
]

// 分类统计
export const projectStats = {
  total: githubProjects.length,
  aiRelated: githubProjects.filter(p => p.aiRelated).length,
  byCategory: {
    'AI/LLM': githubProjects.filter(p => p.category === 'AI/LLM').length,
    '开发工具': githubProjects.filter(p => p.category === '开发工具').length,
    '效率工具': githubProjects.filter(p => p.category === '效率工具').length,
    '系统工具': githubProjects.filter(p => p.category === '系统工具').length
  },
  totalStars: githubProjects.reduce((sum, p) => sum + p.stars, 0)
}

// 热门标签
export const projectTags = [
  'LLM', 'AI', 'Agent', '工作流', '自动化',
  '低代码', '可视化', '自托管', '开源', '跨平台'
]

// 按热度排序
export const topProjects = [...githubProjects].sort((a, b) => b.stars - a.stars).slice(0, 10)
