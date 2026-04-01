import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import numpy as np
import os

# Dataset path
DATASET_PATH = r"archive (5)\Cows datasets"

# Image parameters
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 50

# Create data generators with augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)

test_datagen = ImageDataGenerator(rescale=1./255)

# Load training data
train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

# Load validation data
validation_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=True
)

# Get number of classes
num_classes = len(train_generator.class_indices)
class_names = list(train_generator.class_indices.keys())
# Sort class names to ensure consistent ordering
class_names = sorted(class_names)
print(f"Classes: {class_names}")
print(f"Class indices mapping: {train_generator.class_indices}")
print(f"Number of classes: {num_classes}")

# Create a mapping from index to class name based on the actual class indices
# The class_indices dict maps class_name -> index
index_to_class = {v: k for k, v in train_generator.class_indices.items()}
print(f"Index to class mapping: {index_to_class}")

# Build CNN Model
model = Sequential([
    # First Convolutional Block
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    Dropout(0.25),
    
    # Second Convolutional Block
    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    Dropout(0.25),
    
    # Third Convolutional Block
    Conv2D(128, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    Dropout(0.25),
    
    # Fourth Convolutional Block
    Conv2D(256, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2, 2),
    Dropout(0.25),
    
    # Flatten and Dense Layers
    Flatten(),
    Dense(512, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

# Compile model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Model summary
model.summary()

# Callbacks
checkpoint = ModelCheckpoint(
    'cow_disease_model.h5',
    monitor='val_accuracy',
    save_best_only=True,
    mode='max',
    verbose=1
)

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    patience=5,
    min_lr=0.00001,
    verbose=1
)

# Train model
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=[checkpoint, early_stop, reduce_lr],
    verbose=1
)

# Save final model (always save, even if early stopping occurred)
try:
    model.save('cow_disease_model_final.h5')
    print("Final model saved as 'cow_disease_model_final.h5'")
except Exception as e:
    print(f"Warning: Could not save final model: {str(e)}")
    # Try to load the best checkpoint and save it
    try:
        if os.path.exists('cow_disease_model.h5'):
            best_model = load_model('cow_disease_model.h5')
            best_model.save('cow_disease_model_final.h5')
            print("Best checkpoint model saved as 'cow_disease_model_final.h5'")
        else:
            print("Warning: No model file found to save!")
    except Exception as e2:
        print(f"Error saving model: {str(e2)}")

# Save class names and indices mapping
import json
# Create index to class mapping based on the actual indices from the generator
index_to_class_dict = {int(v): k for k, v in train_generator.class_indices.items()}
save_data = {
    'class_names': class_names,
    'class_indices': train_generator.class_indices,
    'index_to_class': index_to_class_dict
}
with open('class_names.json', 'w') as f:
    json.dump(save_data, f, indent=2)
print(f"Saved class mapping to class_names.json")

# Plot training history
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.savefig('training_history.png')
print("\n" + "="*50)
print("Training completed!")
print("="*50)
# Check which model files exist
if os.path.exists('cow_disease_model.h5'):
    print("✓ Best model saved as 'cow_disease_model.h5'")
if os.path.exists('cow_disease_model_final.h5'):
    print("✓ Final model saved as 'cow_disease_model_final.h5'")
if os.path.exists('class_names.json'):
    print("✓ Class names saved to 'class_names.json'")
print(f"Class names: {class_names}")
print("="*50)
