#!/usr/bin/env python3
"""
RSS Architect Launcher
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import requests
        import bs4
        import feedgenerator
        import validators
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    print("🚀 Starting RSS Architect...")
    
    if not check_requirements():
        sys.exit(1)
    
    # Run Streamlit app with browser auto-open disabled to avoid distutils error
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ]
        print("📱 Open your browser to: http://localhost:8501")
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 RSS Architect stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()