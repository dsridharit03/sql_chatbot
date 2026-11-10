"""
Django NL2SQL - Development Server Launcher
Start both Django backend and React frontend with one command
"""
import subprocess
import sys
import os
import time

def main():
    """Main function to start both servers"""
    
    print("\n" + "="*60)
    print("  Django NL2SQL - Starting Development Servers")
    print("="*60 + "\n")
    
    # Get directories
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, 'backend')
    frontend_dir = os.path.join(root_dir, 'frontend')
    
    # Check if backend exists
    if not os.path.exists(backend_dir):
        print(f"❌ Error: Backend directory not found at {backend_dir}")
        sys.exit(1)
    
    # Check if frontend exists
    if not os.path.exists(frontend_dir):
        print(f"❌ Error: Frontend directory not found at {frontend_dir}")
        sys.exit(1)
    
    # Check for virtual environment - MODIFIED TO USE sqlvenv
    venv_python = os.path.join(root_dir, 'sqlvenv', 'Scripts', 'python.exe')
    if not os.path.exists(venv_python):
        print(f"❌ Error: Virtual environment not found!")
        print(f"   Expected at: {venv_python}")
        print(f"\n   Create it with: python -m venv sqlvenv")
        sys.exit(1)
    
    print("✅ Backend directory found")
    print("✅ Frontend directory found")
    print("✅ Virtual environment found (sqlvenv)")
    print()
    
    # Start Backend Server
    print("🚀 Starting Django Backend Server...")
    backend_cmd = f'cd /d "{backend_dir}" && "{venv_python}" manage.py runserver'
    
    try:
        backend_process = subprocess.Popen(
            backend_cmd,
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print("   ✓ Backend server starting in new window")
    except Exception as e:
        print(f"   ❌ Failed to start backend: {e}")
        sys.exit(1)
    
    # Wait for backend to initialize
    print("\n⏳ Waiting for backend to initialize (3 seconds)...")
    time.sleep(3)
    
    # Start Frontend Server
    print("🚀 Starting React Frontend Server...")
    frontend_cmd = f'cd /d "{frontend_dir}" && npm start'
    
    try:
        frontend_process = subprocess.Popen(
            frontend_cmd,
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        print("   ✓ Frontend server starting in new window")
    except Exception as e:
        print(f"   ❌ Failed to start frontend: {e}")
        backend_process.terminate()
        sys.exit(1)
    
    # Success message
    print("\n" + "="*60)
    print("  ✅ Both servers are running!")
    print("="*60)
    print()
    print("  Backend Server:  http://127.0.0.1:8000")
    print("  Frontend App:    http://localhost:3000")
    print()
    print("  Two new console windows have opened:")
    print("  1. Django Backend (Python)")
    print("  2. React Frontend (Node.js)")
    print()
    print("  To stop servers: Close both console windows")
    print("  Or press Ctrl+C in those windows")
    print()
    print("="*60)
    print("\n  Press Ctrl+C here to exit this launcher")
    print("  (Servers will continue running in separate windows)")
    print()
    
    try:
        # Keep this script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Launcher closed.")
        print("   Note: Servers are still running in their windows")
        print("   Close those windows to stop the servers\n")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)