"""
Management command to create a superuser with a pre-hashed password.

Used during automated provisioning when the update server has already
generated a password hash. This avoids exposing plaintext passwords
in commands or environment variables.

Usage:
    python manage.py createsuperuser_programmatic \
        --email merchant@example.com \
        --password-hash 'pbkdf2_sha256$...'

    # With custom username
    python manage.py createsuperuser_programmatic \
        --email merchant@example.com \
        --password-hash 'pbkdf2_sha256$...' \
        --username merchant
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser with a pre-hashed password (for automated provisioning)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            required=True,
            help="Email address for the superuser",
        )
        parser.add_argument(
            "--password-hash",
            required=True,
            help="Pre-computed password hash (e.g., pbkdf2_sha256$...)",
        )
        parser.add_argument(
            "--username",
            default="admin",
            help="Username for the superuser (default: admin)",
        )

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        email = options["email"]
        password_hash = options["password_hash"]
        username = options["username"]

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists, skipping.'))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email "{email}" already exists, skipping.')
            )
            return

        user = User(
            username=username,
            email=email,
            is_staff=True,
            is_superuser=True,
        )
        # Set pre-hashed password directly, bypassing set_password()
        user.password = password_hash
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Superuser "{username}" ({email}) created with pre-hashed password.'
            )
        )
