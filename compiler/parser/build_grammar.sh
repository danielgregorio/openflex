#!/bin/bash
# Build tree-sitter grammar for AS4

set -e

echo "🔨 Building AS4 tree-sitter grammar..."

cd "$(dirname "$0")/tree-sitter-as4"

# Check if tree-sitter CLI is installed
if ! command -v tree-sitter &> /dev/null; then
    echo "❌ tree-sitter CLI not found"
    echo "Install with: npm install -g tree-sitter-cli"
    exit 1
fi

# Generate parser
echo "📝 Generating parser from grammar..."
tree-sitter generate

# Build shared library
echo "🔧 Building shared library..."
tree-sitter build

echo "✅ Grammar built successfully!"
echo "Library: build/as4.so"
