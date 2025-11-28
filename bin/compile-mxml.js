#!/usr/bin/env node

/**
 * OpenFlex Neo - MXML Compiler CLI
 * Compile MXML to Web Components
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
  const mxmlScript = path.join(packageRoot, 'compile-mxml.py');

  if (!fs.existsSync(mxmlScript)) {
    console.error('❌ Error: MXML compiler not found');
    console.error(`   Expected at: ${mxmlScript}`);
    process.exit(1);
  }

  const args = process.argv.slice(2);

  const compiler = spawn(pythonCmd, [mxmlScript, ...args], {
    stdio: 'inherit',
    cwd: packageRoot
  });

  compiler.on('error', (err) => {
    console.error('❌ Error running MXML compiler:', err.message);
    process.exit(1);
  });

  compiler.on('close', (code) => {
    process.exit(code || 0);
  });
}

main();
