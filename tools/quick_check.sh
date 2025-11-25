#!/bin/bash
# Quick Integrity Check for OpenFlex Neo
# Fast sanity check before committing changes

set -e

echo "⚡ Running quick integrity check..."
echo ""

cd "$(dirname "$0")/.."

# Quick smoke tests
echo "1️⃣  Checking Python syntax..."
python -m py_compile compiler/parser/as4_parser.py
python -m py_compile compiler/analyzer/type_checker.py
python -m py_compile compiler/parser/mxml_parser.py
echo "   ✅ Python syntax OK"
echo ""

echo "2️⃣  Running core parser tests..."
python -m pytest tests/parser/test_as4_parser.py -q --tb=no
echo "   ✅ Parser tests OK"
echo ""

echo "3️⃣  Running type checker tests..."
python -m pytest tests/analyzer/test_type_checker.py -q --tb=no
echo "   ✅ Type checker tests OK"
echo ""

echo "✅ Quick check passed! Safe to commit."
