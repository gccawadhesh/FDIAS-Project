import os
from deepface import DeepFace
from core.bot import TelegramBot
from dotenv import load_dotenv
import time
import sys

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

load_dotenv()

# Create bot instance - we only need to send messages, not receive
import telebot
bot_token = os.getenv("TOKEN")
bot = telebot.TeleBot(bot_token, parse_mode=None)

chat_id = os.getenv("CHAT_ID")
if not chat_id:
    print("[MONITOR] ERROR: CHAT_ID not found in .env file", flush=True)
    exit(1)

print(f"[MONITOR] Starting face recognition monitor...", flush=True)
print(f"[MONITOR] Alerts will be sent to Telegram chat ID: {chat_id}", flush=True)
print(f"[MONITOR] Current working directory: {os.getcwd()}", flush=True)

script_dir = os.path.dirname(os.path.abspath(__file__))
unknown_dir = os.path.join(script_dir, 'storage', 'unknown')
faces_db_path = os.path.join(script_dir, 'storage', 'faces')

print(f"[MONITOR] Monitoring directory: {unknown_dir}", flush=True)
print(f"[MONITOR] Face database path: {faces_db_path}", flush=True)
print(f"[MONITOR] Checking if paths exist...", flush=True)
print(f"[MONITOR] Unknown dir exists: {os.path.exists(unknown_dir)}", flush=True)
print(f"[MONITOR] Faces DB exists: {os.path.exists(faces_db_path)}", flush=True)
print("[MONITOR] Waiting for faces to analyze...", flush=True)

while True:
    try:
        if not os.path.exists(unknown_dir):
            time.sleep(2)
            continue
        
        persons = [d for d in os.listdir(unknown_dir) if os.path.isdir(os.path.join(unknown_dir, d))]
        if persons:
            print(f"[MONITOR] Found {len(persons)} person folder(s): {persons}", flush=True)
            
        for person_folder in os.listdir(unknown_dir):
            person_path = os.path.join(unknown_dir, person_folder)
            if os.path.isdir(person_path):
                for frame_file in os.listdir(person_path):
                    if frame_file.endswith(('.jpg', '.png', '.jpeg')):
                        frame_path = os.path.join(person_path, frame_file)
                        print(f"[MONITOR] Analyzing face from {person_folder}...", flush=True)
                        
                        try:
                            # Check if database has any faces
                            has_faces = False
                            for item in os.listdir(faces_db_path):
                                item_path = os.path.join(faces_db_path, item)
                                if os.path.isdir(item_path):
                                    # Check if folder has any image files
                                    for file in os.listdir(item_path):
                                        if file.endswith(('.jpg', '.png', '.jpeg')):
                                            has_faces = True
                                            break
                                if has_faces:
                                    break
                            
                            is_unknown = True
                            
                            if has_faces:
                                faces = DeepFace.find(
                                    frame_path,
                                    db_path=faces_db_path,
                                    detector_backend='retinaface',
                                    enforce_detection=False,
                                    model_name='Facenet512',
                                    distance_metric='euclidean_l2',
                                    threshold=0.9,
                                    silent=True
                                )

                                if len(faces) > 0:
                                    for face in faces:
                                        if not face.empty:
                                            name = face['identity'][0]
                                            distance = face['distance'][0]
                                            threshold = face['threshold'][0]
                                            print(f"[MONITOR] ✓ Face matched: {name} (distance: {distance:.2f}, threshold: {threshold})", flush=True)
                                            is_unknown = False
                                            break
                            else:
                                print(f"[MONITOR] ⚠️ No faces in database - treating as unknown", flush=True)
                            
                            # Send alert for unknown faces
                            if is_unknown:
                                print(f"[MONITOR] ⚠️ UNKNOWN INTRUDER DETECTED! Sending alert...", flush=True)
                                try:
                                    with open(frame_path, 'rb') as photo:
                                        bot.send_photo(
                                            chat_id=chat_id,
                                            photo=photo,
                                            caption=f"🚨 INTRUSION ALERT 🚨\n\nUnknown person detected at door!\nTime: {frame_file.split('.')[0]}\nPerson ID: {person_folder}"
                                        )
                                    print(f"[MONITOR] ✓ Alert with photo sent to Telegram!", flush=True)
                                except Exception as e:
                                    print(f"[MONITOR] ✗ Failed to send alert: {e}", flush=True)
                        
                        except Exception as e:
                            print(f"[MONITOR] Error analyzing face: {e}", flush=True)
                        
                        # Clean up
                        try:
                            os.remove(frame_path)
                            if not os.listdir(person_path):
                                os.rmdir(person_path)
                        except Exception as e:
                            print(f"[MONITOR] Error cleaning up: {e}", flush=True)
        
        time.sleep(2)
    except Exception as e:
        print(f"[MONITOR] Error in monitoring loop: {e}", flush=True)
        time.sleep(2)
