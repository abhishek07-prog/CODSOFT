# Image Captioning AI

An AI-powered desktop application that generates natural language descriptions for images using the Salesforce BLIP (Bootstrapping Language-Image Pre-training) model.

## Features

- Upload images from your device
- Preview selected images
- Generate AI-powered captions
- Responsive GUI built with CustomTkinter
- GPU acceleration support (CUDA) when available
- Local image caption generation using PyTorch

## Technologies Used

- Python
- CustomTkinter
- PyTorch
- Hugging Face Transformers
- Salesforce BLIP Model
- Pillow (PIL)

## Installation

```bash
pip install -r requirements.txt

python captioner_gui.py
```

## How It Works

1. Select an image from your computer.
2. The image is processed using the BLIP processor.
3. The BLIP model analyzes visual features in the image.
4. A descriptive caption is generated and displayed in the application.

## Learning Outcomes

Through this project, I gained hands-on experience with:

- Transformer-based AI models
- Image Captioning
- Computer Vision Applications
- Hugging Face Transformers
- GUI Development using CustomTkinter
- PyTorch Integration

## Author

Abhishek