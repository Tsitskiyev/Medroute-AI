# Pneumonia Detection Integration - User Guide

## What's Been Set Up

Your MedRoute AI application now supports **X-Ray chest image analysis for pneumonia detection**. Here's what was added:

### New Components

1. **XRay Processor** (`backend/app/services/xray_processor.py`)
   - Handles image preprocessing and validation
   - Makes predictions using trained CNN model
   - Converts grayscale to RGB for compatibility

2. **Training Script** (`backend/app/services/train_pneumonia_model.py`)
   - Trains pneumonia detection CNN using transfer learning (MobileNetV2)
   - Uses data augmentation for better accuracy
   - Saves trained model as `models/pneumonia_classifier.h5`

3. **New API Endpoint** (`/analyze-xray`)
   - Accepts X-Ray image uploads
   - Returns pneumonia detection results with confidence scores

4. **Updated Models** (`backend/app/models.py`)
   - `XRayAnalysisResult`: Structure for X-Ray analysis output
   - `XRayRequest`: Structure for X-Ray requests
   - Updated `TriageResponse`: Now includes optional X-Ray analysis

## Installation

All required dependencies have been installed:
- TensorFlow (for deep learning)
- Pillow (for image processing)
- NumPy & scikit-learn (for data processing)

## Step-by-Step Setup

### 1. Prepare Dataset
Your dataset should be in this structure:
```
backend/data/chest_xray/
├── train/
│   ├── NORMAL/     (normal chest X-Ray images)
│   └── PNEUMONIA/  (pneumonia X-Ray images)
├── val/
│   ├── NORMAL/
│   └── PNEUMONIA/
└── test/          (optional for evaluation)
    ├── NORMAL/
    └── PNEUMONIA/
```

### 2. Train the Model

Run the training script to train the model on your dataset:

```bash
cd backend
python -m app.services.train_pneumonia_model "G:/projects/PROJECT3/medroute-ai/backend/data/chest_xray"
```

**Expected Output:**
- Model training will take 10-15 minutes (depending on your GPU)
- Model will be saved as: `backend/models/pneumonia_classifier.h5`
- Test accuracy will be displayed (typically 80-90% with this dataset)

### 3. Start the Backend

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

## Using the API

### Analyze X-Ray Image

**Endpoint:** `POST /analyze-xray`

**Request:**
```bash
curl -X POST "http://localhost:8000/analyze-xray" \
  -H "accept: application/json" \
  -F "file=@/path/to/xray_image.jpg"
```

**Response Example (Normal):**
```json
{
  "error": null,
  "is_pneumonia": false,
  "confidence": 0.2342,
  "class": "Normal",
  "confidence_percent": 23.42
}
```

**Response Example (Pneumonia Detected):**
```json
{
  "error": null,
  "is_pneumonia": true,
  "confidence": 0.8765,
  "class": "Pneumonia",
  "confidence_percent": 87.65
}
```

### From Frontend

In your React/TypeScript frontend, you can send X-Ray images:

```typescript
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('http://localhost:8000/analyze-xray', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

## Understanding Results

- **is_pneumonia**: `true` if pneumonia detected, `false` if normal
- **confidence**: Float between 0-1 (closer to 1 = higher confidence)
- **confidence_percent**: Same as confidence but as percentage
- **error**: Any errors during processing (null if successful)

**Decision Threshold:** 0.5 confidence (customizable in `xray_processor.py`)

## Important Notes

⚠️ **Medical Disclaimer:**
This tool is for **screening and triage purposes only**. It is not a substitute for professional medical diagnosis. All results should be reviewed by a qualified radiologist or medical professional.

## Troubleshooting

**Q: Model not found error**
- A: Run the training script first to generate the model file

**Q: Image processing error**
- A: Ensure image is in supported format (.jpg, .jpeg, .png, .gif, .bmp)

**Q: Low accuracy**
- A: Increase epochs in training script or use more augmentation techniques

**Q: CUDA/GPU errors**
- A: TensorFlow will fall back to CPU automatically if GPU not available

## Next Steps

1. ✅ Put your dataset in `backend/data/chest_xray/`
2. 🔄 Run the training script to generate the model
3. 🚀 Start the backend server
4. 🎨 Update frontend to add X-Ray upload UI
5. 📊 Integrate results into your triage system

---

For questions or issues, check the backend logs for detailed error messages.
