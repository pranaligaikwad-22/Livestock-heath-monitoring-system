# Cow Disease Prediction System

An AI-powered web application that predicts cow diseases using Convolutional Neural Networks (CNN). The system can classify three types of conditions: Healthy, Lumpy Skin Disease, and Foot and Mouth Disease.

## Features

- 🐄 **Disease Prediction**: Upload an image of a cow to get instant disease prediction
- 🤖 **AI Chatbot**: Interactive chatbot that provides information about cow diseases
- 👨‍⚕️ **Doctor's Recommendations**: Get professional suggestions based on the prediction
- 🎨 **Beautiful UI**: Modern, responsive web interface
- 📊 **High Accuracy**: CNN model trained on thousands of images

## Dataset Structure

```
Cows datasets/
├── healthy/          (1291 images)
├── lumpy/            (1207 images)
└── foot-and-mouth/   (746 images)
```

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Train the model** (if not already trained):
```bash
python train_model.py
```

This will:
- Load and preprocess the images
- Train a CNN model with data augmentation
- Save the trained model as `cow_disease_model.h5`
- Generate training history plots

## Usage

1. **Start the Flask server**:
```bash
python app.py
```

2. **Open your browser** and navigate to:
```
http://localhost:5000
```

3. **Upload an image**:
   - Click on the upload area or drag & drop an image
   - Click "Predict Disease" button
   - View the prediction results and doctor's recommendations

4. **Use the Chatbot**:
   - Type questions about cow diseases
   - Get instant information about symptoms, prevention, and treatment

## Model Architecture

The CNN model consists of:
- 4 Convolutional blocks with Batch Normalization
- MaxPooling layers for dimensionality reduction
- Dropout layers for regularization
- Dense layers for classification
- Softmax output layer for 3-class classification

## API Endpoints

### POST `/predict`
Upload an image file to get disease prediction.

**Request**: Form data with `file` field (image file)

**Response**:
```json
{
  "success": true,
  "prediction": "healthy",
  "confidence": 95.5,
  "suggestions": {
    "title": "Healthy Cow",
    "description": "...",
    "suggestions": [...],
    "severity": "None",
    "urgency": "Low"
  },
  "image": "base64_encoded_image"
}
```

### POST `/chatbot`
Send a message to the chatbot.

**Request**:
```json
{
  "message": "What are the symptoms of lumpy skin disease?"
}
```

**Response**:
```json
{
  "success": true,
  "response": "Lumpy Skin Disease (LSD) is a viral disease..."
}
```

## Project Structure

```
.
├── app.py                 # Flask backend application
├── train_model.py         # CNN model training script
├── templates/
│   └── index.html         # Frontend HTML
├── static/
│   ├── style.css          # Styling
│   └── script.js          # Frontend JavaScript
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── archive (5)/
    └── Cows datasets/     # Dataset directory
```

## Notes

- The model file (`cow_disease_model.h5`) will be created after training
- Uploaded images are temporarily stored and then deleted after prediction
- Maximum file size: 16MB
- Supported formats: JPG, PNG, JPEG

## Future Improvements

- Add more disease categories
- Implement model retraining with new data
- Add user authentication
- Store prediction history
- Export prediction reports

## License

This project is for educational purposes.

## Disclaimer

This system is designed to assist veterinarians and farmers but should not replace professional veterinary consultation. Always consult a qualified veterinarian for proper diagnosis and treatment.
