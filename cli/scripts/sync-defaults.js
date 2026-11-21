#!/usr/bin/env node
'use strict';

// Runs before `npm pack` / `npm publish`: copies the repo's shipped
// defaults/ folder into this package, so the published installer carries
// the same example files the plugin does. cli/defaults/ is git-ignored;
// the repo-root defaults/ stays the single source of truth.

const fs = require('node:fs');
const path = require('node:path');

const src = path.join(__dirname, '..', '..', 'defaults');
const dst = path.join(__dirname, '..', 'defaults');

if (!fs.existsSync(path.join(src, 'voice-guide.md'))) {
  console.error(`sync-defaults: no defaults found at ${src}`);
  process.exit(1);
}
fs.rmSync(dst, { recursive: true, force: true });
fs.cpSync(src, dst, { recursive: true });
console.log(`sync-defaults: copied ${src} -> ${dst}`);
