
# AgriSentry: AI-Powered Pest Detection for Indian Agriculture

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Abstract

Crop loss due to pest infestation is a critical challenge for India's agricultural sector, directly impacting farmer livelihoods and national food security. This project, "AgriSentry," proposes a highly accessible, deep learning-based solution for the early detection and identification of common agricultural pests. By leveraging the state-of-the-art YOLOv8 object detection model, AgriSentry is designed to empower farmers by turning a standard smartphone into a powerful diagnostic tool. A farmer can capture an image of a plant, and the system will automatically identify and locate pests such as aphids, whiteflies, and bollworms. This enables timely, targeted intervention, reducing crop damage, minimizing pesticide costs, and promoting sustainable farming practices in line with Integrated Pest Management (IPM).

---

## 1. The Problem: A Microscopic Threat to a National Lifeline

Agriculture is the backbone of the Indian economy, with millions of farmers, particularly in states like Telangana, depending on crops like cotton, rice, and chili. However, these farmers face a relentless battle against pests that can decimate yields. The key challenges are:

* **Delayed Detection:** Infestations often go unnoticed until significant, irreversible damage has occurred.
* **Misidentification:** Many pests are small and look similar. Using the wrong pesticide is ineffective, wastes money, and harms the environment.
* **Overuse of Pesticides:** To avoid risk, farmers may resort to broad-spectrum pesticide spraying, which increases costs, leads to soil and water pollution, and can be hazardous to human health.



---

## 2. The Solution: AgriSentry

AgriSentry is a computer vision system that acts as an "AI expert in the farmer's pocket." It uses a highly-tuned object detection model to find and name pests directly from an image, providing crucial information for immediate action.

**Key Features:**

* **Instant Identification:** Provides on-the-spot identification of common pests on key crops.
* **High Accuracy:** The model is trained on a custom dataset specifically curated for pests prevalent in the Indian subcontinent.
* **Accessible Technology:** Designed to work with images from any standard smartphone, requiring no specialized equipment.
* **Decision Support:** By accurately identifying the threat, the system helps farmers make informed decisions about using the right treatment at the right time.

---

## 3. Methodology

The project follows a proven deep learning pipeline: Data Collection, Annotation, Model Training, and Inference.

### 3.1. Data Collection & Annotation

This is the most critical phase for ensuring model accuracy. The custom dataset will be constructed by:

1.  **Sourcing Images:** Gathering thousands of high-resolution images of pests on plant leaves from agricultural research portals (e.g., ICAR, Professor Jayashankar Telangana State Agricultural University), farmer forums, and expert videos on YouTube.
2.  **Data Augmentation:** Applying techniques like rotation, scaling, and brightness adjustments to increase the diversity of the dataset and make the model more robust.
3.  **Annotation:** Using a tool like Roboflow or CVAT to manually draw bounding boxes around each pest in the images and assign the correct class label (e.g., `pink_bollworm`, `aphid`, `whitefly`).

### 3.2. Model & Training

* **Model:** We will use the **YOLOv8** object detection model from Ultralytics, pre-trained on the COCO dataset. This transfer learning approach allows the model to learn pest-specific features much more efficiently.
* **Training:** The model will be fine-tuned on our custom annotated pest dataset. The `src/train.py` script will manage the training process, saving the best model weights for inference.

### 3.3. Inference

The `src/predict.py` script is the operational core of the project. It loads the trained AgriSentry model and runs it on a new image, outputting a copy of the image with bounding boxes and labels drawn around any detected pests.

---

## 4. Installation & Usage

### 4.1. Prerequisites

* Python 3.8+
* PyTorch
* FFmpeg (for video data processing)

### 4.2. Installation

```bash
# 1. Clone the repository
git clone [https://github.com/your-username/AgriSentry.git](https://github.com/your-username/AgriSentry.git)
cd AgriSentry

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# 3. Install dependencies
pip install -r requirements.txt
````

### 4.3. How to Use

#### Training (with your own dataset)

1.  Place your annotated dataset in the `data/` directory.
2.  Update the `data/pest_dataset.yaml` file with your dataset paths and class names.
3.  Run the training script:
    ```bash
    python src/train.py
    ```

#### Prediction (with the trained model)

```bash
# Predict on a single image of a crop leaf
python src/predict.py --source /path/to/your/leaf_image.jpg
```

-----

## 5\. Future Work & Impact

AgriSentry is a powerful proof-of-concept with a clear path to real-world deployment.

  * **Future Work:**
      * **Mobile App Development:** Integrate the model into a simple Android application for seamless use by farmers.
      * **Severity Estimation:** Enhance the model to not only detect pests but also estimate the density of the infestation (e.g., low, medium, high).
      * **Disease Detection:** Expand the dataset to include common plant diseases, making the tool a comprehensive crop health monitor.
  * **Impact:** By democratizing access to expert-level pest identification, AgriSentry can significantly improve crop yields, increase farmer profitability, and promote a more sustainable and food-secure future for India.

<!-- end list -->

