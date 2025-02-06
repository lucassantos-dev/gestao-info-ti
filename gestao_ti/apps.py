from django.apps import AppConfig


class GestaoTiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestao_ti'
    def ready(self):
        import gestao_ti.signals  