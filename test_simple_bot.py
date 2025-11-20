import os
from dotenv import load_dotenv
import telebot

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print(f"Testing Telegram bot...")
print(f"TOKEN: {TOKEN[:20]}...")
print(f"CHAT_ID: {CHAT_ID}")

bot = telebot.TeleBot(TOKEN, parse_mode=None)

print("\nSending test message...")
try:
    result = bot.send_message(
        chat_id=CHAT_ID,
        text="🚨 TEST ALERT 🚨\n\nThis is a test message from FDIAS!\nIf you see this, the bot is working!"
    )
    print(f"✓ Message sent successfully!")
    print(f"Message ID: {result.message_id}")
    print(f"Chat ID: {result.chat.id}")
    print("\nCheck your Telegram app now!")
except Exception as e:
    print(f"✗ Failed to send message: {e}")
    import traceback
    traceback.print_exc()
