#!/usr/bin/env python3
"""创建新任务目录和 MANIFEST.json"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

TEMPLATE = """{{
  "id": "{task_id}",
  "name": "{name}",
  "description": "{description}",
  "created": "{created}",
  "status": "pending",
  "current_step": 0,
  "total_steps": 0,
  "steps": []
}}"""

def make_task_id(name: str) -> str:
    """从任务名生成短 id"""
    import hashlib, time
    seed = f"{name}{time.time()}"
    return seed[:20].replace(" ", "-").replace("/", "-")

def main():
    parser = argparse.ArgumentParser(description="初始化一个新任务")
    parser.add_argument("name", help="任务名称（简短）")
    parser.add_argument("description", help="任务详细描述")
    parser.add_argument("--path", default=os.path.expanduser("~/.qclaw/workspace/tasks"), help="任务根目录")
    parser.add_argument("--id", help="指定任务ID（默认自动生成）")
    args = parser.parse_args()

    task_id = args.id or make_task_id(args.name)
    task_dir = os.path.join(args.path, task_id)

    if os.path.exists(task_dir):
        print(f"❌ 任务 {task_id} 已存在: {task_dir}")
        sys.exit(1)

    os.makedirs(task_dir, exist_ok=True)

    manifest = TEMPLATE.format(
        task_id=task_id,
        name=args.name,
        description=args.description,
        created=datetime.now(timezone.utc).isoformat().replace("+00:00", "+08:00"),
    )

    manifest_path = os.path.join(task_dir, "MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest)

    print(f"✅ 任务已创建:")
    print(f"   目录: {task_dir}")
    print(f"   ID:   {task_id}")
    print(f"   名称: {args.name}")
    print(f"   路径: {manifest_path}")

if __name__ == "__main__":
    main()
