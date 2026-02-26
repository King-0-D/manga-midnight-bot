import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.environ.get("BOT_TOKEN")  # Your BotFather token in Render environment

# ================= Commands =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Manga Midnight bot is alive.")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong")

# ================= Post Buttons =================

# 5 buttons (2 rows + owner)
buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📢 Main Channel", url="https://t.me/Midnight_Panels"),
        InlineKeyboardButton("💬 Chat Group", url="https://t.me/Midnight_Panels_Chat")
    ],
    [
        InlineKeyboardButton("📝 Request Channel", url="https://t.me/+9Fy0jWSTMII5ZjM0"),
        InlineKeyboardButton("📚 Request Manga/Manhua", url="https://t.me/BoredKing_bot")
    ],
    [
        InlineKeyboardButton("👑 Owner", url="https://t.me/BoredKing_bot")
    ]
])

# Command to post banner + caption + buttons (manual posting)
async def post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("Please reply to the image you want to post with /post")
        return

    # Get the image file_id from the replied photo
    photo_file_id = update.message.reply_to_message.photo[-1].file_id

    # Send to main channel
    await context.bot.send_photo(
        chat_id="@Midnight_Panels",
        photo=photo_file_id,
        caption="✨ Welcome to Midnight Panels ✨\nChoose an option below 👇",
        reply_markup=buttons
    )
    await update.message.reply_text("✅ Banner posted with buttons!")

# ================= Handle Private Requests =================

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        # Forward request to owner
        owner_id = 8539205651  # Your numeric Telegram ID
        text = f"📬 New Request from @{update.message.from_user.username}:\n{update.message.text}"
        await context.bot.send_message(chat_id=owner_id, text=text)
        await update.message.reply_text("✅ Your request has been received! We will check it soon.")

# ================= Main =================

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Core commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("post", post))

    # Handle private messages as requests
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_request))

    app.run_polling()