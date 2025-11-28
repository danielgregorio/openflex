#!/usr/bin/env node

/**
 * OpenFlex Neo - Watch Mode CLI
 * Auto-recompile on file changes
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const packageRoot = path.join(__dirname, '..');

function checkPython() {
  const pythonCommands = ['python3', 'python'];

  for (const cmd of pythonCommands) {
    try {
      const result = spawn(cmd, ['--version'], { stdio: 'pipe' });
      return cmd;
    } catch (e) {
      continue;
    }
  }

  console.error('❌ Error: Python 3.9+ is required but not found');
  process.exit(1);
}

function main() {
  const pythonCmd = checkPython();
  const watchScript = path.join(packageRoot, 'watch.py');

  if (!fs.existsSync(watchScript)) {
    console.error('❌ Error: Watch script not found');
    console.error(`   Expected at: ${watchScript}`);
    process.exit(1);
  }

  const args = process.argv.slice(2);

  const watcher = spawn(pythonCmd, [watchScript, ...args], {
    stdio: 'inherit',
    cwd: packageRoot
  });

  watcher.on('error', (err) => {
    console.error('❌ Error running watch mode:', err.message);
    process.exit(1);
  });

  watcher.on('close', (code) => {
    process.exit(code || 0);
  });
}

main();
