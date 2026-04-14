# QClaw Task Runner

QClaw 技能：把大任务拆成小步骤，文件持久化，断点续做。

## 解决的问题

- 大任务超出上下文限制 → 拆成小步骤
- 上下文被压缩后丢失进度 → 每步结果写文件
- 任务中途失败无法继续 → 从断点恢复

## 安装

```bash
# 克隆到 skills 目录
git clone https://github.com/Jia-Yee/qclaw-task-runner.git ~/.qclaw/skills/task-runner
```

## 使用方法

### 在 QClaw 对话中使用

当你描述一个大任务时，QClaw 会自动触发此技能，自动拆分步骤并执行。

### 命令行工具

```bash
# 新建任务
python3 ~/.qclaw/skills/task-runner/scripts/init_task.py "项目名称" "任务描述"

# 查看状态
python3 ~/.qclaw/skills/task-runner/scripts/status.py <task-id>

# 添加并执行下一步
python3 ~/.qclaw/skills/task-runner/scripts/run_next.py <task-id> --title "步骤标题"

# 标记步骤完成
python3 ~/.qclaw/skills/task-runner/scripts/run_next.py <task-id> --mark-done <step-id>
```

## 任务数据存储

所有任务数据保存在 `~/.qclaw/workspace/tasks/<task-id>/`：

```
tasks/<task-id>/
├── MANIFEST.json      # 任务清单
├── step-001.json      # 每步的输入/输出
├── step-002.json
└── ...
```

## 原则

1. **永远拆分** — 大任务变成多个小步骤
2. **每步写文件** — 不靠对话传递状态
3. **失败即停** — 不硬撑，报告问题
4. **断点可续** — 下次对话直接说"继续"

## 依赖

- Python 3.x
- QClaw

## License

MIT
