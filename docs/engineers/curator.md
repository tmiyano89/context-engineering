@ai[2025-10-16 00:00] 目的: Reflectorの出力を検証し、構造化指示(JSON)へ落とし込み、SQLiteへ登録する。

## 指示(JSON)フォーマット例
```json
{
  "op": "add",
  "target_section": "プロジェクトコンテキストの原則",
  "content": "- 単一の真実の源\n- 三役分離\n- 検証可能性"
}
```

## 登録方法
- `db/context_updates.sqlite` の `instructions` に1レコードとして登録。
- `created_at` はISO8601。

