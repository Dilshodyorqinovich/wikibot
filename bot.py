# python 3.11.4
# pip install wikipedia
# pip install python-telegram-bot 
from typing import Final
from telegram import _update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import wikipedia

wikipedia.set_lang("uz")
TOKEN: Final = "your token"
BOT_USERNAME: Final = "@wikiuzpedbot"

# commands


async def start_command(update: _update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('hello thanks for chatting')


async def help_command(update: _update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('pls type sth so i can respond')


async def custom_command(update: _update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('this is a custom command')

# response
def handle_response(text):
    # Implement this function to handle responses for group messages
    pass


async def handle_message(update: _update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str =update.message.text

    print(f"user ({update.message.chat.id}) in {message_type}:'({text})'")

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            try:
                response = wikipedia.summary(new_text)
            except wikipedia.exceptions.WikipediaException:
                response = 'No article found.'
            #response = handle_response(new_text)
        else:
            return
    else:
        try:
            response = wikipedia.summary(text)
        except wikipedia.exceptions.WikipediaException:
            response = 'No article found.'

    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: _update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused {context.error}")


if __name__ == "__main__":
    print('starting bot')
    app = Application.builder().token(TOKEN).build()
    # commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom',custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    # errors
    app.add_error_handler(error)
    print('polling...')
    app.run_polling(poll_interval=3)

