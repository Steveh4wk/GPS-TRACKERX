#!/usr/bin/env python3
"""
SAFE WSGI Entry Point for GPS Danger Zone Tracker
Handles missing dependencies gracefully
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Set environment variables for production
os.environ.setdefault('APP_DEBUG', 'false')
os.environ.setdefault('APP_LOG_LEVEL', 'INFO')
os.environ.setdefault('WEB_HOST', '0.0.0.0')
os.environ.setdefault('WEB_PORT', str(os.getenv('PORT', '10000')))

try:
    from web.app import create_web_app
    print("✅ Web app module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import web.app: {e}")
    # Create minimal Flask app fallback
    from flask import Flask
    def create_web_app(config=None):
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'fallback_secret_key'
        
        @app.route('/')
        def index():
            return """
            <h1>🚀 GPS Tracker</h1>
            <p>Server is running but some features may be limited.</p>
            <p><a href="/admin">Admin Panel</a></p>
            """
            
        @app.route('/admin')
        def admin():
            return "<h1>Admin Panel</h1><p>Basic admin interface</p>"
            
        @app.route('/api/status')
        def status():
            return {'status': 'running', 'mode': 'minimal'}
            
        return app

try:
    from utils.config_manager import ConfigManager
    config_manager = ConfigManager()
    config = config_manager.load_config()
    print("✅ Configuration loaded successfully")
except ImportError as e:
    print(f"⚠️ Config manager not available: {e}")
    config = {}

# Create Flask application
application = create_web_app(config)
app = application

if __name__ == "__main__":
    port = int(os.getenv('PORT', 10000))
    print(f"🚀 Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)