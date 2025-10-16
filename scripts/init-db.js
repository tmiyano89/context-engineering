// @ai[2025-10-16 00:00] 目的: SQLiteデータベースを初期化し、instructionsテーブルを作成する。
const fs = require('fs');
const path = require('path');
const Database = require('better-sqlite3');

const dbPath = path.join(process.cwd(), 'db', 'context_updates.sqlite');
fs.mkdirSync(path.dirname(dbPath), { recursive: true });
const db = new Database(dbPath);
db.exec(`CREATE TABLE IF NOT EXISTS instructions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  op TEXT NOT NULL CHECK(op IN ('add','update','delete')),
  target_section TEXT NOT NULL,
  content TEXT NOT NULL,
  applied INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL
);`);
console.log('initialized:', dbPath);

