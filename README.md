# Deepfake Web App

A real-time face swapping web application built with Flask, OpenCV, and InsightFace. Upload a face image and see it swapped onto your webcam feed in real-time.

## Features

- **Real-time Face Swapping**: Instant deepfake processing using your webcam
- **Drag & Drop Upload**: Easy image upload with drag and drop support
- **Face Detection**: Automatic validation to ensure uploaded images contain faces
- **Responsive Design**: Works on desktop and mobile devices
- **Single Page Interface**: Clean, modern UI that fits in one viewport
- **High Performance**: Optimized processing for smooth real-time performance

## Requirements

### Python Dependencies
```bash
pip install flask opencv-python insightface numpy
```

### System Requirements
- Python 3.7+
- Webcam access
- CUDA-compatible GPU (recommended for better performance)
- At least 4GB RAM

## Installation

1. Clone or download the application
2. Install dependencies:
   ```bash
   pip install flask opencv-python insightface numpy
   ```
3. Run the application:
   ```bash
   python fake.py
   ```
4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Start the Application**: Run the Flask app and open the web interface
2. **Upload a Face Image**: 
   - Click the "Upload Image" button or drag and drop an image
   - The image must contain a clearly visible face
   - Supported formats: JPG, PNG, etc.
3. **Real-time Deepfake**: 
   - Allow webcam access when prompted
   - Your face will be replaced with the uploaded face in real-time
   - Face swapping updates every 5 frames for optimal performance

## Technical Details

### Core Technologies
- **Flask**: Web framework for the backend
- **OpenCV**: Computer vision and webcam handling
- **InsightFace**: Advanced face detection and swapping
- **NumPy**: Numerical computations

### Performance Optimizations
- **Frame Skipping**: Processes every 5th frame to maintain smooth performance
- **Image Scaling**: Uses 0.2x scale for face detection to reduce computation
- **Model Caching**: InsightFace models are loaded once and reused
- **Efficient Streaming**: Uses Flask's Response streaming for real-time video

### File Structure
```
├── fake.py              # Main Flask application
├── source.png          # Uploaded face image (created at runtime)
└── README.md           # This file
```

## Troubleshooting

### Common Issues

**"No face detected" error:**
- Ensure the uploaded image has a clear, front-facing face
- Use good lighting and avoid sunglasses or face coverings
- Try a different image with better quality

**Webcam not working:**
- Check browser permissions for camera access
- Ensure no other applications are using the webcam
- Try refreshing the page (or press Escape key)

**Slow performance:**
- Close other applications to free up system resources
- Use a GPU-enabled system for better performance
- Reduce browser window size if needed

**Model download issues:**
- Ensure stable internet connection for first run
- InsightFace will automatically download required models
- Check firewall settings if download fails

## Browser Compatibility

- **Chrome**: Fully supported (recommended)
- **Firefox**: Fully supported
- **Safari**: Supported with some limitations
- **Edge**: Fully supported

## Security Notes

- Images are temporarily saved as `source.png` and overwritten with each upload
- No data is permanently stored or transmitted to external servers
- Webcam feed is processed locally and not saved

## Controls

- **Upload**: Click the upload button or drag & drop images
- **Reset**: Press `Escape` key to reload the application
- **Mobile**: Touch-friendly interface with responsive design

## Performance Tips

1. Use well-lit, high-quality face images for best results
2. Ensure stable lighting for your webcam
3. Close unnecessary browser tabs to free up resources
4. Use a wired internet connection if experiencing issues

## License

This project is for educational and research purposes. Please ensure you have proper consent when using face images and comply with local laws regarding deepfake technology.

## Credits

- **InsightFace**: Advanced face analysis toolkit
- **OpenCV**: Computer vision library
- **Flask**: Python web framework