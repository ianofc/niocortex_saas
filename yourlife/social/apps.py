from django.apps import AppConfig

class YourlifeSocialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'yourlife.social'
    label = 'yourlife_social'  # Label único para evitar conflitos
