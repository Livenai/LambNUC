#!/usr/bin/python3
# -*- coding: utf-8 -*-
import telepot
from telepot.loop import MessageLoop
import os
import time
from FileManager import get_saved_info


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


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        text = msg["text"]
        if text == "/status":
            my_bot.sendMessage(chat_id=chat_id, text=str(get_saved_info()))
        elif "/" in text:
            my_bot.sendMessage(chat_id=chat_id, text="There's nothing to do here... ")


if __name__ == '__main__':
    with open(os.path.join(os.path.expanduser("~"), "LambNN", "etc", "telegram_token.txt"), "r") as f:
        my_token = f.readline()[:-1]
    my_bot = telepot.Bot(my_token)

    MessageLoop(my_bot, {'chat': on_chat_message}).run_as_thread()
    print('Listening ...')

    while 1:
        time.sleep(10)
