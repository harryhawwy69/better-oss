#!/usr/bin/env node
'use strict';

// better-oss installer. `npx better-oss-cli init`:
//   1. checks the programs the tools call (python3, git, gh, claude),
//   2. installs the better-oss Claude Code plugin through the claude CLI,
//   3. copies the shipped example files you are meant to make your own into
//      ~/.claude/better-oss/, without overwriting anything you already have.
// It never edits Claude Code's settings.json: the plugin's hooks come with
// the plugin. Node only, no dependencies.

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const VERSION = require('../package.json').version;
const PLUGIN = 'better-oss';
const DEFAULT_MARKETPLACE = 'mobeloper/better-oss';
const SCOPES = ['user', 'project', 'local'];

// The personal files: yours to edit, read from your folder first. Keep in
// sync with PERSONAL_FILES in core/init.py (a test checks they match).
const PERSONAL_FILES = [
  'fit-profile.md',
  'search-strategy.md',
  'voice-guide.md',
  'playbook.md',
];

const HELP = `better-oss-cli ${VERSION}

Usage: better-oss-cli init [options]

Installs the better-oss Claude Code plugin and copies the example files you
are meant to make your own into your better-oss folder.

Options:
  --home <dir>          your better-oss folder
                        (default: $BETTER_OSS_HOME or ~/.claude/better-oss)
  --no-plugin           only copy the example files; skip the plugin install
  --force               overwrite your files with the shipped examples
  --dry-run             show what would happen; change nothing
  --scope <scope>       plugin scope: user (default), project, or local
  --marketplace <src>   where to install the plugin from
                        (default: ${DEFAULT_MARKETPLACE}; a git URL or local path also works)
  -v, --version         print the version
  -h, --help            print this help
`;

function fail(message, code = 2) {
  console.error(`better-oss: ${message}`);
  process.exit(code);
}

function parseArgs(argv) {
  const opts = {
    command: null,
    home: null,
    plugin: true,
    force: false,
    dryRun: false,
    scope: 'user',
    marketplace: DEFAULT_MARKETPLACE,
  };
  const takeValue = (i, flag) => {
    if (i + 1 >= argv.length || argv[i + 1].startsWith('--')) {
      fail(`${flag} needs a value (see --help)`);
    }
    return argv[i + 1];
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h' || a === '--help') {
      process.stdout.write(HELP);
      process.exit(0);
    } else if (a === '-v' || a === '--version') {
      console.log(VERSION);
      process.exit(0);
    } else if (a === '--home') {
      opts.home = takeValue(i, a); i++;
    } else if (a === '--scope') {
      opts.scope = takeValue(i, a); i++;
      if (!SCOPES.includes(opts.scope)) {
        fail(`--scope must be one of: ${SCOPES.join(', ')}`);
      }
    } else if (a === '--marketplace') {
      opts.marketplace = takeValue(i, a); i++;
    } else if (a === '--no-plugin') {
      opts.plugin = false;
    } else if (a === '--force') {
      opts.force = true;
    } else if (a === '--dry-run') {
      opts.dryRun = true;
    } else if (a.startsWith('-')) {
      fail(`unknown option ${a} (see --help)`);
    } else if (opts.command === null) {
      opts.command = a;
    } else {
      fail(`unexpected argument ${a} (see --help)`);
    }
  }
  if (opts.command === null) opts.command = 'init';
  if (opts.command !== 'init') {
    fail(`unknown command ${opts.command} (the only command is init; see --help)`);
  }
  return opts;
}

function expandHome(p) {
  return p === '~' || p.startsWith('~/') ? path.join(os.homedir(), p.slice(1)) : p;
}

function dataDir(opts) {
  const chosen = opts.home || process.env.BETTER_OSS_HOME;
  return path.resolve(expandHome(chosen || path.join(os.homedir(), '.claude', 'better-oss')));
}

// The shipped examples: next to bin/ in the published package, or at the
// repo root when run from a checkout (node cli/bin/better-oss.js).
function defaultsDir() {
  const candidates = [
    path.join(__dirname, '..', 'defaults'),
    path.join(__dirname, '..', '..', 'defaults'),
  ];
  const found = candidates.find((d) => fs.existsSync(path.join(d, 'voice-guide.md')));
  if (!found) {
    fail(`could not find the shipped defaults (looked in ${candidates.join(' and ')}). Reinstall better-oss.`, 1);
  }
  return found;
}

function run(cmd, args) {
  try {
    return spawnSync(cmd, args, { encoding: 'utf8', timeout: 20000 });
  } catch (e) {
    return { error: e };
  }
}

function hasProgram(cmd) {
  const r = run(cmd, ['--version']);
  return !r.error && r.status === 0;
}

// Returns { missing: string[], claudeMissing: boolean }; prints one line each.
function checkPrerequisites() {
  const missing = [];
  console.log('prerequisites:');

  const py = run('python3', ['-c', 'import sys; print(sys.version_info >= (3, 9))']);
  if (!py.error && py.status === 0 && py.stdout.trim() === 'True') {
    console.log('  ok       python3 (3.9 or newer)');
  } else {
    console.log('  MISSING  python3 3.9 or newer: the hooks and tools run on it');
    missing.push('python3');
  }
  for (const [cmd, why] of [
    ['git', 'reads your branch and diff'],
    ['gh', 'searches and reads GitHub'],
    ['claude', 'runs the model passes (Sonnet) and hosts the plugin'],
  ]) {
    if (hasProgram(cmd)) {
      console.log(`  ok       ${cmd}`);
    } else {
      console.log(`  MISSING  ${cmd}: ${why}`);
      missing.push(cmd);
    }
  }
  if (!missing.includes('gh')) {
    const auth = run('gh', ['auth', 'status']);
    if (!auth.error && auth.status === 0) {
      console.log('  ok       gh is logged in');
    } else {
      console.log('  MISSING  gh login: run `gh auth login`');
      missing.push('gh login');
    }
  }
  return { missing, claudeMissing: missing.includes('claude') };
}

function installPlugin(opts) {
  const args = ['plugin', 'install', PLUGIN, '--marketplace', opts.marketplace, '--scope', opts.scope];
  console.log(`plugin: claude ${args.join(' ')}`);
  if (opts.dryRun) return true;
  const r = spawnSync('claude', args, { stdio: 'inherit' });
  if (r.error || r.status !== 0) {
    console.error('plugin: the install did not complete. Inside Claude Code you can run:');
    console.error(`  /plugin install ${PLUGIN} --marketplace ${opts.marketplace}`);
    return false;
  }
  return true;
}

function seedFiles(opts) {
  const src = defaultsDir();
  const dst = dataDir(opts);
  console.log(`better-oss folder: ${dst}`);
  if (!opts.dryRun) fs.mkdirSync(dst, { recursive: true });
  let ok = true;
  for (const name of PERSONAL_FILES) {
    const from = path.join(src, name);
    const to = path.join(dst, name);
    if (!fs.existsSync(from)) {
      console.error(`  MISSING shipped file ${from} (reinstall better-oss)`);
      ok = false;
      continue;
    }
    const exists = fs.existsSync(to);
    if (exists && !opts.force) {
      console.log(`  kept     ${name} (already there)`);
      continue;
    }
    if (!opts.dryRun) fs.copyFileSync(from, to);
    const verb = exists ? 'replaced' : 'created ';
    console.log(`  ${opts.dryRun ? 'would ' : ''}${verb} ${name} (an EXAMPLE you should rewrite)`);
  }
  return ok;
}

// Read-only: an older, hand-installed copy of the two hooks would run the
// guards twice next to the plugin's. Warn; never edit the file.
function warnAboutOldHooks() {
  const configDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
  const file = path.join(configDir, 'settings.json');
  let text;
  try {
    text = fs.readFileSync(file, 'utf8');
  } catch {
    return;
  }
  if (/voice-guard[\\/]check_voice\.py|ship-gate[\\/]check_gate\.py/.test(text)) {
    console.log('');
    console.log(`WARNING: ${file} already registers a voice-guard or ship-gate hook.`);
    console.log('The plugin brings its own copies, so with both in place each guard runs');
    console.log('twice. Remove the old entries yourself (this installer never edits your');
    console.log('settings), then restart Claude Code.');
  }
}

function init(opts) {
  if (opts.dryRun) console.log('(dry run: nothing will be changed)\n');
  const { missing, claudeMissing } = checkPrerequisites();
  console.log('');

  let failed = false;
  if (opts.plugin) {
    if (claudeMissing && !opts.dryRun) {
      console.error('plugin: skipped, the claude CLI is not on PATH. Install Claude Code, then run this again.');
      failed = true;
    } else if (!installPlugin(opts)) {
      failed = true;
    }
    console.log('');
  }
  if (!seedFiles(opts)) failed = true;
  warnAboutOldHooks();

  console.log('');
  console.log('next steps:');
  console.log('  1. Rewrite voice-guide.md in your own voice. The voice-guard hook enforces it');
  console.log('     on your outgoing comments, so until you do it enforces the example.');
  console.log('  2. Edit fit-profile.md and search-strategy.md for the issues you want.');
  console.log('  3. Restart Claude Code, then try /better-oss:issue-scout.');
  console.log('  4. Per repository, copy ship-manifest.md and claude-local-template.md into');
  console.log('     your clone (/better-oss:init prints the commands).');
  if (missing.length && !failed) {
    console.log('');
    console.log(`note: fix the MISSING prerequisites above (${missing.join(', ')}) before using the tools.`);
  }
  return failed ? 1 : 0;
}

process.exit(init(parseArgs(process.argv.slice(2))));
