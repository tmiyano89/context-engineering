# Context Engineering

コンテキストエンジニアリングの実験・体系化・フレームワーク提案・評価プロジェクト

## 概要

このプロジェクトでは、コンテキストエンジニアリング（Context Engineering）の研究・実験を行い、その体系化と新しいフレームワークの提案・評価を目的としています。

@ai[2025-10-16 00:00] 参考・出典: 提案のインスピレーションは次の動画に基づきます。`https://www.youtube.com/watch?v=PWOJ0QANGsA`

## 背景・目的

### コンテキストエンジニアリングとは
コンテキストエンジニアリングは、AIシステムにおいて適切なコンテキスト（文脈）を設計・構築・管理する技術分野です。効果的なコンテキスト設計により、AIの性能向上、一貫性の確保、意図の正確な理解を実現します。

### 研究目的
1. **実験的検証**: 様々なコンテキスト設計手法の効果を実験的に検証
2. **体系化**: 既存の手法を整理し、体系的な知識ベースを構築
3. **フレームワーク提案**: 新しいコンテキストエンジニアリングフレームワークの設計・提案
4. **評価**: 提案フレームワークの有効性を定量的・定性的に評価

## プロジェクト構成

```
context-engineering/
├── README.md                    # このファイル
├── docs/                       # ドキュメント
│   ├── research/               # 研究資料
│   ├── experiments/            # 実験記録
│   ├── ai-logs/               # AI開発ログ
│   ├── engineers/             # 各AIエンジニアの人物設定
│   └── context-management-flow.md  # コンテキスト管理フロー
├── src/                        # ソースコード
│   ├── frameworks/             # フレームワーク実装
│   ├── experiments/            # 実験コード
│   └── utils/                  # ユーティリティ
├── data/                       # データセット
├── results/                    # 実験結果
└── tests/                      # テストコード
```

## 研究領域

### 1. コンテキスト設計手法
- プロンプトエンジニアリング
- コンテキストウィンドウ最適化
- 動的コンテキスト生成
- マルチモーダルコンテキスト

### 2. 評価指標
- タスク性能指標
- 一貫性指標
- 効率性指標
- ユーザビリティ指標

### 3. 応用領域
- 自然言語処理
- コード生成・理解
- 対話システム
- 知識ベース構築

## 開発方針

### 設計原則
- **型安全性**: TypeScriptを活用した型安全な実装
- **エラー検証性**: 包括的なエラーハンドリングとassertion
- **拡張性**: モジュラー設計による柔軟な拡張
- **保守性**: 明確な意図とコメントによる保守性向上

### コーディング規約
- コメントには `@ai[yyyy-mm-dd hh:mm]` ヘッダーを付与
- 意図を反映したassertionコードを積極的に記述
- セクションごとに目的・背景・意図を要約記載

## コンテキスト管理フレームワーク

@ai[2025-10-16 00:00] 目的: AIエージェントの作業で発生するコンテキストの崩壊（具体的情報の欠落や肥大化）に対処し、共有すべきプロジェクト文脈を単一ソースで正確に保つ。

### 基本方針
- **単一の真実の源（SSOT）**: 管理対象のコンテキストは単一のMarkdown（`docs/project-context.md`）に集約（プロジェクトコンテキスト）。
- **三役分離**: Reflector / Curator / Updator の3エージェントで役割を分担し、反省→指示→適用を分離。
- **検証性・可観測性**: Curatorの更新指示はSQLiteに保存し、適用済みフラグで追跡。

### 3つのAIエンジニア
- **Reflector**: タスク完了や区切りで振り返り、共有すべき新情報、修正・削除候補を抽出して要約。
- **Curator**: Reflectorの要約を検証し、追加・修正・削除を構造化指示（JSON）に変換してSQLiteへ登録。
- **Updator**: SQLiteの未適用指示を読み、`docs/project-context.md`を更新し、適用済みにマーキング。

### データ構造（SQLite `db/context_updates.sqlite`）
- `instructions(id INTEGER PK, op TEXT CHECK(op IN ('add','update','delete')), target_section TEXT, content TEXT, applied INTEGER DEFAULT 0, created_at TEXT)`

### 使い方（フロー）
1. Reflectorが`docs/engineers/reflector.md`のプロンプトに従い要約を作成。
2. Curatorが要約を検証し、指示（add/update/delete）を`instructions`に登録。
3. Updatorが`instructions.applied=0`を順に適用し、`docs/project-context.md`を更新、適用後`applied=1`に設定。

詳細は `docs/context-management-flow.md` を参照。

## 進捗管理

- タスクはチェックリスト形式で管理
- 各タスクの結果は `docs/ai-logs/` に記録
- ログには概要・実装内容・次のステップを含める

## ライセンス

MIT License

## 貢献

このプロジェクトへの貢献を歓迎します。詳細は [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

## 連絡先

- プロジェクトオーナー: [@tmiyano89](https://github.com/tmiyano89)
- リポジトリ: https://github.com/tmiyano89/context-engineering
