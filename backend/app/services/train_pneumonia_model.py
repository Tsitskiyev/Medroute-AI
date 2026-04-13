"""
Training script for pneumonia detection CNN model.
Run this once to train and save the model.

Usage:
    python -m app.services.train_pneumonia_model <path_to_dataset>
    
Example:
    python -m app.services.train_pneumonia_model G:/projects/PROJECT3/medroute-ai/backend/data/chest_xray
"""

import sys
from pathlib import Path

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def build_model(input_shape=(224, 224, 3)):
    """
    Build CNN model for X-Ray classification.
    Uses transfer learning approach for better performance.
    """
    # Base model: pre-trained MobileNetV2
    base_model = keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Add custom layers on top
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')  # Binary classification
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-4),
        loss='binary_crossentropy',
        metrics=['accuracy', keras.metrics.AUC()]
    )
    
    return model


def train_model(dataset_path: str = None):
    """
    Train pneumonia detection model on dataset.
    
    Args:
        dataset_path: Path to dataset folder containing train/test/val subdirectories.
                     If not provided, uses default location: backend/app/data/chest_xray
    """
    if dataset_path is None:
        # Use default location
        dataset_path = Path(__file__).resolve().parent.parent / "data" / "chest_xray"
    else:
        dataset_path = Path(dataset_path)
    
    if not dataset_path.exists():
        print(f"Error: Dataset path not found: {dataset_path}")
        print(f"Expected structure:")
        print(f"  {dataset_path}/")
        print(f"  ├── train/")
        print(f"  │   ├── NORMAL/")
        print(f"  │   └── PNEUMONIA/")
        print(f"  ├── val/")
        print(f"  │   ├── NORMAL/")
        print(f"  │   └── PNEUMONIA/")
        print(f"  └── test/")
        sys.exit(1)
    
    # Image augmentation for training data
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Just rescaling for validation/test data
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load training data
    print("Loading training data...")
    train_generator = train_datagen.flow_from_directory(
        str(dataset_path / 'train'),
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',
        color_mode='rgb'
    )
    
    # Load validation data
    print("Loading validation data...")
    val_generator = val_datagen.flow_from_directory(
        str(dataset_path / 'val'),
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',
        color_mode='rgb'
    )
    
    # Build and train model
    print("Building model...")
    model = build_model()
    
    print("Training model...")
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=20,
        steps_per_epoch=100,
        validation_steps=50,
        verbose=1
    )
    
    # Save model
    models_dir = Path(__file__).resolve().parent.parent.parent / 'models'
    models_dir.mkdir(exist_ok=True)
    
    model_path = models_dir / 'pneumonia_classifier.h5'
    model.save(str(model_path))
    print(f"\nModel saved to: {model_path}")
    
    # Evaluate on test set if available
    if (dataset_path / 'test').exists():
        print("\nEvaluating on test set...")
        test_generator = val_datagen.flow_from_directory(
            str(dataset_path / 'test'),
            target_size=(224, 224),
            batch_size=32,
            class_mode='binary',
            color_mode='rgb'
        )
        
        test_loss, test_accuracy, test_auc = model.evaluate(test_generator)
        print(f"Test Accuracy: {test_accuracy:.4f}")
        print(f"Test AUC: {test_auc:.4f}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Training pneumonia detection model...")
        print("Using default dataset path: backend/app/data/chest_xray")
        train_model()  # Use default path
    else:
        dataset_path = sys.argv[1]
        train_model(dataset_path)
