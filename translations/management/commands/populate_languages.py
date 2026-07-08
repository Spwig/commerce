from django.core.management.base import BaseCommand
from django.db import transaction
from translations.models import SiteLanguage
import json


class Command(BaseCommand):
    help = 'Populate site languages with M2M100 and NLLB supported languages'

    # M2M100 language data
    M2M100_LANGUAGES = {
        'af': ('Afrikaans', 'Afrikaans', '🇿🇦', False),
        'am': ('Amharic', 'አማርኛ', '🇪🇹', False),
        'ar': ('Arabic', 'العربية', '🇸🇦', True),
        'ast': ('Asturian', 'Asturianu', '🇪🇸', False),
        'az': ('Azerbaijani', 'Azərbaycan', '🇦🇿', False),
        'ba': ('Bashkir', 'Башҡортса', '🇷🇺', False),
        'be': ('Belarusian', 'Беларуская', '🇧🇾', False),
        'bg': ('Bulgarian', 'Български', '🇧🇬', False),
        'bn': ('Bengali', 'বাংলা', '🇧🇩', False),
        'br': ('Breton', 'Brezhoneg', '🇫🇷', False),
        'bs': ('Bosnian', 'Bosanski', '🇧🇦', False),
        'ca': ('Catalan', 'Català', '🇦🇩', False),
        'ceb': ('Cebuano', 'Sinugboanong', '🇵🇭', False),
        'cs': ('Czech', 'Čeština', '🇨🇿', False),
        'cy': ('Welsh', 'Cymraeg', '🏴󐁧󐁢󐁷󐁬󐁳󐁿', False),
        'da': ('Danish', 'Dansk', '🇩🇰', False),
        'de': ('German', 'Deutsch', '🇩🇪', False),
        'el': ('Greek', 'Ελληνικά', '🇬🇷', False),
        'en': ('English', 'English', '🇬🇧', False),
        'es': ('Spanish', 'Español', '🇪🇸', False),
        'et': ('Estonian', 'Eesti', '🇪🇪', False),
        'fa': ('Persian', 'فارسی', '🇮🇷', True),
        'ff': ('Fulah', 'Fulfulde', '🇸🇳', False),
        'fi': ('Finnish', 'Suomi', '🇫🇮', False),
        'fr': ('French', 'Français', '🇫🇷', False),
        'fy': ('Western Frisian', 'Frysk', '🇳🇱', False),
        'ga': ('Irish', 'Gaeilge', '🇮🇪', False),
        'gd': ('Scottish Gaelic', 'Gàidhlig', '🏴󐁧󐁢󐁳󐁣󐁴󐁿', False),
        'gl': ('Galician', 'Galego', '🇪🇸', False),
        'gu': ('Gujarati', 'ગુજરાતી', '🇮🇳', False),
        'ha': ('Hausa', 'Hausa', '🇳🇬', False),
        'he': ('Hebrew', 'עברית', '🇮🇱', True),
        'hi': ('Hindi', 'हिन्दी', '🇮🇳', False),
        'hr': ('Croatian', 'Hrvatski', '🇭🇷', False),
        'ht': ('Haitian Creole', 'Kreyòl ayisyen', '🇭🇹', False),
        'hu': ('Hungarian', 'Magyar', '🇭🇺', False),
        'hy': ('Armenian', 'Հայերեն', '🇦🇲', False),
        'id': ('Indonesian', 'Bahasa Indonesia', '🇮🇩', False),
        'ig': ('Igbo', 'Igbo', '🇳🇬', False),
        'ilo': ('Iloko', 'Ilokano', '🇵🇭', False),
        'is': ('Icelandic', 'Íslenska', '🇮🇸', False),
        'it': ('Italian', 'Italiano', '🇮🇹', False),
        'ja': ('Japanese', '日本語', '🇯🇵', False),
        'jv': ('Javanese', 'Basa Jawa', '🇮🇩', False),
        'ka': ('Georgian', 'ქართული', '🇬🇪', False),
        'kk': ('Kazakh', 'Қазақ тілі', '🇰🇿', False),
        'km': ('Central Khmer', 'ភាសាខ្មែរ', '🇰🇭', False),
        'kn': ('Kannada', 'ಕನ್ನಡ', '🇮🇳', False),
        'ko': ('Korean', '한국어', '🇰🇷', False),
        'lb': ('Luxembourgish', 'Lëtzebuergesch', '🇱🇺', False),
        'lg': ('Ganda', 'Luganda', '🇺🇬', False),
        'ln': ('Lingala', 'Lingála', '🇨🇩', False),
        'lo': ('Lao', 'ລາວ', '🇱🇦', False),
        'lt': ('Lithuanian', 'Lietuvių', '🇱🇹', False),
        'lv': ('Latvian', 'Latviešu', '🇱🇻', False),
        'mg': ('Malagasy', 'Malagasy', '🇲🇬', False),
        'mk': ('Macedonian', 'Македонски', '🇲🇰', False),
        'ml': ('Malayalam', 'മലയാളം', '🇮🇳', False),
        'mn': ('Mongolian', 'Монгол', '🇲🇳', False),
        'mr': ('Marathi', 'मराठी', '🇮🇳', False),
        'ms': ('Malay', 'Bahasa Melayu', '🇲🇾', False),
        'my': ('Burmese', 'မြန်မာဘာသာ', '🇲🇲', False),
        'ne': ('Nepali', 'नेपाली', '🇳🇵', False),
        'nl': ('Dutch', 'Nederlands', '🇳🇱', False),
        'no': ('Norwegian', 'Norsk', '🇳🇴', False),
        'ns': ('Northern Sotho', 'Sesotho sa Leboa', '🇿🇦', False),
        'oc': ('Occitan', 'Occitan', '🇫🇷', False),
        'or': ('Odia', 'ଓଡ଼ିଆ', '🇮🇳', False),
        'pa': ('Punjabi', 'ਪੰਜਾਬੀ', '🇮🇳', False),
        'pl': ('Polish', 'Polski', '🇵🇱', False),
        'ps': ('Pashto', 'پښتو', '🇦🇫', True),
        'pt': ('Portuguese', 'Português', '🇵🇹', False),
        'ro': ('Romanian', 'Română', '🇷🇴', False),
        'ru': ('Russian', 'Русский', '🇷🇺', False),
        'sd': ('Sindhi', 'سنڌي', '🇵🇰', True),
        'si': ('Sinhala', 'සිංහල', '🇱🇰', False),
        'sk': ('Slovak', 'Slovenčina', '🇸🇰', False),
        'sl': ('Slovenian', 'Slovenščina', '🇸🇮', False),
        'so': ('Somali', 'Soomaali', '🇸🇴', False),
        'sq': ('Albanian', 'Shqip', '🇦🇱', False),
        'sr': ('Serbian', 'Српски', '🇷🇸', False),
        'ss': ('Swati', 'SiSwati', '🇸🇿', False),
        'su': ('Sundanese', 'Basa Sunda', '🇮🇩', False),
        'sv': ('Swedish', 'Svenska', '🇸🇪', False),
        'sw': ('Swahili', 'Kiswahili', '🇹🇿', False),
        'ta': ('Tamil', 'தமிழ்', '🇮🇳', False),
        'th': ('Thai', 'ไทย', '🇹🇭', False),
        'tl': ('Tagalog', 'Tagalog', '🇵🇭', False),
        'tn': ('Tswana', 'Setswana', '🇧🇼', False),
        'tr': ('Turkish', 'Türkçe', '🇹🇷', False),
        'uk': ('Ukrainian', 'Українська', '🇺🇦', False),
        'ur': ('Urdu', 'اردو', '🇵🇰', True),
        'uz': ('Uzbek', 'Oʻzbek', '🇺🇿', False),
        'vi': ('Vietnamese', 'Tiếng Việt', '🇻🇳', False),
        'wo': ('Wolof', 'Wolof', '🇸🇳', False),
        'xh': ('Xhosa', 'isiXhosa', '🇿🇦', False),
        'yi': ('Yiddish', 'ייִדיש', '🇮🇱', True),
        'yo': ('Yoruba', 'Yorùbá', '🇳🇬', False),
        'zh-hans': ('Simplified Chinese', '简体中文', '🇨🇳', False),
        'zh-hant': ('Traditional Chinese', '繁體中文', '🇹🇼', False),
        'zu': ('Zulu', 'isiZulu', '🇿🇦', False),
    }

    # Languages with limited support in M2M100 418M (better in 1.2B)
    LIMITED_M2M100 = {
        'ast', 'ba', 'br', 'ceb', 'ff', 'fy', 'gd', 'ha',
        'ig', 'ilo', 'lb', 'lg', 'ln', 'mg', 'ns', 'oc',
        'or', 'ps', 'sd', 'ss', 'su', 'sw', 'tl', 'tn',
        'wo', 'xh', 'yi', 'yo', 'zu'
    }

    # NLLB-only languages (not in M2M100)
    NLLB_ONLY = {
        'te': ('Telugu', 'తెలుగు', '🇮🇳', False),
        'gl_ES': ('Galician (Spain)', 'Galego (España)', '🇪🇸', False),
        'sl_SI': ('Slovene (Slovenia)', 'Slovenščina (Slovenija)', '🇸🇮', False),
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing languages before populating',
        )
        parser.add_argument(
            '--activate-common',
            action='store_true',
            help='Activate common languages (en, es, fr, de, zh, ja, ar)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Deleting existing languages...')
            SiteLanguage.objects.all().delete()

        created_count = 0
        updated_count = 0

        # Process M2M100 languages
        for code, (name, native_name, flag, rtl) in self.M2M100_LANGUAGES.items():
            # Determine support level
            if code in self.LIMITED_M2M100:
                m2m100_support = 'limited'
            else:
                m2m100_support = 'full'

            # All M2M100 languages have full NLLB support
            nllb_support = 'full'

            lang, created = SiteLanguage.objects.update_or_create(
                code=code,
                defaults={
                    'name': name,
                    'native_name': native_name,
                    'flag': flag,
                    'rtl': rtl,
                    'm2m100_support': m2m100_support,
                    'nllb_support': nllb_support,
                    'requires_nllb': False,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'Created: {name} ({code})')
            else:
                updated_count += 1
                self.stdout.write(f'Updated: {name} ({code})')

        # Process NLLB-only languages
        for code, (name, native_name, flag, rtl) in self.NLLB_ONLY.items():
            lang, created = SiteLanguage.objects.update_or_create(
                code=code,
                defaults={
                    'name': name,
                    'native_name': native_name,
                    'flag': flag,
                    'rtl': rtl,
                    'm2m100_support': 'none',
                    'nllb_support': 'full',
                    'requires_nllb': True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'Created (NLLB-only): {name} ({code})')
            else:
                updated_count += 1
                self.stdout.write(f'Updated (NLLB-only): {name} ({code})')

        # Activate common languages if requested
        if options['activate_common']:
            common_codes = ['en', 'es', 'fr', 'de', 'zh-hans', 'ja', 'ar', 'pt', 'ru', 'it']
            for i, code in enumerate(common_codes):
                try:
                    lang = SiteLanguage.objects.get(code=code)
                    lang.is_active = True
                    lang.order = i
                    if code == 'en':
                        lang.is_default = True
                    lang.save()
                    self.stdout.write(f'Activated: {lang.name}')
                except SiteLanguage.DoesNotExist:
                    self.stdout.write(f'Language not found: {code}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nComplete! Created {created_count} languages, updated {updated_count} languages.'
            )
        )

        # Display statistics
        total = SiteLanguage.objects.count()
        active = SiteLanguage.objects.filter(is_active=True).count()
        m2m100_full = SiteLanguage.objects.filter(m2m100_support='full').count()
        m2m100_limited = SiteLanguage.objects.filter(m2m100_support='limited').count()
        nllb_only = SiteLanguage.objects.filter(requires_nllb=True).count()

        self.stdout.write(f'\nStatistics:')
        self.stdout.write(f'  Total languages: {total}')
        self.stdout.write(f'  Active languages: {active}')
        self.stdout.write(f'  M2M100 full support: {m2m100_full}')
        self.stdout.write(f'  M2M100 limited support: {m2m100_limited}')
        self.stdout.write(f'  NLLB-only languages: {nllb_only}')