#!/usr/bin/env python3
"""
ChatterBox TTS Kaggle Setup Verification Script

This script checks if your Kaggle environment is properly configured
for running ChatterBox TTS demonstrations.

Usage:
    python kaggle_setup_check.py

Author: Resemble AI
License: MIT
"""

import sys
import subprocess
import importlib
import platform
from pathlib import Path

def print_header():
    """Print a nice header for the setup check"""
    print("=" * 60)
    print("🎙️  ChatterBox TTS - Kaggle Setup Check")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("   ✅ Python version is compatible")
        return True
    else:
        print("   ❌ Python 3.8+ required")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed and importable"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"   ✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"   ❌ {package_name}: Not installed")
        return False

def check_dependencies():
    """Check all required dependencies"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        ("torch", "torch"),
        ("torchaudio", "torchaudio"), 
        ("librosa", "librosa"),
        ("numpy", "numpy"),
        ("IPython", "IPython")
    ]
    
    all_good = True
    for package, import_name in required_packages:
        if not check_package(package, import_name):
            all_good = False
    
    return all_good

def check_chatterbox():
    """Check if ChatterBox TTS is installed"""
    print("\n🤖 Checking ChatterBox TTS...")
    try:
        from chatterbox.tts import ChatterboxTTS
        print("   ✅ ChatterBox TTS: Available")
        return True
    except ImportError:
        print("   ❌ ChatterBox TTS: Not installed")
        print("   💡 Run: pip install chatterbox-tts")
        return False

def check_device_support():
    """Check available compute devices"""
    print("\n💻 Checking device support...")
    
    try:
        import torch
        
        # Check CUDA
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"   🚀 CUDA GPU: {gpu_name} ({gpu_memory:.1f}GB)")
            return "cuda"
        
        # Check MPS (Apple Silicon)
        elif torch.backends.mps.is_available():
            print("   🍎 Apple MPS: Available")
            return "mps"
        
        else:
            print("   💻 CPU only: No GPU acceleration")
            return "cpu"
            
    except ImportError:
        print("   ❌ Cannot check device support (PyTorch not available)")
        return None

def check_disk_space():
    """Check available disk space"""
    print("\n💾 Checking disk space...")
    
    try:
        import shutil
        free_space = shutil.disk_usage('.').free / 1e9
        print(f"   📊 Available space: {free_space:.1f}GB")
        
        if free_space >= 3.0:
            print("   ✅ Sufficient space for model downloads")
            return True
        else:
            print("   ⚠️  Low disk space (need ~3GB for models)")
            return False
            
    except Exception as e:
        print(f"   ❌ Cannot check disk space: {e}")
        return False

def check_internet():
    """Check internet connectivity"""
    print("\n🌐 Checking internet connectivity...")
    
    try:
        import urllib.request
        urllib.request.urlopen('https://huggingface.co', timeout=10)
        print("   ✅ Internet connection: Available")
        return True
    except Exception:
        print("   ❌ Internet connection: Not available")
        print("   💡 Enable internet in Kaggle notebook settings")
        return False

def install_missing_packages():
    """Offer to install missing packages"""
    print("\n🔧 Installing missing packages...")
    
    packages_to_install = []
    
    # Check if ChatterBox is missing
    try:
        import chatterbox
    except ImportError:
        packages_to_install.append("chatterbox-tts")
    
    # Check other packages
    try:
        import librosa
    except ImportError:
        packages_to_install.append("librosa")
    
    try:
        import IPython
    except ImportError:
        packages_to_install.append("IPython")
    
    if packages_to_install:
        print(f"   📥 Installing: {', '.join(packages_to_install)}")
        for package in packages_to_install:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", package, "--quiet"
                ])
                print(f"   ✅ Installed: {package}")
            except subprocess.CalledProcessError as e:
                print(f"   ❌ Failed to install {package}: {e}")
    else:
        print("   ✅ All packages already installed")

def print_summary(results):
    """Print a summary of the setup check"""
    print("\n" + "=" * 60)
    print("📋 SETUP SUMMARY")
    print("=" * 60)
    
    all_good = all(results.values())
    
    if all_good:
        print("🎉 Your environment is ready for ChatterBox TTS!")
        print("\n✅ All checks passed:")
    else:
        print("⚠️  Some issues found. Please address them before proceeding.")
        print("\n📊 Check results:")
    
    for check, status in results.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {check}")
    
    if not all_good:
        print("\n💡 Troubleshooting tips:")
        if not results.get("Dependencies"):
            print("   • Run the notebook's first cell to install dependencies")
        if not results.get("Internet"):
            print("   • Enable internet access in Kaggle settings")
        if not results.get("Disk Space"):
            print("   • Free up disk space or use a different environment")

def main():
    """Main setup check function"""
    print_header()
    
    # Run all checks
    results = {}
    results["Python Version"] = check_python_version()
    results["Dependencies"] = check_dependencies()
    results["ChatterBox TTS"] = check_chatterbox()
    results["Device Support"] = check_device_support() is not None
    results["Disk Space"] = check_disk_space()
    results["Internet"] = check_internet()
    
    # Offer to install missing packages
    if not results["ChatterBox TTS"] or not results["Dependencies"]:
        install_missing_packages()
    
    # Print summary
    print_summary(results)
    
    print("\n🚀 Ready to start? Open the ChatterBox TTS demo notebook!")
    print("📓 File: chatterbox_tts_kaggle_demo.ipynb")

if __name__ == "__main__":
    main()
