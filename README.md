# VisionReasoner

VisionReasoner is an AI assistant for **scene analysis and visual reasoning**. It combines object detection, scene understanding, and a local Large Language Model (LLM) to answer natural language questions about uploaded images.

Instead of generating responses directly from raw images, the system first extracts structured visual information using a computer vision pipeline, then performs reasoning over that information to produce accurate and explainable answers.

## Features

* Upload an image through a Streamlit web interface.
* Detect objects using YOLOv8.
* Perform scene analysis using custom reasoning modules.
* Ask questions in natural language about the uploaded image.
* Generate contextual answers using a local Llama 3 model via Ollama.
* Runs locally without requiring cloud APIs.

---

## System Architecture

```text
User Image
     │
     ▼
YOLOv8 Object Detection
     │
     ▼
Scene Analysis Module
     │
     ▼
Prompt Generation
     │
     ▼
Llama 3 (Ollama)
     │
     ▼
Natural Language Answer
```

---

## Technologies

* Python
* Streamlit
* YOLOv8 (Ultralytics)
* Ollama
* Llama 3
* PyTorch

---

## Project Structure

```text
VisionReasoner/
│
├── app.py
├── OBJECT_DETECTION.py
├── scene_analyzer.py
├── LLM.py
├── yolov8n.pt
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/VisionReasoner.git
cd VisionReasoner
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Install Ollama:

https://ollama.com/

Download the Llama model:

```bash
ollama pull llama3.2:3b
```

Run the application:

```bash
streamlit run app.py
```

---

## Example Questions

* Is this environment safe?
* Describe the scene.
* How many vehicles are visible?
* Could this place be suitable for studying?
* Is the road busy?
* Are there objects close to each other?
* What type of environment is this?

---

## Current Capabilities

The scene analysis module currently performs:

* Object counting
* Scene estimation
* Indoor/Outdoor estimation
* Vehicle density estimation
* Object position analysis
* Spatial relationship detection

The language model answers questions only using the extracted visual information avoiding unsupported assumptions whenever possible.


## Future Improvements

* Image captioning module
* Object attribute extraction
* Better spatial reasoning
* Scene graph generation
* Multi-image support
* Stronger Visual Language Models

---

## License

This project is intended for educational and research purposes.
