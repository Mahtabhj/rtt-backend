from django.apps import AppConfig


class RttnewsConfig(AppConfig):
    name = 'rttnews'

    def ready(self):
        import rttnews.signals
