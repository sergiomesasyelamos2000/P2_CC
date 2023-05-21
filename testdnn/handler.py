import os
import cv2
import numpy as np
import urllib.request
import base64

def handle(inputURL):
    # Model architecture
    prototxt = "/home/app/function/deploy.prototxt"
    # Weights
    weights = "/home/app/function/res10_300x300_ssd_iter_140000.caffemodel"
    model = cv2.dnn.readNetFromCaffe(prototxt, weights)

    # Read image from URL
    resp = urllib.request.urlopen(inputURL)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Preprocess image for face detection
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0), False, False)

    # Pass the preprocessed image through the network
    model.setInput(blob)
    detections = model.forward()

    # Process the detections
    (h, w) = image.shape[:2]
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # Add detection frames to the original image
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Convert image to base64
    _, buffer = cv2.imencode('.png', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Construct data URL
    data_url = f'data:image/png;base64,{image_base64}'

    # Return data URL
    return data_url
