# Food Inspection Dataset - Fruits and Vegetables

## Overview

This repository contains a hosted version of a fruits and vegetables computer vision dataset used for the **YOLO Fruit Vision - Food Inspection MLOps Pipeline**.

The dataset is designed for **object detection tasks**, where a deep learning model learns to identify and localize different categories of fruits and vegetables using bounding box annotations.

This dataset is integrated into an end-to-end MLOps workflow including:

- Dataset ingestion
- Cloud-based dataset storage
- Data preprocessing
- Dataset versioning
- YOLO model training
- Model evaluation
- Model deployment preparation

The purpose of this repository is to provide a reproducible dataset source for experimentation and development of computer vision models.

---

# Dataset Source and Attribution

## Original Dataset

This dataset is based on the original:

**LVIS Fruits And Vegetables Dataset**

Original source:

- Dataset provider: ACH-2003
- Original dataset page:

https://huggingface.co/datasets/ACH-2003/LVIS_Fruits_And_Vegetables


The original dataset creators retain ownership of the dataset, images, annotations, and associated resources.

This repository does **not** claim ownership of the original dataset.

This repository provides a hosted and organized version of the dataset for:

- Educational purposes
- Research experimentation
- Computer vision model development
- MLOps pipeline demonstration


Users should consult the original dataset source for the official license and usage conditions.

---

# Dataset Description

The dataset contains images of different fruits and vegetables annotated for object detection.

Each annotation provides:

- Object category
- Bounding box coordinates
- Object location inside the image


The dataset can be used for:

- Fruit detection
- Vegetable detection
- Food inspection systems
- Agricultural computer vision
- Object detection benchmarking
- YOLO model training


Example model output:

```json
{
    "class": "apple",
    "confidence": 0.95,
    "bounding_box": [
        120,
        80,
        350,
        300
    ]
}
```

---

# Dataset Structure

The dataset follows an object detection format compatible with YOLO-based training pipelines.

```
LVIS_Fruits_And_Vegetables/

│
├── images/
│   │
│   ├── train/
│   │   ├── image001.jpg
│   │   ├── image002.jpg
│   │   └── ...
│   │
│   ├── val/
│   │   ├── image101.jpg
│   │   └── ...
│   │
│   └── test/
│       ├── image201.jpg
│       └── ...
│
│
├── labels/
│   │
│   ├── train/
│   │   ├── image001.txt
│   │   └── ...
│   │
│   ├── val/
│   │   └── ...
│   │
│   └── test/
│       └── ...
│
│
└── data.yaml
```

---

# Annotation Format

The annotations use the YOLO object detection format.

Each image has a corresponding text annotation file.

Each line represents one detected object:

```
class_id x_center y_center width height
```

Example:

```
3 0.512 0.431 0.213 0.184
```

Where:

| Value | Description |
|---|---|
| class_id | Object category identifier |
| x_center | Normalized bounding box center X coordinate |
| y_center | Normalized bounding box center Y coordinate |
| width | Normalized bounding box width |
| height | Normalized bounding box height |

All coordinates are normalized between:

```
0 and 1
```

---

# Classes

The dataset contains multiple fruit and vegetable categories.

The complete class list is defined inside:

```
data.yaml
```

Example:

```yaml
names:
  0: apple
  1: banana
  2: orange
  3: tomato
```

Number of classes:

```
[INSERT NUMBER OF CLASSES]
```

---

# Dataset Splits

The dataset provides predefined splits for machine learning experiments.

| Split | Purpose |
|---|---|
| Train | Used for model learning |
| Validation | Used for evaluation during training |
| Test | Used for final performance evaluation |

Dataset organization:

```
train/
    images
    labels


val/
    images
    labels


test/
    images
    labels
```

Dataset split statistics:

| Split | Number of Images |
|---|---|
| Train | [INSERT VALUE] |
| Validation | [INSERT VALUE] |
| Test | [INSERT VALUE] |

---

# Cloud Storage

This dataset is hosted on the Hugging Face Hub.

Dataset repository:

```
https://huggingface.co/datasets/ACH-2003/food-inspection-mlops
```

Hugging Face is used as the cloud storage layer for the MLOps pipeline.

The dataset can be accessed remotely from training environments such as:

- Google Colab
- Kaggle Notebooks
- Cloud training instances


---

# MLOps Data Pipeline

The dataset follows this workflow:

```
                 Dataset Source

                       |
                       v

             Hugging Face Dataset Hub

                       |
                       v

              Data Ingestion Component

                       |
                       v

               Raw Dataset Storage

                       |
                       v

             Data Validation Component

                       |
                       v

          Data Transformation Component

                       |
                       v

             Processed Dataset Storage

                       |
                       v

              YOLO Training Pipeline

                       |
                       v

                 Trained Model

                       |
                       v

             Model Evaluation / Deployment
```

---

# Loading the Dataset

The dataset can be downloaded using the Hugging Face Hub API.

Example:

```python
from huggingface_hub import snapshot_download


dataset_path = snapshot_download(
    repo_id="ACH-2003/food-inspection-mlops",
    repo_type="dataset"
)


print(dataset_path)
```

---

# Integration With YOLO

The dataset is intended to be compatible with YOLO object detection models.

Example training workflow:

```
Dataset
   |
   |
   v

YOLO Data Loader

   |
   |
   v

YOLO Backbone

   |
   |
   v

Detection Head

   |
   |
   v

Bounding Boxes + Classes
```

Possible supported models:

- YOLOv8
- YOLOv9
- YOLOv10
- YOLOv11

---

# Dataset Versioning

Dataset versions are managed as part of the MLOps workflow.

Example:

```
Dataset v1
    |
    |
Dataset v2
    |
    |
Dataset v3
```

Each version represents a reproducible state of:

- Images
- Labels
- Metadata
- Processing steps

---

# Project Usage

This dataset is used in the following project:

## YOLO Fruit Vision - Food Inspection System

The objective is to build a computer vision system capable of:

- Detecting food ingredients
- Identifying fruit and vegetable categories
- Supporting automated inspection workflows
- Providing structured detection outputs


---

# License and Disclaimer

This repository is intended for educational and research purposes.

The original dataset license, terms, and conditions remain applicable.

The original dataset creators should be credited when this dataset is used.

For commercial usage, users must verify permissions from the original dataset source.

---

# Maintainer

Dataset integration and MLOps pipeline:

**Achraf Saadali**

Project:

**YOLO Fruit Vision - Food Inspection MLOps**
