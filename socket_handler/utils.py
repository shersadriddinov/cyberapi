import os
import json
from websocket import create_connection
from dotenv import load_dotenv
from cyberAPI.settings import dotenv_path

load_dotenv(dotenv_path)


def send_to_socket(data, host=os.environ.get("SOCKET_HOST"), port=os.environ.get("SOCKET_PORT")):
	"""
	Function to make connection to web socket and send data via json

	:param data - python dictionary to send converting to json
	:param host - ip address of websocket, by default specified in environmental vars
	:param port - ip address port of websocket, by default specified in environmental vars
	:return True on succeed, or exception
	"""

	url = "ws://" + host + ":" + port + "/lobby"
	try:
		ws = create_connection(url)
	except:
		return "web socket connection error, tried url: " + url
	else:
		ws.send(json.dumps(data))
		ws.close()
		return True
