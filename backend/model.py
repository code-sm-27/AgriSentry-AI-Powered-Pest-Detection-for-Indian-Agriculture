import os
import cv2
import numpy as np
import time
from ultralytics import YOLO
from huggingface_hub import hf_hub_download
import base64

class PestDetectionModel:
    def __init__(self, repo_id: str = None, filename: str = "../models/best.pt"):
        self.model_path = "../models/yolov8n.pt"  # Fallback to base model
        
        # If repo_id is provided, try to download from Hugging Face
        if repo_id:
            try:
                print(f"Downloading model from Hugging Face: {repo_id}/{filename}")
                self.model_path = hf_hub_download(repo_id=repo_id, filename=filename)
            except Exception as e:
                print(f"Failed to download from HF: {e}. Falling back to default {self.model_path}")
        # Otherwise if there's a local best.pt, use it
        elif os.path.exists("best.pt"):
            self.model_path = "best.pt"
            
        print(f"Loading YOLO model from: {self.model_path}")
        self.model = YOLO(self.model_path)
        
    def predict(self, image_bytes: bytes):
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Failed to decode image. Please ensure the uploaded file is a valid image.")
        
        start_time = time.time()
        # Run inference
        results = self.model.predict(source=img, conf=0.25)
        end_time = time.time()
        inference_time_ms = (end_time - start_time) * 1000
        
        detections = []
        # results is a list of Results objects, we just need the first one (for the single image)
        result = results[0]
        
        # Extract detections
        for box in result.boxes:
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            cls_name = self.model.names[cls_id]
            
            # Bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            
            detections.append({
                "pest_class": cls_name,
                "confidence": conf,
                "bbox": [x1, y1, x2, y2]
            })
            
        # Get annotated image
        annotated_img = result.plot()
        
        # Convert annotated image to base64
        _, buffer = cv2.imencode('.jpg', annotated_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return detections, img_base64, inference_time_ms
