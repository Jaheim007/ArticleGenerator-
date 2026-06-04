import os
from dotenv import load_dotenv
from openai import OpenAI

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Send me a topic and I will generate a complete article for you.\n\n"
        "Example:\n"
        "The importance of cybersecurity for small businesses"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 How to use this bot:\n\n"
        "1. Send me any article topic.\n"
        "2. I will generate a structured article.\n"
        "3. You can ask for another topic anytime.\n\n"
        "Example:\n"
        "Write an article about AI in education"
    )


def generate_article(topic: str) -> str:
    prompt = f"""
You are a professional article writer.

Write a complete, clear, and well-structured article about:

"{topic}"

The article must include:
- A strong title
- An introduction
- 4 to 6 main sections with headings
- Practical examples
- A conclusion
- A professional but simple tone

Make the article useful for beginners.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text

    await update.message.reply_text("✍️ Generating your article...")

    try:
        article = generate_article(topic)

        # Telegram has message length limits, so we split long articles
        max_length = 3500

        for i in range(0, len(article), max_length):
            await update.message.reply_text(article[i:i + max_length])

    except Exception as e:
        await update.message.reply_text(
            "❌ Sorry, something went wrong while generating the article.\n\n"
            f"Error: {str(e)}"
        )


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN in .env file")

    if not OPENAI_API_KEY:
        raise ValueError("Missing OPENAI_API_KEY in .env file")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()