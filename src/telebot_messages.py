#!/usr/bin/python3
# -*- coding: utf-8 -*-
import telepot
from telepot.loop import MessageLoop
import os
import time
from FileManager import get_saved_info
from threading import currentThread
from emoji import emojize


def send_msg(text: str):
    print("\n\n========      Enviando mensaje      ========\n")
    print("cuerpo:\"" + text + "\"\n")

    try:
        # iniciamos el bot
        with open(os.path.join(os.path.expanduser("~"), "LambNN", "etc", "telegram_token.txt"), "r") as f:
            token = f.readline()[:-1]
        BOT = telepot.Bot(token)
        telegram_config = os.path.join(os.path.expanduser("~"), "LambNN", "etc", "telegram_ids.cfg")

        # obtenemos los IDs a los que vamos a enviar el mensaje y enviamos el mensaje a cada ID
        with open(telegram_config, "r") as f:
            for user_id in f:
                BOT.sendMessage(user_id, text)

        print("\n\n======== Mensaje enviado correctamente ========\n")

    except Exception as e:
        print(type(e))
        print(e)
        print("\n\n!!!!!!!!!!!!!!   Error al enviar el mensaje   !!!!!!!!!!!!!!\n")


def start_bot():
    t = currentThread()
    parent_folder = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

    with open(os.path.join(os.path.expanduser("~"), "LambNN", "etc", "telegram_token.txt"), "r") as f:
        my_token = f.readline()[:-1]
    my_bot = telepot.Bot(my_token)

    def on_chat_message(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        pass_file = open(os.path.join(parent_folder, "etc", "sys_pass.txt"), "r")
        sys_pass = pass_file.readline()
        print(sys_pass)
        pass_file.close()
        sudo = "echo \"" + sys_pass + "\" | sudo -S " # es importante que haya un espacio despues de -S
        if content_type == "text":
            text = msg["text"]
            if text == "/restart_nuc":
                my_bot.sendMessage(chat_id=chat_id, text="Restarting NUC...")
                os.system(sudo + "shutdown -r 0")

            elif text == "/start_ngrok":
                my_bot.sendMessage(chat_id=chat_id, text="Starting Ngrok service...")
                ret = os.system(sudo + "service server_ngrok start")
                if ret == 0:
                    my_bot.sendMessage(chat_id=chat_id, text=emojize(':thumbs_up:'))
                else:
                    my_bot.sendMessage(chat_id=chat_id, text='fail')

            elif text == "/stop_ngrok":
                my_bot.sendMessage(chat_id=chat_id, text="Stopping Ngrok service...")
                ret = os.system(sudo + "service server_ngrok stop")
                if ret == 0:
                    my_bot.sendMessage(chat_id=chat_id, text=emojize(':thumbs_up:'))
                else:
                    my_bot.sendMessage(chat_id=chat_id, text='fail')

            elif text == "/status":
                my_bot.sendMessage(chat_id=chat_id, text=str(get_saved_info()))

            elif "/" in text:
                my_bot.sendMessage(chat_id=chat_id, text="There's nothing to do here... ")
                
            else:
                my_bot.sendMessage(chat_id=chat_id, text="/restart_nuc\n/start_ngrok\n/stop_ngrok\n/status")



    MessageLoop(my_bot, {'chat': on_chat_message}).run_as_thread()
    print('Listening ...')

    while getattr(t, "do_run", True):
        time.sleep(10)
