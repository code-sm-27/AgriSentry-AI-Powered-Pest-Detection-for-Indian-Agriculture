from pydantic import BaseModel, Field
from typing import List

class Detection(BaseModel):
    pest_class: str = Field(..., description="The name of the detected pest.")
    confidence: float = Field(..., description="Confidence score of the detection (0 to 1).")
    bbox: List[float] = Field(..., description="Bounding box coordinates [x1, y1, x2, y2].")
    recommendation: str = Field(..., description="Actionable recommendation for the detected pest.")

class DetectionResponse(BaseModel):
    detections: List[Detection] = Field(..., description="List of all pests detected in the image.")
    total_pests_detected: int = Field(..., description="Total number of pests detected.")
    annotated_image_base64: str = Field(..., description="Base64 encoded string of the annotated image.")
    inference_time_ms: float = Field(..., description="Time taken to run model inference in milliseconds.")
