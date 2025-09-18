#!/usr/bin/env python3
"""
MINIMAL GPS Tracker App - Only Flask + standard library
No dependencies issues, bulletproof deployment
"""

import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'gps_tracker_minimal_key')

# HTML Templates as strings to avoid file dependency issues
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPS Tracker Admin - Minimal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .card { border: none; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .stat-card { background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white; }
        .text-gps { color: #4CAF50; font-weight: bold; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <span class="navbar-brand"><i class="fas fa-satellite-dish"></i> GPS Tracker - Minimal Admin</span>
        </div>
    </nav>
    
    <div class="container mt-4">
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <h3 id="devices">1</h3>
                        <p>Active Device</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <h3 id="tracks">96</h3>
                        <p>GPS Tracks</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <h3 id="distance">45.2</h3>
                        <p>Distance (km)</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <h3 id="alerts">3</h3>
                        <p>Alerts Today</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-map-marker-alt"></i> Current GPS Position</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <strong>Latitude:</strong><br>
                                <span class="text-gps fs-4" id="lat">40.712800</span>
                            </div>
                            <div class="col-md-6">
                                <strong>Longitude:</strong><br>
                                <span class="text-gps fs-4" id="lng">-74.006000</span>
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col-md-4">
                                <strong>Speed:</strong> <span id="speed">18.5</span> km/h
                            </div>
                            <div class="col-md-4">
                                <strong>Accuracy:</strong> <span id="accuracy">5.2</span> m
                            </div>
                            <div class="col-md-4">
                                <strong>Battery:</strong> <span id="battery">85</span>%
                            </div>
                        </div>
                        <div class="mt-3">
                            <a href="#" class="btn btn-primary" id="mapLink">
                                <i class="fas fa-map"></i> View on Google Maps
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-info-circle"></i> System Status</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-2">
                            <strong>Status:</strong> 
                            <span class="badge bg-success">Online</span>
                        </div>
                        <div class="mb-2">
                            <strong>Last Update:</strong><br>
                            <small id="lastUpdate">{{ current_time }}</small>
                        </div>
                        <div class="mb-2">
                            <strong>Device:</strong> GPS Tracker v1.0
                        </div>
                        <div>
                            <strong>Mode:</strong> Minimal Deployment
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function updateData() {
            fetch('/api/minimal/gps')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('lat').textContent = data.latitude.toFixed(6);
                    document.getElementById('lng').textContent = data.longitude.toFixed(6);
                    document.getElementById('speed').textContent = data.speed.toFixed(1);
                    document.getElementById('accuracy').textContent = data.accuracy.toFixed(1);
                    document.getElementById('lastUpdate').textContent = new Date(data.timestamp).toLocaleString();
                    
                    const mapUrl = `https://maps.google.com/?q=${data.latitude},${data.longitude}`;
                    document.getElementById('mapLink').href = mapUrl;
                })
                .catch(error => console.log('Data fetch error:', error));
        }
        
        updateData();
        setInterval(updateData, 30000); // Update every 30 seconds
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    return """
    <h1>🚀 GPS Tracker - Minimal Version</h1>
    <p>Server is running successfully!</p>
    <p><a href="/admin">→ Admin Panel</a></p>
    <p><a href="/api/status">→ API Status</a></p>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; background: #f5f5f5; }
        h1 { color: #333; } a { color: #007bff; text-decoration: none; }
    </style>
    """

@app.route('/admin')
def admin():
    """Admin dashboard"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template_string(ADMIN_TEMPLATE, current_time=current_time)

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'online',
        'version': 'minimal-1.0',
        'deployment': 'render-safe',
        'timestamp': datetime.now().isoformat(),
        'features': ['gps_tracking', 'admin_panel', 'api_endpoints']
    })

@app.route('/api/minimal/gps')
def api_gps():
    """Minimal GPS data endpoint"""
    # Simulate GPS data with slight variations
    import random
    base_time = datetime.now()
    
    return jsonify({
        'latitude': 40.7128 + (random.random() - 0.5) * 0.001,
        'longitude': -74.0060 + (random.random() - 0.5) * 0.001,
        'speed': 15.0 + random.random() * 20.0,
        'accuracy': 3.0 + random.random() * 5.0,
        'battery': 80 + random.randint(0, 20),
        'timestamp': base_time.isoformat(),
        'device_id': 'minimal_tracker_001'
    })

@app.route('/health')
def health():
    """Health check for Render"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)