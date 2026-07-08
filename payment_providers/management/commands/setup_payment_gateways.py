from django.core.management.base import BaseCommand
from payment_providers.models import PaymentGateway


class Command(BaseCommand):
    help = 'Setup default payment gateways for demonstration'

    def handle(self, *args, **options):
        """Create sample payment gateways"""
        
        # Stripe (Test Mode)
        stripe_gateway, created = PaymentGateway.objects.get_or_create(
            name='stripe',
            defaults={
                'display_name': 'Credit/Debit Cards (Stripe)',
                'is_active': False,  # Initially inactive until configured
                'environment': 'sandbox',
                'description': 'Accept all major credit and debit cards securely',
                'sort_order': 1,
                'supports_recurring': True,
                'supports_refunds': True,
                'supports_partial_refunds': True,
                'configuration': {
                    'publishable_key': 'pk_test_...',
                    'secret_key': 'sk_test_...',
                    'webhook_secret': 'whsec_...'
                }
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✓ Created Stripe payment gateway')
            )
        else:
            self.stdout.write(
                self.style.WARNING('! Stripe gateway already exists')
            )
        
        # PayPal (Test Mode)
        paypal_gateway, created = PaymentGateway.objects.get_or_create(
            name='paypal',
            defaults={
                'display_name': 'PayPal',
                'is_active': False,  # Initially inactive until configured
                'environment': 'sandbox',
                'description': 'Pay with PayPal account or credit card through PayPal',
                'sort_order': 2,
                'supports_recurring': True,
                'supports_refunds': True,
                'supports_partial_refunds': True,
                'configuration': {
                    'client_id': 'your_paypal_client_id',
                    'client_secret': 'your_paypal_client_secret',
                    'webhook_id': 'your_webhook_id'
                }
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✓ Created PayPal payment gateway')
            )
        else:
            self.stdout.write(
                self.style.WARNING('! PayPal gateway already exists')
            )
        
        # Square (Test Mode)
        square_gateway, created = PaymentGateway.objects.get_or_create(
            name='square',
            defaults={
                'display_name': 'Square',
                'is_active': False,
                'environment': 'sandbox',
                'description': 'Accept payments through Square payment processing',
                'sort_order': 3,
                'supports_recurring': False,
                'supports_refunds': True,
                'supports_partial_refunds': True,
                'configuration': {
                    'application_id': 'your_square_application_id',
                    'access_token': 'your_square_access_token',
                    'location_id': 'your_location_id'
                }
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('✓ Created Square payment gateway')
            )
        else:
            self.stdout.write(
                self.style.WARNING('! Square gateway already exists')
            )
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS('🎉 Payment gateway setup complete!')
        )
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Go to Admin → Site Settings to see payment methods status')
        self.stdout.write('2. Click "Manage Gateways" to configure your API credentials')
        self.stdout.write('3. Set gateways to "active" once properly configured')
        self.stdout.write('4. Test transactions using the admin interface')
        
        # Display summary
        total_gateways = PaymentGateway.objects.count()
        active_gateways = PaymentGateway.objects.filter(is_active=True).count()
        
        self.stdout.write(f'\n📊 Current Status:')
        self.stdout.write(f'   Total gateways: {total_gateways}')
        self.stdout.write(f'   Active gateways: {active_gateways}')
        self.stdout.write(f'   Ready for configuration: {total_gateways - active_gateways}')