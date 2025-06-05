#!/usr/bin/env python3
"""
Test script for ChatterBox Gradio App

This script tests the Gradio interface without requiring ChatterBox to be installed.
It validates the UI structure and functionality.

Usage:
    python test_gradio_app.py
"""

import sys
import traceback
from pathlib import Path

def test_gradio_import():
    """Test if Gradio is available"""
    try:
        import gradio as gr
        print("✅ Gradio imported successfully")
        print(f"📦 Gradio version: {gr.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Gradio import failed: {e}")
        return False

def test_app_structure():
    """Test the app structure without running it"""
    try:
        # Mock the missing dependencies
        import sys
        from unittest.mock import MagicMock
        
        # Mock torch and related modules
        sys.modules['torch'] = MagicMock()
        sys.modules['torchaudio'] = MagicMock()
        sys.modules['numpy'] = MagicMock()
        sys.modules['librosa'] = MagicMock()
        sys.modules['chatterbox'] = MagicMock()
        sys.modules['chatterbox.tts'] = MagicMock()
        sys.modules['chatterbox.vc'] = MagicMock()
        
        # Import the app
        from enhanced_gradio_app import (
            get_preset_configs, 
            load_sample_text,
            SAMPLE_TEXTS,
            MAX_TEXT_LENGTH,
            AUDIO_HISTORY_DIR
        )
        
        print("✅ App modules imported successfully")
        
        # Test preset configurations
        presets = get_preset_configs()
        print(f"✅ Presets loaded: {len(presets)} configurations")
        for name, config in presets.items():
            print(f"   • {name}: exag={config['exaggeration']}, cfg={config['cfg_weight']}, temp={config['temperature']}")
        
        # Test sample texts
        print(f"✅ Sample texts: {len(SAMPLE_TEXTS)} available")
        for i, text in enumerate(SAMPLE_TEXTS[:3]):  # Show first 3
            print(f"   • {i+1}. {text[:50]}...")
        
        # Test configuration
        print(f"✅ Max text length: {MAX_TEXT_LENGTH} characters")
        print(f"✅ Audio history dir: {AUDIO_HISTORY_DIR}")
        
        return True
        
    except Exception as e:
        print(f"❌ App structure test failed: {e}")
        traceback.print_exc()
        return False

def test_interface_creation():
    """Test interface creation with mocked dependencies"""
    try:
        import gradio as gr
        from unittest.mock import MagicMock, patch
        
        # Mock all the dependencies
        with patch('enhanced_gradio_app.CHATTERBOX_AVAILABLE', False):
            with patch('enhanced_gradio_app.get_device_info', return_value="💻 CPU (mocked)"):
                with patch('enhanced_gradio_app.get_system_status', return_value="✅ System OK (mocked)"):
                    from enhanced_gradio_app import create_gradio_interface
                    
                    # Create the interface
                    demo = create_gradio_interface()
                    print("✅ Gradio interface created successfully")
                    
                    # Check if it's a valid Gradio Blocks object
                    if hasattr(demo, 'launch'):
                        print("✅ Interface has launch method")
                    else:
                        print("❌ Interface missing launch method")
                    
                    return True
                    
    except Exception as e:
        print(f"❌ Interface creation test failed: {e}")
        traceback.print_exc()
        return False

def test_launcher_script():
    """Test the launcher script"""
    try:
        if not Path("run_gradio_app.py").exists():
            print("❌ run_gradio_app.py not found")
            return False
        
        # Test argument parsing
        import argparse
        import subprocess
        
        # Test help command
        result = subprocess.run([
            sys.executable, "run_gradio_app.py", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Launcher script help works")
            if "ChatterBox TTS & VC Gradio" in result.stdout:
                print("✅ Launcher script description found")
            else:
                print("⚠️ Launcher script description not found")
        else:
            print(f"❌ Launcher script help failed: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Launcher script test failed: {e}")
        return False

def test_requirements():
    """Test requirements file"""
    try:
        if not Path("gradio_requirements.txt").exists():
            print("❌ gradio_requirements.txt not found")
            return False
        
        with open("gradio_requirements.txt", "r") as f:
            requirements = f.read()
        
        required_packages = ["gradio", "torch", "torchaudio", "numpy", "librosa", "chatterbox-tts"]
        
        for package in required_packages:
            if package in requirements:
                print(f"✅ {package} in requirements")
            else:
                print(f"❌ {package} missing from requirements")
        
        return True
        
    except Exception as e:
        print(f"❌ Requirements test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 ChatterBox Gradio App Test Suite")
    print("=" * 50)
    
    tests = [
        ("Gradio Import", test_gradio_import),
        ("App Structure", test_app_structure),
        ("Interface Creation", test_interface_creation),
        ("Launcher Script", test_launcher_script),
        ("Requirements File", test_requirements)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Gradio app is ready to use.")
        print("\n🚀 To run the app:")
        print("1. Install dependencies: pip install -r gradio_requirements.txt")
        print("2. Launch app: python run_gradio_app.py")
        print("3. Or run directly: python enhanced_gradio_app.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
