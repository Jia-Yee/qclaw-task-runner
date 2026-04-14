---
name: task-runner
description: 大任务执行技能。当用户说"做XXX"且任务复杂/耗时，需要分步执行、断点续做、防止上下文丢失时触发。核心场景：代码项目、批量文件处理、多步骤分析、内容生成等任何可能超出上下文限制的任务。
---

# Task Runner — 大任务分步执行

## 核心思想

**永远不要在一个回合里做完整件事。** 大任务拆成小步骤，每步结果写文件，下一步从文件读取，即使上下文被压缩也不丢进度。

## 工作目录

所有任务数据存在 `~/.qclaw/workspace/tasks/<task-id>/`

```
tasks/<task-id>/
├── MANIFEST.json      # 任务清单（元数据 + 步骤列表）
├── step-001.json      # 每步的输入/输出/状态
├── step-002.json
└── ...
```

## 触发时机

满足任一即触发：
- 用户说"做XXX"且任务明显复杂（多文件、多步骤、超10分钟工作量）
- 用户说"继续做"、"接着上次的"
- 用户说"太大了，分步做"
- 任何感觉上下文可能撑不住的时候

## 执行流程

### Phase 1：建任务（第一次对话）

1. 创建任务目录和 MANIFEST.json
2. 把大任务拆成 N 个具体步骤（每步不超过 5-10 分钟工作量）
3. 写入 `~/.qclaw/workspace/tasks/<task-id>/MANIFEST.json`
4. **立即执行第一步**，把结果写入 `step-001.json`
5. 报告进展，问用户确认后继续

### Phase 2：继续（后续对话）

1. 读 MANIFEST.json + 最新完成的步骤
2. 执行下一步
3. 重复直到全部完成

## MANIFEST.json 格式

```json
{
  "id": "project-build-001",
  "name": "博客项目",
  "description": "用 Hexo 建一个技术博客",
  "created": "2026-04-14T20:00:00+08:00",
  "status": "in_progress",
  "current_step": 2,
  "total_steps": 6,
  "steps": [
    {
      "id": 1,
      "title": "初始化 Hexo 项目",
      "status": "done",
      "result_file": "step-001.json",
      "summary": "项目创建成功，依赖安装完成"
    },
    {
      "id": 2,
      "title": "配置主题",
      "status": "in_progress",
      "result_file": null,
      "summary": null
    }
  ]
}
```

## 步骤结果文件格式（step-NNN.json）

```json
{
  "step_id": 1,
  "title": "初始化 Hexo 项目",
  "status": "done",
  "started": "2026-04-14T20:00:00+08:00",
  "completed": "2026-04-14T20:03:00+08:00",
  "input": {
    "instruction": "初始化 Hexo 项目..."
  },
  "output": {
    "summary": "项目创建成功，依赖安装完成",
    "files_created": ["package.json", "hexo.config.js"],
    "files_modified": [],
    "errors": [],
    "next_steps_hints": ["安装主题依赖", "配置 _config.yml"]
  },
  "artifacts": [
    "workspace/blog/package.json"
  ]
}
```

## 关键规则

### 必须遵守
- **每步必须写文件**，不能只靠对话传递状态
- **每步控制在 5-10 分钟内**，大了就继续拆
- **失败立即停**，不要硬撑着继续，报告问题
- **step id 永不复用**，失败步骤保留记录

### 可以灵活
- 步骤数量不固定，根据实际情况增减
- 步骤之间可以合并或拆分
- 用户可以随时打断，问问题，再继续

## 命令

- `任务状态 <task-id>` — 查看任务当前进度
- `继续任务 <task-id>` — 从当前步骤继续执行
- `新建任务 <描述>` — 创建新任务并开始第一步

## 脚本工具

详见 scripts/ 目录：
- `init_task.py` — 创建新任务
- `run_next.py` — 执行下一步（可独立调用）
- `status.py` — 查看任务状态

```bash
# 示例：初始化任务
python3 scripts/init_task.py "博客项目" "用 Hexo 建一个技术博客" --path ~/.qclaw/workspace/tasks

# 示例：查看状态
python3 scripts/status.py project-build-001 --path ~/.qclaw/workspace/tasks

# 示例：执行下一步
python3 scripts/run_next.py project-build-001 --path ~/.qclaw/workspace/tasks
```
