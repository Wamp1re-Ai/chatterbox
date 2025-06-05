# 🎙️ ChatterBox TTS - Kaggle Demo

This repository contains a comprehensive Jupyter notebook demonstrating the ChatterBox TTS (Text-to-Speech) system on Kaggle.

## 📋 Overview

ChatterBox TTS is Resemble AI's state-of-the-art open-source text-to-speech model that offers:

- **Zero-shot TTS**: Generate speech from any text without training
- **Voice Cloning**: Clone voices from short audio samples  
- **Emotion Control**: Adjust speech intensity and exaggeration
- **High Quality**: Outperforms many commercial TTS systems
- **MIT Licensed**: Free for commercial use

## 🚀 Quick Start on Kaggle

1. **Upload the Notebook**: Upload `chatterbox_tts_kaggle_demo.ipynb` to Kaggle
2. **Enable Internet**: Ensure internet access is enabled for model downloads
3. **Select GPU**: Choose GPU accelerator for faster inference (optional but recommended)
4. **Run All Cells**: Execute the notebook from top to bottom

## 📁 Files Included

- `chatterbox_tts_kaggle_demo.ipynb` - Main demonstration notebook
- `KAGGLE_DEMO_README.md` - This documentation file

## 🎯 What the Notebook Covers

### 1. Environment Setup
- Automatic dependency installation
- Device detection (GPU/CPU)
- Error handling for common setup issues

### 2. Basic Text-to-Speech
- Simple text-to-speech generation
- Audio playback in Jupyter
- File saving and management

### 3. Advanced Parameter Tuning
- Emotion exaggeration control
- CFG weight adjustment
- Temperature variation
- Side-by-side comparisons

### 4. Voice Cloning
- Using audio prompts for voice cloning
- Reference audio creation
- Voice characteristic transfer

### 5. Interactive Generation
- Customizable text input
- Real-time parameter adjustment
- Performance monitoring

### 6. Troubleshooting & Optimization
- System diagnostics
- Common error solutions
- Performance tips
- Memory management

## ⚙️ System Requirements

### Minimum Requirements
- **RAM**: 4GB+ (8GB+ recommended)
- **Storage**: 3GB free space for model downloads
- **Internet**: Required for initial model download

### Recommended Setup
- **GPU**: CUDA-compatible GPU with 4GB+ VRAM
- **RAM**: 8GB+ system memory
- **Storage**: SSD for faster model loading

## 🎛️ Parameter Guide

### Exaggeration (0.0 - 1.0+)
- `0.2-0.5`: Calm, controlled speech
- `0.5-0.8`: Normal, natural speech  
- `0.8+`: Dramatic, expressive speech

### CFG Weight (0.0 - 1.0)
- `0.3-0.5`: More expressive, varied output
- `0.5-0.7`: Balanced control and expression
- `0.7+`: Highly controlled, stable output

### Temperature (0.0 - 1.0+)
- `0.6-0.8`: Stable, predictable generation
- `0.8-1.0`: Varied, natural generation
- `1.0+`: Creative, diverse generation

## 🔧 Troubleshooting

### Common Issues

**1. Model Download Fails**
- Ensure internet access is enabled in Kaggle
- Check available disk space (need ~2GB)
- Try restarting the kernel

**2. CUDA Out of Memory**
- Restart kernel and try again
- Switch to CPU: `device="cpu"`
- Generate shorter text segments

**3. Slow Generation on CPU**
- This is normal - CPU inference is slower
- Consider using GPU if available
- Generate shorter texts for faster results

**4. Audio Playback Issues**
- Check browser audio permissions
- Download .wav files to play locally
- Ensure speakers/headphones are connected

### Performance Tips

**Speed Optimization:**
- Use GPU when available (CUDA > MPS > CPU)
- Generate shorter text segments
- Lower temperature values generate faster

**Quality Optimization:**
- Use proper punctuation in text
- Avoid very long sentences (>100 words)
- Clean reference audio for voice cloning

## 📊 Expected Performance

### Generation Times (approximate)
- **GPU (T4)**: ~2-5 seconds for 10-20 words
- **CPU**: ~10-30 seconds for 10-20 words
- **Voice Cloning**: +1-2 seconds additional processing

### Memory Usage
- **Model Loading**: ~1.5GB GPU/RAM
- **Generation**: +0.5GB per concurrent generation
- **Total Recommended**: 4GB+ GPU memory or 8GB+ RAM

## 🎤 Voice Cloning Tips

1. **Reference Audio Quality**:
   - Use clean, high-quality audio (16kHz+ sample rate)
   - 3-10 seconds of speech is optimal
   - Avoid background noise
   - Single speaker works best

2. **Best Practices**:
   - Choose representative speech samples
   - Avoid music or sound effects
   - Use clear, well-articulated speech
   - Test different reference segments

## 📚 Additional Resources

- **GitHub Repository**: [https://github.com/resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox)
- **Hugging Face Demo**: [https://huggingface.co/spaces/ResembleAI/Chatterbox](https://huggingface.co/spaces/ResembleAI/Chatterbox)
- **Discord Community**: [https://discord.gg/XqS7RxUp](https://discord.gg/XqS7RxUp)
- **Resemble AI**: [https://resemble.ai](https://resemble.ai)

## 🤝 Contributing

ChatterBox TTS is open source under the MIT License. Contributions are welcome!

- Report bugs and request features on GitHub
- Share your creations with the community
- Help improve documentation and examples
- Join the Discord for discussions

## 📄 License

This demo and ChatterBox TTS are released under the MIT License. See the main repository for full license details.

## 🙏 Acknowledgments

- **Resemble AI** for developing and open-sourcing ChatterBox TTS
- **Kaggle** for providing the platform for AI experimentation
- **PyTorch** and **Hugging Face** for the underlying infrastructure

---

**Happy voice synthesis! 🎤✨**

*Made with ♥️ by [Resemble AI](https://resemble.ai)*
