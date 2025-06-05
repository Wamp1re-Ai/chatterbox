# 🎙️ ChatterBox TTS & VC Gradio Studio

A comprehensive web interface for ChatterBox Text-to-Speech and Voice Conversion with public URL sharing capability.

## 🌟 Features

### 🎤 Text-to-Speech
- **Zero-shot TTS**: Generate speech from any text without training
- **Voice Cloning**: Clone voices using short audio samples
- **Advanced Controls**: Emotion exaggeration, CFG weight, temperature
- **Preset Configurations**: Quick settings for different use cases
- **Sample Texts**: Built-in examples for quick testing
- **Real-time Generation**: Live audio playback and download

### 🎭 Voice Conversion
- **Voice-to-Voice**: Convert any voice to match a target voice
- **Default Voice**: Use built-in voice when no target provided
- **High Quality**: Maintains audio quality during conversion

### 🔧 System Features
- **Public URL Sharing**: Automatically generates shareable public URLs
- **Audio History**: Automatic saving and management of generated files
- **System Diagnostics**: Real-time status monitoring and troubleshooting
- **Device Detection**: Automatic GPU/CPU detection with fallbacks
- **Error Handling**: Comprehensive error messages and recovery tips

## 🚀 Quick Start

### Option 1: Easy Launcher (Recommended)
```bash
# Clone or download the files
python run_gradio_app.py --install-deps
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r gradio_requirements.txt

# Run the app
python enhanced_gradio_app.py
```

### Option 3: Direct Installation
```bash
# Install ChatterBox and Gradio
pip install chatterbox-tts gradio

# Run the app
python enhanced_gradio_app.py
```

## 📋 Requirements

### System Requirements
- **Python**: 3.8+ 
- **RAM**: 4GB+ (8GB+ recommended)
- **Storage**: 3GB+ free space for models
- **Internet**: Required for initial model download

### Recommended Hardware
- **GPU**: CUDA-compatible GPU with 4GB+ VRAM
- **CPU**: Multi-core processor for faster generation
- **Network**: Stable internet for public URL sharing

## 🎛️ Interface Guide

### Text-to-Speech Tab
1. **Text Input**: Enter or select sample text
2. **Reference Audio**: Upload audio for voice cloning (optional)
3. **Presets**: Choose from predefined configurations
4. **Manual Controls**: Fine-tune exaggeration, CFG weight, temperature
5. **Generate**: Click to create speech audio
6. **Download**: Save generated audio files

### Voice Conversion Tab
1. **Input Audio**: Upload or record source audio
2. **Target Voice**: Upload target voice sample (optional)
3. **Convert**: Process voice conversion
4. **Download**: Save converted audio

### System & History Tab
- **System Status**: View device info and model status
- **Audio History**: Access all generated files
- **Troubleshooting**: Tips and diagnostic information

## 🎯 Parameter Guide

### Exaggeration (0.0 - 2.0)
- **0.1-0.3**: Robotic, very controlled
- **0.4-0.6**: Natural, balanced speech
- **0.7-1.0**: Expressive, emotional
- **1.1+**: Dramatic, intense (may be unstable)

### CFG Weight (0.0 - 1.0)
- **0.2-0.4**: More creative, varied output
- **0.5-0.7**: Balanced control and expression
- **0.8-1.0**: Highly controlled, stable output

### Temperature (0.1 - 2.0)
- **0.5-0.7**: Stable, predictable generation
- **0.8-1.0**: Natural variation
- **1.1+**: Creative, diverse (may be inconsistent)

## 🔧 Configuration Options

### Launch Options
```bash
python run_gradio_app.py --help

Options:
  --port PORT         Port to run on (default: 7860)
  --host HOST         Host to bind to (default: 0.0.0.0)
  --no-share         Don't create public URL
  --cpu              Force CPU usage
  --install-deps     Install dependencies before running
```

### Environment Variables
```bash
# Custom configuration
export GRADIO_SERVER_PORT=8080
export GRADIO_SHARE=True
export CUDA_VISIBLE_DEVICES=0  # Use specific GPU
```

## 🌐 Public URL Sharing

The app automatically generates public URLs for easy sharing:

1. **Automatic**: Public URL created by default
2. **Shareable**: Send the URL to others for remote access
3. **Temporary**: URLs expire after 72 hours
4. **Secure**: Gradio handles secure tunneling

### Disable Public Sharing
```bash
python run_gradio_app.py --no-share
```

## 📁 File Management

### Audio History
- **Location**: `./audio_history/` directory
- **Format**: WAV files with timestamps
- **Naming**: `{type}_{timestamp}.wav`
- **Access**: Download via System tab

### Generated Files
- `tts_20240101_120000.wav` - TTS generated audio
- `vc_20240101_120000.wav` - Voice conversion audio

## 🔍 Troubleshooting

### Common Issues

**1. Model Loading Fails**
```
❌ Failed to load model: Connection error
```
**Solution**: Check internet connection and disk space

**2. CUDA Out of Memory**
```
❌ CUDA out of memory
```
**Solution**: Use `--cpu` flag or restart with smaller batch size

**3. Audio Generation Fails**
```
❌ Generation failed: Invalid input
```
**Solution**: Check text length and audio format

**4. Public URL Not Working**
```
❌ Could not create public URL
```
**Solution**: Check firewall settings and network connectivity

### Performance Tips

**Speed Optimization**:
- Use GPU when available
- Generate shorter text segments
- Lower temperature values

**Quality Optimization**:
- Use proper punctuation
- Avoid very long sentences
- Use high-quality reference audio

**Memory Management**:
- Clear audio history regularly
- Restart app if memory issues occur
- Use CPU mode for limited GPU memory

## 🎨 Customization

### Adding Custom Presets
Edit `enhanced_gradio_app.py`:
```python
def get_preset_configs():
    return {
        "Custom Preset": {
            "exaggeration": 0.7,
            "cfg_weight": 0.4,
            "temperature": 0.9
        }
    }
```

### Custom Sample Texts
Edit the `SAMPLE_TEXTS` list in `enhanced_gradio_app.py`

### UI Styling
Modify the CSS in the `create_gradio_interface()` function

## 📊 API Integration

The Gradio interface can be integrated into other applications:

```python
import gradio as gr
from enhanced_gradio_app import create_gradio_interface

# Create interface
demo = create_gradio_interface()

# Launch programmatically
demo.launch(share=False, server_port=7860)
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Test the Gradio interface thoroughly
4. Submit a pull request

## 📄 License

This Gradio interface is released under the MIT License, same as ChatterBox TTS.

## 🙏 Acknowledgments

- **Resemble AI** for ChatterBox TTS
- **Gradio Team** for the excellent web interface framework
- **PyTorch** and **Hugging Face** for the underlying infrastructure

---

**🎉 Ready to create amazing voices? Launch the app and start experimenting!**

```bash
python run_gradio_app.py
```
