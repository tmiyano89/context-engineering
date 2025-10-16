#!/usr/bin/env python3
"""
@ai[2025-10-16 00:25] 目的: SQLiteデータベースを初期化するPythonスクリプト
"""

import sqlite3
import os
from pathlib import Path

def main():
    """データベース初期化"""
    script_dir = Path(__file__).parent
    db_path = script_dir.parent / "db" / "context_updates.sqlite"
    
    # ディレクトリ作成
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # データベース接続
    conn = sqlite3.connect(str(db_path))
    
    # テーブル作成
    conn.execute("""
        CREATE TABLE IF NOT EXISTS instructions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            op TEXT NOT NULL CHECK(op IN ('add','update','delete')),
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            applied INTEGER NOT NULL DEFAULT 0,
            created_at INTEGER NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized: {db_path}")

if __name__ == "__main__":
    main()
