#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import telebot
import cherrypy
import config

WEBHOOK_HOST = '127.0.0.1'
WEBHOOK_PORT = 5000
WEBHOOK_LISTEN = '127.0.0.1'

# WEBHOOK_SSL_CERT = '/etc/nginx/ssl/ickd.ru/ssl-bundle.crt'  
# WEBHOOK_SSL_PRIV = '/etc/nginx/ssl/ickd.ru/ickd_ru.key'

WEBHOOK_URL_BASE = "http://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

bot = telebot.TeleBot(config.token)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            length = int(cherrypy.request.headers['content-length'])
            print(cherrypy.request.body.read(length))
            raise cherrypy.HTTPError(403)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
	print(message)
	bot.reply_to(message, message.text)

# bot.remove_webhook()

# bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,certificate=open(WEBHOOK_SSL_CERT, 'r'))


cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin'#,
    # 'server.ssl_certificate': WEBHOOK_SSL_CERT,
    # 'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

