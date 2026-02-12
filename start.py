#!/usr/bin/env python
"""
Flable.ai - One-Click Launcher
Run this script to start everything!
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

# Colors for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    print(f"""
{Colors.BLUE}{Colors.BOLD}
  ███████╗██╗      █████╗ ██████╗ ██╗     ███████╗     █████╗ ██╗
  ██╔════╝██║     ██╔══██╗██╔══██╗██║     ██╔════╝    ██╔══██╗██║
  █████╗  ██║     ███████║██████╔╝██║     █████╗      ███████║██║
  ██╔══╝  ██║     ██╔══██║██╔══██╗██║     ██╔══╝      ██╔══██║██║
  ██║     ███████╗██║  ██║██████╔╝███████╗███████╗    ██║  ██║██║
  ╚═╝     ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝
{Colors.END}
  {Colors.GREEN}AI-Powered Marketing Platform{Colors.END}
  {Colors.YELLOW}═══════════════════════════════════════════════════════════{Colors.END}
""")

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print(f"{Colors.RED}✗ Python 3.8+ required. You have {sys.version}{Colors.END}")
        return False
    print(f"{Colors.GREEN}✓ Python {sys.version.split()[0]}{Colors.END}")
    return True

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{Colors.GREEN}✓ Node.js {result.stdout.strip()}{Colors.END}")
            return True
    except FileNotFoundError:
        pass
    print(f"{Colors.RED}✗ Node.js not found{Colors.END}")
    return False

def setup_backend():
    """Setup backend virtual environment and dependencies"""
    backend_dir = Path('backend')
    venv_dir = backend_dir / 'venv'
    
    print(f"\n{Colors.BOLD}[1/3] Setting up Backend...{Colors.END}")
    
    # Create virtual environment if it doesn't exist
    if not venv_dir.exists():
        print(f"{Colors.YELLOW}  Creating virtual environment...{Colors.END}")
        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)
        print(f"{Colors.GREEN}  ✓ Virtual environment created{Colors.END}")
    else:
        print(f"{Colors.GREEN}  ✓ Virtual environment exists{Colors.END}")
    
    # Determine pip path
    if os.name == 'nt':  # Windows
        pip_path = venv_dir / 'Scripts' / 'pip.exe'
        python_path = venv_dir / 'Scripts' / 'python.exe'
    else:  # Unix
        pip_path = venv_dir / 'bin' / 'pip'
        python_path = venv_dir / 'bin' / 'python'
    
    # Install dependencies
    requirements = backend_dir / 'requirements.txt'
    if requirements.exists():
        print(f"{Colors.YELLOW}  Installing Python dependencies...{Colors.END}")
        subprocess.run([str(pip_path), 'install', '-q', '-r', str(requirements)], check=True)
        print(f"{Colors.GREEN}  ✓ Dependencies installed{Colors.END}")
    
    # Initialize database
    print(f"{Colors.YELLOW}  Initializing database...{Colors.END}")
    os.chdir('backend')
    try:
        subprocess.run([
            str(python_path), '-c',
            'from database.connection import init_db; init_db()'
        ], check=True, capture_output=True)
        print(f"{Colors.GREEN}  ✓ Database initialized{Colors.END}")
    except:
        print(f"{Colors.YELLOW}  ⚠ Database will be created on first run{Colors.END}")
    os.chdir('..')
    
    return python_path

def setup_frontend():
    """Setup frontend dependencies"""
    frontend_dir = Path('frontend')
    node_modules = frontend_dir / 'node_modules'
    
    print(f"\n{Colors.BOLD}[2/3] Setting up Frontend...{Colors.END}")
    
    if not node_modules.exists():
        print(f"{Colors.YELLOW}  Installing Node dependencies (this may take a minute)...{Colors.END}")
        os.chdir('frontend')
        subprocess.run(['npm', 'install'], check=True, stdout=subprocess.DEVNULL)
        os.chdir('..')
        print(f"{Colors.GREEN}  ✓ Dependencies installed{Colors.END}")
    else:
        print(f"{Colors.GREEN}  ✓ Dependencies already installed{Colors.END}")

def start_services(python_path):
    """Start backend and frontend services"""
    print(f"\n{Colors.BOLD}[3/3] Starting Services...{Colors.END}")
    
    # Start backend
    print(f"{Colors.YELLOW}  Starting backend on http://localhost:8000...{Colors.END}")
    backend_process = subprocess.Popen(
        [str(python_path), '-m', 'uvicorn', 'main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'],
        cwd='backend',
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Wait for backend to start
    time.sleep(3)
    
    # Start frontend
    print(f"{Colors.YELLOW}  Starting frontend on http://localhost:3000...{Colors.END}")
    frontend_process = subprocess.Popen(
        ['npm', 'run', 'dev'],
        cwd='frontend',
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True
    )
    
    # Wait for frontend to start
    time.sleep(5)
    
    return backend_process, frontend_process

def main():
    """Main launcher function"""
    print_header()
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print(f"{Colors.BOLD}Checking prerequisites...{Colors.END}\n")
    
    # Check Python
    if not check_python_version():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Check Node.js
    if not check_node():
        print(f"\n{Colors.RED}Please install Node.js from https://nodejs.org{Colors.END}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"\n{Colors.GREEN}✓ All prerequisites met!{Colors.END}")
    
    # Setup
    try:
        python_path = setup_backend()
        setup_frontend()
    except Exception as e:
        print(f"\n{Colors.RED}✗ Setup failed: {e}{Colors.END}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Start services
    try:
        backend_proc, frontend_proc = start_services(python_path)
    except Exception as e:
        print(f"\n{Colors.RED}✗ Failed to start services: {e}{Colors.END}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Success!
    print(f"""
{Colors.GREEN}{Colors.BOLD}
═══════════════════════════════════════════════════════════
  ✓ FLABLE.AI IS NOW RUNNING!
═══════════════════════════════════════════════════════════
{Colors.END}

{Colors.BOLD}Access your platform:{Colors.END}
  🌐 Frontend:  {Colors.BLUE}http://localhost:3000{Colors.END}
  🔧 Backend:   {Colors.BLUE}http://localhost:8000{Colors.END}
  📚 API Docs:  {Colors.BLUE}http://localhost:8000/docs{Colors.END}

{Colors.BOLD}Next steps:{Colors.END}
  1. Visit http://localhost:3000
  2. Register a new account
  3. Explore the dashboard
  4. Connect Shopify (if configured)
  5. Create your first campaign!

{Colors.YELLOW}Press Ctrl+C to stop both services{Colors.END}
""")
    
    # Open browser
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:3000')
    except:
        pass
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Shutting down...{Colors.END}")
        backend_proc.terminate()
        frontend_proc.terminate()
        time.sleep(2)
        backend_proc.kill()
        frontend_proc.kill()
        print(f"{Colors.GREEN}✓ Services stopped{Colors.END}\n")

if __name__ == '__main__':
    main()
