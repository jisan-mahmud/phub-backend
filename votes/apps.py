from django.apps import AppConfig


class VoteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'votes'

    def ready(self) -> None:
        from votes import signals
        super().ready()
