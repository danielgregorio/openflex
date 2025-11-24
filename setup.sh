#!/bin/bash
# OpenFlex Setup Script

set -e

echo "🚀 Setting up OpenFlex..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

required_version="3.11"
if [[ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]]; then
    echo "❌ Error: Python 3.11+ required"
    exit 1
fi
echo "✓ Python version OK"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -e ".[dev]"
echo "✓ Dependencies installed"
echo ""

# Verify installation
echo "🧪 Verifying installation..."
if command -v openflex &> /dev/null; then
    echo "✓ OpenFlex CLI installed successfully"
    openflex version
else
    echo "❌ Installation verification failed"
    exit 1
fi
echo ""

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Try the examples:"
echo "     openflex build examples/hello-world/App.mxml"
echo ""
echo "  3. Read the docs:"
echo "     cat README.md"
echo ""
echo "Happy coding! 🎉"
