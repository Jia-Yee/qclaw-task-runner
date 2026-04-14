#!/usr/bin/env python3
"""
执行任务的下一个步骤。

用法:
  python3 run_next.py <task-id> --path <tasks-root>

这个脚本本身只是标记状态 + 写入下一步配置，
实际执行由 AI agent 在读取 MANIFEST 后完成。
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

def main():
    parser = argparse.ArgumentParser(description="准备执行下一步骤（标记 in_progress）")
    parser.add_argument("task_id", help="任务ID")
    parser.add_argument("--path", default=os.path.expanduser("~/.qclaw/workspace/tasks"), help="任务根目录")
    parser.add_argument("--title", help="下一步骤标题（新增步骤时用）")
    parser.add_argument("--mark-done", type=int, metavar="STEP_ID", help="将指定步骤标记为 done")
    args = parser.parse_args()

    manifest_path = os.path.join(args.path, args.task_id, "MANIFEST.json")

    if not os.path.exists(manifest_path):
        print(f"❌ 任务不存在: {args.task_id}")
        sys.exit(1)

    with open(manifest_path, encoding="utf-8") as f:
        m = json.load(f)

    # --- 标记已有步骤完成 ---
    if args.mark_done:
        for s in m["steps"]:
            if s["id"] == args.mark_done:
                s["status"] = "done"
                s["completed"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "+08:00")
                m["current_step"] = args.mark_done
                m["status"] = "in_progress"
                print(f"✅ 步骤 {args.mark_done} 已标记为 done")
                break
        else:
            print(f"❌ 未找到步骤: {args.mark_done}")
            sys.exit(1)

    # --- 添加新步骤并设为 in_progress ---
    elif args.title:
        next_id = max((s["id"] for s in m["steps"]), default=0) + 1
        step = {
            "id": next_id,
            "title": args.title,
            "status": "in_progress",
            "result_file": None,
            "summary": None,
        }
        m["steps"].append(step)
        m["current_step"] = next_id
        m["total_steps"] = len(m["steps"])

        # 创建步骤结果文件模板
        step_file = os.path.join(args.path, args.task_id, f"step-{next_id:03d}.json")
        step_data = {
            "step_id": next_id,
            "title": args.title,
            "status": "in_progress",
            "started": datetime.now(timezone.utc).isoformat().replace("+00:00", "+08:00"),
            "completed": None,
            "input": {},
            "output": {
                "summary": None,
                "files_created": [],
                "files_modified": [],
                "errors": [],
                "next_steps_hints": [],
            },
            "artifacts": [],
        }
        with open(step_file, "w", encoding="utf-8") as f:
            json.dump(step_data, f, ensure_ascii=False, indent=2)

        print(f"🔄 步骤 {next_id} 已创建并设为 in_progress: {args.title}")
        print(f"   结果文件: {step_file}")

    else:
        # 显示当前状态，不做修改
        cur = m["current_step"]
        next_step = next((s for s in m["steps"] if s["id"] == cur and s["status"] == "in_progress"), None)
        if next_step:
            print(f"🔄 当前进行中: 步骤 {cur} — {next_step['title']}")
        else:
            next_pending = next((s for s in m["steps"] if s["status"] == "pending"), None)
            if next_pending:
                print(f"⬜ 下一个待执行: 步骤 {next_pending['id']} — {next_pending['title']}")
            else:
                print(f"✅ 任务已完成: {m['name']}")

    # 保存 manifest
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
