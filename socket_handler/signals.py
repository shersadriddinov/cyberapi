from django.db.models.signals import post_save
from django.dispatch import receiver
from socket_handler.models import *
from socket_handler.utils import send_to_socket

import logging
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Server)
def create_new_server(sender, instance, created, **kwargs):
	"""
	Auto notify all players with new server created
	"""
	if created:
		send_to_socket(data={"action": "new_server"})
