"""
X-Ray image preprocessing and model management for pneumonia detection.
"""

import os
from pathlib import Path
from typing import Tuple

import numpy as np
from PIL import Image
from tensorflow import keras
from tensorflow.keras.preprocessing import image


class XRayProcessor:
    """Handle X-Ray image preprocessing and prediction."""
    
    IMG_SIZE = 224
    BATCH_SIZE = 32
    MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "models" / "pneumonia_classifier.h5"
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained model or create new one."""
        if self.MODEL_PATH.exists():
            self.model = keras.models.load_model(str(self.MODEL_PATH))
        else:
            print(f"Model not found at {self.MODEL_PATH}. Train model first.")
    
    @staticmethod
    def preprocess_image(image_path: str) -> np.ndarray:
        """
        Load and preprocess a single X-Ray image.
        
        Args:
            image_path: Path to X-Ray image file
            
        Returns:
            Preprocessed image array ready for prediction
        """
        # Load image in grayscale
        img = Image.open(image_path).convert('L')
        
        # Resize to model input size
        img = img.resize((XRayProcessor.IMG_SIZE, XRayProcessor.IMG_SIZE))
        
        # Convert to array and normalize
        img_array = np.array(img, dtype=np.float32) / 255.0
        
        # Convert grayscale to RGB (3 channels) for compatibility with pre-trained models
        img_array = np.stack([img_array] * 3, axis=-1)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def predict(self, image_path: str) -> dict:
        """
        Make prediction on X-Ray image.
        
        Args:
            image_path: Path to X-Ray image file
            
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            return {
                "error": "Model not loaded. Train model first.",
                "is_pneumonia": None,
                "confidence": None
            }
        
        try:
            # Preprocess image
            img_array = self.preprocess_image(image_path)
            
            # Make prediction
            prediction = self.model.predict(img_array, verbose=0)
            confidence = float(prediction[0][0])
            
            # Threshold: > 0.5 means pneumonia
            is_pneumonia = confidence > 0.5
            
            return {
                "error": None,
                "is_pneumonia": is_pneumonia,
                "confidence": round(confidence, 4),
                "class": "Pneumonia" if is_pneumonia else "Normal",
                "confidence_percent": round(confidence * 100, 2)
            }
        except Exception as e:
            return {
                "error": str(e),
                "is_pneumonia": None,
                "confidence": None
            }
    
    @staticmethod
    def validate_image_file(file_path: str) -> Tuple[bool, str]:
        """
        Validate if file is a valid X-Ray image.
        
        Args:
            file_path: Path to image file
            
        Returns:
            Tuple of (is_valid, message)
        """
        if not os.path.exists(file_path):
            return False, "File not found"
        
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext not in allowed_extensions:
            return False, f"Invalid file format. Allowed: {allowed_extensions}"
        
        try:
            img = Image.open(file_path)
            img.verify()
            return True, "Valid image file"
        except Exception as e:
            return False, f"Invalid image: {str(e)}"
