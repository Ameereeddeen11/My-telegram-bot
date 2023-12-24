from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

user_name = os.environ.get('USER_NAME')
token: str = os.environ.get('TOKEN')

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!')

'''async def costom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!')'''

# Message handlers and responses
def message_handler(text: str) -> str:
    processed_text = text.lower()
    if 'hello' in processed_text:
        return 'Hello!'

    elif 'how are you?' in processed_text:
        return 'I am fine, thanks. How are you?'

    elif 'happy christmas' in processed_text:
        return 'Merry Christmas!'

    return 'Sorry, I do not understand you!'

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type # type of chat: private, group, supergroup, channel
    text: str = update.message.text # text of message

    print(f'User ({update.message.chat.id}) in {message_type}: {text}')

    if message_type == 'group':
        if user_name in text:
            new_text = text.replace(user_name, '').strip()
            response = message_handler(new_text)
        else:
            return
    else:
        response: str = message_handler(text)

    print(f'Bot: {response}')
    await update.message.reply_text(response)

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Main function
if __name__ == '__main__':
    print('Starting bot')
    app = Application.builder().token(token).build()

    # Command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    #app.add_handler(CommandHandler('costom', costom_command))

    # Message handlers
    app.add_handler(MessageHandler(filters.TEXT, handle_user_message))

    # Error handler
    app.add_error_handler(error_handler)

    app.run_polling(poll_interval=5)