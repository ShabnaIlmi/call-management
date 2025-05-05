import logging
import mysql.connector
from plyer import notification
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

# Connect to MySQL
def connect_db():
    logging.debug("Connecting to MySQL...")
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="management_system"
    )

# Send desktop notification
def send_desktop_notification(sender, message):
    logging.debug(f"Sending desktop notification: {sender}: {message}")
    notification.notify(
        title=f"New message from {sender}",
        message=message,
        app_name="Telegram Bot",
        timeout=5
    )

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("/start command triggered.")
    await update.message.reply_text("👋 I'm active and listening to group messages!")

# Handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        logging.warning("Received non-text message or null message.")
        return

    sender = update.effective_user.username or update.effective_user.full_name or "Anonymous"
    message = update.message.text
    logging.info(f"Received message from {sender}: {message}")

    send_desktop_notification(sender, message)

    try:
        db = connect_db()
        cursor = db.cursor()
        query = "INSERT INTO messages (sender, message, status) VALUES (%s, %s, %s)"
        values = (sender, message, 'unread')
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        db.close()
        logging.info("✅ Message saved to DB.")
    except Exception as e:
        logging.error(f"❌ DB Error: {e}")

def main():
    logging.info("🚀 Starting Telegram bot...")

    try:
        BOT_TOKEN = "8048205415:AAHe3HQ_bUqWXccfeb6xd9tPuphXHjt9sMA"  # Replace with your token
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        app.run_polling()
    except Exception as e:
        logging.critical(f"🔥 Failed to start the bot: {e}")

if __name__ == "__main__":
    main()
