import datetime
import numpy as np
import subprocess
import cv2
import os
import sys
import atexit
from dotenv import load_dotenv
from core.tools import is_far, is_moving
from core.yolo import YOLOv8_face

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

load_dotenv()

print("[FDIAS] Initializing Face Detection System...", flush=True)
weights_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weights", "yolov8n-face.onnx")
print(f"[FDIAS] Loading YOLO model from: {weights_path}", flush=True)
facemodel = YOLOv8_face(weights_path, conf_thres=0.45, iou_thres=0.5)
print("[FDIAS] Model loaded successfully!", flush=True)

# Simple tracker state
def init_tracker():
    global next_track_id, last_positions, track_history
    next_track_id = 1
    last_positions = {}  # Track ID -> last position
    track_history = {}   # Track ID -> list of positions

init_tracker()
print("[FDIAS] Opening camera...", flush=True)
cap = cv2.VideoCapture(0)  # Use default camera
if not cap.isOpened():
    raise Exception("Could not open video device")
print("[FDIAS] Camera opened successfully!", flush=True)
print("[FDIAS] System ready! Press 'q' in the video window to quit.", flush=True)
print("[FDIAS] Position yourself 3-6 feet from camera and look directly at it.", flush=True)
print("="*60, flush=True)

seen_ids = set()

previous_frame = None
process = None

def cleanup_subprocess():
    if process.poll() is None:
        print("Terminating subprocess...")
        process.terminate()
        process.wait()

atexit.register(cleanup_subprocess)

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count < 5: continue

    if previous_frame is not None and is_moving(previous_frame, frame):
        previous_frame = frame.copy()
    else:
        previous_frame = frame.copy()

        if process == None or process.poll() is not None:
            python_executable = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "venv", "Scripts", "python.exe")
            monitor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monitor.py")
            print("[FDIAS] Starting monitoring process...", flush=True)
            process = subprocess.Popen([python_executable, "-u", monitor_path])

        try:
            boxes, scores, classids, kpts = facemodel.detect(frame)
            detections = []

            for box, score, kp in zip(boxes, scores, kpts):
                x, y, w, h = box.astype(int)

                if is_far(frame, (x, y, (x + w), (y + h))):
                    print("[FDIAS] ⚠️  Face detected but too far - move closer to camera")
                    continue

                lefteye = int(kp[0 * 3])
                righteye = int(kp[1 * 3])

                cv2.circle(frame, (int(kp[0 * 3]), int(kp[0 * 3 + 1])), 4, (0, 255, 0), thickness=-1)
                cv2.circle(frame, (int(kp[1 * 3]), int(kp[1 * 3 + 1])), 4, (0, 255, 0), thickness=-1)
                
                eye_threshold = 30
                eye_difference = abs(lefteye - righteye)
                
                if eye_difference <= eye_threshold:
                    print(f"[FDIAS] ⚠️  Face detected but not looking at camera (eye diff: {eye_difference})")
                    continue

                detections.append([x, y, x + w, y + h, score, 0])

            global next_track_id, last_positions, track_history
            
            tracked_objects = []
            if len(detections) > 0:
                current_detections = np.array(detections)
                
                # For each detection, find closest match in last_positions
                for det in current_detections:
                    x1, y1, x2, y2 = map(int, det[:4])
                    center = np.array([(x1 + x2)/2, (y1 + y2)/2])
                    
                    best_dist = float('inf')
                    best_id = None
                    
                    # Compare with last known positions
                    for track_id, last_pos in last_positions.items():
                        dist = np.linalg.norm(center - last_pos)
                        if dist < best_dist and dist < 100:  # Max distance threshold
                            best_dist = dist
                            best_id = track_id
                    
                    if best_id is None:
                        # New track
                        best_id = next_track_id
                        next_track_id += 1
                        track_history[best_id] = []
                    
                    # Update position
                    last_positions[best_id] = center
                    track_history[best_id].append((x1, y1, x2, y2))
                    
                    # Add to tracked objects
                    tracked_objects.append([x1, y1, x2, y2, best_id])
            
            # Clean up old tracks
            current_tracks = set(t[4] for t in tracked_objects)
            for track_id in list(last_positions.keys()):
                if track_id not in current_tracks:
                    del last_positions[track_id]
                    if track_id in track_history:
                        del track_history[track_id]
            
            for track in tracked_objects:
                x1, y1, x2, y2, track_id = map(int, track)

                if track_id not in seen_ids:
                    seen_ids.add(track_id)
                    person_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage", "unknown", f"person_{track_id}")
                    if not os.path.exists(person_dir): os.makedirs(person_dir)

                    timestamp = int(datetime.datetime.now().timestamp() * 1000)
                    frame_path = os.path.join(person_dir, f"{timestamp}.jpg")
                    cv2.imwrite(frame_path, previous_frame)
                    print(f"[FDIAS] ✓ New person detected! ID: {track_id} - Saved for recognition")

                label = f"ID: {track_id}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        except Exception as e:
            pass  # No faces in frame
    
    cv2.imshow('Output', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
