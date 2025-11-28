#!/usr/bin/env node

/**
 * OpenFlex Neo - CLI Wrapper
 * Calls the Python compiler with command-line arguments
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the root directory of the package
const packageRoot = path.join(__dirname, '..');

// Check if Python is available
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
  console.error('   Please install Python from https://www.python.org/');
  process.exit(1);
}

// Main CLI entry point
function main() {
  const pythonCmd = checkPython();
  const cliScript = path.join(packageRoot, 'compiler', 'cli.py');

  // Check if CLI script exists
  if (!fs.existsSync(cliScript)) {
    console.error('❌ Error: OpenFlex compiler not found');
    console.error(`   Expected at: ${cliScript}`);
    process.exit(1);
  }

  // Get command-line arguments (skip 'node' and script name)
  const args = process.argv.slice(2);

  // Spawn Python compiler
  const compiler = spawn(pythonCmd, [cliScript, ...args], {
    stdio: 'inherit',
    cwd: packageRoot
  });

  compiler.on('error', (err) => {
    console.error('❌ Error running OpenFlex compiler:', err.message);
    process.exit(1);
  });

  compiler.on('close', (code) => {
    process.exit(code || 0);
  });
}

// Run CLI
main();
