#!/bin/bash
# Pre-install script for Render
echo "🔧 Fixing setuptools for Render build..."

# Upgrade pip first
python -m pip install --upgrade pip

# Force install latest setuptools and wheel
pip install --upgrade setuptools>=68.0.0 wheel>=0.40.0

# Install requirements
pip install -r requirements.txt

echo "✅ Dependencies installed successfully!"