#!/usr/bin/env python3
"""
Test script per verificare il server Flask
"""
import os
import sys
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    print("🔍 Testing imports...")
    from web.app import create_web_app
    from utils.config_manager import ConfigManager
    print("✅ All imports successful")
    
    print("🔍 Loading configuration...")
    config_manager = ConfigManager()
    config = config_manager.load_config()
    print("✅ Configuration loaded")
    
    print("🔍 Creating Flask app...")
    app = create_web_app(config)
    print("✅ Flask app created")
    
    print("🔍 Testing routes...")
    with app.test_client() as client:
        # Test main route
        response = client.get('/')
        print(f"/ : {response.status_code}")
        
        # Test admin routes
        response = client.get('/admin')
        print(f"/admin : {response.status_code}")
        
        response = client.get('/admin/tracking')
        print(f"/admin/tracking : {response.status_code}")
        
        # Test API routes
        response = client.get('/api/status')
        print(f"/api/status : {response.status_code}")
        
        response = client.get('/api/admin/statistics')
        print(f"/api/admin/statistics : {response.status_code}")
    
    print("✅ All tests passed! Server is ready")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()