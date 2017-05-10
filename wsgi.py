#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import telebot
import config
import logging, sys
import logging.config

logging.basicConfig(stream=sys.stderr)
logging.config.fileConfig('/opt/gibot/etc/logging_config.ini')
logger = logging.getLogger('wsgi')


bot = telebot.TeleBot(config.token,threaded=False)

def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    # logger.info('test info message')
    # When the method is POST the variable will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ['wsgi.input'].read(request_body_size).decode("utf-8")
    # logger.info(request_body)
    update = telebot.types.Update.de_json(request_body)
    # bot.reply_to(update.message, 'sdf')
    # logger.info(update)
    bot.process_new_messages([update.message])
    

    start_response('200 OK', [('Content-Type', 'text/html')])
    return ''


@bot.message_handler(commands=['help', 'start'])
def echo_message(message):
#     # logger.info(message.text)
    bot.send_message(message.chat.id, 'старт или хелп')

    
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
#     # logger.info(message.text)
    bot.send_message(message.chat.id, 'ыва')



