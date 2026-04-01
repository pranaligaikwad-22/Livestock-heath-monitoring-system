# Quick Start Guide

## Step 1: Install Dependencies

Open your terminal/command prompt and run:

```bash
pip install -r requirements.txt
```

## Step 2: Train the Model

Train the CNN model on your dataset:

```bash
python train_model.py
```

**Note**: This will take some time (30-60 minutes depending on your hardware). The model will be saved as `cow_disease_model.h5`.

**What happens during training:**
- Images are loaded and preprocessed
- Data augmentation is applied (rotation, zoom, flip, etc.)
- Model is trained with validation split (80% train, 20% validation)
- Best model is saved automatically
- Training history graph is generated

## Step 3: Run the Web Application

Start the Flask server:

```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

## Step 4: Open in Browser

Navigate to: **http://localhost:5000**

## Step 5: Use the Application

1. **Upload Image**: Click the upload area or drag & drop a cow image
2. **Predict**: Click "Predict Disease" button
3. **View Results**: See prediction, confidence, and doctor's recommendations
4. **Chat**: Ask questions in the chatbot about cow diseases

## Troubleshooting

### Model Not Found Error
- Make sure you've run `train_model.py` first
- Check that `cow_disease_model.h5` exists in the project directory

### Dataset Path Error
- Verify the dataset is at: `archive (5)\Cows datasets\`
- Check that folders `healthy`, `lumpy`, and `foot-and-mouth` exist

### Port Already in Use
- Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

### Memory Issues During Training
- Reduce `BATCH_SIZE` in `train_model.py` (try 16 or 8)
- Reduce `IMG_SIZE` (try 128 instead of 224)

## Tips

- **Better Accuracy**: Train for more epochs (increase `EPOCHS` in `train_model.py`)
- **Faster Training**: Use GPU if available (TensorFlow will detect automatically)
- **Test Images**: Use clear, well-lit images of cows for best results
