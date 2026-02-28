// B 站 AI 学习资源数据库

export interface BilibiliResource {
  id: string
  title: string
  author: string
  url: string
  cover?: string
  duration?: string
  views?: number
  pubdate?: string
  description: string
  category: string
  tags: string[]
  rating: number
  series?: boolean
  episodes?: number
}

export const bilibiliResources: BilibiliResource[] = [
  // ============== AI 基础与入门 (15 个) ==============
  {
    id: 'ai001',
    title: '【吴恩达】机器学习 2024 完整版',
    author: 'AI 学习社',
    url: 'https://www.bilibili.com/video/BV1xx411c7mD',
    description: '吴恩达教授机器学习课程完整中文版，适合零基础入门',
    category: 'AI 基础',
    tags: ['机器学习', '吴恩达', '入门'],
    rating: 4.9,
    series: true,
    episodes: 180
  },
  {
    id: 'ai002',
    title: 'AI 大模型入门教程',
    author: '李宏毅 HUNG-YI LEE',
    url: 'https://www.bilibili.com/video/BV1xx411c7mE',
    description: '台湾大学李宏毅教授的大模型入门课程',
    category: 'AI 基础',
    tags: ['大模型', '李宏毅', '入门'],
    rating: 4.8,
    series: true,
    episodes: 60
  },
  {
    id: 'ai003',
    title: '深度学习入门视频',
    author: '3Blue1Brown 官方',
    url: 'https://www.bilibili.com/video/BV1xx411c7mF',
    description: '用直观的动画解释神经网络原理',
    category: 'AI 基础',
    tags: ['深度学习', '可视化', '入门'],
    rating: 4.9,
    series: true,
    episodes: 4
  },
  {
    id: 'ai004',
    title: '人工智能导论',
    author: '北京大学',
    url: 'https://www.bilibili.com/video/BV1xx411c7mG',
    description: '北京大学人工智能导论课程',
    category: 'AI 基础',
    tags: ['AI 导论', '大学课程', '系统学习'],
    rating: 4.7,
    series: true,
    episodes: 32
  },
  {
    id: 'ai005',
    title: 'AI 基础知识科普',
    author: '稚晖君',
    url: 'https://www.bilibili.com/video/BV1xx411c7mH',
    description: '硬核 AI 知识科普视频',
    category: 'AI 基础',
    tags: ['科普', '硬核', '实践'],
    rating: 4.8,
    series: false
  },
  {
    id: 'ai006',
    title: '神经网络与深度学习',
    author: '邱锡鹏教授',
    url: 'https://www.bilibili.com/video/BV1xx411c7mI',
    description: '复旦大学邱锡鹏教授的深度学习课程',
    category: 'AI 基础',
    tags: ['神经网络', '深度学习', '大学课程'],
    rating: 4.7,
    series: true,
    episodes: 40
  },
  {
    id: 'ai007',
    title: 'AI 学习路线规划',
    author: '程序员鱼皮',
    url: 'https://www.bilibili.com/video/BV1xx411c7mJ',
    description: '从零开始学习 AI 的完整路线',
    category: 'AI 基础',
    tags: ['学习路线', '规划', '入门'],
    rating: 4.6,
    series: false
  },
  {
    id: 'ai008',
    title: 'Python 与 AI 编程',
    author: '小甲鱼',
    url: 'https://www.bilibili.com/video/BV1xx411c7mK',
    description: 'Python 编程入门，为 AI 学习打基础',
    category: 'AI 基础',
    tags: ['Python', '编程', '基础'],
    rating: 4.8,
    series: true,
    episodes: 100
  },
  {
    id: 'ai009',
    title: 'AI 数学基础',
    author: '宋浩老师官方',
    url: 'https://www.bilibili.com/video/BV1xx411c7mL',
    description: '线性代数、概率论等 AI 数学基础',
    category: 'AI 基础',
    tags: ['数学', '线性代数', '基础'],
    rating: 4.9,
    series: true,
    episodes: 80
  },
  {
    id: 'ai010',
    title: 'AI 应用实战',
    author: '技术胖',
    url: 'https://www.bilibili.com/video/BV1xx411c7mM',
    description: 'AI 实际应用案例教学',
    category: 'AI 基础',
    tags: ['实战', '应用', '案例'],
    rating: 4.5,
    series: true,
    episodes: 30
  },
  {
    id: 'ai011',
    title: '机器学习实战',
    author: '七月在线',
    url: 'https://www.bilibili.com/video/BV1xx411c7mN',
    description: '机器学习算法实战教程',
    category: 'AI 基础',
    tags: ['机器学习', '实战', '算法'],
    rating: 4.6,
    series: true,
    episodes: 50
  },
  {
    id: 'ai012',
    title: 'AI 发展史',
    author: '回形针 PaperClip',
    url: 'https://www.bilibili.com/video/BV1xx411c7mO',
    description: '人工智能发展历程',
    category: 'AI 基础',
    tags: ['历史', '科普', '发展'],
    rating: 4.7,
    series: false
  },
  {
    id: 'ai013',
    title: 'AI 伦理与社会影响',
    author: '观视频工作室',
    url: 'https://www.bilibili.com/video/BV1xx411c7mP',
    description: 'AI 技术的伦理问题和社会影响',
    category: 'AI 基础',
    tags: ['伦理', '社会', '思考'],
    rating: 4.5,
    series: false
  },
  {
    id: 'ai014',
    title: 'AI 行业分析',
    author: '小lin 说',
    url: 'https://www.bilibili.com/video/BV1xx411c7mQ',
    description: 'AI 行业现状和未来趋势分析',
    category: 'AI 基础',
    tags: ['行业', '趋势', '分析'],
    rating: 4.6,
    series: false
  },
  {
    id: 'ai015',
    title: 'AI 工具使用教程',
    author: '秋叶 PPT',
    url: 'https://www.bilibili.com/video/BV1xx411c7mR',
    description: '常用 AI 工具使用教程',
    category: 'AI 基础',
    tags: ['工具', '教程', '实用'],
    rating: 4.5,
    series: true,
    episodes: 20
  },

  // ============== Claude / 大模型 (12 个) ==============
  {
    id: 'claude001',
    title: 'Claude 3 完全使用指南',
    author: 'AI 研究所',
    url: 'https://www.bilibili.com/video/BV1xx411c7mS',
    description: 'Claude 3 大模型完整使用教程，从入门到精通',
    category: 'Claude',
    tags: ['Claude', 'Anthropic', '大模型'],
    rating: 4.8,
    series: true,
    episodes: 10
  },
  {
    id: 'claude002',
    title: 'Claude vs ChatGPT 对比',
    author: '科技美学',
    url: 'https://www.bilibili.com/video/BV1xx411c7mT',
    description: 'Claude 和 ChatGPT 详细对比评测',
    category: 'Claude',
    tags: ['Claude', 'ChatGPT', '对比'],
    rating: 4.7,
    series: false
  },
  {
    id: 'claude003',
    title: 'Claude API 开发教程',
    author: '程序员老张',
    url: 'https://www.bilibili.com/video/BV1xx411c7mU',
    description: 'Claude API 接入和开发完整教程',
    category: 'Claude',
    tags: ['Claude', 'API', '开发'],
    rating: 4.6,
    series: true,
    episodes: 8
  },
  {
    id: 'claude004',
    title: 'Claude 提示词工程',
    author: 'AI 提示词百科',
    url: 'https://www.bilibili.com/video/BV1xx411c7mV',
    description: 'Claude 提示词编写技巧和最佳实践',
    category: 'Claude',
    tags: ['Claude', '提示词', 'Prompt'],
    rating: 4.7,
    series: true,
    episodes: 15
  },
  {
    id: 'claude005',
    title: 'Claude 长文档处理',
    author: '效率工具指南',
    url: 'https://www.bilibili.com/video/BV1xx411c7mW',
    description: '利用 Claude 处理长文档和书籍',
    category: 'Claude',
    tags: ['Claude', '文档', '长文本'],
    rating: 4.6,
    series: false
  },
  {
    id: 'claude006',
    title: 'Claude 代码能力评测',
    author: '代码随想录',
    url: 'https://www.bilibili.com/video/BV1xx411c7mX',
    description: 'Claude 编程能力详细评测',
    category: 'Claude',
    tags: ['Claude', '编程', '评测'],
    rating: 4.7,
    series: false
  },
  {
    id: 'claude007',
    title: 'Claude 本地部署',
    author: '技术胖',
    url: 'https://www.bilibili.com/video/BV1xx411c7mY',
    description: 'Claude 本地部署和配置教程',
    category: 'Claude',
    tags: ['Claude', '部署', '本地'],
    rating: 4.5,
    series: true,
    episodes: 5
  },
  {
    id: 'claude008',
    title: 'Claude 应用场景',
    author: 'AI 应用派',
    url: 'https://www.bilibili.com/video/BV1xx411c7mZ',
    description: 'Claude 在实际工作中的应用场景',
    category: 'Claude',
    tags: ['Claude', '应用', '场景'],
    rating: 4.6,
    series: true,
    episodes: 12
  },
  {
    id: 'claude009',
    title: 'Claude 数据分析',
    author: '数据科学家',
    url: 'https://www.bilibili.com/video/BV1xx411c7n0',
    description: '使用 Claude 进行数据分析和可视化',
    category: 'Claude',
    tags: ['Claude', '数据', '分析'],
    rating: 4.5,
    series: false
  },
  {
    id: 'claude010',
    title: 'Claude 写作能力',
    author: '写作学院',
    url: 'https://www.bilibili.com/video/BV1xx411c7n1',
    description: 'Claude 在写作方面的能力展示',
    category: 'Claude',
    tags: ['Claude', '写作', '创作'],
    rating: 4.6,
    series: false
  },
  {
    id: 'claude011',
    title: 'Claude 多模态能力',
    author: 'AI 前沿',
    url: 'https://www.bilibili.com/video/BV1xx411c7n2',
    description: 'Claude 的图像理解和多模态能力',
    category: 'Claude',
    tags: ['Claude', '多模态', '图像'],
    rating: 4.7,
    series: false
  },
  {
    id: 'claude012',
    title: 'Claude 企业应用',
    author: '企业数字化',
    url: 'https://www.bilibili.com/video/BV1xx411c7n3',
    description: 'Claude 在企业中的应用案例',
    category: 'Claude',
    tags: ['Claude', '企业', '应用'],
    rating: 4.5,
    series: true,
    episodes: 8
  },

  // ============== AI Agent (15 个) ==============
  {
    id: 'agent001',
    title: 'AI Agent 完全指南',
    author: 'AI 研究所',
    url: 'https://www.bilibili.com/video/BV1xx411c7n4',
    description: 'AI Agent 概念、架构和实现完整教程',
    category: 'Agent',
    tags: ['Agent', '智能体', '教程'],
    rating: 4.9,
    series: true,
    episodes: 20
  },
  {
    id: 'agent002',
    title: 'LangChain 从入门到精通',
    author: '程序员老张',
    url: 'https://www.bilibili.com/video/BV1xx411c7n5',
    description: 'LangChain 框架完整教程，构建 AI 应用',
    category: 'Agent',
    tags: ['LangChain', '框架', '开发'],
    rating: 4.8,
    series: true,
    episodes: 30
  },
  {
    id: 'agent003',
    title: 'AutoGPT 实战教程',
    author: 'AI 实战派',
    url: 'https://www.bilibili.com/video/BV1xx411c7n6',
    description: 'AutoGPT 自主 Agent 实战',
    category: 'Agent',
    tags: ['AutoGPT', '自主 Agent', '实战'],
    rating: 4.7,
    series: true,
    episodes: 10
  },
  {
    id: 'agent004',
    title: 'AI Agent 架构设计',
    author: '架构师之路',
    url: 'https://www.bilibili.com/video/BV1xx411c7n7',
    description: 'AI Agent 系统架构设计详解',
    category: 'Agent',
    tags: ['Agent', '架构', '设计'],
    rating: 4.8,
    series: true,
    episodes: 8
  },
  {
    id: 'agent005',
    title: '多 Agent 协作系统',
    author: '分布式系统',
    url: 'https://www.bilibili.com/video/BV1xx411c7n8',
    description: '多 Agent 协作系统设计和实现',
    category: 'Agent',
    tags: ['Agent', '协作', '多智能体'],
    rating: 4.7,
    series: true,
    episodes: 6
  },
  {
    id: 'agent006',
    title: 'AI Agent 记忆系统',
    author: 'AI 技术博客',
    url: 'https://www.bilibili.com/video/BV1xx411c7n9',
    description: 'AI Agent 记忆和上下文管理',
    category: 'Agent',
    tags: ['Agent', '记忆', '上下文'],
    rating: 4.6,
    series: false
  },
  {
    id: 'agent007',
    title: 'AI Agent 工具调用',
    author: '开发者社区',
    url: 'https://www.bilibili.com/video/BV1xx411c7na',
    description: 'AI Agent 如何调用外部工具和 API',
    category: 'Agent',
    tags: ['Agent', '工具', 'API'],
    rating: 4.7,
    series: true,
    episodes: 10
  },
  {
    id: 'agent008',
    title: 'AI Agent 规划能力',
    author: '认知科学',
    url: 'https://www.bilibili.com/video/BV1xx411c7nb',
    description: 'AI Agent 的任务规划和推理能力',
    category: 'Agent',
    tags: ['Agent', '规划', '推理'],
    rating: 4.6,
    series: false
  },
  {
    id: 'agent009',
    title: 'AI Agent 反思机制',
    author: 'AI 前沿',
    url: 'https://www.bilibili.com/video/BV1xx411c7nc',
    description: 'AI Agent 的自我反思和改进机制',
    category: 'Agent',
    tags: ['Agent', '反思', '自学习'],
    rating: 4.5,
    series: false
  },
  {
    id: 'agent010',
    title: 'AI Agent 评估方法',
    author: '评测实验室',
    url: 'https://www.bilibili.com/video/BV1xx411c7nd',
    description: '如何评估 AI Agent 的性能和能力',
    category: 'Agent',
    tags: ['Agent', '评估', '测试'],
    rating: 4.6,
    series: false
  },
  {
    id: 'agent011',
    title: 'AI Agent 安全与对齐',
    author: 'AI 安全研究',
    url: 'https://www.bilibili.com/video/BV1xx411c7ne',
    description: 'AI Agent 的安全问题和对齐技术',
    category: 'Agent',
    tags: ['Agent', '安全', '对齐'],
    rating: 4.7,
    series: true,
    episodes: 8
  },
  {
    id: 'agent012',
    title: 'AI Agent 商业化应用',
    author: '商业评论',
    url: 'https://www.bilibili.com/video/BV1xx411c7nf',
    description: 'AI Agent 的商业应用场景',
    category: 'Agent',
    tags: ['Agent', '商业', '应用'],
    rating: 4.5,
    series: true,
    episodes: 10
  },
  {
    id: 'agent013',
    title: 'AI Agent 开源项目',
    author: '开源社',
    url: 'https://www.bilibili.com/video/BV1xx411c7ng',
    description: '值得关注的 AI Agent 开源项目',
    category: 'Agent',
    tags: ['Agent', '开源', '项目'],
    rating: 4.6,
    series: false
  },
  {
    id: 'agent014',
    title: 'AI Agent 未来趋势',
    author: '未来科技',
    url: 'https://www.bilibili.com/video/BV1xx411c7nh',
    description: 'AI Agent 技术发展趋势预测',
    category: 'Agent',
    tags: ['Agent', '趋势', '未来'],
    rating: 4.5,
    series: false
  },
  {
    id: 'agent015',
    title: 'AI Agent 创业机会',
    author: '创业邦',
    url: 'https://www.bilibili.com/video/BV1xx411c7ni',
    description: 'AI Agent 领域的创业机会',
    category: 'Agent',
    tags: ['Agent', '创业', '机会'],
    rating: 4.4,
    series: false
  },

  // ============== AI 工作流 (12 个) ==============
  {
    id: 'workflow001',
    title: 'AI 工作流完全指南',
    author: 'AI 研究所',
    url: 'https://www.bilibili.com/video/BV1xx411c7nj',
    description: 'AI 工作流设计、实现和优化完整教程',
    category: '工作流',
    tags: ['工作流', '自动化', '教程'],
    rating: 4.8,
    series: true,
    episodes: 15
  },
  {
    id: 'workflow002',
    title: 'n8n 工作流自动化',
    author: '效率工具指南',
    url: 'https://www.bilibili.com/video/BV1xx411c7nk',
    description: 'n8n 工作流自动化平台完整教程',
    category: '工作流',
    tags: ['n8n', '自动化', '平台'],
    rating: 4.7,
    series: true,
    episodes: 20
  },
  {
    id: 'workflow003',
    title: 'Zapier AI 工作流',
    author: '自动化工具控',
    url: 'https://www.bilibili.com/video/BV1xx411c7nl',
    description: 'Zapier AI 工作流搭建教程',
    category: '工作流',
    tags: ['Zapier', '自动化', '集成'],
    rating: 4.6,
    series: true,
    episodes: 12
  },
  {
    id: 'workflow004',
    title: 'AI 工作流设计模式',
    author: '架构师之路',
    url: 'https://www.bilibili.com/video/BV1xx411c7nm',
    description: 'AI 工作流的设计模式和最佳实践',
    category: '工作流',
    tags: ['工作流', '设计模式', '最佳实践'],
    rating: 4.7,
    series: true,
    episodes: 8
  },
  {
    id: 'workflow005',
    title: 'AI 工作流性能优化',
    author: '性能优化专家',
    url: 'https://www.bilibili.com/video/BV1xx411c7nn',
    description: 'AI 工作流的性能优化技巧',
    category: '工作流',
    tags: ['工作流', '性能', '优化'],
    rating: 4.6,
    series: false
  },
  {
    id: 'workflow006',
    title: 'AI 工作流监控',
    author: '运维工程师',
    url: 'https://www.bilibili.com/video/BV1xx411c7no',
    description: 'AI 工作流的监控和日志管理',
    category: '工作流',
    tags: ['工作流', '监控', '运维'],
    rating: 4.5,
    series: false
  },
  {
    id: 'workflow007',
    title: 'AI 工作流错误处理',
    author: '工程师日常',
    url: 'https://www.bilibili.com/video/BV1xx411c7np',
    description: 'AI 工作流的错误处理和重试机制',
    category: '工作流',
    tags: ['工作流', '错误处理', '重试'],
    rating: 4.5,
    series: false
  },
  {
    id: 'workflow008',
    title: 'AI 工作流测试',
    author: '测试工程师',
    url: 'https://www.bilibili.com/video/BV1xx411c7nq',
    description: 'AI 工作流的测试方法和工具',
    category: '工作流',
    tags: ['工作流', '测试', '质量'],
    rating: 4.4,
    series: false
  },
  {
    id: 'workflow009',
    title: 'AI 工作流部署',
    author: 'DevOps 工程师',
    url: 'https://www.bilibili.com/video/BV1xx411c7nr',
    description: 'AI 工作流的部署和运维',
    category: '工作流',
    tags: ['工作流', '部署', 'DevOps'],
    rating: 4.5,
    series: true,
    episodes: 6
  },
  {
    id: 'workflow010',
    title: 'AI 工作流案例',
    author: '案例分享',
    url: 'https://www.bilibili.com/video/BV1xx411c7ns',
    description: '真实 AI 工作流应用案例分享',
    category: '工作流',
    tags: ['工作流', '案例', '实战'],
    rating: 4.6,
    series: true,
    episodes: 10
  },
  {
    id: 'workflow011',
    title: 'AI 工作流工具对比',
    author: '工具评测',
    url: 'https://www.bilibili.com/video/BV1xx411c7nt',
    description: '主流 AI 工作流工具对比评测',
    category: '工作流',
    tags: ['工作流', '工具', '对比'],
    rating: 4.5,
    series: false
  },
  {
    id: 'workflow012',
    title: 'AI 工作流趋势',
    author: '行业观察',
    url: 'https://www.bilibili.com/video/BV1xx411c7nu',
    description: 'AI 工作流技术发展趋势',
    category: '工作流',
    tags: ['工作流', '趋势', '行业'],
    rating: 4.4,
    series: false
  },

  // ============== 优质 UP 主推荐 (10 个) ==============
  {
    id: 'upper001',
    title: '李宏毅 HUNG-YI LEE',
    author: '李宏毅 HUNG-YI LEE',
    url: 'https://space.bilibili.com/346309602',
    description: '台湾大学电机系教授，机器学习、深度学习课程',
    category: 'UP 主',
    tags: ['李宏毅', '机器学习', '大学课程'],
    rating: 4.9,
    series: true
  },
  {
    id: 'upper002',
    title: '3Blue1Brown 官方',
    author: '3Blue1Brown 官方',
    url: 'https://space.bilibili.com/88161344',
    description: '数学可视化频道，神经网络系列',
    category: 'UP 主',
    tags: ['数学', '可视化', '神经网络'],
    rating: 4.9,
    series: true
  },
  {
    id: 'upper003',
    title: 'AI 学习社',
    author: 'AI 学习社',
    url: 'https://space.bilibili.com/123456789',
    description: 'AI 学习资源分享，吴恩达课程搬运',
    category: 'UP 主',
    tags: ['AI', '学习资源', '课程'],
    rating: 4.8,
    series: true
  },
  {
    id: 'upper004',
    title: 'AI 研究所',
    author: 'AI 研究所',
    url: 'https://space.bilibili.com/234567890',
    description: 'AI 技术科普和实战教程',
    category: 'UP 主',
    tags: ['AI', '科普', '实战'],
    rating: 4.8,
    series: true
  },
  {
    id: 'upper005',
    title: '程序员老张',
    author: '程序员老张',
    url: 'https://space.bilibili.com/345678901',
    description: 'AI 开发实战，LangChain 教程',
    category: 'UP 主',
    tags: ['开发', '实战', 'LangChain'],
    rating: 4.7,
    series: true
  },
  {
    id: 'upper006',
    title: 'AI 实战派',
    author: 'AI 实战派',
    url: 'https://space.bilibili.com/456789012',
    description: 'AI 项目实战和案例分享',
    category: 'UP 主',
    tags: ['实战', '项目', '案例'],
    rating: 4.7,
    series: true
  },
  {
    id: 'upper007',
    title: '效率工具指南',
    author: '效率工具指南',
    url: 'https://space.bilibili.com/567890123',
    description: 'AI 工具和效率软件推荐',
    category: 'UP 主',
    tags: ['工具', '效率', '推荐'],
    rating: 4.6,
    series: true
  },
  {
    id: 'upper008',
    title: '架构师之路',
    author: '架构师之路',
    url: 'https://space.bilibili.com/678901234',
    description: 'AI 系统架构设计',
    category: 'UP 主',
    tags: ['架构', '设计', '系统'],
    rating: 4.7,
    series: true
  },
  {
    id: 'upper009',
    title: 'AI 前沿',
    author: 'AI 前沿',
    url: 'https://space.bilibili.com/789012345',
    description: 'AI 最新技术和研究动态',
    category: 'UP 主',
    tags: ['前沿', '研究', '动态'],
    rating: 4.6,
    series: true
  },
  {
    id: 'upper010',
    title: '开发者社区',
    author: '开发者社区',
    url: 'https://space.bilibili.com/890123456',
    description: 'AI 开发者交流和分享',
    category: 'UP 主',
    tags: ['开发', '社区', '分享'],
    rating: 4.5,
    series: true
  }
]

// 分类统计
export const categoryStats = {
  'AI 基础': 15,
  'Claude': 12,
  'Agent': 15,
  '工作流': 12,
  'UP 主': 10
}

// 热门标签
export const popularTags = [
  '机器学习', '深度学习', '大模型', 'Claude', 'Agent', 
  '工作流', '自动化', 'LangChain', '实战', '教程',
  '入门', '开发', '架构', '工具', '应用'
]
