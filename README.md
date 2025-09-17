# 🎨 FourierDrawing: Interactive Fourier Series Visualization

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.85+-green.svg)](https://fastapi.tiangolo.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)

> **Transform any image into a mesmerizing animation of rotating vectors using Fourier series decomposition**

FourierDrawing is an interactive web application that demonstrates the mathematical beauty of Fourier series by converting uploaded images into animated drawings created by rotating complex vectors. Watch as hundreds of spinning circles work together to trace out your favorite images!

## 🌟 Live Demo

![FourierDrawing Demo](https://user-images.githubusercontent.com/79348782/198857561-531d9705-e81f-4219-a8e2-4f63ab1243f0.png)

*Example: The π symbol being drawn by 200 rotating vectors*

## ✨ Features

### 🔄 **Real-time Fourier Transform Visualization**
- Convert any image into a series of rotating complex vectors
- Watch as mathematical precision creates artistic beauty
- Supports up to 200+ vectors for high-fidelity reconstruction

### 🖼️ **Universal Image Support**
- **Input formats**: JPEG, PNG, PNM, SVG
- **Automatic conversion**: Non-SVG images converted to vector format using Potrace
- **Smart processing**: Handles complex shapes and multiple disconnected paths

### 🎮 **Interactive Controls**
- **Play/Pause**: Space bar or button control
- **Speed adjustment**: 11 speed levels (1x to maximum)
- **Vector count**: Dynamically adjust from 1 to 200+ vectors
- **Visual toggles**: Show/hide rotating circles and connecting vectors
- **Path clearing**: Reset the drawn path at any time

### 🎯 **Advanced Mathematical Implementation**

#### **Fourier Series Decomposition**
- Custom implementation of complex Fourier coefficient calculation
- Support for both cubic and linear Bézier curves
- Integration by parts for precise coefficient computation
- Frequency ordering: 0, 1, -1, 2, -2, 3, -3, ... for optimal visual progression

#### **SVG Path Processing**
- Complete SVG path parser supporting:
  - Move commands (M, m)
  - Cubic Bézier curves (C, c)
  - Linear segments (L, l)
  - Path closing (Z, z)
- Automatic path optimization and curve fitting

#### **Geometric Algorithms**
- Distance-based curve parameterization
- Automatic bounding box calculation
- Coordinate system transformations
- Curve length approximation using adaptive stepping

## 🏗️ Architecture

### **Backend (Python + FastAPI)**
```
API/
├── server.py          # FastAPI server and main endpoint
├── coeff.py          # Fourier coefficient calculator
├── bezier.py         # Bézier curve implementations
├── svg.py            # SVG parser and path processor  
├── complex_vector.py # Complex vector mathematics
├── utils.py          # Utility functions
└── config.py         # Configuration settings
```

### **Frontend (Vanilla JavaScript + HTML5 Canvas)**
```
front/
├── index.html        # Main application interface
├── static/
│   ├── js/index.js  # Animation engine and UI logic
│   └── css/main.css # Responsive styling
```

## 🚀 Getting Started

### Prerequisites

1. **ImageMagick** - For image format conversion
   ```bash
   # macOS
   brew install imagemagick
   
   # Ubuntu/Debian
   sudo apt-get install imagemagick
   
   # Windows
   # Download from: https://imagemagick.org/script/download.php
   ```

2. **Potrace** - For bitmap to vector conversion
   ```bash
   # macOS
   brew install potrace
   
   # Ubuntu/Debian  
   sudo apt-get install potrace
   
   # Windows
   # Download from: https://potrace.sourceforge.net/
   ```

3. **Python 3.10+**
   ```bash
   python --version  # Should be 3.10 or higher
   ```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/FourierDrawing.git
   cd FourierDrawing
   ```

2. **Set up Python environment**
   ```bash
   cd API/API
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install additional dependencies**
   ```bash
   pip install fastapi uvicorn python-multipart
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd API/API
   python server.py
   ```
   Server will start on `http://localhost:3000`

2. **Open the frontend**
   ```bash
   cd ../../front
   # Serve the files using any HTTP server, e.g.:
   python -m http.server 5500
   # Or use Live Server in VS Code
   ```
   Open `http://localhost:5500` in your browser

3. **Upload and animate!**
   - Click "Choose File" and select an image
   - Click "UPLOAD" to process
   - Watch your image come to life!

## 🎛️ Controls

| Control | Action | Shortcut |
|---------|--------|----------|
| **Play/Pause** | Toggle animation | `Space` |
| **Quit** | Return to upload screen | `Q` |
| **Clear Path** | Erase drawn path | `Backspace` |
| **Vector Count** | Adjust number of vectors | `←/→ Arrow Keys` |
| **Speed** | Change animation speed | Slider (1-11) |
| **Show Circles** | Toggle rotating circles | Toggle switch |
| **Show Vectors** | Toggle connecting lines | Toggle switch |

## 🧮 Mathematical Foundation

### Fourier Series Representation

Any closed curve can be represented as a sum of rotating complex vectors:

```
f(t) = Σ(n=-∞ to ∞) cₙ × e^(2πint)
```

Where:
- `cₙ` are the complex Fourier coefficients
- `n` represents the frequency (rotation speed)
- `t` is the parameter (time)

### Coefficient Calculation

For each Bézier curve segment, coefficients are calculated using:

```
cₙ = ∫₀¹ f(t) × e^(-2πint) dt
```

The integration is performed analytically for both linear and cubic Bézier curves using integration by parts.

### Path Reconstruction

The final path is reconstructed by:
1. Computing vector positions at each time step
2. Summing all vector contributions
3. Tracing the path of the final point

## 📊 Performance Metrics

- **Backend Processing**: ~0.1-2 seconds per image (depending on complexity)
- **Frontend Rendering**: 60 FPS animation capability
- **Memory Usage**: ~50MB for typical images
- **Vector Capacity**: Up to 500+ vectors (200 default for optimal performance)
- **Supported Image Sizes**: Up to 4K resolution

## 🎨 Example Gallery

The application includes 50+ pre-processed example images:
- Greek letters (π, φ, λ, ω, etc.)
- Corporate logos (Tesla, Nike, Apple, etc.)
- Mathematical symbols
- Custom artwork

## 🔧 Configuration

Key parameters can be adjusted in `config.py`:

```python
class Config:
    NUM_VECTORS = 200      # Default vector count
    DT = 0.01             # Time step for calculations
    BY_DIST = True        # Distance-based parameterization
    ACCEPTABLE_EXTENSIONS = ["jpeg", "jpg", "png", "pnm", "svg"]
```

## 🛠️ Technical Highlights

### **Advanced SVG Processing**
- Regex-based path parsing with support for all standard SVG commands
- Automatic relative/absolute coordinate handling
- Multi-path support for complex images

### **Optimized Mathematics**
- Custom implementation of complex number operations
- Analytical integration for precise coefficient calculation
- Efficient curve parameterization algorithms

### **Real-time Rendering**
- Dual-canvas architecture for smooth animation
- Optimized drawing algorithms for 60 FPS performance
- Dynamic quality adjustment based on vector count

### **User Experience**
- Responsive design for all screen sizes
- Intuitive keyboard shortcuts
- Real-time parameter adjustment without restart

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional curve types (quadratic Bézier, elliptical arcs)
- WebGL acceleration for higher vector counts
- Mobile touch controls
- Batch processing capabilities
- Export functionality (GIF, MP4)

## 📚 Educational Value

This project demonstrates:
- **Complex Analysis**: Fourier series and complex exponentials
- **Numerical Methods**: Integration techniques and approximation
- **Computer Graphics**: Path rendering and animation
- **Web Development**: Full-stack application architecture
- **Signal Processing**: Frequency domain representation

Perfect for:
- Mathematics and engineering students
- Educators teaching Fourier analysis
- Developers learning mathematical visualization
- Anyone curious about the mathematics behind animations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Fourier Series Theory**: Based on classical mathematical analysis
- **Potrace**: Bitmap to vector conversion
- **ImageMagick**: Image format handling
- **FastAPI**: Modern Python web framework
- **HTML5 Canvas**: High-performance 2D rendering

## 📞 Contact

**Your Name** - [your.email@example.com](mailto:your.email@example.com)

Project Link: [https://github.com/yourusername/FourierDrawing](https://github.com/yourusername/FourierDrawing)

---

*"Mathematics is the art of giving the same name to different things." - Henri Poincaré*

**Transform your images into mathematical art with FourierDrawing!** 🎨✨
