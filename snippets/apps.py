from django.apps import AppConfig


class SnippetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'snippets'
    def ready(self) -> None:
        from . import signals
        return super().ready()