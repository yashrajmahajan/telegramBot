import pytz
import telegram
from datetime import datetime
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from faunadb import query as q
from faunadb.objects import Ref
import re
import logging
from faunadb.client import FaunaClient
from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup

telegram_bot_token = "token is private"
fauna_secret = "Key is private"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher
client = FaunaClient(secret=fauna_secret)

def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id, text="Welcome to vaccine slot registration. 😊\n\nHere are a few commands to guide you\n/name - start booking\n/show - list a booked slots")


def name(update, context):
    chat_id = update.effective_chat.id

    context.bot.send_message(
        chat_id=chat_id, text="Enter your name, sent it and click here /location")

def location(update, context):
    chat_id = update.effective_chat.id
    name = update.message.text
    
    result = client.query(q.insert(
    q.ref(q.collection("users"), "1"),
    ts=1,
    action="create",
    params={
      "data": {
        "name": name,
        
        }}))

    context.bot.send_message(
        chat_id=chat_id, text="Enter city and click here /date")

def date(update, context):
    chat_id = update.effective_chat.id
    location = update.message.text

    result = client.query(q.insert(
    q.ref(q.collection("users"), "1"),
    ts=1,
    action="create",
    params={
      "data": {
        "location": location,
        
        }}))

    presentday = datetime.now()
    thirdday = presentday + timedelta(1)
    thirdday = thirdday + timedelta(1)
    tomorrow = presentday + timedelta(1)

    
    keyboard = [[presentday.strftime('%d-%m-%Y')], [tomorrow.strftime('%d-%m-%Y')], [thirdday.strftime('%d-%m-%Y')]]

    #reply_markup = InlineKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    menu_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)



    #update.message.reply_text('Please choose date and click here /time:', reply_markup=reply_markup)
    context.bot.send_message(
        chat_id=chat_id, text="Please choose date and click here /time:", reply_markup=menu_markup)

def time(update, context):
    chat_id = update.effective_chat.id

    date = update.message.text

    result = client.query(q.insert(
    q.ref(q.collection("users"), "1"),
    ts=1,
    action="create",
    params={
      "data": {
        "date": date,
        
        }}))

    menu_keyboard = [['morning, 10AM-12PM'], ['afternoon,12PM-2PM'], ['evening,4PM-6PM']]
    menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
    #bot.send_message(chat_id=chat_id, text='choose option:', reply_markup=menu_markup)

    context.bot.send_message(
        chat_id=chat_id, text="choose time and click on /submit", reply_markup=menu_markup)

def show(update, context):
    chat_id = update.effective_chat.id

    result = 'Currently this feature is not working contact: @yashrajmahajan' #client.query(q.get(q.match(q.index("users"),"1")))
    context.bot.send_message(chat_id=chat_id, text=result)

def submit(update, context):
    chat_id = update.effective_chat.id
    time = update.message.text

    result = client.query(q.insert(
    q.ref(q.collection("users"), "1"),
    ts=1,
    action="create",
    params={
      "data": {
        "time": time,
        
        }}))

    '''client.query(q.update(q.ref(q.collection("users"), user["ref"].id()), {
                     "data": {"last_command": ""}}))'''
    context.bot.send_message(
            chat_id=chat_id, text="Successfully added slot. 👍\n\nSee your date and time /show")


dispatcher.add_handler(CommandHandler("Book", start))
dispatcher.add_handler(CommandHandler("name", name))
dispatcher.add_handler(CommandHandler("location", location))
dispatcher.add_handler(CommandHandler("date", date))
dispatcher.add_handler(CommandHandler("time", time))
dispatcher.add_handler(CommandHandler("submit", submit))
dispatcher.add_handler(CommandHandler("show", show))

#dispatcher.add_handler(MessageHandler(Filters.text, show))

updater.start_polling()
