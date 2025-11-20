import os
from core.bot import TelegramBot
from dotenv import load_dotenv

load_dotenv()

print("Testing Telegram Bot...")
print(f"TOKEN: {os.getenv('TOKEN')[:20]}...")
print(f"CHAT_ID: {os.getenv('CHAT_ID')}")

tel = TelegramBot(os.getenv("TOKEN"))
tel.run()

chat_id = os.getenv("CHAT_ID")

print("\nSending test message...")
try:
    tel.bot.send_message(chat_id, "🔔 Test Alert: FDIAS system is working!")
    print("✓ Message sent successfully!")
except Exception as e:
    print(f"✗ Error sending message: {e}")

print("\nSending test photo...")
try:
    # Create a test image path - using one from storage/faces if available
    test_image = None
    faces_dir = './storage/faces'
    
    for person in os.listdir(faces_dir):
        person_path = os.path.join(faces_dir, person)
        if os.path.isdir(person_path):
            for file in os.listdir(person_path):
                if file.endswith(('.jpg', '.png', '.jpeg')):
                    test_image = os.path.join(person_path, file)
                    break
        if test_image:
            break
    
    if test_image:
        with open(test_image, 'rb') as photo:
            tel.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption="🚨 TEST INTRUSION ALERT 🚨\n\nThis is a test alert from FDIAS!"
            )
        print("✓ Photo sent successfully!")
    else:
        print("✗ No test image found")
except Exception as e:
    print(f"✗ Error sending photo: {e}")

print("\n✓ Test complete! Check your Telegram for messages.")
