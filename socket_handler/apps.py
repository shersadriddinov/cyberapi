from django.apps import AppConfig


class SocketHandlerConfig(AppConfig):
    name = 'socket_handler'

    def ready(self):
        import socket_handler.signals
