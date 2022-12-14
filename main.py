from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from pytube import YouTube
import os

app = ApplicationBuilder().token("5734822065:AAEzl4vtqT7NvENRIut48dQ13ygBmAkNV3k").build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    file = YouTube(text).streams.get_lowest_resolution().download()

    chat_id = update.message.chat_id

    await context.bot.send_video(chat_id=chat_id, video=open(file, 'rb'), supports_streaming=True)

    os.remove(file)


app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

app.run_polling()
