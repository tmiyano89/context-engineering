@ai[2025-10-16 00:00] 目的: コンテキスト崩壊を防ぎ、共有知の単一化と検証可能な更新履歴を確保する。

## フロー概要
1. Reflector: 振り返りを行い、共有すべき変更点を抽出する。
2. Curator: Reflector出力を精査し、追加・修正・削除の指示（JSON）を作成、SQLiteに登録する。
3. Updator: SQLiteから未適用の指示を取得し、`docs/project-context.md`へ反映、適用済みフラグを更新する。

## SQLite スキーマ
```sql
CREATE TABLE IF NOT EXISTS instructions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  op TEXT NOT NULL CHECK(op IN ('add','update','delete')),
  target_section TEXT NOT NULL,
  content TEXT NOT NULL,
  applied INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL
);
```

## 指示(JSON)の意味論
- `op`: 'add'|'update'|'delete'
- `target_section`: Markdown見出し（例: "コンテキスト管理フレームワーク"）。
- `content`: セクション本文（Markdown可）。

## 適用規則
- add: セクションが存在しなければ末尾に新規作成。既存なら末尾に追記。
- update: 完全置換（見出しは維持）。
- delete: セクション全体を削除。

## 参考
インスピレーション元動画: [`YouTube`](https://www.youtube.com/watch?v=PWOJ0QANGsA)

