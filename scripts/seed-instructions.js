// @ai[2025-10-16 00:00] 目的: サンプルの指示をinstructionsに登録する。
const path = require('path');
const Database = require('better-sqlite3');

const dbPath = path.join(process.cwd(), 'db', 'context_updates.sqlite');
const db = new Database(dbPath);
const now = new Date().toISOString();

const insert = db.prepare(`INSERT INTO instructions (op, target_section, content, created_at) VALUES (?,?,?,?)`);
insert.run('add', '研究課題', '- 評価指標の具体化\n- Reflectorの出力テンプレ策定', now);
insert.run('update', '原則', '- 単一の真実の源\n- 三役分離（Reflector/Curator/Updator）\n- 検証可能性（SQLiteでの指示管理）\n- トレーサビリティ（適用履歴の保持）', now);
console.log('seeded');

