#!/usr/bin/env python3
"""
@ai[2025-10-16 00:25] 目的: SQLiteの未適用指示を反映し、プロジェクトコンテキストを更新するPythonスクリプト
"""

import sqlite3
import os
import shutil
from datetime import datetime
from pathlib import Path

def assert_condition(condition, message):
    """アサーション関数"""
    if not condition:
        raise AssertionError(message)

def load_markdown(file_path):
    """Markdownファイルを読み込む"""
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_markdown(file_path, content):
    """Markdownファイルを保存する"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def find_section_indices(markdown, heading):
    """セクションの開始・終了位置を取得"""
    lines = markdown.split('\n')
    start = -1
    
    # 見出しを検索（# レベルまで含む）
    for i, line in enumerate(lines):
        if line.strip().startswith('#') and heading in line:
            start = i
            break
    
    if start == -1:
        return None
    
    # 次の同レベル以下の見出しを探す
    current_level = len(lines[start]) - len(lines[start].lstrip('#'))
    end = len(lines)
    
    for i in range(start + 1, len(lines)):
        if lines[i].strip().startswith('#'):
            level = len(lines[i]) - len(lines[i].lstrip('#'))
            if level <= current_level:
                end = i
                break
    
    return {"start": start, "end": end}

def apply_add(markdown, heading, content):
    """セクションを追加"""
    lines = markdown.split('\n') if markdown else []
    
    if not markdown:
        return f"# {heading}\n\n{content}\n"
    
    indices = find_section_indices(markdown, heading)
    if not indices:
        return markdown + f"\n\n# {heading}\n\n{content}\n"
    
    before = '\n'.join(lines[:indices["end"]])
    after = '\n'.join(lines[indices["end"]:])
    insertion = f"\n{content}\n" if lines[indices["end"] - 1].strip() else f"{content}\n"
    
    return before + insertion + (f"\n{after}" if after else "")

def apply_update(markdown, heading, content):
    """セクションを更新"""
    indices = find_section_indices(markdown, heading)
    if not indices:
        return apply_add(markdown, heading, content)
    
    lines = markdown.split('\n')
    before = '\n'.join(lines[:indices["start"] + 1])
    after = '\n'.join(lines[indices["end"]:])
    mid = f"\n{content}\n" if content else "\n"
    
    return before + mid + (f"\n{after}" if after else "")

def apply_delete(markdown, heading):
    """セクションを削除"""
    indices = find_section_indices(markdown, heading)
    if not indices:
        return markdown
    
    lines = markdown.split('\n')
    before = '\n'.join(lines[:indices["start"]])
    after = '\n'.join(lines[indices["end"]:])
    
    return '\n\n'.join(filter(None, [before, after]))

def main():
    """メイン処理"""
    # パス設定
    script_dir = Path(__file__).parent
    db_path = script_dir.parent / "db" / "context_updates.sqlite"
    context_path = script_dir.parent / "docs" / "project-context.md"
    
    # データベース存在確認
    assert_condition(db_path.exists(), f"Database not found at {db_path}")
    
    # データベース接続
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode = WAL")
    
    # テーブル作成（存在しない場合）
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
    
    # 未適用の指示を取得
    cursor = conn.execute(
        "SELECT id, op, title, content, applied, created_at FROM instructions WHERE applied = 0 ORDER BY id ASC"
    )
    instructions = cursor.fetchall()
    
    if not instructions:
        print("No pending instructions.")
        return
    
    # バックアップ作成
    if context_path.exists():
        backup_path = context_path.with_suffix('.md.bak')
        shutil.copy2(context_path, backup_path)
        print(f"Backup created: {backup_path}")
    
    # Markdownファイル読み込み
    markdown = load_markdown(context_path)
    
    # 指示を適用
    for instruction in instructions:
        id_val, op, title, content, applied, created_at = instruction
        
        try:
            if op == 'add':
                markdown = apply_add(markdown, title, content)
            elif op == 'update':
                markdown = apply_update(markdown, title, content)
            elif op == 'delete':
                markdown = apply_delete(markdown, title)
            else:
                assert_condition(False, f"Unknown operation: {op}")
            
            # 適用済みにマーク
            conn.execute("UPDATE instructions SET applied = 1 WHERE id = ?", (id_val,))
            print(f"Applied instruction {id_val}: {op} - {title}")
            
        except Exception as e:
            print(f"Error applying instruction {id_val}: {e}")
            # エラー時はロールバック
            if context_path.exists() and backup_path.exists():
                shutil.copy2(backup_path, context_path)
                print("Rolled back to backup")
            raise
    
    # 変更を保存
    save_markdown(context_path, markdown)
    
    # コミット
    conn.commit()
    conn.close()
    
    print(f"Applied {len(instructions)} instruction(s).")

if __name__ == "__main__":
    main()
