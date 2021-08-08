'''"COVID-19 Vaccination Camp Registration Telegram Bot"

I was try to develop this code from various ways such as
1. message passing.
2. only work through the CommandHandlers.
3. develop from existing main bots.
4. MessageHandler as well as CommandHandler used.

I also tried the 4 databases here:
1. SQL, 2.SQlite 3.MongoDB 4.Fauna DB (Serverless)
'''
import logging
import re
from telegram.ext import *
from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
import telegram

API_KEY = '1946266244:AAEifSpYvkVUQPzHFjK4wQQqdBm0gAvaEP8'

# Set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Start Bot')
logger = logging.getLogger(__name__)

def start_command(update, context):
    update.message.reply_text('Welcome to registration for largest Vaccination Camp. \n\nPlease provide your following details to book your free slot. \n\nType your as ("name, YOUR NAME")')

def help_command(update, context):
    update.message.reply_text('Contact developer @yashrajmahajan')

def process_message(message, response_array, response):
    # Splits the message and the punctuation into an array
    list_message = re.findall(r"[\w']+|[.,!?;]", message.lower())

    # Scores the amount of words in the message
    score = 0
    for word in list_message:
        if word in response_array:
            score = score + 1

    # Returns the response and the score of the response
    # print(score, response)
    return [score, response]

def dates(update: Update, context: CallbackContext) -> None:

    presentday = datetime.now()
    thirdday = presentday + timedelta(1)
    thirdday = thirdday + timedelta(1)
    tomorrow = presentday + timedelta(1)

    keyboard = [
        [
            InlineKeyboardButton(presentday.strftime('%d-%m-%Y'), callback_data= presentday.strftime('%d-%m-%Y')),
            InlineKeyboardButton(tomorrow.strftime('%d-%m-%Y'), callback_data= tomorrow.strftime('%d-%m-%Y')),
        ],
        [InlineKeyboardButton(thirdday.strftime('%d-%m-%Y'), callback_data= thirdday.strftime('%d-%m-%Y'))],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose date:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query1 = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query1.answer()

    query1.edit_message_text(text=f'Selected option: {query1.data} \n\nplease type your age (e.g. age, 21)')
    button.var = query1.data

def times(update, context):
    bot = telegram.Bot(API_KEY)
    chat_id = update.effective_chat.id
    menu_keyboard = [['morning, 10AM-12PM'], ['afternoon,12PM-2PM'], ['evening,4PM-6PM']]
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
    bot.send_message(chat_id=chat_id, text='choose option:', reply_markup=menu_markup)

def get_response(message):
    # Add your custom responses here
     
    response_list = [
        process_message(message, ['name'], 'Enter your Location (e.g. location, pune)'),
        process_message(message, ['location'], 'Click on "/date" for date selection.'),
        process_message(message, ['age'], 'Click on "/time" for date selection.'),
        process_message(message, ['morning', 'afternoon', 'evening'], 'thanks for your registration. Click here "/show" for your details.')
    ]
    

    # Checks all of the response scores and returns the best matching response
    response_scores = []
    for response in response_list:
        response_scores.append(response[0])

    # Get the max value for the best response and store it into a variable
    winning_response = max(response_scores)
    matching_response = response_list[response_scores.index(winning_response)]

    # Return the matching response to the user
    if winning_response == 0:
        bot_response = 'I didn\'t understand what you wrote. please follow above instructions.'
    else:
        bot_response = matching_response[1]

    print('Bot response:', bot_response)
    return bot_response

def handle_message(update, context):
    text = str(update.message.text).lower()
    logging.info(f'User ({update.message.chat.id}) says: {text}')

    # Bot response
    response = get_response(text)
    update.message.reply_text(response)
    handle_message.var = text

def show(update, context):
    update.message.reply_text('your date and time',handle_message.var, button.var)

def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')


def main() -> None:
    updater = Updater(API_KEY, use_context=True)
    bot = telegram.Bot(API_KEY)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('show', show))

    dp.add_handler(CommandHandler('date', dates))
    dp.add_handler(CallbackQueryHandler(button))

    dp.add_handler(CommandHandler('time', times))
    #dp.add_handler(CallbackQueryHandler(button2))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()




# Run the programme
if __name__ == '__main__':
    main()