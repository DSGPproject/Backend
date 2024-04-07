#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import math
import os
import sys
from ultralytics import YOLO



if len(sys.argv) > 1:
    image_path = sys.argv[1]
else:
    print("No image path provided.")
    sys.exit(1)
# In[2]:


# Function to detect if an image contains a plant leaf
def detect_leaf(image_path, model, class_names):
    # Load the image
    img = cv2.imread(image_path)

    # Perform object detection
    results = model(img)

    # Check if any leaf is detected
    for r in results:
        for box in r.boxes.data:
            if box[5] == "leaf":
                return True

    return False


# In[8]:


def draw_boxes(img, results, class_names, objects_to_detect, confidence_threshold=0.5):
    object_detected = False
    object_boxes = []  # Store bounding box coordinates of detected objects
    for r in results:
        boxes = r.boxes.data

        for box in boxes:
            x1, y1, x2, y2 = map(int, box[:4])  # Extracting the first 4 elements
            confidence = math.ceil((box[4] * 100)) / 100

            # Check if the detected class index is within the range of class_names
            if int(box[5]) < len(class_names):
                # Check if the detected object is in the objects_to_detect list
                if confidence > confidence_threshold and class_names[int(box[5])] in objects_to_detect:
                    object_detected = True
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    object_boxes.append((x1, y1, x2, y2))  # Store bounding box coordinates

                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2

                    cv2.putText(img, f"{class_names[int(box[5])]} {confidence:.2f}", org, font, fontScale, color, thickness)

    return object_detected, object_boxes


# In[3]:


# model
model = YOLO("yolo-Weights/yolov8n.pt")


# In[4]:


# from google.colab import drive
# drive.mount('/content/drive')


# In[5]:


# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "potato", "tomato", "mango", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush","leaf"
              ]


# In[10]:


objects_to_detect = ["leaf"]


# In[17]:


def detect_leaf_from_image(image_path):
    img = cv2.imread(image_path)
    results = model(img)
    object_detected, _ = draw_boxes(img, results, classNames, objects_to_detect)
    return object_detected

# Example usage
# image_path = "/content/drive/MyDrive/dataset/unchanged/white spot/UNADJUSTEDNONRAW_thumb_f1.jpg"  # Replace with the path to the image
is_leaf = detect_leaf_from_image(image_path)

if is_leaf:
    print("The image contains a plant leaf.")
else:
    print("The image does not contain a plant leaf.")


# In[18]:


img = cv2.imread(image_path)


# In[19]:


# Function to draw bounding boxes, labels, and confidence scores
def draw_boxes(img, results, class_names, objects_to_detect, confidence_threshold=0.5):
    object_detected = False
    object_boxes = []  # Store bounding box coordinates of detected objects
    for r in results:
        boxes = r.boxes.data

        for box in boxes:
            x1, y1, x2, y2 = map(int, box[:4])  # Extracting the first 4 elements
            confidence = math.ceil((box[4] * 100)) / 100

            # Check if the detected class index is within the range of class_names
            if int(box[5]) < len(class_names):
                # Check if the detected object is in the objects_to_detect list
                if confidence > confidence_threshold and class_names[int(box[5])] in objects_to_detect:
                    object_detected = True
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    object_boxes.append((x1, y1, x2, y2))  # Store bounding box coordinates

                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 1
                    color = (255, 0, 0)
                    thickness = 2

                    cv2.putText(img, f"{class_names[int(box[5])]} {confidence:.2f}", org, font, fontScale, color, thickness)

    return object_detected, object_boxes

# Function to check if leaf is present
def is_leaf_present(results, class_names, confidence_threshold=0.5):
  for r in results:
    boxes = r.boxes.data
    for box in boxes:
      confidence = math.ceil((box[4] * 100)) / 100
      # Check if detected object is leaf with high confidence
      if confidence > confidence_threshold and class_names[int(box[5])] == "leaf":
        return True
  return False


# In[20]:


# Run object detection on the image
results = model(img)

# Check for leaf before drawing boxes
if is_leaf_present(results, classNames):
  object_detected, object_boxes = draw_boxes(img, results, classNames, objects_to_detect)
  # Display the image with bounding boxes (if a leaf is found)
  cv2.imshow('Image', img)
  cv2.waitKey(0)  # Wait for a key press to close the window
else:
  print("Image does not contain a leaf.")


# In[ ]:




