# AI Projects Repository

A collection of diverse AI and computer vision projects showcasing various applications of machine learning, computer vision, and web development technologies.

## 📁 Project Structure

### 🤖 Context-Based Chatbot
**Location**: `Context-Based_Chatbot/`

A sophisticated chatbot application that allows users to chat with AI personas of famous historical figures.

**Features**:
- Multiple AI personas (Isaac Newton, Marie Curie, William Shakespeare, Adam Smith, Alan Turing)
- Session-based conversations with context retention
- FastAPI backend with modern web interface
- Google Gemini AI integration

**Technologies**:
- FastAPI
- Google Generative AI (Gemini)
- HTML/CSS/JavaScript frontend
- Python-dotenv for configuration

**Files**:
- `main.py` - FastAPI backend server
- `static/` - Frontend files (HTML, CSS, JS)
- `requirements.txt` - Python dependencies

### 😂 Joke Generator
**Location**: `Joke_Generator/`

A web application that generates custom jokes on any topic using AI.

**Features**:
- Topic-based joke generation
- Random joke generation
- Simple and intuitive web interface
- Google Gemini AI integration

**Technologies**:
- Flask web framework
- Google Generative AI API
- HTML templates

**Files**:
- `app.py` - Flask application server
- `templates/` - HTML templates
- `test.py` - Testing utilities

### 🏃‍♂️ Multiple People Jump Counter
**Location**: `multiplePeopleJumpCount/`

An advanced computer vision project that tracks multiple people in a video and counts their jumps using AI object detection and pose estimation.

**Features**:
- Multi-person tracking and identification
- Real-time jump detection and counting
- YOLOv8 object detection
- MediaPipe pose estimation
- ByteTrack for robust person tracking

**Technologies**:
- YOLOv8 (Ultralytics)
- MediaPipe
- OpenCV
- ByteTrack
- Computer Vision

**Files**:
- `main.py` - Main jump counting application
- `jump_counter.py` - Alternative implementation
- `video.mp4` - Sample video for testing
- `ByteTrack/` - ByteTrack tracking library
- `yolov8n.pt` - Pre-trained YOLO model

### 🧩 Sudoku Game & Solver
**Location**: `sudoku/`

A comprehensive Sudoku application featuring multiple grid sizes, difficulty levels, and both game interface and API endpoints.

**Features**:
- Multiple grid sizes (4x4, 9x9, 16x16)
- Three difficulty levels (Easy, Medium, Hard)
- Automatic puzzle generation and solving
- FastAPI endpoints for integration
- Pygame-based game interface
- Web deployment support

**Technologies**:
- FastAPI
- Pygame
- Python algorithms
- WebAssembly (pygbag) for web deployment

**Files**:
- `main.py` - FastAPI server with puzzle generation
- `sudoku.py` - Core Sudoku logic and Pygame interface
- `logic.py` - Sudoku solving algorithms
- `returns_json.py` - JSON API utilities
- `requirements.txt` - Dependencies including pygbag for web deployment

## 🛠 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Global Dependencies
Install the main project dependencies:
```bash
pip install -r requirements.txt
```

### Project-Specific Setup

#### Context-Based Chatbot
```bash
cd Context-Based_Chatbot
pip install -r requirements.txt
# Create .env file with your Google API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env
uvicorn main:app --reload
```

#### Joke Generator
```bash
cd Joke_Generator
# Update API key in app.py (consider using environment variables)
python app.py
```

#### Multiple People Jump Counter
```bash
cd multiplePeopleJumpCount
pip install ultralytics opencv-python mediapipe
# Ensure yolov8n.pt model is present
python main.py
```

#### Sudoku
```bash
cd sudoku
pip install -r requirements.txt
# For web version
python -m pygbag sudoku.py
# For API server
python main.py
```

## 🚀 Usage

### Context-Based Chatbot
1. Start the FastAPI server
2. Navigate to `http://localhost:8000`
3. Select a persona and start chatting

### Joke Generator
1. Run the Flask application
2. Open your browser to the provided URL
3. Enter a topic or request a random joke

### Sudoku
- **Game Mode**: Run `sudoku.py` for the Pygame interface
- **API Mode**: Run `main.py` for RESTful endpoints
- **Web Mode**: Use pygbag to deploy to web browsers

## 🔧 Configuration

### API Keys
Several projects require API keys:
- **Context-Based Chatbot**: Google Gemini API key in `.env` file
- **Joke Generator**: Google Gemini API key (update in source code or use environment variables)

## 📋 Requirements

### Core Dependencies
- Flask
- FastAPI
- Google Generative AI
- Pygame

### Development Tools
- uvicorn (ASGI server)
- python-dotenv (environment management)
- pygbag (web deployment)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🆘 Troubleshooting

### Common Issues
1. **Missing API Keys**: Ensure all required API keys are properly configured
2. **Dependencies**: Install project-specific requirements for each subproject

### Support
For issues or questions, please check the documentation of individual projects or create an issue in the repository.

---

**Note**: This repository contains educational and demonstration projects. Some API keys and file paths may need to be updated for your specific environment.
