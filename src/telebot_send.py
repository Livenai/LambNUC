#!/usr/bin/python3
# -*- coding: utf-8 -*-                                                                                                                                                                                                                                                        import telepot
import telepot
from telepot.loop import MessageLoop
import os
from emoji import emojize

parent_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def send_msg(text: str):
    print("\n\n========      Enviando mensaje      ========\n")
    print("cuerpo:\"" + text + "\"\n")

    try:
        # iniciamos el bot
        with open(os.path.join(parent_folder, "etc", "telegram_token.txt"), "r") as f:
            token = f.readline()[:-1]
        bot = telepot.Bot(token)
        telegram_config = os.path.join(parent_folder, "etc", "telegram_ids.cfg")

        # obtenemos los IDs a los que vamos a enviar el mensaje y enviamos el mensaje a cada ID
        with open(telegram_config, "r") as f:
            for user_id in f:
                bot.sendMessage(user_id, emojize(text))

        print("\n\n======== Mensaje enviado correctamente ========\n")

    except Exception as e:
        print(type(e))
        print(e)
        print("\n\n!!!!!!!!!!!!!!   Error al enviar el mensaje   !!!!!!!!!!!!!!\n")
