# 🎙️ ChatterBox TTS - Gradio UI Notebooks

Interactive Jupyter notebooks for running ChatterBox TTS with Gradio web interface and public URL sharing.

## 📋 Available Notebooks

### 🔵 Kaggle Notebook
**File**: `chatterbox_kaggle_gradio.ipynb`
- **Platform**: Kaggle Notebooks
- **GPU**: Free T4 GPU available
- **Internet**: Required for model downloads
- **Public URL**: ✅ Automatic sharing enabled

### 🟠 Google Colab Notebook  
**File**: `chatterbox_colab_gradio.ipynb`
- **Platform**: Google Colab
- **GPU**: Free T4/K80 GPU available
- **Internet**: Always available
- **Public URL**: ✅ Automatic sharing enabled

## 🌟 Key Features

### 🌐 Public URL Sharing
Both notebooks automatically generate **public URLs** that you can share with anyone:
- **Zero configuration** - works out of the box
- **Instant sharing** - send URL to anyone worldwide
- **Cross-platform** - works on any device with a browser
- **Secure HTTPS** - encrypted connections
- **Temporary URLs** - expire after 72 hours for security

### 🎤 Gradio Web Interface
Professional web interface with:
- **Text-to-Speech** with advanced parameter controls
- **Voice Cloning** using audio prompts
- **Preset configurations** for different use cases
- **Sample texts** for quick testing
- **Real-time audio** playback and download
- **System diagnostics** and troubleshooting

### 🚀 GPU Acceleration
- **Automatic GPU detection** on both platforms
- **Fast model loading** with GPU acceleration
- **Quick speech generation** (2-5 seconds typical)
- **CPU fallback** if GPU unavailable

## 🚀 Quick Start

### Option 1: Kaggle (Recommended for beginners)

1. **Upload notebook** to Kaggle
2. **Enable internet** in notebook settings
3. **Run all cells** (Runtime → Run All)
4. **Copy public URL** from the output
5. **Share URL** with anyone for instant access

### Option 2: Google Colab (Recommended for advanced users)

1. **Open in Colab**: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wamp1re-Ai/chatterbox/blob/master/chatterbox_colab_gradio.ipynb)
2. **Enable GPU**: Runtime → Change runtime type → GPU
3. **Run all cells** (Runtime → Run all)
4. **Wait for restart** after dependency installation
5. **Copy public URL** from the final output
6. **Share URL** for collaborative testing

## 📊 What You'll See

### 🔗 URL Generation
```
🚀 Launching ChatterBox TTS Gradio Interface...
📡 Creating public URL for worldwide access...

Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://abc123def456.gradio.live

📤 Share the public URL with anyone for instant access!
```

### 🎛️ Interface Features
- **Text Input**: Enter any text or select samples
- **Voice Cloning**: Upload audio for voice cloning
- **Presets**: 6 configurations (Neutral, Dramatic, Robotic, etc.)
- **Manual Controls**: Exaggeration, CFG weight, temperature
- **Audio Output**: Play and download generated speech
- **Status Monitor**: Real-time generation feedback

## 🎯 Use Cases

### 🎓 Educational
- **Workshops**: Share URL with students instantly
- **Demonstrations**: Show TTS capabilities live
- **Learning**: Hands-on experience with AI voice synthesis

### 🤝 Professional
- **Client demos**: Professional TTS presentations
- **Team collaboration**: Remote voice project work
- **Prototyping**: Quick voice interface testing

### 🔬 Research
- **Academic collaboration**: Share with researchers worldwide
- **Parameter exploration**: Test different configurations
- **Reproducible results**: Share exact settings via URL

## 🎛️ Parameter Guide

### 🎲 Presets
- **Neutral**: Balanced, natural speech
- **Calm & Controlled**: Stable, measured delivery
- **Expressive & Dynamic**: Emotional, varied speech
- **Dramatic & Intense**: High emotion, theatrical
- **Robotic & Stable**: Mechanical, consistent
- **Creative & Varied**: Diverse, experimental

### 🎚️ Manual Controls
- **Exaggeration (0.0-2.0)**: Emotion intensity
  - 0.1-0.3: Very controlled, robotic
  - 0.4-0.6: Natural, balanced
  - 0.7-1.0: Expressive, emotional
  - 1.1+: Dramatic, intense

- **CFG Weight (0.0-1.0)**: Generation stability
  - 0.2-0.4: More creative, varied
  - 0.5-0.7: Balanced control
  - 0.8-1.0: Highly controlled, stable

- **Temperature (0.1-2.0)**: Output variation
  - 0.5-0.7: Stable, predictable
  - 0.8-1.0: Natural variation
  - 1.1+: Creative, diverse

## 🔧 Troubleshooting

### Common Issues

**1. Model Loading Fails**
```
❌ Failed to load model: Connection error
```
**Solution**: Check internet connection and disk space

**2. No Public URL Generated**
```
❌ Cannot launch interface - model not loaded
```
**Solution**: Ensure model loading cell completed successfully

**3. Slow Generation**
```
⏳ Generation taking too long...
```
**Solution**: Enable GPU in runtime settings

**4. Interface Not Responding**
```
❌ Interface crashed or frozen
```
**Solution**: Restart runtime and run all cells again

### Platform-Specific Tips

#### Kaggle
- **Enable Internet**: Required for model downloads
- **Use GPU**: Select GPU accelerator in settings
- **Keep Running**: Don't close the notebook tab
- **File Downloads**: Use Output tab to download audio

#### Google Colab
- **Runtime Restart**: Normal after dependency installation
- **GPU Selection**: Choose GPU in Runtime settings
- **Session Limits**: Free tier has usage limits
- **File Access**: Files saved in Colab's temporary storage

## 💡 Best Practices

### 🎯 For Best Results
- **Text Quality**: Use clear, well-punctuated sentences
- **Voice Cloning**: Upload 3-10 seconds of clear speech
- **Parameter Tuning**: Start with presets, then fine-tune
- **Audio Quality**: Use high-quality reference audio (16kHz+)

### 🔗 For Sharing
- **Test First**: Verify the interface works before sharing
- **Clear Instructions**: Tell users what to expect
- **Monitor Usage**: Keep the notebook running while shared
- **Security**: Don't share URLs with sensitive content publicly

### ⚡ For Performance
- **Use GPU**: Enable GPU acceleration when available
- **Shorter Text**: Generate shorter segments for faster results
- **Batch Generation**: Generate multiple samples efficiently
- **Monitor Resources**: Watch memory usage on free tiers

## 📚 Additional Resources

- **ChatterBox GitHub**: [https://github.com/resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox)
- **Gradio Documentation**: [https://gradio.app/docs](https://gradio.app/docs)
- **Kaggle Notebooks**: [https://www.kaggle.com/code](https://www.kaggle.com/code)
- **Google Colab**: [https://colab.research.google.com](https://colab.research.google.com)

## 🤝 Contributing

Found an issue or want to improve the notebooks?
1. Fork the repository
2. Make your changes
3. Test thoroughly on both platforms
4. Submit a pull request

## 📄 License

These notebooks are released under the MIT License, same as ChatterBox TTS.

---

**🎉 Ready to create amazing voices?**

Choose your platform and start generating speech with public URL sharing:
- 🔵 **Kaggle**: Upload `chatterbox_kaggle_gradio.ipynb`
- 🟠 **Colab**: Click the "Open in Colab" badge above

**🔗 Share the generated public URL** and let the world experience ChatterBox TTS!
