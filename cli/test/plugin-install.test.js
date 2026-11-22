'use strict';

// Issue #22: the `claude plugin install` step had no coverage. cli.test.js seeds
// the example files with --no-plugin, so a broken install command, a wrong
// --scope, or a silent failure of the CLI itself would pass every test here.
//
// Each test puts a fake `claude` first on PATH. The fake records its arguments
// and exits with a chosen status, so the assertions are on what the installer
// actually invokes, not on the real Claude Code.

const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const BIN = path.join(__dirname, '..', 'bin', 'better-oss.js');

function tmp() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'better-oss-plugin-'));
}

// A fake `claude` that appends its arguments to `log` and exits with `status`.
// It answers `--version` with 0 whatever `status` is, because the prerequisite
// probe must pass for the install to be reached at all.
function fakeClaude(dir, status = 0) {
  const log = path.join(dir, 'calls.log');
  const script = path.join(dir, 'claude');
  fs.writeFileSync(
    script,
    `#!/bin/sh\nprintf '%s\\n' "$*" >> ${JSON.stringify(log)}\n` +
      `if [ "$1" = "--version" ]; then exit 0; fi\nexit ${status}\n`,
  );
  fs.chmodSync(script, 0o755);
  return log;
}

// `--version` is the prerequisite probe, not an install; the assertions are on
// the install calls, so it is left out.
function calls(log) {
  if (!fs.existsSync(log)) return [];
  return fs
    .readFileSync(log, 'utf8')
    .split('\n')
    .filter((line) => line && line !== '--version');
}

// `bin` is prepended to PATH, so it is where the fake `claude` lives. An empty
// `bin` means no `claude` at all.
function cli(args, { bin = tmp(), pathOnly = false } = {}) {
  const home = path.join(tmp(), 'home');
  const r = spawnSync(process.execPath, [BIN, ...args, '--home', home], {
    encoding: 'utf8',
    env: {
      ...process.env,
      CLAUDE_CONFIG_DIR: tmp(),
      PATH: pathOnly ? bin : `${bin}:${process.env.PATH}`,
    },
  });
  return { r, home };
}

// A PATH holding the tools the installer probes (git, gh, python3, sh) but no
// `claude`. Symlinked by absolute path, so it does not matter where they live;
// a development host with Claude Code installed would otherwise satisfy the
// prerequisite and the "missing" case could never be reached.
function pathWithoutClaude() {
  const dir = tmp();
  for (const cmd of ['git', 'gh', 'python3', 'sh']) {
    const found = spawnSync('sh', ['-c', `command -v ${cmd}`], { encoding: 'utf8' })
      .stdout.trim();
    if (found) fs.symlinkSync(found, path.join(dir, cmd));
  }
  return dir;
}

const DEFAULT_CALL = 'plugin install better-oss --marketplace mobeloper/better-oss --scope user';

test('the plugin install reaches claude and succeeds', () => {
  const bin = tmp();
  const log = fakeClaude(bin, 0);

  const { r, home } = cli(['init'], { bin });

  assert.strictEqual(r.status, 0, r.stderr);
  assert.deepStrictEqual(calls(log), [DEFAULT_CALL]);
  // The install is one step, not the whole job: the files are still seeded.
  assert.ok(fs.existsSync(path.join(home, 'voice-guide.md')), 'the example files are seeded');
});

test('a failing install prints the manual fallback and exits 1', () => {
  const bin = tmp();
  const log = fakeClaude(bin, 1);

  const { r } = cli(['init'], { bin });

  assert.strictEqual(r.status, 1);
  assert.match(r.stderr, /the install did not complete/);
  assert.match(r.stderr, /\/plugin install better-oss --marketplace mobeloper\/better-oss/);
  assert.strictEqual(calls(log).length, 1, 'claude was called exactly once');
});

test('each --scope reaches claude', () => {
  for (const scope of ['user', 'project', 'local']) {
    const bin = tmp();
    const log = fakeClaude(bin, 0);

    const { r } = cli(['init', '--scope', scope], { bin });

    assert.strictEqual(r.status, 0, `${scope}: ${r.stderr}`);
    assert.deepStrictEqual(calls(log), [
      `plugin install better-oss --marketplace mobeloper/better-oss --scope ${scope}`,
    ]);
  }
});

test('--marketplace overrides the default', () => {
  const bin = tmp();
  const log = fakeClaude(bin, 0);

  const { r } = cli(['init', '--marketplace', '/some/path', '--scope', 'project'], { bin });

  assert.strictEqual(r.status, 0, r.stderr);
  assert.deepStrictEqual(calls(log), [
    'plugin install better-oss --marketplace /some/path --scope project',
  ]);
});

test('a missing claude skips the install, says so, and exits 1', () => {
  // A PATH with every tool the installer probes except `claude`.
  const bin = pathWithoutClaude();

  const { r } = cli(['init'], { bin, pathOnly: true });

  assert.strictEqual(r.status, 1);
  assert.match(r.stderr, /the claude CLI is not on PATH/);
});

test('--dry-run shows the command and never calls claude', () => {
  const bin = tmp();
  const log = fakeClaude(bin, 0);

  const { r } = cli(['init', '--dry-run'], { bin });

  assert.strictEqual(r.status, 0, r.stderr);
  assert.deepStrictEqual(calls(log), [], 'claude is not invoked');
  assert.match(r.stdout, /claude plugin install better-oss/);
});
