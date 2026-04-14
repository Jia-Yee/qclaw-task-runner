#!/usr/bin/env python3
"""查看任务状态"""
import argparse
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="查看任务状态")
    parser.add_argument("task_id", help="任务ID")
    parser.add_argument("--path", default=os.path.expanduser("~/.qclaw/workspace/tasks"), help="任务根目录")
    args = parser.parse_args()

    manifest_path = os.path.join(args.path, args.task_id, "MANIFEST.json")

    if not os.path.exists(manifest_path):
        print(f"❌ 任务不存在: {args.task_id}")
        sys.exit(1)

    with open(manifest_path, encoding="utf-8") as f:
        m = json.load(f)

    print(f"\n📋 任务: {m['name']}")
    print(f"   ID: {m['id']}")
    print(f"   描述: {m['description']}")
    print(f"   状态: {m['status']}  |  进度: {m['current_step']}/{m['total_steps']}")
    print(f"   创建: {m['created']}\n")

    if m["steps"]:
        print("  步骤:")
        for s in m["steps"]:
            icon = {"done": "✅", "in_progress": "🔄", "pending": "⬜", "failed": "❌"}.get(s["status"], "⬜")
            print(f"  {icon} [{s['id']:03d}] {s['title']} — {s['status']}")
            if s.get("summary"):
                print(f"       {s['summary']}")
    else:
        print("  (尚无步骤)")
    print()

if __name__ == "__main__":
    main()
