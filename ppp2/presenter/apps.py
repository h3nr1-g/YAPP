from django.apps import AppConfig


class PresenterConfig(AppConfig):
    name = 'presenter'

    def ready(self):
        import presenter.signals
