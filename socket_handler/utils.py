import os
from websocket import create_connection
from dotenv import load_dotenv
from cyberAPI.settings import dotenv_path

load_dotenv(dotenv_path)


def send_to_socket(data, host=os.environ.get("SOCKET_HOST"), port=os.environ.get("SOCKET_PORT")):
	"""
	#TODO: write clear docs
	"""

	url = host + ":" + port
	try:
		ws = create_connection(url)
	except:
		return "web socket connection error, tried url: " + url
	else:
		ws.send(data)
		ws.close()
		return True
