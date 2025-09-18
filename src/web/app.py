"""
Web Application for GPS Danger Zone Tracker

Provides a web interface for monitoring and managing the GPS tracker.
"""

import os
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from typing import Dict, Any
from datetime import datetime, timedelta
import json


def create_web_app(config: Dict[str, Any]) -> Flask:
    """Create and configure the Flask web application.
    
    Args:
        config: Application configuration dictionary
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    # Use secret key from config or environment
    secret_key = config.get('web_interface', {}).get('secret_key') or os.getenv('WEB_SECRET_KEY', 'gps_tracker_secret_key')
    app.config['SECRET_KEY'] = secret_key
    
    # Initialize SocketIO for real-time updates
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    web_config = config.get('web_interface', {})
    
    @app.route('/')
    def index():
        """Main dashboard page."""
        return render_template('index.html')
    
    @app.route('/api/status')
    def get_status():
        """Get current application status."""
        # This would be connected to the main application instance
        return jsonify({
            'status': 'running',
            'gps_connected': True,
            'zones_loaded': True,
            'alerts_enabled': True
        })
    
    @app.route('/api/location')
    def get_current_location():
        """Get current GPS location."""
        # Placeholder - would be connected to GPS tracker
        return jsonify({
            'latitude': 40.7128,
            'longitude': -74.0060,
            'accuracy': 5.0,
            'timestamp': '2024-01-01T12:00:00Z'
        })
    
    @app.route('/api/zones')
    def get_zones():
        """Get all danger zones."""
        # Placeholder - would be connected to zone manager
        return jsonify({
            'zones': [
                {
                    'id': 'zone_001',
                    'name': 'Construction Site Alpha',
                    'type': 'construction',
                    'active': True,
                    'severity': 'high'
                }
            ]
        })
    
    @app.route('/api/alerts')
    def get_alerts():
        """Get recent alerts."""
        # Placeholder - would be connected to alert system
        return jsonify({
            'alerts': [
                {
                    'timestamp': '2024-01-01T12:00:00Z',
                    'zone_name': 'Construction Site Alpha',
                    'severity': 'high',
                    'message': 'Entered danger zone'
                }
            ]
        })
    
    # ADMIN ROUTES
    @app.route('/admin')
    def admin_dashboard():
        """Admin dashboard page."""
        return render_template('admin/dashboard.html')
    
    @app.route('/admin/tracking')
    def admin_tracking():
        """Admin tracking page with detailed GPS data."""
        return render_template('admin/tracking.html')
    
    @app.route('/api/admin/tracking_data')
    def get_tracking_data():
        """Get comprehensive tracking data for admin dashboard."""
        # Sample tracking data - in real app this would come from database/tracker
        current_time = datetime.now()
        
        # Generate sample GPS tracks for last 24 hours
        tracks = []
        for i in range(100):
            time_offset = timedelta(minutes=i * 15)
            timestamp = current_time - time_offset
            
            # Sample GPS coordinates (moving pattern)
            base_lat = 40.7128 + (i * 0.001)
            base_lng = -74.0060 + (i * 0.0015)
            
            tracks.append({
                'timestamp': timestamp.isoformat(),
                'latitude': base_lat,
                'longitude': base_lng,
                'accuracy': 5.0 + (i % 10),
                'speed': 15.5 + (i % 20),
                'altitude': 10.0 + (i % 50),
                'device_id': 'GPS_001'
            })
        
        return jsonify({
            'tracks': tracks,
            'total_points': len(tracks),
            'time_range': {
                'start': tracks[-1]['timestamp'] if tracks else None,
                'end': tracks[0]['timestamp'] if tracks else None
            }
        })
    
    @app.route('/api/admin/statistics')
    def get_admin_statistics():
        """Get tracking statistics for admin dashboard."""
        return jsonify({
            'active_devices': 1,
            'total_tracks_today': 96,
            'total_distance_km': 45.2,
            'avg_speed_kmh': 18.5,
            'zones_triggered': 3,
            'alerts_today': 5,
            'system_uptime': '2 days, 14 hours',
            'last_update': datetime.now().isoformat(),
            'battery_level': 85,
            'gps_signal': 'Strong'
        })
    
    @app.route('/api/admin/recent_locations')
    def get_recent_locations():
        """Get most recent GPS locations for live tracking."""
        current_time = datetime.now()
        recent_locations = []
        
        # Last 10 locations
        for i in range(10):
            time_offset = timedelta(minutes=i * 5)
            timestamp = current_time - time_offset
            
            recent_locations.append({
                'timestamp': timestamp.isoformat(),
                'latitude': 40.7128 + (i * 0.0001),
                'longitude': -74.0060 + (i * 0.00015),
                'accuracy': 3.5,
                'speed': 12.3,
                'heading': 45 + (i * 10)
            })
        
        return jsonify({
            'locations': recent_locations,
            'device_status': 'online',
            'last_seen': recent_locations[0]['timestamp'] if recent_locations else None
        })
    
    # SocketIO events for real-time updates
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        print('Client connected')
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        print('Client disconnected')
    
    return app