#!/usr/bin/env python3
"""
Enhanced ChatterBox TTS & VC Gradio Interface

A comprehensive web interface for ChatterBox TTS and Voice Conversion
with public URL exposure for easy sharing and testing.

Features:
- Text-to-Speech with advanced parameter controls
- Voice Cloning with audio prompts
- Voice Conversion
- Preset configurations for different use cases
- Real-time generation monitoring
- Public URL sharing capability
- Audio history and management
- System diagnostics and troubleshooting

Author: Resemble AI
License: MIT
"""

import os
import sys
import time
import random
import traceback
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List

import torch
import numpy as np
import gradio as gr
import torchaudio

# Import ChatterBox models
try:
    from chatterbox.tts import ChatterboxTTS
    from chatterbox.vc import ChatterboxVC
    CHATTERBOX_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ ChatterBox not available: {e}")
    CHATTERBOX_AVAILABLE = False

# Global configuration
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_TEXT_LENGTH = 500
SAMPLE_RATE = 24000
AUDIO_HISTORY_DIR = Path("audio_history")
AUDIO_HISTORY_DIR.mkdir(exist_ok=True)

# Global model states
tts_model = None
vc_model = None

def set_seed(seed: int):
    """Set random seed for reproducible generation"""
    if seed == 0:
        seed = random.randint(1, 1000000)
    
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    random.seed(seed)
    np.random.seed(seed)
    return seed

def get_device_info() -> str:
    """Get detailed device information"""
    info = []
    info.append(f"🖥️ Device: {DEVICE}")
    
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        info.append(f"🚀 GPU: {gpu_name} ({gpu_memory:.1f}GB)")
        
        allocated = torch.cuda.memory_allocated() / 1e9
        cached = torch.cuda.memory_reserved() / 1e9
        info.append(f"💾 Memory: {allocated:.2f}GB allocated, {cached:.2f}GB cached")
    else:
        info.append("💻 Using CPU (no GPU available)")
    
    return "\n".join(info)

def load_tts_model() -> Tuple[Optional[ChatterboxTTS], str]:
    """Load ChatterBox TTS model with error handling"""
    global tts_model
    
    if not CHATTERBOX_AVAILABLE:
        return None, "❌ ChatterBox not installed. Please install with: pip install chatterbox-tts"
    
    try:
        if tts_model is None:
            print("📥 Loading ChatterBox TTS model...")
            start_time = time.time()
            tts_model = ChatterboxTTS.from_pretrained(device=DEVICE)
            load_time = time.time() - start_time
            
            status = f"✅ TTS Model loaded successfully in {load_time:.1f}s\n"
            status += f"🎵 Sample rate: {tts_model.sr} Hz\n"
            status += f"🎯 Device: {tts_model.device}"
            return tts_model, status
        else:
            return tts_model, "✅ TTS Model already loaded"
            
    except Exception as e:
        error_msg = f"❌ Failed to load TTS model: {str(e)}\n\n"
        error_msg += "🔧 Troubleshooting:\n"
        error_msg += "1. Ensure internet connection for model download\n"
        error_msg += "2. Check available disk space (~2GB needed)\n"
        error_msg += "3. Try restarting if memory issues occur"
        return None, error_msg

def load_vc_model() -> Tuple[Optional[ChatterboxVC], str]:
    """Load ChatterBox VC model with error handling"""
    global vc_model
    
    if not CHATTERBOX_AVAILABLE:
        return None, "❌ ChatterBox not installed. Please install with: pip install chatterbox-tts"
    
    try:
        if vc_model is None:
            print("📥 Loading ChatterBox VC model...")
            start_time = time.time()
            vc_model = ChatterboxVC.from_pretrained(device=DEVICE)
            load_time = time.time() - start_time
            
            status = f"✅ VC Model loaded successfully in {load_time:.1f}s\n"
            status += f"🎵 Sample rate: {vc_model.sr} Hz\n"
            status += f"🎯 Device: {vc_model.device}"
            return vc_model, status
        else:
            return vc_model, "✅ VC Model already loaded"
            
    except Exception as e:
        error_msg = f"❌ Failed to load VC model: {str(e)}\n\n"
        error_msg += "🔧 Troubleshooting:\n"
        error_msg += "1. Ensure internet connection for model download\n"
        error_msg += "2. Check available disk space (~1GB needed)\n"
        error_msg += "3. Try restarting if memory issues occur"
        return None, error_msg

def save_audio_to_history(audio_data: np.ndarray, sample_rate: int, prefix: str = "generated") -> str:
    """Save generated audio to history directory"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.wav"
    filepath = AUDIO_HISTORY_DIR / filename
    
    # Convert to tensor if needed
    if isinstance(audio_data, np.ndarray):
        audio_tensor = torch.from_numpy(audio_data)
    else:
        audio_tensor = audio_data
    
    # Ensure correct shape
    if audio_tensor.dim() == 1:
        audio_tensor = audio_tensor.unsqueeze(0)
    
    torchaudio.save(str(filepath), audio_tensor, sample_rate)
    return str(filepath)

def generate_tts(
    text: str,
    reference_audio,
    exaggeration: float,
    cfg_weight: float,
    temperature: float,
    seed: int,
    preset: str
) -> Tuple[Optional[Tuple[int, np.ndarray]], str]:
    """Generate TTS audio with comprehensive error handling"""
    
    if not text or not text.strip():
        return None, "❌ Please enter some text to synthesize"
    
    if len(text) > MAX_TEXT_LENGTH:
        return None, f"❌ Text too long. Maximum {MAX_TEXT_LENGTH} characters allowed."
    
    # Load model if needed
    model, status = load_tts_model()
    if model is None:
        return None, status
    
    try:
        # Apply preset if selected
        if preset != "Custom":
            preset_configs = get_preset_configs()
            if preset in preset_configs:
                config = preset_configs[preset]
                exaggeration = config["exaggeration"]
                cfg_weight = config["cfg_weight"]
                temperature = config["temperature"]
        
        # Set seed for reproducibility
        actual_seed = set_seed(seed)
        
        # Generate audio
        start_time = time.time()
        
        generation_params = {
            "exaggeration": exaggeration,
            "cfg_weight": cfg_weight,
            "temperature": temperature
        }
        
        if reference_audio is not None:
            generation_params["audio_prompt_path"] = reference_audio
        
        wav = model.generate(text, **generation_params)
        generation_time = time.time() - start_time
        
        # Convert to numpy for Gradio
        audio_np = wav.squeeze(0).numpy()
        
        # Save to history
        history_path = save_audio_to_history(audio_np, model.sr, "tts")
        
        # Calculate stats
        duration = len(audio_np) / model.sr
        rtf = generation_time / duration
        
        status_msg = f"✅ Generated {duration:.1f}s audio in {generation_time:.1f}s\n"
        status_msg += f"📊 Real-time factor: {rtf:.2f}x\n"
        status_msg += f"🎲 Seed used: {actual_seed}\n"
        status_msg += f"💾 Saved to: {history_path}\n"
        status_msg += f"🎛️ Settings: exag={exaggeration}, cfg={cfg_weight}, temp={temperature}"
        
        return (model.sr, audio_np), status_msg
        
    except Exception as e:
        error_msg = f"❌ Generation failed: {str(e)}\n\n"
        error_msg += f"🔍 Debug info:\n{traceback.format_exc()}"
        return None, error_msg

def get_preset_configs() -> dict:
    """Get preset configurations for different use cases"""
    return {
        "Neutral": {"exaggeration": 0.5, "cfg_weight": 0.5, "temperature": 0.8},
        "Calm & Controlled": {"exaggeration": 0.2, "cfg_weight": 0.7, "temperature": 0.6},
        "Expressive & Dynamic": {"exaggeration": 0.8, "cfg_weight": 0.3, "temperature": 0.9},
        "Dramatic & Intense": {"exaggeration": 1.2, "cfg_weight": 0.2, "temperature": 1.0},
        "Robotic & Stable": {"exaggeration": 0.1, "cfg_weight": 0.8, "temperature": 0.5},
        "Creative & Varied": {"exaggeration": 0.7, "cfg_weight": 0.4, "temperature": 1.2}
    }

def apply_preset(preset: str) -> Tuple[float, float, float]:
    """Apply preset configuration"""
    if preset == "Custom":
        return 0.5, 0.5, 0.8  # Default values
    
    configs = get_preset_configs()
    if preset in configs:
        config = configs[preset]
        return config["exaggeration"], config["cfg_weight"], config["temperature"]
    
    return 0.5, 0.5, 0.8  # Fallback to default

def generate_vc(
    input_audio,
    target_voice_audio
) -> Tuple[Optional[Tuple[int, np.ndarray]], str]:
    """Generate voice conversion audio"""

    if input_audio is None:
        return None, "❌ Please provide input audio for voice conversion"

    # Load model if needed
    model, status = load_vc_model()
    if model is None:
        return None, status

    try:
        start_time = time.time()

        wav = model.generate(
            input_audio,
            target_voice_path=target_voice_audio
        )

        generation_time = time.time() - start_time

        # Convert to numpy for Gradio
        audio_np = wav.squeeze(0).numpy()

        # Save to history
        history_path = save_audio_to_history(audio_np, model.sr, "vc")

        # Calculate stats
        duration = len(audio_np) / model.sr

        status_msg = f"✅ Converted {duration:.1f}s audio in {generation_time:.1f}s\n"
        status_msg += f"💾 Saved to: {history_path}"

        return (model.sr, audio_np), status_msg

    except Exception as e:
        error_msg = f"❌ Voice conversion failed: {str(e)}\n\n"
        error_msg += f"🔍 Debug info:\n{traceback.format_exc()}"
        return None, error_msg

def get_audio_history() -> List[str]:
    """Get list of generated audio files"""
    if not AUDIO_HISTORY_DIR.exists():
        return []

    audio_files = []
    for file_path in AUDIO_HISTORY_DIR.glob("*.wav"):
        audio_files.append(str(file_path))

    return sorted(audio_files, reverse=True)  # Most recent first

def clear_audio_history() -> str:
    """Clear audio history directory"""
    try:
        for file_path in AUDIO_HISTORY_DIR.glob("*.wav"):
            file_path.unlink()
        return "✅ Audio history cleared successfully"
    except Exception as e:
        return f"❌ Failed to clear history: {str(e)}"

def get_system_status() -> str:
    """Get comprehensive system status"""
    status = []

    # Device info
    status.append("🖥️ SYSTEM INFORMATION")
    status.append("=" * 40)
    status.append(get_device_info())
    status.append("")

    # Model status
    status.append("🤖 MODEL STATUS")
    status.append("=" * 40)

    global tts_model, vc_model

    if tts_model is not None:
        status.append("✅ TTS Model: Loaded")
        status.append(f"   📊 Sample rate: {tts_model.sr} Hz")
        status.append(f"   🎯 Device: {tts_model.device}")
    else:
        status.append("❌ TTS Model: Not loaded")

    if vc_model is not None:
        status.append("✅ VC Model: Loaded")
        status.append(f"   📊 Sample rate: {vc_model.sr} Hz")
        status.append(f"   🎯 Device: {vc_model.device}")
    else:
        status.append("❌ VC Model: Not loaded")

    status.append("")

    # Audio history
    history_files = get_audio_history()
    status.append("📁 AUDIO HISTORY")
    status.append("=" * 40)
    status.append(f"📊 Total files: {len(history_files)}")

    if history_files:
        total_size = sum(Path(f).stat().st_size for f in history_files) / 1024 / 1024
        status.append(f"📦 Total size: {total_size:.1f} MB")
        status.append("📋 Recent files:")
        for file_path in history_files[:5]:  # Show last 5 files
            file_name = Path(file_path).name
            file_size = Path(file_path).stat().st_size / 1024
            status.append(f"   • {file_name} ({file_size:.1f} KB)")
    else:
        status.append("📂 No audio files generated yet")

    return "\n".join(status)

# Sample texts for quick testing
SAMPLE_TEXTS = [
    "Hello! Welcome to ChatterBox TTS, the state-of-the-art open source text-to-speech system.",
    "The quick brown fox jumps over the lazy dog. This pangram contains every letter of the alphabet.",
    "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole filled with worms and oozy smells.",
    "To be or not to be, that is the question. Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune.",
    "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness.",
    "Space: the final frontier. These are the voyages of the starship Enterprise, to boldly go where no one has gone before."
]

def load_sample_text(sample_choice: str) -> str:
    """Load a sample text for quick testing"""
    if sample_choice == "Custom":
        return ""

    try:
        index = int(sample_choice.split(".")[0]) - 1
        if 0 <= index < len(SAMPLE_TEXTS):
            return SAMPLE_TEXTS[index]
    except:
        pass

    return ""

def create_gradio_interface():
    """Create the main Gradio interface"""

    # Custom CSS for better styling
    css = """
    .gradio-container {
        max-width: 1200px !important;
    }
    .status-box {
        background-color: #f0f0f0;
        border-radius: 8px;
        padding: 10px;
        font-family: monospace;
        font-size: 12px;
    }
    .header-text {
        text-align: center;
        color: #2d5aa0;
        margin-bottom: 20px;
    }
    .tab-content {
        padding: 20px;
    }
    """

    with gr.Blocks(css=css, title="ChatterBox TTS & VC Studio") as demo:

        # Header
        gr.HTML("""
        <div class="header-text">
            <h1>🎙️ ChatterBox TTS & VC Studio</h1>
            <p>State-of-the-art Text-to-Speech and Voice Conversion powered by Resemble AI</p>
            <p><strong>Features:</strong> Zero-shot TTS • Voice Cloning • Voice Conversion • Emotion Control</p>
        </div>
        """)

        with gr.Tabs():

            # Text-to-Speech Tab
            with gr.Tab("🎤 Text-to-Speech", elem_classes="tab-content"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.Markdown("### 📝 Text Input")

                        # Sample text selector
                        sample_dropdown = gr.Dropdown(
                            choices=["Custom"] + [f"{i+1}. {text[:50]}..." for i, text in enumerate(SAMPLE_TEXTS)],
                            value="Custom",
                            label="Quick Sample Texts - Select a sample or choose 'Custom' to write your own"
                        )

                        # Text input
                        text_input = gr.Textbox(
                            value="Hello! Welcome to ChatterBox TTS, the state-of-the-art open source text-to-speech system.",
                            label=f"Text to Synthesize (Maximum {MAX_TEXT_LENGTH} characters)",
                            placeholder="Enter your text here...",
                            lines=4,
                            max_lines=8
                        )

                        # Reference audio for voice cloning
                        reference_audio = gr.Audio(
                            sources=["upload", "microphone"],
                            type="filepath",
                            label="Reference Audio (Optional) - Upload or record audio to clone the voice"
                        )

                        gr.Markdown("### 🎛️ Generation Settings")

                        # Preset selector
                        preset_dropdown = gr.Dropdown(
                            choices=["Custom"] + list(get_preset_configs().keys()),
                            value="Neutral",
                            label="Preset Configurations - Choose a preset or select 'Custom' for manual control"
                        )

                        with gr.Row():
                            exaggeration_slider = gr.Slider(
                                0.0, 2.0, step=0.1, value=0.5,
                                label="Exaggeration - Emotion intensity (0.5 = neutral, higher = more expressive)"
                            )
                            cfg_weight_slider = gr.Slider(
                                0.0, 1.0, step=0.05, value=0.5,
                                label="CFG Weight - Generation control (higher = more stable)"
                            )

                        with gr.Row():
                            temperature_slider = gr.Slider(
                                0.1, 2.0, step=0.1, value=0.8,
                                label="Temperature - Variation control (higher = more diverse)"
                            )
                            seed_input = gr.Number(
                                value=0,
                                label="Seed - Random seed (0 = random)"
                            )

                        # Generate button
                        tts_generate_btn = gr.Button(
                            "🎵 Generate Speech",
                            variant="primary",
                            size="lg"
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("### 🔊 Generated Audio")

                        # Audio output
                        tts_audio_output = gr.Audio(
                            label="Generated Speech",
                            show_download_button=True
                        )

                        # Status display
                        tts_status = gr.Textbox(
                            label="Generation Status",
                            lines=8,
                            max_lines=12,
                            elem_classes="status-box",
                            interactive=False
                        )

                        # Quick actions
                        gr.Markdown("### ⚡ Quick Actions")
                        with gr.Row():
                            load_tts_btn = gr.Button("📥 Load TTS Model", size="sm")
                            clear_tts_btn = gr.Button("🗑️ Clear", size="sm")

            # Voice Conversion Tab
            with gr.Tab("🎭 Voice Conversion", elem_classes="tab-content"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.Markdown("### 🎵 Audio Input")

                        # Input audio
                        vc_input_audio = gr.Audio(
                            sources=["upload", "microphone"],
                            type="filepath",
                            label="Input Audio - Upload or record the audio you want to convert"
                        )

                        # Target voice audio
                        vc_target_audio = gr.Audio(
                            sources=["upload", "microphone"],
                            type="filepath",
                            label="Target Voice Audio (Optional) - Upload target voice or leave empty for default"
                        )

                        # Generate button
                        vc_generate_btn = gr.Button(
                            "🎭 Convert Voice",
                            variant="primary",
                            size="lg"
                        )

                    with gr.Column(scale=1):
                        gr.Markdown("### 🔊 Converted Audio")

                        # Audio output
                        vc_audio_output = gr.Audio(
                            label="Converted Audio",
                            show_download_button=True
                        )

                        # Status display
                        vc_status = gr.Textbox(
                            label="Conversion Status",
                            lines=8,
                            max_lines=12,
                            elem_classes="status-box",
                            interactive=False
                        )

                        # Quick actions
                        gr.Markdown("### ⚡ Quick Actions")
                        with gr.Row():
                            load_vc_btn = gr.Button("📥 Load VC Model", size="sm")
                            clear_vc_btn = gr.Button("🗑️ Clear", size="sm")

            # System & History Tab
            with gr.Tab("🔧 System & History", elem_classes="tab-content"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📊 System Status")

                        system_status = gr.Textbox(
                            label="System Information",
                            lines=20,
                            max_lines=25,
                            elem_classes="status-box",
                            interactive=False
                        )

                        with gr.Row():
                            refresh_status_btn = gr.Button("🔄 Refresh Status", size="sm")
                            clear_history_btn = gr.Button("🗑️ Clear History", size="sm")

                    with gr.Column():
                        gr.Markdown("### 📁 Audio History")

                        history_files = gr.File(
                            file_count="multiple",
                            label="Generated Audio Files",
                            interactive=False
                        )

                        gr.Markdown("### 💡 Tips & Troubleshooting")
                        gr.Markdown("""
                        **🎯 For best results:**
                        - Use clear, well-punctuated text
                        - Keep sentences under 100 words
                        - Use high-quality reference audio (16kHz+)
                        - Reference audio should be 3-10 seconds long

                        **🔧 If you encounter issues:**
                        - Restart the interface if models fail to load
                        - Check internet connection for model downloads
                        - Ensure sufficient disk space (~3GB)
                        - Try CPU mode if GPU memory is insufficient

                        **📊 Parameter Guide:**
                        - **Exaggeration**: 0.2-0.5 (calm), 0.5-0.8 (normal), 0.8+ (dramatic)
                        - **CFG Weight**: 0.3-0.5 (expressive), 0.5-0.7 (balanced), 0.7+ (controlled)
                        - **Temperature**: 0.6-0.8 (stable), 0.8-1.0 (varied), 1.0+ (creative)
                        """)

        # Event handlers

        # TTS Events
        sample_dropdown.change(
            fn=load_sample_text,
            inputs=[sample_dropdown],
            outputs=[text_input]
        )

        preset_dropdown.change(
            fn=apply_preset,
            inputs=[preset_dropdown],
            outputs=[exaggeration_slider, cfg_weight_slider, temperature_slider]
        )

        tts_generate_btn.click(
            fn=generate_tts,
            inputs=[
                text_input,
                reference_audio,
                exaggeration_slider,
                cfg_weight_slider,
                temperature_slider,
                seed_input,
                preset_dropdown
            ],
            outputs=[tts_audio_output, tts_status]
        )

        load_tts_btn.click(
            fn=load_tts_model,
            inputs=[],
            outputs=[gr.State(), tts_status]
        )

        clear_tts_btn.click(
            fn=lambda: (None, ""),
            inputs=[],
            outputs=[tts_audio_output, tts_status]
        )

        # VC Events
        vc_generate_btn.click(
            fn=generate_vc,
            inputs=[vc_input_audio, vc_target_audio],
            outputs=[vc_audio_output, vc_status]
        )

        load_vc_btn.click(
            fn=load_vc_model,
            inputs=[],
            outputs=[gr.State(), vc_status]
        )

        clear_vc_btn.click(
            fn=lambda: (None, ""),
            inputs=[],
            outputs=[vc_audio_output, vc_status]
        )

        # System Events
        refresh_status_btn.click(
            fn=get_system_status,
            inputs=[],
            outputs=[system_status]
        )

        clear_history_btn.click(
            fn=clear_audio_history,
            inputs=[],
            outputs=[system_status]
        )

        # Load initial system status
        demo.load(
            fn=get_system_status,
            inputs=[],
            outputs=[system_status]
        )

    return demo

def main():
    """Main function to launch the Gradio interface"""
    print("🎙️ ChatterBox TTS & VC Studio")
    print("=" * 50)
    print(f"🖥️ Device: {DEVICE}")
    print(f"📦 ChatterBox Available: {CHATTERBOX_AVAILABLE}")
    print(f"📁 Audio History: {AUDIO_HISTORY_DIR}")
    print()

    # Create interface
    demo = create_gradio_interface()

    # Launch configuration
    launch_kwargs = {
        "server_name": "0.0.0.0",  # Allow external access
        "server_port": 7860,
        "share": True,  # Create public URL
        "show_error": True,
        "quiet": False,
        "show_tips": True,
        "enable_queue": True,
        "max_threads": 4
    }

    print("🚀 Launching Gradio interface...")
    print("📡 Public URL will be generated for easy sharing")
    print("🔗 Local URL: http://localhost:7860")
    print()

    try:
        demo.queue(
            max_size=50,
            default_concurrency_limit=2
        ).launch(**launch_kwargs)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error launching interface: {e}")
        print("🔧 Try running with different port or settings")

if __name__ == "__main__":
    main()
