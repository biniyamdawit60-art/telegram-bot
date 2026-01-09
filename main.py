from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = 7924632947:AAFgcB6nGni1e4sRpOBzkOxOiv5gPngiRzg

taken_numbers = {}   # number -> username
user_numbers = {}    # username -> number

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text.strip()

    # ቁጥር ካልሆነ አትመልስ
    if not text.isdigit():
        return

    number = int(text)

    # 1–100 ብቻ
    if number < 1 or number > 100:
        return

    user = update.effective_user
    username = user.username if user.username else user.first_name

    # ሰውዬው ቀድሞ ቁጥር ይዞአል?
    if username in user_numbers:
        await update.message.reply_text(
            f"❌ {username} ቀድሞ {user_numbers[username]} ይዞአል"
        )
        return

    # ቁጥሩ ተይዟል?
    if number in taken_numbers:
        await update.message.reply_text(
            f"❌ ቁጥር {number} ተይዟል በ {taken_numbers[number]}"
        )
        return

    # መዝግብ
    taken_numbers[number] = username
    user_numbers[username] = number

    await update.message.reply_text(
        f"✅ {username} ቁጥር {number} በተሳካ ሁኔታ መዝግቧል"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
