from core.management.commands._seed_base import SeedCommand


class Command(SeedCommand):
    seed_name = 'carrier_presets'
    seed_version = 1
    help = 'Seed shipping carrier presets from presets.py (200 global carriers)'

    def seed(self) -> int:
        from shipping.carriers.presets import CARRIER_PRESETS
        from shipping.models import CarrierPreset

        count = 0
        for preset_data in CARRIER_PRESETS:
            _, created = CarrierPreset.objects.get_or_create(
                slug=preset_data['slug'],
                defaults={
                    'name': preset_data['name'],
                    'country_of_operation': preset_data.get('country_of_operation', ''),
                    'tracking_url_template': preset_data.get('tracking_url_template', ''),
                    'description': str(preset_data.get('description', '')),
                    'is_system': preset_data.get('is_system', True),
                    'is_active': False,  # Opt-in: merchants activate carriers they use
                },
            )
            if created:
                count += 1
        return count
