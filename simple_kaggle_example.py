#!/usr/bin/env python3
"""
Simple ChatterBox TTS Example for Kaggle

A minimal example showing how to use ChatterBox TTS in Kaggle.
This script can be run independently or used as reference.

Usage:
    python simple_kaggle_example.py

Author: Resemble AI
License: MIT
"""

import sys
import subprocess
import time
from pathlib import Path

def install_chatterbox():
    """Install ChatterBox TTS if not already installed"""
    try:
        import chatterbox
        print("✅ ChatterBox TTS already installed")
        return True
    except ImportError:
        print("📥 Installing ChatterBox TTS...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "chatterbox-tts", "--quiet"
            ])
            print("✅ ChatterBox TTS installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install ChatterBox TTS: {e}")
            return False

def detect_device():
    """Detect the best available device"""
    try:
        import torch
        
        if torch.cuda.is_available():
            device = "cuda"
            gpu_name = torch.cuda.get_device_name(0)
            print(f"🚀 Using CUDA GPU: {gpu_name}")
        elif torch.backends.mps.is_available():
            device = "mps"
            print("🍎 Using Apple MPS")
        else:
            device = "cpu"
            print("💻 Using CPU (no GPU available)")
        
        return device
        
    except ImportError:
        print("❌ PyTorch not available")
        return None

def load_model(device):
    """Load the ChatterBox TTS model"""
    try:
        from chatterbox.tts import ChatterboxTTS
        
        print("📥 Loading ChatterBox TTS model...")
        print("⏳ This may take a few minutes on first run...")
        
        start_time = time.time()
        model = ChatterboxTTS.from_pretrained(device=device)
        load_time = time.time() - start_time
        
        print(f"✅ Model loaded in {load_time:.1f} seconds")
        print(f"🎵 Sample rate: {model.sr} Hz")
        
        return model
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return None

def generate_speech(model, text, filename="output.wav"):
    """Generate speech from text"""
    try:
        import torchaudio
        
        print(f"🎯 Generating speech: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        start_time = time.time()
        wav = model.generate(text)
        generation_time = time.time() - start_time
        
        # Save audio file
        torchaudio.save(filename, wav, model.sr)
        
        # Calculate stats
        audio_duration = wav.shape[-1] / model.sr
        rtf = generation_time / audio_duration
        
        print(f"✅ Generated {audio_duration:.1f}s audio in {generation_time:.1f}s")
        print(f"📊 Real-time factor: {rtf:.2f}x")
        print(f"💾 Saved to: {filename}")
        
        return wav
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return None

def demonstrate_voice_cloning(model):
    """Demonstrate voice cloning with a reference"""
    try:
        import torchaudio
        
        print("\n🎭 Voice Cloning Demonstration")
        
        # Generate reference audio
        reference_text = "Hello, this is my voice that will be cloned."
        print(f"📝 Creating reference: '{reference_text}'")
        
        reference_wav = model.generate(reference_text)
        reference_file = "reference.wav"
        torchaudio.save(reference_file, reference_wav, model.sr)
        print(f"💾 Reference saved: {reference_file}")
        
        # Clone voice with new text
        target_text = "Now I'm saying something completely different with the same voice!"
        print(f"📝 Cloning voice for: '{target_text}'")
        
        cloned_wav = model.generate(
            target_text, 
            audio_prompt_path=reference_file,
            exaggeration=0.5
        )
        
        cloned_file = "cloned.wav"
        torchaudio.save(cloned_file, cloned_wav, model.sr)
        print(f"💾 Cloned voice saved: {cloned_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice cloning failed: {e}")
        return False

def main():
    """Main demonstration function"""
    print("🎙️ ChatterBox TTS - Simple Kaggle Example")
    print("=" * 50)
    
    # Install dependencies
    if not install_chatterbox():
        print("❌ Cannot proceed without ChatterBox TTS")
        return
    
    # Detect device
    device = detect_device()
    if device is None:
        print("❌ Cannot detect compute device")
        return
    
    # Load model
    model = load_model(device)
    if model is None:
        print("❌ Cannot proceed without model")
        return
    
    print("\n🎤 Basic Text-to-Speech Examples")
    print("-" * 40)
    
    # Example texts
    examples = [
        "Welcome to ChatterBox TTS, the open source text-to-speech system!",
        "This is a demonstration of high-quality speech synthesis.",
        "ChatterBox can generate natural-sounding speech from any text."
    ]
    
    # Generate speech for each example
    for i, text in enumerate(examples, 1):
        filename = f"example_{i}.wav"
        wav = generate_speech(model, text, filename)
        if wav is not None:
            print(f"🔊 Audio saved: {filename}")
        print()
    
    # Demonstrate voice cloning
    demonstrate_voice_cloning(model)
    
    # List generated files
    print("\n📁 Generated Files:")
    wav_files = list(Path('.').glob('*.wav'))
    for file_path in wav_files:
        file_size = file_path.stat().st_size / 1024
        print(f"   📄 {file_path.name} ({file_size:.1f} KB)")
    
    print(f"\n✨ Generated {len(wav_files)} audio files!")
    print("\n💡 Tips:")
    print("   • In Kaggle, check the 'Output' tab to download files")
    print("   • Try the full demo notebook for more features")
    print("   • Experiment with different texts and parameters")
    
    print("\n🎉 Demo complete! Happy voice synthesis!")

if __name__ == "__main__":
    main()
