import telebot
import threading
import time

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token, parse_mode=None)
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            welcome_msg = """🔒 FDIAS - Face Detection & Intrusion Alert System

Hi! I'm monitoring your security system and will notify you about:
• Unknown faces detected
• Security events at your door

Commands:
/start - Show this message
/status - Check system status
/help - Show help

System is active and monitoring! 👀"""
            self.bot.reply_to(message, welcome_msg)
        
        @self.bot.message_handler(commands=['status'])
        def send_status(message):
            self.bot.reply_to(message, "✅ System is running and monitoring for intrusions!")
        
        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message):
            self.bot.reply_to(message, f"Hi! I received your message: '{message.text}'\n\nI'm working correctly and will notify you about security events!")

    def send_message(self, user_id, message):
        try:
            self.bot.send_message(user_id, message)
        except Exception as e:
            print(f"Error sending message: {e}")

    def run(self):
        polling_thread = threading.Thread(target=self.bot.infinity_polling)
        polling_thread.daemon = True
        polling_thread.start()