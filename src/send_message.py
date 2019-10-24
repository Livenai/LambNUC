#!/usr/bin/python3
# -*- coding: utf-8 -*-
import telepot
import os


def send_msg(text: str):
	print("\n\n========      Enviando mensaje      ========\n")
	print("cuerpo:\"" + text + "\"\n")

	try:
		# iniciamos el bot
		token = os.environ['telegram_token']
		BOT = telepot.Bot(token)
		telegram_config = os.path.join(os.path.expanduser("~"), "LambSM", "src", "telegram_ids.cfg")

		# obtenemos los IDs a los que vamos a enviar el mensaje y enviamos el mensaje a cada ID
		with open(telegram_config, "r") as f:
			for user_id in f:
				BOT.sendMessage(user_id, text)

		print("\n\n======== Mensaje enviado correctamente ========\n")

	except Exception as e:
		print(type(e))
		print(e)
		print("\n\n!!!!!!!!!!!!!!   Error al enviar el mensaje   !!!!!!!!!!!!!!\n")
