#!/usr/bin/env python3
"""
ChatterBox TTS & VC Gradio App Launcher

This script provides an easy way to launch the ChatterBox Gradio interface
with automatic dependency checking and installation.

Usage:
    python run_gradio_app.py [options]

Options:
    --port PORT         Port to run on (default: 7860)
    --host HOST         Host to bind to (default: 0.0.0.0)
    --no-share         Don't create public URL
    --cpu              Force CPU usage
    --install-deps     Install dependencies before running
    --help             Show this help message

Author: Resemble AI
License: MIT
"""

import sys
import subprocess
import argparse
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        "gradio",
        "torch",
        "torchaudio",
        "numpy",
        "librosa"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Install from requirements file if it exists
        if Path("gradio_requirements.txt").exists():
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "-r", "gradio_requirements.txt"
            ])
        else:
            # Install core packages
            packages = [
                "gradio>=4.0.0",
                "torch>=2.0.0", 
                "torchaudio>=2.0.0",
                "numpy>=1.21.0",
                "librosa>=0.9.0",
                "chatterbox-tts"
            ]
            
            for package in packages:
                print(f"Installing {package}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package
                ])
        
        print("✅ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_chatterbox():
    """Check if ChatterBox is properly installed"""
    try:
        from chatterbox.tts import ChatterboxTTS
        from chatterbox.vc import ChatterboxVC
        print("✅ ChatterBox TTS & VC available")
        return True
    except ImportError as e:
        print(f"❌ ChatterBox not available: {e}")
        print("💡 Try installing with: pip install chatterbox-tts")
        return False

def get_device_info():
    """Get device information"""
    try:
        import torch
        
        if torch.cuda.is_available():
            device = "cuda"
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"🚀 CUDA GPU: {gpu_name} ({gpu_memory:.1f}GB)")
        elif torch.backends.mps.is_available():
            device = "mps"
            print("🍎 Apple MPS available")
        else:
            device = "cpu"
            print("💻 Using CPU (no GPU acceleration)")
        
        return device
        
    except ImportError:
        print("❌ PyTorch not available")
        return "cpu"

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="Launch ChatterBox TTS & VC Gradio Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_gradio_app.py                    # Launch with defaults
    python run_gradio_app.py --port 8080        # Use custom port
    python run_gradio_app.py --no-share         # No public URL
    python run_gradio_app.py --install-deps     # Install deps first
    python run_gradio_app.py --cpu              # Force CPU usage
        """
    )
    
    parser.add_argument("--port", type=int, default=7860,
                       help="Port to run on (default: 7860)")
    parser.add_argument("--host", default="0.0.0.0",
                       help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--no-share", action="store_true",
                       help="Don't create public URL")
    parser.add_argument("--cpu", action="store_true",
                       help="Force CPU usage")
    parser.add_argument("--install-deps", action="store_true",
                       help="Install dependencies before running")
    
    args = parser.parse_args()
    
    print("🎙️ ChatterBox TTS & VC Gradio Launcher")
    print("=" * 50)
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_dependencies():
            sys.exit(1)
    
    # Check dependencies
    print("\n📋 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("💡 Run with --install-deps to install automatically")
        print("💡 Or install manually: pip install -r gradio_requirements.txt")
        sys.exit(1)
    
    # Check ChatterBox
    print("\n🤖 Checking ChatterBox...")
    if not check_chatterbox():
        print("💡 Install ChatterBox: pip install chatterbox-tts")
        sys.exit(1)
    
    # Device info
    print("\n🖥️ Device information...")
    device = get_device_info()
    
    if args.cpu:
        print("🔧 Forcing CPU usage as requested")
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    
    # Launch the app
    print(f"\n🚀 Launching Gradio interface...")
    print(f"🌐 Host: {args.host}")
    print(f"🔌 Port: {args.port}")
    print(f"📡 Public URL: {'Yes' if not args.no_share else 'No'}")
    print(f"🎯 Device: {device}")
    print()
    
    try:
        # Import and run the enhanced app
        if not Path("enhanced_gradio_app.py").exists():
            print("❌ enhanced_gradio_app.py not found!")
            print("💡 Make sure you're running from the correct directory")
            sys.exit(1)
        
        # Set environment variables for the app
        os.environ["GRADIO_SERVER_NAME"] = args.host
        os.environ["GRADIO_SERVER_PORT"] = str(args.port)
        if args.no_share:
            os.environ["GRADIO_SHARE"] = "False"
        else:
            os.environ["GRADIO_SHARE"] = "True"
        
        # Import and run
        from enhanced_gradio_app import main as run_app
        run_app()
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"\n❌ Error launching app: {e}")
        print("🔧 Check the error message above for troubleshooting")
        sys.exit(1)

if __name__ == "__main__":
    main()
