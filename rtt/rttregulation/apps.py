from django.apps import AppConfig


class RttregulationConfig(AppConfig):
    name = 'rttregulation'

    def ready(self):
        import rttregulation.signals
