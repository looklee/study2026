'use client'

import { useState, useCallback, useMemo } from 'react'
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  MarkerType,
  Panel,
  BackgroundVariant,
  ConnectionMode,
  Position,
  Handle
} from 'reactflow'
import 'reactflow/dist/style.css'
import {
  Plus, Play, Save, Trash2, Settings, Zap, Clock, Bell,
  FileText, GitBranch, CheckCircle, XCircle, Link as LinkIcon,
  Cpu, Database, Webhook, MessageSquare, Code, Folder,
  Mail, Send, Calendar, TrendingUp, FileCheck, Upload, Download,
  Search, Filter, Repeat, Pause, StopCircle, Eye, Copy, Move,
  AlertCircle, Info, ChevronRight, ChevronDown, Minus, Sparkles,
  BookOpen, Video, User, Star, Heart, Coffee, Gamepad
} from 'lucide-react'

// ==================== 节点库定义 ====================

// 节点分类
const NODE_CATEGORIES = [
  { id: 'trigger', name: '触发器', icon: Zap, color: 'green' },
  { id: 'action', name: '动作', icon: Play, color: 'blue' },
  { id: 'condition', name: '条件', icon: GitBranch, color: 'orange' },
  { id: 'llm', name: 'AI 模型', icon: Cpu, color: 'indigo' },
  { id: 'api', name: 'API 集成', icon: Webhook, color: 'purple' },
  { id: 'data', name: '数据处理', icon: Database, color: 'teal' },
  { id: 'learning', name: '学习相关', icon: BookOpen, color: 'pink' },
  { id: 'notification', name: '通知消息', icon: Bell, color: 'yellow' }
] as const

// 节点定义
const NODE_DEFINITIONS = [
  // 触发器节点
  { category: 'trigger', type: 'trigger', label: '定时触发', icon: 'clock', description: '按指定时间触发', config: { time: '09:00', timezone: 'Asia/Shanghai' } },
  { category: 'trigger', type: 'trigger', label: 'Webhook', icon: 'webhook', description: 'HTTP 回调触发', config: { path: '/webhook', method: 'POST' } },
  { category: 'trigger', type: 'trigger', label: '进度更新', icon: 'trending', description: '学习进度变化时触发', config: { threshold: 50, field: 'progress' } },
  { category: 'trigger', type: 'trigger', label: '签到触发', icon: 'calendar', description: '用户签到时触发', config: { user_type: 'all' } },
  { category: 'trigger', type: 'trigger', label: '完成课程', icon: 'file-check', description: '完成课程时触发', config: { course_id: '' } },
  
  // 动作节点
  { category: 'action', type: 'action', label: '发送邮件', icon: 'mail', description: '发送电子邮件', config: { template: '', to: '', subject: '' } },
  { category: 'action', type: 'action', label: '发送通知', icon: 'bell', description: '发送站内通知', config: { channel: 'email', priority: 'normal' } },
  { category: 'action', type: 'action', label: '生成报告', icon: 'file-text', description: '生成学习报告', config: { format: 'pdf', include_charts: true } },
  { category: 'action', type: 'action', label: '更新进度', icon: 'trending-up', description: '更新学习进度', config: { field: 'progress', value: 0 } },
  { category: 'action', type: 'action', label: '颁发徽章', icon: 'star', description: '颁发成就徽章', config: { badge_id: '', reason: '' } },
  { category: 'action', type: 'action', label: '等待延迟', icon: 'clock', description: '延迟执行后续节点', config: { delay_seconds: 60 } },
  { category: 'action', type: 'action', label: '循环迭代', icon: 'repeat', description: '循环执行子流程', config: { items: [], max_iterations: 10 } },
  
  // 条件节点
  { category: 'condition', type: 'condition', label: '判断条件', icon: 'git-branch', description: '条件分支判断', config: { operator: '>=', value: 0, field: '' } },
  { category: 'condition', type: 'condition', label: '数值比较', icon: 'filter', description: '数值大小比较', config: { compare_type: 'number', operator: '>', threshold: 0 } },
  { category: 'condition', type: 'condition', label: '文本匹配', icon: 'search', description: '文本内容匹配', config: { match_type: 'contains', pattern: '' } },
  { category: 'condition', type: 'condition', label: '时间判断', icon: 'clock', description: '时间条件判断', config: { time_range: ['09:00', '18:00'] } },
  
  // AI 模型节点
  { category: 'llm', type: 'llm', label: '调用 LLM', icon: 'cpu', description: '调用大语言模型', config: { model: 'qwen-plus', temperature: 0.7, max_tokens: 2000 } },
  { category: 'llm', type: 'llm', label: '文本摘要', icon: 'file-text', description: '生成文本摘要', config: { model: 'qwen-turbo', summary_length: 'short' } },
  { category: 'llm', type: 'llm', label: '情感分析', icon: 'heart', description: '分析文本情感', config: { model: 'qwen-turbo', categories: ['positive', 'negative', 'neutral'] } },
  { category: 'llm', type: 'llm', label: '代码生成', icon: 'code', description: '生成代码片段', config: { model: 'qwen-coder', language: 'python' } },
  { category: 'llm', type: 'llm', label: '翻译', icon: 'message-square', description: '多语言翻译', config: { source_lang: 'zh', target_lang: 'en' } },
  { category: 'llm', type: 'llm', label: '问答', icon: 'message-square', description: '智能问答', config: { model: 'qwen-plus', context_window: 4096 } },
  
  // API 集成节点
  { category: 'api', type: 'api', label: 'HTTP 请求', icon: 'webhook', description: '发送 HTTP 请求', config: { method: 'GET', url: '', headers: {} } },
  { category: 'api', type: 'api', label: 'API 调用', icon: 'plug', description: '调用外部 API', config: { provider: '', endpoint: '', auth: 'api_key' } },
  { category: 'api', type: 'api', label: '数据导入', icon: 'download', description: '从外部导入数据', config: { source: '', format: 'json' } },
  { category: 'api', type: 'api', label: '数据导出', icon: 'upload', description: '导出数据到外部', config: { destination: '', format: 'json' } },
  
  // 数据节点
  { category: 'data', type: 'data', label: '保存数据', icon: 'database', description: '保存到数据库', config: { table: '', operation: 'insert' } },
  { category: 'data', type: 'data', label: '查询数据', icon: 'search', description: '从数据库查询', config: { table: '', query: {} } },
  { category: 'data', type: 'data', label: '更新数据', icon: 'repeat', description: '更新数据库记录', config: { table: '', where: {}, update: {} } },
  { category: 'data', type: 'data', label: '删除数据', icon: 'trash', description: '删除数据库记录', config: { table: '', where: {} } },
  { category: 'data', type: 'data', label: '数据转换', icon: 'repeat', description: '转换数据格式', config: { from_format: 'json', to_format: 'csv' } },
  { category: 'data', type: 'data', label: '数据聚合', icon: 'filter', description: '聚合统计数据', config: { group_by: '', aggregations: [] } },
  
  // 学习相关节点
  { category: 'learning', type: 'learning', label: '生成学习路径', icon: 'book-open', description: 'AI 生成学习路径', config: { goal: '', duration_days: 30, difficulty: 'medium' } },
  { category: 'learning', type: 'learning', label: '推荐资源', icon: 'star', description: '推荐学习资源', config: { topic: '', limit: 5, difficulty: 'medium' } },
  { category: 'learning', type: 'learning', label: '检查进度', icon: 'trending-up', description: '检查学习进度', config: { path_id: '', check_type: 'completion' } },
  { category: 'learning', type: 'learning', label: '发送提醒', icon: 'bell', description: '学习提醒', config: { reminder_type: 'daily', time: '09:00' } },
  { category: 'learning', type: 'learning', label: '测验评估', icon: 'file-check', description: '测验和评估', config: { quiz_id: '', pass_score: 80 } },
  { category: 'learning', type: 'learning', label: '视频学习', icon: 'video', description: '视频学习任务', config: { video_url: '', track_progress: true } },
  
  // 通知消息节点
  { category: 'notification', type: 'notification', label: '邮件通知', icon: 'mail', description: '发送邮件通知', config: { template: '', recipients: [] } },
  { category: 'notification', type: 'notification', label: '站内消息', icon: 'message-square', description: '发送站内消息', config: { user_ids: [], message: '' } },
  { category: 'notification', type: 'notification', label: '推送通知', icon: 'bell', description: '推送通知', config: { platform: 'all', title: '', body: '' } },
  { category: 'notification', type: 'notification', label: '钉钉通知', icon: 'send', description: '钉钉机器人通知', config: { webhook: '', msgtype: 'text' } },
  { category: 'notification', type: 'notification', label: '企业微信', icon: 'send', description: '企业微信通知', config: { webhook: '', msgtype: 'text' } }
] as const

// 节点类型定义
const nodeTypes = {
  trigger: TriggerNode,
  action: ActionNode,
  condition: ConditionNode,
  api: APINode,
  llm: LLMNode,
  data: DataNode,
  learning: LearningNode,
  notification: NotificationNode
}

// 预置工作流模板
const workflowTemplates = [
  {
    id: 'daily_reminder',
    name: '每日学习提醒',
    description: '每天早上 9 点发送学习提醒',
    icon: Bell,
    color: 'blue',
    nodes: [
      { id: '1', type: 'trigger', position: { x: 100, y: 200 }, data: { label: '定时触发', icon: 'clock', config: { time: '09:00' } } },
      { id: '2', type: 'notification', position: { x: 400, y: 200 }, data: { label: '发送邮件', icon: 'mail', config: { template: 'daily_reminder' } } },
    ],
    edges: [{ id: 'e1-2', source: '1', target: '2', type: 'smoothstep', animated: false, markerEnd: { type: MarkerType.ArrowClosed } }],
    logic: 'AND'
  },
  {
    id: 'milestone_notify',
    name: '里程碑通知',
    description: '学习进度达到里程碑时发送通知',
    icon: Zap,
    color: 'green',
    nodes: [
      { id: '1', type: 'trigger', position: { x: 100, y: 200 }, data: { label: '进度更新', icon: 'trending', config: { threshold: 50 } } },
      { id: '2', type: 'condition', position: { x: 400, y: 200 }, data: { label: '判断进度', icon: 'git-branch', config: { operator: '>=', value: 50 } } },
      { id: '3', type: 'notification', position: { x: 700, y: 200 }, data: { label: '发送通知', icon: 'bell', config: { channel: 'email' } } },
    ],
    edges: [{ id: 'e1-2', source: '1', target: '2', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } }, { id: 'e2-3', source: '2', target: '3', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } }],
    logic: 'AND'
  },
  {
    id: 'ai_learning_path',
    name: 'AI 学习路径生成',
    description: '用户提交目标后自动生成学习路径',
    icon: FileText,
    color: 'purple',
    nodes: [
      { id: '1', type: 'trigger', position: { x: 100, y: 200 }, data: { label: 'Webhook', icon: 'webhook', config: { path: '/api/path-request' } } },
      { id: '2', type: 'llm', position: { x: 400, y: 200 }, data: { label: '调用 LLM', icon: 'cpu', config: { model: 'qwen-plus' } } },
      { id: '3', type: 'data', position: { x: 700, y: 200 }, data: { label: '保存路径', icon: 'database', config: { table: 'learning_paths' } } },
      { id: '4', type: 'action', position: { x: 1000, y: 200 }, data: { label: '返回结果', icon: 'code', config: { format: 'json' } } },
    ],
    edges: [
      { id: 'e1-2', source: '1', target: '2', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e2-3', source: '2', target: '3', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e3-4', source: '3', target: '4', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } }
    ],
    logic: 'AND'
  },
  {
    id: 'study_report',
    name: '学习报告生成',
    description: '每周自动生成学习报告并发送',
    icon: FileCheck,
    color: 'purple',
    nodes: [
      { id: '1', type: 'trigger', position: { x: 100, y: 200 }, data: { label: '定时触发', icon: 'clock', config: { time: '09:00', weekday: 1 } } },
      { id: '2', type: 'data', position: { x: 400, y: 200 }, data: { label: '查询数据', icon: 'search', config: { table: 'study_logs', query: { week: 'last' } } } },
      { id: '3', type: 'llm', position: { x: 700, y: 200 }, data: { label: '生成报告', icon: 'file-text', config: { model: 'qwen-plus', template: 'weekly_report' } } },
      { id: '4', type: 'notification', position: { x: 1000, y: 200 }, data: { label: '发送邮件', icon: 'mail', config: { template: 'report_email' } } },
    ],
    edges: [
      { id: 'e1-2', source: '1', target: '2', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e2-3', source: '2', target: '3', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e3-4', source: '3', target: '4', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } }
    ],
    logic: 'AND'
  },
  {
    id: 'pet_interaction',
    name: '宠物互动奖励',
    description: '用户与宠物互动后给予奖励',
    icon: Heart,
    color: 'pink',
    nodes: [
      { id: '1', type: 'trigger', position: { x: 100, y: 200 }, data: { label: '宠物互动', icon: 'heart', config: { action: 'feed' } } },
      { id: '2', type: 'learning', position: { x: 400, y: 200 }, data: { label: '更新经验', icon: 'star', config: { exp: 10 } } },
      { id: '3', type: 'condition', position: { x: 700, y: 200 }, data: { label: '检查升级', icon: 'git-branch', config: { field: 'level', operator: 'changed' } } },
      { id: '4', type: 'notification', position: { x: 1000, y: 100 }, data: { label: '升级通知', icon: 'bell', config: { type: 'level_up' } } },
    ],
    edges: [
      { id: 'e1-2', source: '1', target: '2', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e2-3', source: '2', target: '3', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } },
      { id: 'e3-4', source: '3', target: '4', type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } }
    ],
    logic: 'AND'
  }
]

// ==================== 节点组件 ====================

function TriggerNode({ data, selected }: { data: any; selected?: boolean }) {
  return (
    <div className={`px-4 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg shadow-lg min-w-[180px] border-2 ${selected ? 'border-white' : 'border-green-400'}`}>
      <Handle type="source" position={Position.Right} id="out" className="!w-4 !h-4 !bg-white !border-2 !border-green-500 cursor-crosshair hover:!scale-125 transition-transform" />
      <div className="flex items-center gap-2 mb-2">
        <Zap className="h-4 w-4" />
        <span className="font-bold text-sm">触发器</span>
      </div>
      <div className="text-sm font-medium">{data.label}</div>
      {data.config && Object.keys(data.config).length > 0 && (
        <div className="mt-2 text-xs bg-white/20 rounded p-2 max-h-20 overflow-y-auto">
          {Object.entries(data.config).slice(0, 3).map(([key, value]) => (
            <div key={key}>{key}: {String(value)}</div>
          ))}
        </div>
      )}
    </div>
  )
}

function ActionNode({ data, selected }: { data: any; selected?: boolean }) {
  return (
    <div className={`px-4 py-3 bg-gradient-to-r from-blue-500 to-cyan-600 text-white rounded-lg shadow-lg min-w-[180px] border-2 ${selected ? 'border-white' : 'border-blue-400'}`}>
      <Handle type="target" position={Position.Left} id="in" className="!w-4 !h-4 !bg-white !border-2 !border-blue-500 cursor-crosshair hover:!scale-125 transition-transform" />
      <div className="flex items-center gap-2 mb-2">
        <Play className="h-4 w-4" />
        <span className="font-bold text-sm">动作</span>
      </div>
      <div className="text-sm font-medium">{data.label}</div>
      {data.config && Object.keys(data.config).length > 0 && (
        <div className="mt-2 text-xs bg-white/20 rounded p-2 max-h-20 overflow-y-auto">
          {Object.entries(data.config).slice(0, 3).map(([key, value]) => (
            <div key={key}>{key}: {String(value)}</div>
          ))}
        </div>
      )}
      <Handle type="source" position={Position.Right} id="out" className="!w-4 !h-4 !bg-white !border-2 !border-blue-500 cursor-crosshair hover:!scale-125 transition-transform" />
    </div>
  )
}

function ConditionNode({ data, selected }: { data: any; selected?: boolean }) {
  return (
    <div className={`px-4 py-3 bg-gradient-to-r from-orange-500 to-red-600 text-white rounded-lg shadow-lg min-w-[180px] border-2 ${selected ? 'border-white' : 'border-orange-400'}`}>
      <Handle type="target" position={Position.Left} id="in" className="!w-4 !h-4 !bg-white !border-2 !border-orange-500 cursor-crosshair hover:!scale-125 transition-transform" />
      <div className="flex items-center gap-2 mb-2">
        <GitBranch className="h-4 w-4" />
        <span className="font-bold text-sm">条件</span>
      </div>
      <div className="text-sm font-medium">{data.label}</div>
      {data.config && (
        <div className="mt-2 text-xs bg-white/20 rounded p-2 max-h-20 overflow-y-auto">
          {data.config.operator} {data.config.value}
        </div>
      )}
      <Handle type="source" position={Position.Right} id="yes" className="!w-4 !h-4 !bg-green-400 !border-2 !border-white cursor-crosshair hover:!scale-125 transition-transform !top-1/4 !-right-2" title="是" />
      <Handle type="source" position={Position.Right} id="no" className="!w-4 !h-4 !bg-red-400 !border-2 !border-white cursor-crosshair hover:!scale-125 transition-transform !bottom-1/4 !-right-2" title="否" />
    </div>
  )
}

function APINode({ data, selected }: { data: any; selected?: boolean }) {
  return (
    <div className={`px-4 py-3 bg-gradient-to-r from-purple-500 to-pink-600 text-white rounded-lg shadow-lg min-w-[180px] border-2 ${selected ? 'border-white' : 'border-purple-400'}`}>
      <Handle type="target" position={Position.Left} id="in" className="!w-4 !h-4 !bg-white !border-2 !border-purple-500 cursor-crosshair hover:!scale-125 transition-transform" />
      <div className="flex items-center gap-2 mb-2">
        <Webhook className="h-4 w-4" />
        <span className="font-bold text-sm">API</span>
      </div>
      <div className="text-sm font-medium">{data.label}</div>
      {data.config && (
        <div className="mt-2 text-xs bg-white/20 rounded p-2 max-h-20 overflow-y-auto">
          {data.config.method || 'GET'} {data.config.endpoint?.substring(0, 20) || '/api'}
        </div>
      )}
      <Handle type="source" position={Position.Right} id="out" className="!w-4 !h-4 !bg-white !border-2 !border-purple-500 cursor-crosshair hover:!scale-125 transition-transform" />
    </div>
  )
}

function LLMNode({ data, selected }: { data: any; selected?: boolean }) {
  return (
    <div className={`px-4 py-3 bg-gradient-to-r from-indigo-500 to-violet-600 text-white rounded-lg shadow-lg min-w-[180px] border-2 ${selected ? 'border-white' : 'border-indigo-400'}`}>
      <Handle type="target" position={Position.Left} id="in" className="!w-4 !h-4 !bg-white !border-2 !border-indigo-500 cursor-crosshair hover:!scale-125 transition-transform" />
      <div className="flex items-center gap-2 mb-2">
        <Cpu className="h-4 w-4" />
        <span className="font-bold text-sm">AI 模型</span>
      </div>
      <div className="text-sm font-medium">{data.label}</div>
      {data.config && (
        <div className="mt-2 text-xs bg-white/20 rounded p-2 max-h-20 overflow-y-auto">
          模型：{data.config.model || 'qwen-plus'}
        </div>
      )}
      <Handle type="source" position={Position.Right} id="out" className="!w-4 !h-4 !bg-white !border-2 !border-indigo-500 cursor-crosshair hover:!scale-125 transition-transform" />
    </div>
  )
}

function DataNode({ data, selected }: { data: any; selected?: boolean }) {
  return (
    <div className={`px-4 py-3 bg-gradient-to-r from-teal-500 to-emerald-600 text-white rounded-lg shadow-lg min-w-[180px] border-2 ${selected ? 'border-white' : 'border-teal-400'}`}>
      <Handle type="target" position={Position.Left} id="in" className="!w-4 !h-4 !bg-white !border-2 !border-teal-500 cursor-crosshair hover:!scale-125 transition-transform" />
      <div className="flex items-center gap-2 mb-2">
        <Database className="h-4 w-4" />
        <span className="font-bold text-sm">数据</span>
      </div>
      <div className="text-sm font-medium">{data.label}</div>
      {data.config && (
        <div className="mt-2 text-xs bg-white/20 rounded p-2 max-h-20 overflow-y-auto">
          表：{data.config.table || 'data'}
        </div>
      )}
      <Handle type="source" position={Position.Right} id="out" className="!w-4 !h-4 !bg-white !border-2 !border-teal-500 cursor-crosshair hover:!scale-125 transition-transform" />
    </div>
  )
}

function LearningNode({ data, selected }: { data: any; selected?: boolean }) {
  return (
    <div className={`px-4 py-3 bg-gradient-to-r from-pink-500 to-rose-600 text-white rounded-lg shadow-lg min-w-[180px] border-2 ${selected ? 'border-white' : 'border-pink-400'}`}>
      <Handle type="target" position={Position.Left} id="in" className="!w-4 !h-4 !bg-white !border-2 !border-pink-500 cursor-crosshair hover:!scale-125 transition-transform" />
      <div className="flex items-center gap-2 mb-2">
        <BookOpen className="h-4 w-4" />
        <span className="font-bold text-sm">学习</span>
      </div>
      <div className="text-sm font-medium">{data.label}</div>
      {data.config && (
        <div className="mt-2 text-xs bg-white/20 rounded p-2 max-h-20 overflow-y-auto">
          {Object.entries(data.config).slice(0, 2).map(([key, value]) => (
            <div key={key}>{key}: {String(value)}</div>
          ))}
        </div>
      )}
      <Handle type="source" position={Position.Right} id="out" className="!w-4 !h-4 !bg-white !border-2 !border-pink-500 cursor-crosshair hover:!scale-125 transition-transform" />
    </div>
  )
}

function NotificationNode({ data, selected }: { data: any; selected?: boolean }) {
  return (
    <div className={`px-4 py-3 bg-gradient-to-r from-yellow-500 to-amber-600 text-white rounded-lg shadow-lg min-w-[180px] border-2 ${selected ? 'border-white' : 'border-yellow-400'}`}>
      <Handle type="target" position={Position.Left} id="in" className="!w-4 !h-4 !bg-white !border-2 !border-yellow-500 cursor-crosshair hover:!scale-125 transition-transform" />
      <div className="flex items-center gap-2 mb-2">
        <Bell className="h-4 w-4" />
        <span className="font-bold text-sm">通知</span>
      </div>
      <div className="text-sm font-medium">{data.label}</div>
      {data.config && (
        <div className="mt-2 text-xs bg-white/20 rounded p-2 max-h-20 overflow-y-auto">
          渠道：{data.config.channel || data.config.platform || 'email'}
        </div>
      )}
      <Handle type="source" position={Position.Right} id="out" className="!w-4 !h-4 !bg-white !border-2 !border-yellow-500 cursor-crosshair hover:!scale-125 transition-transform" />
    </div>
  )
}

// ==================== 主页面组件 ====================

export default function WorkflowsPage() {
  const [activeTab, setActiveTab] = useState<'editor' | 'templates' | 'history' | 'nodelib'>('nodelib')
  const [workflowName, setWorkflowName] = useState('我的工作流')
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [selectedNode, setSelectedNode] = useState<Node | null>(null)
  const [logicMode, setLogicMode] = useState<'AND' | 'OR'>('AND')
  const [nodeSearch, setNodeSearch] = useState('')
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>({
    trigger: true,
    action: true,
    learning: true
  })
  const [executionHistory, setExecutionHistory] = useState([
    { id: 1, workflow: '每日学习提醒', status: 'success', time: '2 分钟前', duration: '1.2s', nodes: 2 },
    { id: 2, workflow: '里程碑通知', status: 'success', time: '1 小时前', duration: '3.5s', nodes: 3 },
    { id: 3, workflow: 'AI 学习路径', status: 'error', time: '3 小时前', duration: '0.5s', nodes: 4 },
  ])

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge({ ...params, type: 'smoothstep', markerEnd: { type: MarkerType.ArrowClosed } }, eds)),
    [setEdges],
  )

  const onNodeClick = useCallback((_: any, node: Node) => {
    setSelectedNode(node)
  }, [])

  const loadTemplate = (template: any) => {
    setNodes(template.nodes)
    setEdges(template.edges)
    setWorkflowName(template.name)
    setLogicMode(template.logic || 'AND')
    setActiveTab('editor')
  }

  const saveWorkflow = () => {
    const workflow = {
      id: Date.now(),
      name: workflowName,
      nodes,
      edges,
      logic: logicMode,
      created_at: new Date().toISOString()
    }
    localStorage.setItem('workflows', JSON.stringify([...JSON.parse(localStorage.getItem('workflows') || '[]'), workflow]))
    alert(`工作流已保存！\n节点数：${nodes.length}\n连接数：${edges.length}\n逻辑：${logicMode}`)
  }

  const runWorkflow = async () => {
    if (nodes.length === 0) {
      alert('请先添加节点')
      return
    }

    try {
      const response = await fetch('http://localhost:8001/api/v1/workflows/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nodes,
          edges,
          logic: logicMode,
          input_data: { timestamp: new Date().toISOString() }
        })
      })

      const result = await response.json()

      if (result.status === 'success') {
        const newExecution = {
          id: Date.now(),
          workflow: workflowName,
          status: result.result?.status || 'success',
          time: '刚刚',
          duration: '-',
          nodes: nodes.length,
          execution_id: result.execution_id
        }
        setExecutionHistory([newExecution, ...executionHistory])
        alert(`工作流执行完成！\n状态：${result.result?.status}\n执行节点：${result.nodes_executed}个`)
      } else {
        alert(`执行失败：${result.error}`)
      }
    } catch (error) {
      alert(`执行错误：${error}`)
    }
  }

  const addNode = (type: string, label: string, icon: string, defaultConfig?: any) => {
    const newNode: Node = {
      id: `node-${Date.now()}`,
      type,
      position: { x: 100 + nodes.length * 250, y: 200 },
      data: { label, icon, config: defaultConfig || {} },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
      draggable: true
    }
    setNodes((nds) => [...nds, newNode])
  }

  const deleteSelectedNode = () => {
    if (selectedNode) {
      setNodes(nodes.filter(n => n.id !== selectedNode.id))
      setEdges(edges.filter(e => e.source !== selectedNode.id && e.target !== selectedNode.id))
      setSelectedNode(null)
    }
  }

  const toggleCategory = (categoryId: string) => {
    setExpandedCategories(prev => ({ ...prev, [categoryId]: !prev[categoryId] }))
  }

  // 过滤节点
  const filteredNodes = useMemo(() => {
    if (!nodeSearch) return NODE_DEFINITIONS
    return NODE_DEFINITIONS.filter(node =>
      node.label.toLowerCase().includes(nodeSearch.toLowerCase()) ||
      node.description.toLowerCase().includes(nodeSearch.toLowerCase())
    )
  }, [nodeSearch])

  // 获取图标组件
  const getIcon = (iconName: string) => {
    const icons: Record<string, any> = {
      clock: Clock, webhook: Webhook, trending: TrendingUp, calendar: Calendar,
      'file-check': FileCheck, mail: Mail, bell: Bell, 'file-text': FileText,
      'trending-up': TrendingUp, star: Star, repeat: Repeat, 'git-branch': GitBranch,
      filter: Filter, search: Search, cpu: Cpu, code: Code, 'message-square': MessageSquare,
      plug: Webhook, download: Download, upload: Upload, database: Database,
      'book-open': BookOpen, video: Video, heart: Heart, send: Send,
      trash: Trash2, sparkles: Sparkles, user: User, coffee: Coffee, gamepad: Gamepad
    }
    return icons[iconName] || Zap
  }

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col">
      {/* Header */}
      <div className="border-b bg-white px-6 py-4">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4 flex-1">
            <input
              type="text"
              value={workflowName}
              onChange={(e) => setWorkflowName(e.target.value)}
              className="text-xl font-bold border-none focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1"
            />
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-500">逻辑:</span>
              <div className="flex items-center gap-1 bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setLogicMode('AND')}
                  className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                    logicMode === 'AND' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  AND (与)
                </button>
                <button
                  onClick={() => setLogicMode('OR')}
                  className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                    logicMode === 'OR' ? 'bg-blue-600 text-white' : 'text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  OR (或)
                </button>
              </div>
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-500">
              <span className="flex items-center gap-1">
                <div className="w-2 h-2 bg-green-500 rounded-full" />
                {nodes.length} 节点
              </span>
              <span className="flex items-center gap-1">
                <LinkIcon className="h-3 w-3" />
                {edges.length} 连接
              </span>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => { setNodes([]); setEdges([]); }}
              className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <Trash2 className="h-4 w-4" />
              清空
            </button>
            <button
              onClick={saveWorkflow}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Save className="h-4 w-4" />
              保存
            </button>
            <button
              onClick={runWorkflow}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Play className="h-4 w-4" />
              运行
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-4">
          <TabButton active={activeTab === 'nodelib'} onClick={() => setActiveTab('nodelib')}>
            <Folder className="h-4 w-4" />
            节点库
          </TabButton>
          <TabButton active={activeTab === 'editor'} onClick={() => setActiveTab('editor')}>
            <Settings className="h-4 w-4" />
            编辑器
          </TabButton>
          <TabButton active={activeTab === 'templates'} onClick={() => setActiveTab('templates')}>
            <Sparkles className="h-4 w-4" />
            模板中心
          </TabButton>
          <TabButton active={activeTab === 'history'} onClick={() => setActiveTab('history')}>
            <Clock className="h-4 w-4" />
            执行历史
          </TabButton>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'nodelib' && (
          <div className="h-full overflow-y-auto bg-gray-50 p-6">
            <div className="max-w-6xl mx-auto">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">📦 节点库</h2>
                <p className="text-gray-600">浏览所有可用节点，点击添加到工作流</p>
              </div>

              {/* 搜索框 */}
              <div className="mb-6">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    value={nodeSearch}
                    onChange={(e) => setNodeSearch(e.target.value)}
                    placeholder="搜索节点..."
                    className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              {/* 节点分类 */}
              {NODE_CATEGORIES.map((category) => {
                const categoryNodes = filteredNodes.filter(n => n.category === category.id)
                if (categoryNodes.length === 0) return null
                const Icon = category.icon
                const isExpanded = expandedCategories[category.id]

                return (
                  <div key={category.id} className="mb-6">
                    <button
                      onClick={() => toggleCategory(category.id)}
                      className="flex items-center gap-2 mb-3 text-lg font-semibold text-gray-800 hover:text-blue-600 transition-colors"
                    >
                      <div className={`p-2 rounded-lg bg-${category.color}-100`}>
                        <Icon className={`h-5 w-5 text-${category.color}-600`} />
                      </div>
                      {category.name}
                      <span className="text-sm text-gray-400">({categoryNodes.length})</span>
                      {isExpanded ? <ChevronDown className="h-5 w-5" /> : <ChevronRight className="h-5 w-5" />}
                    </button>

                    {isExpanded && (
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {categoryNodes.map((node, index) => {
                          const NodeIcon = getIcon(node.icon)
                          return (
                            <div
                              key={`${category.id}-${index}`}
                              onClick={() => addNode(node.type, node.label, node.icon, node.config)}
                              className="bg-white rounded-xl p-4 border-2 border-gray-200 hover:border-blue-400 cursor-pointer transition-all hover:shadow-lg group"
                            >
                              <div className="flex items-start gap-3">
                                <div className={`p-2 rounded-lg bg-${category.color}-100 group-hover:bg-${category.color}-200 transition-colors`}>
                                  <NodeIcon className={`h-5 w-5 text-${category.color}-600`} />
                                </div>
                                <div className="flex-1">
                                  <h3 className="font-semibold text-gray-900">{node.label}</h3>
                                  <p className="text-sm text-gray-500 mt-1">{node.description}</p>
                                  <div className="flex items-center gap-2 mt-2">
                                    <span className="text-xs text-gray-400">点击添加</span>
                                    <Plus className="h-3 w-3 text-gray-400" />
                                  </div>
                                </div>
                              </div>
                            </div>
                          )
                        })}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {activeTab === 'editor' && (
          <div className="h-full flex">
            {/* Node Palette - 简化版 */}
            <div className="w-64 border-r bg-gray-50 p-4 overflow-y-auto">
              <h3 className="font-bold text-gray-900 mb-4 text-sm flex items-center gap-2">
                <Folder className="h-4 w-4" />
                快速添加
              </h3>

              <div className="space-y-3">
                {NODE_CATEGORIES.slice(0, 5).map((category) => {
                  const categoryNodes = NODE_DEFINITIONS.filter(n => n.category === category.id).slice(0, 2)
                  const Icon = category.icon
                  return (
                    <div key={category.id}>
                      <div className="flex items-center gap-2 mb-2 text-xs font-semibold text-gray-500 uppercase">
                        <Icon className="h-3 w-3" />
                        {category.name}
                      </div>
                      <div className="space-y-1">
                        {categoryNodes.map((node, index) => {
                          const NodeIcon = getIcon(node.icon)
                          return (
                            <button
                              key={index}
                              onClick={() => addNode(node.type, node.label, node.icon, node.config)}
                              className="w-full flex items-center gap-2 px-3 py-2 rounded-lg border bg-white hover:border-blue-400 hover:bg-blue-50 transition-colors text-left text-sm"
                            >
                              <NodeIcon className="h-4 w-4 text-gray-500" />
                              {node.label}
                            </button>
                          )
                        })}
                      </div>
                    </div>
                  )
                })}
              </div>

              <button
                onClick={() => setActiveTab('nodelib')}
                className="w-full mt-4 flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
              >
                <Folder className="h-4 w-4" />
                完整节点库
              </button>
            </div>

            {/* Flow Editor */}
            <div className="flex-1">
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onConnect={onConnect}
                onNodeClick={onNodeClick}
                nodeTypes={nodeTypes}
                fitView
                snapToGrid
                snapGrid={[15, 15]}
                connectionMode={ConnectionMode.Loose}
                connectOnClick={true}
                defaultEdgeOptions={{
                  type: 'smoothstep',
                  markerEnd: { type: MarkerType.ArrowClosed },
                  animated: false
                }}
              >
                <Controls />
                <Background variant={BackgroundVariant.Dots} gap={20} size={1} />
                <Panel position="top-right" className="bg-white p-2 rounded-lg shadow border flex gap-2">
                  <button
                    onClick={deleteSelectedNode}
                    className="p-2 hover:bg-red-50 rounded text-red-600"
                    title="删除选中节点"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => { setNodes([]); setEdges([]); }}
                    className="p-2 hover:bg-gray-100 rounded"
                    title="清空画布"
                  >
                    <XCircle className="h-4 w-4 text-gray-600" />
                  </button>
                </Panel>
                <Panel position="bottom-left" className="bg-white/90 p-3 rounded-lg shadow border text-xs">
                  <div className="font-medium mb-2">逻辑关系：{logicMode}</div>
                  <div className="text-gray-600">
                    {logicMode === 'AND' ? '所有节点按顺序执行' : '任一节点触发即可'}
                  </div>
                </Panel>
                {nodes.length === 0 && (
                  <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                    <div className="bg-white/90 p-6 rounded-xl shadow-lg border text-center pointer-events-auto">
                      <Folder className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                      <h3 className="text-lg font-semibold text-gray-700 mb-2">开始创建工作流</h3>
                      <p className="text-gray-500 mb-4">从左侧节点库添加节点，或从模板开始</p>
                      <button
                        onClick={() => setActiveTab('nodelib')}
                        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        浏览节点库
                      </button>
                    </div>
                  </div>
                )}
              </ReactFlow>
            </div>

            {/* Node Config Panel */}
            {selectedNode && (
              <div className="w-80 border-l bg-white p-4 overflow-y-auto">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-bold text-gray-900">节点配置</h3>
                  <button onClick={() => setSelectedNode(null)} className="text-gray-500 hover:text-gray-700">
                    <XCircle className="h-5 w-5" />
                  </button>
                </div>

                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">节点名称</label>
                    <input
                      type="text"
                      defaultValue={selectedNode.data.label}
                      className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">节点类型</label>
                    <div className="px-3 py-2 bg-gray-100 rounded-lg text-sm text-gray-600 capitalize">
                      {selectedNode.type}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">图标</label>
                    <div className="flex items-center gap-2">
                      {(() => {
                        const Icon = getIcon(selectedNode.data.icon)
                        return <Icon className="h-5 w-5 text-gray-600" />
                      })()}
                      <span className="text-sm text-gray-600">{selectedNode.data.icon}</span>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">配置参数</label>
                    <div className="space-y-2">
                      {selectedNode.data.config && Object.keys(selectedNode.data.config).length > 0 ? (
                        Object.entries(selectedNode.data.config).map(([key, value]) => (
                          <div key={key} className="grid grid-cols-2 gap-2">
                            <input
                              type="text"
                              defaultValue={key}
                              className="border rounded-lg px-2 py-1 text-xs"
                              placeholder="参数名"
                            />
                            <input
                              type="text"
                              defaultValue={String(value)}
                              className="border rounded-lg px-2 py-1 text-xs"
                              placeholder="参数值"
                            />
                          </div>
                        ))
                      ) : (
                        <div className="text-sm text-gray-500 text-center py-4">
                          暂无配置参数
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="pt-4 border-t">
                    <button
                      onClick={deleteSelectedNode}
                      className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors text-sm font-medium"
                    >
                      <Trash2 className="h-4 w-4" />
                      删除节点
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'templates' && (
          <div className="h-full overflow-y-auto p-6 bg-gray-50">
            <div className="max-w-6xl mx-auto">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">✨ 模板中心</h2>
                <p className="text-gray-600">使用预置模板快速开始创建工作流</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {workflowTemplates.map((template) => {
                  const Icon = template.icon
                  return (
                    <div key={template.id} className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow">
                      <div className="flex items-start gap-4 mb-4">
                        <div className={`${template.color === 'blue' ? 'bg-blue-100 text-blue-600' : template.color === 'green' ? 'bg-green-100 text-green-600' : template.color === 'purple' ? 'bg-purple-100 text-purple-600' : template.color === 'pink' ? 'bg-pink-100 text-pink-600' : 'bg-gray-100 text-gray-600'} p-3 rounded-lg`}>
                          <Icon className="h-6 w-6" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900">{template.name}</h3>
                          <p className="text-sm text-gray-500 mt-1">{template.description}</p>
                        </div>
                      </div>

                      <div className="flex items-center gap-4 text-xs text-gray-500 mb-4">
                        <span className="flex items-center gap-1">
                          <div className="w-2 h-2 bg-green-500 rounded-full" />
                          {template.nodes.length} 节点
                        </span>
                        <span className="flex items-center gap-1">
                          <LinkIcon className="h-3 w-3" />
                          {template.edges.length} 连接
                        </span>
                        <span className="px-2 py-1 bg-gray-100 rounded font-medium">
                          {template.logic || 'AND'}
                        </span>
                      </div>

                      <button
                        onClick={() => loadTemplate(template)}
                        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                      >
                        使用此模板
                      </button>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="h-full overflow-y-auto p-6 bg-gray-50">
            <div className="max-w-6xl mx-auto">
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">📜 执行历史</h2>
                <p className="text-gray-600">查看工作流的执行记录</p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">工作流</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">状态</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">节点数</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">执行时间</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">耗时</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {executionHistory.map((exec) => (
                      <tr key={exec.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 text-sm font-medium text-gray-900">{exec.workflow}</td>
                        <td className="px-6 py-4">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            exec.status === 'success' ? 'bg-green-100 text-green-700' :
                            exec.status === 'error' ? 'bg-red-100 text-red-700' :
                            'bg-yellow-100 text-yellow-700'
                          }`}>
                            {exec.status === 'success' ? '✓ 成功' : exec.status === 'error' ? '✗ 失败' : '⏳ 运行中'}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">{exec.nodes} 个</td>
                        <td className="px-6 py-4 text-sm text-gray-500">{exec.time}</td>
                        <td className="px-6 py-4 text-sm text-gray-500">{exec.duration}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// 辅助组件
function TabButton({ children, active, onClick }: { children: React.ReactNode, active: boolean, onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
        active
          ? 'bg-blue-100 text-blue-700'
          : 'text-gray-600 hover:bg-gray-100'
      }`}
    >
      {children}
    </button>
  )
}
