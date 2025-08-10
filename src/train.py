import os
from ultralytics import YOLO

def main():
    """
    Main function to train the YOLOv8 object detection model on the custom pest dataset.
    """
    # --- 1. Configuration ---
    # Path to the dataset configuration YAML file.
    data_config_path = 'data/pest_dataset.yaml'
    
    # Choose the base model. 'yolov8n.pt' is small and fast.
    model_variant = 'yolov8n.pt'
    
    # Training hyperparameters.
    epochs = 150
    img_size = 640
    batch_size = 16 # Adjust based on your GPU memory.
    
    print(f"Starting training with model: {model_variant}")
    print(f"Dataset config: {data_config_path}")
    print(f"Training for {epochs} epochs with image size {img_size} and batch size {batch_size}.")

    # --- 2. Load the Model ---
    # Load a pre-trained YOLOv8 detection model.
    model = YOLO(model_variant)

    # --- 3. Train the Model ---
    # The `train` method handles the entire training process.
    results = model.train(
        data=data_config_path,
        epochs=epochs,
        imgsz=img_size,
        batch=batch_size,
        project='runs/detect',
        name='agrisentry_run1',
        exist_ok=True
    )

    print("\nTraining complete!")
    print(f"Model and results saved in: {results.save_dir}")
    print("You can now use the best model (runs/detect/agrisentry_run1/weights/best.pt) for prediction.")

if __name__ == '__main__':
    main()
