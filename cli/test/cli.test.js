'use strict';

const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const BIN = path.join(__dirname, '..', 'bin', 'better-oss.js');
const REPO = path.join(__dirname, '..', '..');
const FILES = ['fit-profile.md', 'search-strategy.md', 'voice-guide.md', 'playbook.md'];

function tmp() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'better-oss-test-'));
}

function cli(args, env = {}) {
  // CLAUDE_CONFIG_DIR points at an empty folder so a real settings.json is
  // never read; --no-plugin keeps the tests off the claude CLI.
  return spawnSync(process.execPath, [BIN, ...args], {
    encoding: 'utf8',
    env: { ...process.env, CLAUDE_CONFIG_DIR: tmp(), ...env },
  });
}

test('init --no-plugin copies the four example files', () => {
  const home = path.join(tmp(), 'folder');
  const r = cli(['init', '--no-plugin', '--home', home]);
  assert.strictEqual(r.status, 0, r.stderr);
  for (const f of FILES) {
    const text = fs.readFileSync(path.join(home, f), 'utf8');
    assert.match(text, /<!--\s*EXAMPLE:/, `${f} keeps its EXAMPLE banner`);
  }
});

test('a second run keeps files you edited', () => {
  const home = tmp();
  cli(['--no-plugin', '--home', home]);
  fs.writeFileSync(path.join(home, 'voice-guide.md'), 'mine\n');
  const r = cli(['init', '--no-plugin', '--home', home]);
  assert.strictEqual(r.status, 0, r.stderr);
  assert.strictEqual(fs.readFileSync(path.join(home, 'voice-guide.md'), 'utf8'), 'mine\n');
  assert.match(r.stdout, /kept\s+voice-guide\.md/);
});

test('--force overwrites with the shipped examples', () => {
  const home = tmp();
  cli(['--no-plugin', '--home', home]);
  fs.writeFileSync(path.join(home, 'playbook.md'), 'mine\n');
  const r = cli(['--no-plugin', '--force', '--home', home]);
  assert.strictEqual(r.status, 0, r.stderr);
  assert.match(fs.readFileSync(path.join(home, 'playbook.md'), 'utf8'), /EXAMPLE:/);
});

test('--dry-run changes nothing', () => {
  const home = path.join(tmp(), 'never-created');
  const r = cli(['--dry-run', '--no-plugin', '--home', home]);
  assert.strictEqual(r.status, 0, r.stderr);
  assert.strictEqual(fs.existsSync(home), false);
  assert.match(r.stdout, /would created/);
});

test('--dry-run shows the plugin command when claude is missing', (t) => {
  const root = tmp();
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const home = path.join(root, 'data');
  const r = cli(['--dry-run', '--home', home, '--marketplace', '/some/path', '--scope', 'project'], { PATH: root });
  assert.strictEqual(r.status, 0, r.stderr);
  assert.match(r.stdout, /claude plugin install better-oss --marketplace \/some\/path --scope project/);
  assert.match(r.stdout, /MISSING\s+claude/);
  assert.match(r.stdout, /note: fix the MISSING prerequisites/);
  assert.strictEqual(fs.existsSync(home), false);
});

test('--dry-run previews but never installs with claude on PATH', { skip: process.platform === 'win32' }, (t) => {
  const root = tmp();
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const log = path.join(root, 'calls');
  fs.writeFileSync(path.join(root, 'claude'), '#!/bin/sh\nprintf "%s\\n" "$*" >> "$FAKE_CLAUDE_LOG"\nexit 0\n', { mode: 0o755 });
  const home = path.join(root, 'data');
  const r = cli(['--dry-run', '--home', home], { PATH: root, FAKE_CLAUDE_LOG: log });
  assert.strictEqual(r.status, 0, r.stderr);
  assert.match(r.stdout, /plugin: claude plugin install better-oss/);
  assert.strictEqual(fs.readFileSync(log, 'utf8'), '--version\n', 'only the prerequisite probe runs');
  assert.strictEqual(fs.existsSync(home), false);
});

test('BETTER_OSS_HOME is honored', () => {
  const home = tmp();
  const r = cli(['--no-plugin'], { BETTER_OSS_HOME: home });
  assert.strictEqual(r.status, 0, r.stderr);
  assert.ok(fs.existsSync(path.join(home, 'voice-guide.md')));
});

test('bad input exits 2 with a message', () => {
  for (const args of [['--bogus'], ['frobnicate'], ['--scope', 'nope'], ['--home']]) {
    const r = cli(args);
    assert.strictEqual(r.status, 2, args.join(' '));
    assert.match(r.stderr, /better-oss:/);
  }
});

test('--version matches package.json', () => {
  const r = cli(['--version']);
  assert.strictEqual(r.stdout.trim(), require('../package.json').version);
});

test('warns, without editing, about an older hand-installed hook', () => {
  const config = tmp();
  const settings = path.join(config, 'settings.json');
  const body = JSON.stringify({ hooks: { PreToolUse: [{ hooks: [{ command: 'python3 "$HOME/.claude/voice-guard/check_voice.py"' }] }] } });
  fs.writeFileSync(settings, body);
  const r = cli(['--no-plugin', '--home', tmp()], { CLAUDE_CONFIG_DIR: config });
  assert.match(r.stdout, /WARNING/);
  assert.strictEqual(fs.readFileSync(settings, 'utf8'), body, 'settings.json is untouched');
});

test('the JS file list matches core/init.py and the shipped defaults', () => {
  const py = fs.readFileSync(path.join(REPO, 'core', 'init.py'), 'utf8');
  const block = py.match(/PERSONAL_FILES = \[([^\]]*)\]/)[1];
  const pyFiles = [...block.matchAll(/"([^"]+)"/g)].map((m) => m[1]);
  assert.deepStrictEqual(pyFiles, FILES);
  for (const f of FILES) {
    assert.ok(fs.existsSync(path.join(REPO, 'defaults', f)), `defaults/${f} exists`);
  }
});

test('the repo contains no symlinks (they dangle on other machines and leak local paths)', () => {
  const found = [];
  const walk = (dir) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name === '.git' || entry.name === 'node_modules') continue;
      const full = path.join(dir, entry.name);
      if (entry.isSymbolicLink()) found.push(path.relative(REPO, full));
      else if (entry.isDirectory()) walk(full);
    }
  };
  walk(REPO);
  assert.deepStrictEqual(found, []);
});
