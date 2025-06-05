#!/usr/bin/env python3
"""
ChatterBox TTS Public URL Demo

This script demonstrates how to launch the ChatterBox Gradio interface
with public URL sharing for easy remote access and collaboration.

Features demonstrated:
- Automatic public URL generation
- Easy sharing capabilities
- Remote access from any device
- Collaborative testing environment

Usage:
    python demo_public_url.py

Author: Resemble AI
License: MIT
"""

import sys
import time
import subprocess
from pathlib import Path

def print_banner():
    """Print a nice banner for the demo"""
    print("=" * 60)
    print("🎙️  ChatterBox TTS - Public URL Demo")
    print("=" * 60)
    print()
    print("This demo shows how to launch ChatterBox TTS with public URL")
    print("sharing for easy remote access and collaboration.")
    print()

def check_requirements():
    """Check if the required files exist"""
    required_files = [
        "enhanced_gradio_app.py",
        "run_gradio_app.py", 
        "gradio_requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   • {file_path}")
        print()
        print("💡 Please ensure you have all the Gradio app files.")
        return False
    
    print("✅ All required files found")
    return True

def demonstrate_public_url():
    """Demonstrate the public URL feature"""
    print("🌐 Public URL Sharing Demo")
    print("-" * 40)
    print()
    
    print("🎯 What happens when you launch with public URL:")
    print()
    print("1. 🚀 Gradio starts the local server")
    print("2. 📡 Creates a secure tunnel to Gradio's servers")
    print("3. 🔗 Generates a public URL (e.g., https://abc123.gradio.live)")
    print("4. 🌍 URL is accessible from anywhere in the world")
    print("5. 📱 Works on any device with a web browser")
    print()
    
    print("🔗 Example URLs you might see:")
    print("   Local:  http://localhost:7860")
    print("   Public: https://1a2b3c4d5e6f7g8h.gradio.live")
    print()
    
    print("📊 Benefits:")
    print("   ✅ No port forwarding needed")
    print("   ✅ No firewall configuration required")
    print("   ✅ Instant sharing with colleagues")
    print("   ✅ Cross-platform compatibility")
    print("   ✅ Secure HTTPS connection")
    print()

def show_launch_options():
    """Show different ways to launch with public URLs"""
    print("🚀 Launch Options")
    print("-" * 40)
    print()
    
    print("📋 Option 1: Default (with public URL)")
    print("   python run_gradio_app.py")
    print("   → Creates public URL automatically")
    print()
    
    print("📋 Option 2: Direct app launch")
    print("   python enhanced_gradio_app.py")
    print("   → Also creates public URL by default")
    print()
    
    print("📋 Option 3: Custom port with public URL")
    print("   python run_gradio_app.py --port 8080")
    print("   → Uses port 8080 + public URL")
    print()
    
    print("📋 Option 4: Local only (no public URL)")
    print("   python run_gradio_app.py --no-share")
    print("   → Local access only")
    print()
    
    print("📋 Option 5: Install dependencies first")
    print("   python run_gradio_app.py --install-deps")
    print("   → Installs packages then launches with public URL")
    print()

def show_sharing_workflow():
    """Show how to share the public URL"""
    print("📤 Sharing Workflow")
    print("-" * 40)
    print()
    
    print("🔄 Step-by-step sharing process:")
    print()
    print("1. 🚀 Launch the app:")
    print("   python run_gradio_app.py")
    print()
    print("2. 📋 Copy the public URL from the output:")
    print("   🔗 Public URL: https://abc123.gradio.live")
    print()
    print("3. 📤 Share the URL via:")
    print("   • 📧 Email")
    print("   • 💬 Chat/Slack")
    print("   • 📱 Text message")
    print("   • 🐦 Social media")
    print()
    print("4. 👥 Others can access immediately:")
    print("   • No installation required")
    print("   • Works on any device")
    print("   • Full functionality available")
    print()

def show_use_cases():
    """Show practical use cases for public URLs"""
    print("🎯 Use Cases for Public URLs")
    print("-" * 40)
    print()
    
    use_cases = [
        {
            "title": "🎓 Educational Workshops",
            "description": "Share with students for hands-on TTS learning",
            "benefits": ["No setup time", "Universal access", "Interactive demos"]
        },
        {
            "title": "🤝 Client Demonstrations", 
            "description": "Show ChatterBox capabilities to potential clients",
            "benefits": ["Professional presentation", "Real-time interaction", "Easy access"]
        },
        {
            "title": "👥 Team Collaboration",
            "description": "Work together on voice projects remotely",
            "benefits": ["Shared workspace", "Real-time testing", "Cross-platform"]
        },
        {
            "title": "🔬 Research & Development",
            "description": "Share with researchers for academic collaboration",
            "benefits": ["Easy reproduction", "Parameter sharing", "Result comparison"]
        },
        {
            "title": "🐛 Bug Reporting",
            "description": "Let users reproduce issues easily",
            "benefits": ["Exact reproduction", "Shared parameters", "Quick debugging"]
        }
    ]
    
    for i, use_case in enumerate(use_cases, 1):
        print(f"{i}. {use_case['title']}")
        print(f"   {use_case['description']}")
        print("   Benefits:")
        for benefit in use_case['benefits']:
            print(f"   • {benefit}")
        print()

def show_security_info():
    """Show security and privacy information"""
    print("🔒 Security & Privacy")
    print("-" * 40)
    print()
    
    print("🛡️ Security Features:")
    print("   ✅ HTTPS encryption automatically enabled")
    print("   ✅ Temporary URLs (expire after 72 hours)")
    print("   ✅ No permanent data storage on Gradio servers")
    print("   ✅ Audio files processed locally only")
    print()
    
    print("🔐 Privacy Considerations:")
    print("   • Generated audio stays on your machine")
    print("   • Only the interface is tunneled, not your data")
    print("   • URLs are randomly generated and hard to guess")
    print("   • You can disable public sharing anytime")
    print()
    
    print("⚠️ Best Practices:")
    print("   • Don't share URLs with sensitive content publicly")
    print("   • Use --no-share for confidential work")
    print("   • URLs expire automatically for security")
    print("   • Monitor who has access to your URLs")
    print()

def main():
    """Main demo function"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        return
    
    print()
    
    # Show different sections
    demonstrate_public_url()
    print()
    
    show_launch_options()
    print()
    
    show_sharing_workflow()
    print()
    
    show_use_cases()
    print()
    
    show_security_info()
    print()
    
    # Final instructions
    print("🎉 Ready to Try?")
    print("=" * 60)
    print()
    print("🚀 Launch ChatterBox TTS with public URL:")
    print("   python run_gradio_app.py")
    print()
    print("📋 Or install dependencies first:")
    print("   python run_gradio_app.py --install-deps")
    print()
    print("🔗 The public URL will be displayed in the output.")
    print("📤 Share it with anyone for instant access!")
    print()
    print("💡 Tip: Keep this terminal open while others use the URL.")
    print()

if __name__ == "__main__":
    main()
