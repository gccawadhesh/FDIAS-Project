import os
import cv2
from core.yolo import YOLOv8_face

# Get absolute path to the model
weights_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weights", "yolov8n-face.onnx")
print(f"Model path: {weights_path}")
print(f"Model exists: {os.path.exists(weights_path)}")

# Try to load the model
try:
    print("Trying to load model...")
    facemodel = YOLOv8_face(weights_path, conf_thres=0.45, iou_thres=0.5)
    print("Model loaded successfully")
    
    # Try to open the camera
    print("Trying to open camera...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
    else:
        print("Camera opened successfully")
        ret, frame = cap.read()
        if ret:
            print("Frame captured successfully")
            # Try to run detection on a single frame
            try:
                print("Running detection...")
                boxes, scores, classids, kpts = facemodel.detect(frame)
                print(f"Detection results: {len(boxes)} faces found")
                if len(boxes) > 0:
                    print(f"First box: {boxes[0]}")
            except Exception as e:
                print(f"Detection error: {str(e)}")
        else:
            print("Failed to capture frame")
        cap.release()
except Exception as e:
    print(f"Error loading model: {str(e)}")