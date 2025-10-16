// @ai[2025-10-16 00:00] 目的: SQLiteの指示を`docs/project-context.md`へ適用するスクリプト。
// 注意: Node.js + better-sqlite3 を使用。エラー時は明示的に失敗させる。

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import Database from 'better-sqlite3';

type Instruction = {
  id: number;
  op: 'add' | 'update' | 'delete';
  target_section: string;
  content: string;
  applied: number;
  created_at: string;
};

function assert(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(message);
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const DB_PATH = path.join(ROOT, 'db', 'context_updates.sqlite');
const CONTEXT_PATH = path.join(ROOT, 'docs', 'project-context.md');

function loadMarkdown(filePath: string): string {
  if (!fs.existsSync(filePath)) return '';
  return fs.readFileSync(filePath, 'utf8');
}

function saveMarkdown(filePath: string, content: string) {
  fs.writeFileSync(filePath, content, 'utf8');
}

function findSectionIndices(markdown: string, heading: string): { start: number; end: number } | null {
  const lines = markdown.split('\n');
  const headingPattern = new RegExp(`^#{1,6}\\s+${heading.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\$&')}\\s*$`);
  let start = -1;
  for (let i = 0; i < lines.length; i++) {
    if (headingPattern.test(lines[i])) {
      start = i;
      break;
    }
  }
  if (start === -1) return null;
  let end = lines.length;
  const currentLevel = (lines[start].match(/^#+/) || ['#'])[0].length;
  for (let i = start + 1; i < lines.length; i++) {
    const m = lines[i].match(/^(#+)\s+/);
    if (m) {
      const level = m[1].length;
      if (level <= currentLevel) {
        end = i;
        break;
      }
    }
  }
  return { start, end };
}

function applyAdd(markdown: string, heading: string, content: string): string {
  const lines = markdown ? markdown.split('\n') : [];
  if (!markdown) {
    return [`# ${heading}`, '', content, ''].join('\n');
  }
  const indices = findSectionIndices(markdown, heading);
  if (!indices) {
    return markdown + `\n\n# ${heading}\n\n${content}\n`;
  }
  const before = lines.slice(0, indices.end).join('\n');
  const after = lines.slice(indices.end).join('\n');
  const insertion = (lines[indices.end - 1]?.trim() ? '\n' : '') + content + '\n';
  return before + insertion + (after ? '\n' + after : '');
}

function applyUpdate(markdown: string, heading: string, content: string): string {
  const indices = findSectionIndices(markdown, heading);
  if (!indices) {
    return applyAdd(markdown, heading, content);
  }
  const lines = markdown.split('\n');
  const before = lines.slice(0, indices.start + 1).join('\n');
  const after = lines.slice(indices.end).join('\n');
  const mid = [''].concat(content ? [content] : []).join('\n');
  return before + '\n' + mid + '\n' + (after ? '\n' + after : '');
}

function applyDelete(markdown: string, heading: string): string {
  const indices = findSectionIndices(markdown, heading);
  if (!indices) return markdown;
  const lines = markdown.split('\n');
  const before = lines.slice(0, indices.start).join('\n');
  const after = lines.slice(indices.end).join('\n');
  return [before, after].filter(Boolean).join('\n\n');
}

function main() {
  assert(fs.existsSync(DB_PATH), `DB not found at ${DB_PATH}`);
  const db = new Database(DB_PATH);
  db.pragma('journal_mode = WAL');
  db.prepare(`CREATE TABLE IF NOT EXISTS instructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    op TEXT NOT NULL CHECK(op IN ('add','update','delete')),
    target_section TEXT NOT NULL,
    content TEXT NOT NULL,
    applied INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
  )`).run();

  const select = db.prepare<[]>('SELECT id, op, target_section, content, applied, created_at FROM instructions WHERE applied = 0 ORDER BY id ASC');
  const toApply = select.all() as Instruction[];

  if (toApply.length === 0) {
    console.log('No pending instructions.');
    return;
  }

  let markdown = loadMarkdown(CONTEXT_PATH);
  for (const instr of toApply) {
    if (instr.op === 'add') {
      markdown = applyAdd(markdown, instr.target_section, instr.content);
    } else if (instr.op === 'update') {
      markdown = applyUpdate(markdown, instr.target_section, instr.content);
    } else if (instr.op === 'delete') {
      markdown = applyDelete(markdown, instr.target_section);
    } else {
      assert(false, `Unknown op: ${instr.op}`);
    }
    db.prepare('UPDATE instructions SET applied = 1 WHERE id = ?').run(instr.id);
  }

  saveMarkdown(CONTEXT_PATH, markdown);
  console.log(`Applied ${toApply.length} instruction(s).`);
}

main();


