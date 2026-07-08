"""
Management command to create test data for traffic source analytics
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from geoip.models import VisitorLocation


class Command(BaseCommand):
    help = 'Create test data for traffic source analytics (device types, UTM, referrers)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=200,
            help='Number of visitor records to create (default: 200)'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Spread data over this many days (default: 30)'
        )

    def handle(self, *args, **options):
        count = options['count']
        days = options['days']

        self.stdout.write(f'Creating {count} test visitor records over {days} days...\n')

        # Define test data patterns
        device_types = ['desktop', 'mobile', 'tablet', 'unknown']
        device_weights = [40, 45, 10, 5]  # Percentage distribution

        # Referrer domains
        referrers = [
            'https://www.google.com/search?q=ecommerce',
            'https://www.facebook.com/posts/12345',
            'https://twitter.com/status/67890',
            'https://www.instagram.com/p/abcde',
            'https://www.reddit.com/r/shopping/comments/xyz',
            'https://www.pinterest.com/pin/123456',
            'https://news.ycombinator.com/item?id=12345',
            'https://www.linkedin.com/feed/update/xyz',
            'https://techcrunch.com/article/new-ecommerce-platform',
            'https://www.producthunt.com/posts/amazing-shop',
            '',  # Direct traffic
        ]
        referrer_weights = [25, 15, 10, 8, 5, 5, 3, 3, 5, 6, 15]

        # UTM campaigns
        utm_campaigns = [
            {
                'source': 'google',
                'medium': 'cpc',
                'campaign': 'summer_sale_2025',
                'term': 'buy shoes online',
                'content': 'ad_variant_a'
            },
            {
                'source': 'facebook',
                'medium': 'social',
                'campaign': 'brand_awareness',
                'term': '',
                'content': 'carousel_ad'
            },
            {
                'source': 'newsletter',
                'medium': 'email',
                'campaign': 'weekly_deals',
                'term': '',
                'content': 'header_banner'
            },
            {
                'source': 'instagram',
                'medium': 'social',
                'campaign': 'influencer_collab',
                'term': '',
                'content': 'story_swipe_up'
            },
            {
                'source': 'google',
                'medium': 'organic',
                'campaign': '',
                'term': '',
                'content': ''
            },
            {
                'source': 'bing',
                'medium': 'cpc',
                'campaign': 'competitor_keywords',
                'term': 'best online shop',
                'content': 'text_ad_1'
            },
            {
                'source': 'youtube',
                'medium': 'video',
                'campaign': 'product_reviews',
                'term': '',
                'content': 'pre_roll_ad'
            },
            {
                'source': 'linkedin',
                'medium': 'social',
                'campaign': 'b2b_outreach',
                'term': '',
                'content': 'sponsored_content'
            },
            None,  # No UTM tracking
        ]

        # Countries for variety
        countries = [
            {'code': 'US', 'name': 'United States', 'city': 'New York'},
            {'code': 'GB', 'name': 'United Kingdom', 'city': 'London'},
            {'code': 'CA', 'name': 'Canada', 'city': 'Toronto'},
            {'code': 'DE', 'name': 'Germany', 'city': 'Berlin'},
            {'code': 'FR', 'name': 'France', 'city': 'Paris'},
            {'code': 'AU', 'name': 'Australia', 'city': 'Sydney'},
            {'code': 'JP', 'name': 'Japan', 'city': 'Tokyo'},
            {'code': 'BR', 'name': 'Brazil', 'city': 'São Paulo'},
        ]

        created_count = 0
        now = timezone.now()

        for i in range(count):
            # Random timestamp within the date range
            days_ago = random.randint(0, days)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            timestamp = now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)

            # Select device type
            device_type = random.choices(device_types, weights=device_weights)[0]

            # Select referrer
            referrer_url = random.choices(referrers, weights=referrer_weights)[0]

            # Select UTM campaign (30% chance of UTM tracking)
            utm_data = random.choice(utm_campaigns) if random.random() < 0.3 else None

            # Select country
            country = random.choice(countries)

            # Generate session key
            session_key = f'test_session_{i}_{random.randint(1000, 9999)}'

            # Generate IP address
            ip_address = f'192.168.{random.randint(1, 255)}.{random.randint(1, 255)}'

            # Random page views
            page_views = random.randint(1, 15)

            # Create visitor record
            visitor = VisitorLocation.objects.create(
                session_key=session_key,
                ip_address=ip_address,
                resolved_country=country['code'],
                resolved_region='',
                resolved_city=country['city'],
                device_type=device_type,
                referrer_url=referrer_url,
                utm_source=utm_data['source'] if utm_data else '',
                utm_medium=utm_data['medium'] if utm_data else '',
                utm_campaign=utm_data['campaign'] if utm_data else '',
                utm_term=utm_data['term'] if utm_data else '',
                utm_content=utm_data['content'] if utm_data else '',
                user_agent=self._generate_user_agent(device_type),
                page_views=page_views,
                first_seen=timestamp,
                last_seen=timestamp + timedelta(minutes=random.randint(1, 30))
            )

            created_count += 1

            if (created_count % 50) == 0:
                self.stdout.write(f'  Created {created_count}/{count} visitors...')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} test visitor records!'))
        self.stdout.write('\nData distribution:')
        self.stdout.write(f'  Desktop: ~{device_weights[0]}%')
        self.stdout.write(f'  Mobile: ~{device_weights[1]}%')
        self.stdout.write(f'  Tablet: ~{device_weights[2]}%')
        self.stdout.write(f'  With UTM tracking: ~30%')
        self.stdout.write(f'  With referrers: ~{100 - referrer_weights[-1]}%')
        self.stdout.write(f'  Direct traffic: ~{referrer_weights[-1]}%')

    def _generate_user_agent(self, device_type):
        """Generate a realistic user agent string based on device type"""
        user_agents = {
            'desktop': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            ],
            'mobile': [
                'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.164 Mobile Safari/537.36',
                'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
            ],
            'tablet': [
                'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Linux; Android 13; SM-X900) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            ],
            'unknown': [
                'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            ]
        }

        return random.choice(user_agents.get(device_type, user_agents['desktop']))
