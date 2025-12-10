#!/bin/bash

echo "🎬 KinaMax Bot - ULTRA PRO MAX Setup"
echo "===================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your bot token!"
else
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p temp
mkdir -p downloads

echo ""
echo "✅ Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your bot token"
echo "2. Run: python bot.py"
echo ""
echo "📚 For more info, read README.md"