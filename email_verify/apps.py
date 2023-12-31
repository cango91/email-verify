from django.apps import AppConfig


class EmailVerifyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'email_verify'
    def ready(self):
        import email_verify.signals