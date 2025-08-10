import os
import argparse
from ultralytics import YOLO

def predict(source, model_path):
    """
    Runs YOLOv8 inference on a given image source.

    Args:
        source (str): Path to the input image file.
        model_path (str): Path to the trained YOLOv8 model weights (.pt file).
    """
    if not os.path.exists(model_path):
        print(f"Error: Model weights not found at '{model_path}'")
        print("Please ensure you have a trained model. Run train.py first.")
        return

    if not os.path.exists(source):
        print(f"Error: Input source not found at '{source}'")
        return
        
    print(f"Loading model from: {model_path}")
    model = YOLO(model_path)

    print(f"Running prediction on: {source}")
    
    # Run prediction
    results = model.predict(
        source=source,
        save=True,
        conf=0.4, # Confidence threshold
        project='runs/predict',
        name='agrisentry_prediction',
        exist_ok=True
    )
    
    output_dir = os.path.join('runs/predict', 'agrisentry_prediction')
    print(f"\nPrediction complete. Results saved in '{output_dir}'.")

def main():
    """
    Parses command-line arguments and calls the prediction function.
    """
    parser = argparse.ArgumentParser(description="AgriSentry Prediction Script")
    parser.add_argument(
        '--source', 
        type=str, 
        required=True, 
        help="Path to the input image."
    )
    parser.add_argument(
        '--weights', 
        type=str, 
        default='runs/detect/agrisentry_run1/weights/best.pt', 
        help="Path to the trained model weights (.pt file)."
    )
    
    args = parser.parse_args()
    
    predict(args.source, args.weights)

if __name__ == '__main__':
    main()
