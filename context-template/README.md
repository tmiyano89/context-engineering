# コンテキスト管理テンプレート

このディレクトリは、プロジェクトにコンテキスト管理機能を組み込むためのテンプレートです。

## 使用方法

1. このディレクトリをプロジェクトにコピー
2. 適切な名前にリネーム（例: `my-project-context`）
3. 必要に応じて設定をカスタマイズ

## 構成

```
context-template/
├── README.md                    # このファイル
├── docs/                        # ドキュメント
│   ├── engineers/               # AIエンジニアの人物設定
│   │   ├── reflector.md         # 振り返り・洞察エキスパート
│   │   ├── curator.md           # 構造化・検証エキスパート
│   │   └── updator.md           # ドキュメント整理エキスパート
│   ├── context-management-flow.md  # コンテキスト管理フロー
│   └── project-context.md       # プロジェクトコンテキスト（SSOT）
├── db/                          # データベース
│   └── context_updates.sqlite   # 更新指示を管理するSQLite
└── scripts/                     # 実行スクリプト
    ├── init_db.py              # データベース初期化
    ├── seed_instructions.py    # サンプル指示登録
    └── updator.py              # コンテキスト更新実行
```

## スクリプト実行

### データベース初期化
```bash
cd scripts
python3 init_db.py
```

### サンプル指示登録
```bash
cd scripts
python3 seed_instructions.py
```

### コンテキスト更新実行
```bash
cd scripts
python3 updator.py
```

## フロー

1. **Reflector**: 作業を振り返り、共有すべき変更点を抽出
2. **Curator**: Reflectorの出力を検証し、構造化指示（JSON）を作成してSQLiteに登録
3. **Updator**: SQLiteの未適用指示を読み取り、`docs/project-context.md`を更新

## 注意事項

- 各AIエンジニアの人物設定ファイルは変更しないでください
- 作業内容の変更は`docs/context-management-flow.md`で行ってください
- データベースファイル（`db/context_updates.sqlite`）はバージョン管理に含めないことを推奨します
