from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from backend.config import settings
from backend.schemas import DetectionResponse
from backend.model import PestDetectionModel
from backend.recommendations import get_recommendation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development and demo purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
model_instance = None

@app.on_event("startup")
async def startup_event():
    global model_instance
    try:
        logger.info(f"Starting up application. HF_REPO_ID: {settings.hf_repo_id}")
        model_instance = PestDetectionModel(repo_id=settings.hf_repo_id, filename=settings.model_filename)
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load model during startup: {e}")
        raise e

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.post("/detect", response_model=DetectionResponse)
async def detect_pests(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        
        # Run inference in a threadpool to prevent blocking the async event loop
        detections, img_base64, inference_time_ms = await run_in_threadpool(model_instance.predict, image_bytes)
        
        # Add recommendations to detections
        for det in detections:
            det["recommendation"] = get_recommendation(det["pest_class"])
            
        return DetectionResponse(
            detections=detections,
            total_pests_detected=len(detections),
            annotated_image_base64=img_base64,
            inference_time_ms=inference_time_ms
        )
    except ValueError as ve:
        logger.error(f"Validation error during prediction: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
