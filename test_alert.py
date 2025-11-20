import os
from core.bot import TelegramBot
from dotenv import load_dotenv

load_dotenv()

print("=== FDIAS Telegram Alert Test ===\n")

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print(f"TOKEN: {TOKEN[:20]}...{TOKEN[-10:]}")
print(f"CHAT_ID: {CHAT_ID}\n")

tel = TelegramBot(TOKEN)
tel.run()

print("Sending test text message...")
try:
    tel.bot.send_message(CHAT_ID, "🔔 FDIAS Test: Bot is connected!")
    print("✓ Text message sent!\n")
except Exception as e:
    print(f"✗ Failed to send text: {e}\n")

print("Sending test intrusion alert with photo...")
try:
    # Find any image in storage/faces
    faces_dir = './storage/faces'
    test_image = None
    
    for person in os.listdir(faces_dir):
        person_path = os.path.join(faces_dir, person)
        if os.path.isdir(person_path):
            for file in os.listdir(person_path):
                if file.endswith(('.jpg', '.png', '.jpeg')):
                    test_image = os.path.join(person_path, file)
                    print(f"Using test image: {test_image}")
                    break
        if test_image:
            break
    
    if test_image:
        with open(test_image, 'rb') as photo:
            result = tel.bot.send_photo(
                chat_id=CHAT_ID,
                photo=photo,
                caption="🚨 INTRUSION ALERT 🚨\n\nUnknown person detected at door!\n\n[THIS IS A TEST]"
            )
        print(f"✓ Photo sent successfully! Message ID: {result.message_id}\n")
    else:
        print("✗ No test image found in storage/faces\n")
except Exception as e:
    print(f"✗ Failed to send photo: {e}\n")

print("=== Test Complete ===")
print("Check your Telegram app - you should have received:")
print("  1. A text message")
print("  2. An intrusion alert with photo")
