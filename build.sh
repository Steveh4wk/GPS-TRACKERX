#!/bin/bash
set -e

echo "🔧 Custom Build Script for Render"
echo "Current Python version: $(python --version)"
echo "Current pip version: $(pip --version)"

echo "📦 Installing build essentials..."
python -m pip install --no-deps --force-reinstall pip==24.0
python -m pip install --no-deps --force-reinstall setuptools==69.5.1
python -m pip install --no-deps --force-reinstall wheel==0.43.0

echo "📦 Installing core dependencies..."
pip install flask==2.3.3
pip install gunicorn==21.2.0  
pip install python-dotenv==1.0.0

echo "📦 Installing additional dependencies (if possible)..."
pip install requests==2.31.0 || echo "⚠️ requests failed, continuing..."
pip install pyyaml==6.0.1 || echo "⚠️ pyyaml failed, continuing..."

echo "✅ Build completed!"
python -c "import flask; print('Flask version:', flask.__version__)"