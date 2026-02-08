from telegram import Bot
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(TOKEN)

# Delete all pending updates
bot.delete_webhook(drop_pending_updates=True)
print("Cleared old updates. You can now run the bot safely.")
