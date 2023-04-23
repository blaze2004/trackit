from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        superAdminUserName = os.environ.get("ADMIN_USERNAME")
        if not User.objects.filter(username=superAdminUserName).exists():
            User.objects.create_superuser(superAdminUserName, os.environ.get(
                'ADMIN_EMAIL'), os.environ.get('ADMIN_PSD'))
