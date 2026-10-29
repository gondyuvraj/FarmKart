from django.apps import AppConfig

class AdminPanelConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'admin_panel'
    verbose_name = 'FarmKart Admin Control Center'
