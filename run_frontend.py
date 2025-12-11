#!/usr/bin/env python3
"""
Simple HTTP server for the Todo App frontend.
Serves the frontend on http://localhost:8080
"""

import os
import http.server
import socketserver
import sys
from pathlib import Path

# Get the frontend directory
frontend_dir = Path(__file__).parent / "frontend"

if not frontend_dir.exists():
    print(f"Error: Frontend directory not found at {frontend_dir}")
    sys.exit(1)

# Change to frontend directory
os.chdir(frontend_dir)

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

print(f"📂 Serving frontend from: {frontend_dir}")
print(f"🚀 Starting server on http://localhost:{PORT}")
print(f"📝 Open your browser to http://localhost:{PORT}")
print(f"⛔ Press Ctrl+C to stop the server\n")

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n✋ Server stopped.")
    sys.exit(0)
except OSError as e:
    print(f"❌ Error: {e}")
    print(f"💡 Tip: Port {PORT} might be in use. Try a different port or restart your system.")
    sys.exit(1)
