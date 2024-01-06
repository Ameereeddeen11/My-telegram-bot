from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pprint import pprint
import os, json, datetime, requests

user_name = os.environ.get('USER_NAME')
token: str = os.environ.get('TOKEN')
API_KEY = os.environ.get('API_KEY')

with open('data.json', 'r') as f:
    data = json.load(f)

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!')

# Message handlers and responses
def message_handler(text: str) -> str:
    processed_text = text.lower()
    if 'hello' in processed_text:
        return 'Hello!'

    elif 'how are you?' in processed_text:
        return 'I am fine, thanks. How are you?'

    elif 'happy christmas' in processed_text:
        return 'Merry Christmas!'

    elif 'who has birthday today?' in processed_text:
        now = datetime.date.today()
        today = now.strftime('%d.%m')
        day_after = (now + datetime.timedelta(days=1)).strftime('%d.%m')
        date = data['date']
        for i in date:
            if i['birthday'] == today:
                return f'Today is birthday of: {i["name"]}'
            elif i['birthday'] == day_after:
                return f'Tomorrow will be birthday of: {i["name"]}'
            else:
                return 'Nobody has birthday today or tomorrow'
            
    elif 'who will have birthday near a day?' in processed_text:
        now = datetime.date.today()
        list_date = []

        for person in data['date']:
            # Extract month and day from the JSON data
            bday_month, bday_day = map(int, person['birthday'].split('.'))

            # Create a date object for the current year
            bday = datetime.date(now.year, bday_month, bday_day)

            # Check if birthday has passed for this year, if yes, calculate for next year
            if bday < now:
                bday = datetime.date(now.year + 1, bday_month, bday_day)

            list_date.append(bday)

        # Calculate the differences
        differences = [date - now for date in list_date]
        min_difference = min(differences)
        return f"The closest upcoming birthday is in {min_difference.days} days. {data['date'][differences.index(min_difference)]['name']}'s birthday"

    elif "what is the weather in" in processed_text:
        city = processed_text.split("in", 1)[1]
        url = "http://api.openweathermap.org/data/2.5/weather?appid="+API_KEY+"&q="+city+"&units=metric"
        response = requests.get(url).json()
        pprint(response)
        return f"The weather in {city} is {response['weather'][0]['description']}. The temperature is {response['main']['temp']}°C. The wind speed is {response['wind']['speed']} m/s."

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
