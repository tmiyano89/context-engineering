#!/usr/bin/env python3
"""
@ai[2025-10-16 00:25] 目的: サンプルの指示をデータベースに登録するPythonスクリプト
"""

import sqlite3
import time
from pathlib import Path

def main():
    """サンプル指示を登録"""
    script_dir = Path(__file__).parent
    db_path = script_dir.parent / "db" / "context_updates.sqlite"
    
    # データベース接続
    conn = sqlite3.connect(str(db_path))
    
    # 現在時刻（エポック秒）
    now = int(time.time() * 1000)
    
    # サンプル指示を登録
    instructions = [
        ("add", "研究課題", "- 評価指標の具体化\n- Reflectorの出力テンプレ策定", now),
        ("update", "原則", "- 単一の真実の源\n- 三役分離（Reflector/Curator/Updator）\n- 検証可能性（SQLiteでの指示管理）\n- トレーサビリティ（適用履歴の保持）", now),
    ]
    
    cursor = conn.cursor()
    for op, title, content, created_at in instructions:
        cursor.execute(
            "INSERT INTO instructions (op, title, content, created_at) VALUES (?, ?, ?, ?)",
            (op, title, content, created_at)
        )
    
    conn.commit()
    conn.close()
    
    print(f"Seeded {len(instructions)} instructions.")

if __name__ == "__main__":
    main()
