import logging
from telegram import Update, ForceReply, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Turn on simple logging (helps when debugging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
 
 
MENU_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Check status"), KeyboardButton("Pay bill")],
        [KeyboardButton("Help")]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Choose an option from the menu:",
        reply_markup=MENU_KEYBOARD
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "Check status":
        await update.message.reply_text("You chose: Check status")
    elif text == "Pay bill":
        await update.message.reply_text("You chose: Pay bill")
    elif text == "Help":
        await update.message.reply_text("You chose: Help")
    else:
        await update.message.reply_text(f"You said: {text}")


# /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Send me any message and I will echo it back.")

 


def main() -> None:
    # 1) Put your BotFather token here
    application = Application.builder().token("8435658423:AAFljuvwGtqJmtUChyQVsLm3pwVlsdakCsQ").build()

    # 2) Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # 3) Start polling (press Ctrl+C in terminal to stop)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
