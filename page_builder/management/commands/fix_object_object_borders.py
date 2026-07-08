"""
Management command to fix [object Object] stored in border fields
"""

from django.core.management.base import BaseCommand
from page_builder.models import Element
import json


class Command(BaseCommand):
    help = 'Fix elements with [object Object] stored in border field'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Scanning for [object Object] in border fields...'))

        # Find all elements with [object Object] in border field
        affected_elements = []

        for element in Element.objects.all():
            if element.content.get('border') == '[object Object]':
                affected_elements.append(element)

        if not affected_elements:
            self.stdout.write(self.style.SUCCESS('No elements found with [object Object] in border field'))
            return

        self.stdout.write(f'Found {len(affected_elements)} element(s) with [object Object] in border field')

        for element in affected_elements:
            self.stdout.write(f'\nElement ID: {element.id}')
            self.stdout.write(f'  Current border value: {element.content.get("border")}')

            # Clear the invalid border value
            element.content['border'] = ''
            element.save()

            self.stdout.write(self.style.SUCCESS(f'  ✓ Cleared border field for element {element.id}'))

        self.stdout.write(self.style.SUCCESS(f'\nFixed {len(affected_elements)} element(s)'))