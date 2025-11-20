import os
from dotenv import load_dotenv
import telebot
import time

# Load the token from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Create bot instance
bot = telebot.TeleBot(TOKEN)

# Message handler for /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Hello! Welcome to FDIAS Security System! 🔐\nI'm your security bot and I will notify you about any suspicious activities.")

# Message handler for all messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Hi! I received your message: '{message.text}'\nI'm working correctly and will notify you about security events!")

print("Bot is starting...")
print("Send a message to the bot in Telegram, and it will respond...")
try:
    # Run the bot
    bot.polling(none_stop=True, timeout=60)
except Exception as e:
    print(f"Error: {str(e)}")