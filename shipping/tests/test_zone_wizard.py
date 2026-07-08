"""
Tests for Zone Wizard views
"""

import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from shipping.models import ShippingZone


User = get_user_model()


class ZoneWizardStep1Test(TestCase):
    """Test Zone Wizard Step 1 - Basic Information"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            is_staff=True,
        )
        self.client.login(username='admin', password='testpass123')
        self.url = reverse('shipping:zone_wizard_step1')

    def test_step1_get_requires_staff(self):
        """Test step 1 requires staff login"""
        self.client.logout()
        response = self.client.get(self.url)

        # Should redirect to admin login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_step1_get_renders_template(self):
        """Test step 1 GET renders correct template"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/shipping/zone_wizard/step1_basic.html')

    def test_step1_post_saves_to_session(self):
        """Test step 1 POST saves data to session"""
        data = {
            'name': 'Test Zone',
            'description': 'Test description',
            'priority': '5',
            'is_active': 'on',
        }

        response = self.client.post(self.url, data)

        # Should redirect to step 2
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/zone-wizard/step2/'))

        # Check session data
        session = self.client.session
        self.assertIn('zone_wizard_data', session)
        wizard_data = session['zone_wizard_data']

        self.assertEqual(wizard_data['name'], 'Test Zone')
        self.assertEqual(wizard_data['description'], 'Test description')
        self.assertEqual(wizard_data['priority'], 5)
        self.assertTrue(wizard_data['is_active'])

    def test_step1_post_inactive_checkbox(self):
        """Test step 1 POST with inactive checkbox (unchecked)"""
        data = {
            'name': 'Inactive Zone',
            'priority': '10',
        }

        response = self.client.post(self.url, data)

        session = self.client.session
        wizard_data = session['zone_wizard_data']

        self.assertFalse(wizard_data['is_active'])

    def test_step1_post_default_priority(self):
        """Test step 1 POST with default priority"""
        data = {
            'name': 'Default Priority Zone',
            'is_active': 'on',
        }

        response = self.client.post(self.url, data)

        session = self.client.session
        wizard_data = session['zone_wizard_data']

        self.assertEqual(wizard_data['priority'], 0)


class ZoneWizardStep2Test(TestCase):
    """Test Zone Wizard Step 2 - Geographic Coverage"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            is_staff=True,
        )
        self.client.login(username='admin', password='testpass123')
        self.url = reverse('shipping:zone_wizard_step2')

        # Set up session with step 1 data
        session = self.client.session
        session['zone_wizard_data'] = {
            'name': 'Test Zone',
            'description': '',
            'priority': 0,
            'is_active': True,
        }
        session.save()

    def test_step2_get_requires_staff(self):
        """Test step 2 requires staff login"""
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_step2_get_renders_template(self):
        """Test step 2 GET renders correct template"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/shipping/zone_wizard/step2_coverage.html')

    def test_step2_get_displays_step1_data(self):
        """Test step 2 GET displays data from step 1"""
        response = self.client.get(self.url)

        self.assertIn('zone_data', response.context)
        zone_data = response.context['zone_data']

        self.assertEqual(zone_data['name'], 'Test Zone')

    def test_step2_post_with_countries(self):
        """Test step 2 POST with country codes"""
        data = {
            'countries': 'US, CA, MX',
            'states': '',
            'postal_patterns': '',
        }

        response = self.client.post(self.url, data)

        # Should redirect to step 3
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.endswith('/zone-wizard/step3/'))

        # Check session data
        session = self.client.session
        wizard_data = session['zone_wizard_data']

        self.assertEqual(wizard_data['countries'], ['US', 'CA', 'MX'])
        self.assertEqual(wizard_data['states'], {})
        self.assertEqual(wizard_data['postal_code_patterns'], [])

    def test_step2_post_with_states_json(self):
        """Test step 2 POST with states JSON"""
        states_json = json.dumps({
            'US': ['CA', 'OR', 'WA'],
            'CA': ['BC', 'ON']
        })

        data = {
            'countries': 'US, CA',
            'states': states_json,
            'postal_patterns': '',
        }

        response = self.client.post(self.url, data)

        session = self.client.session
        wizard_data = session['zone_wizard_data']

        self.assertEqual(wizard_data['states']['US'], ['CA', 'OR', 'WA'])
        self.assertEqual(wizard_data['states']['CA'], ['BC', 'ON'])

    def test_step2_post_with_postal_patterns(self):
        """Test step 2 POST with postal code patterns"""
        data = {
            'countries': 'US',
            'states': '',
            'postal_patterns': r'^10\d{3}$, ^11\d{3}$',
        }

        response = self.client.post(self.url, data)

        session = self.client.session
        wizard_data = session['zone_wizard_data']

        self.assertEqual(len(wizard_data['postal_code_patterns']), 2)
        self.assertIn(r'^10\d{3}$', wizard_data['postal_code_patterns'])
        self.assertIn(r'^11\d{3}$', wizard_data['postal_code_patterns'])

    def test_step2_post_empty_coverage(self):
        """Test step 2 POST with no coverage restrictions"""
        data = {
            'countries': '',
            'states': '',
            'postal_patterns': '',
        }

        response = self.client.post(self.url, data)

        session = self.client.session
        wizard_data = session['zone_wizard_data']

        self.assertEqual(wizard_data['countries'], [])
        self.assertEqual(wizard_data['states'], {})
        self.assertEqual(wizard_data['postal_code_patterns'], [])

    def test_step2_post_invalid_json(self):
        """Test step 2 POST with invalid JSON in states field"""
        data = {
            'countries': 'US',
            'states': '{invalid json',
            'postal_patterns': '',
        }

        response = self.client.post(self.url, data)

        # Invalid JSON will be caught and session will have empty dict
        self.assertEqual(response.status_code, 302)
        # Note: Current implementation doesn't validate JSON on POST, moves to step 3

    def test_step2_post_normalizes_country_codes(self):
        """Test step 2 POST normalizes country codes to uppercase"""
        data = {
            'countries': 'us, ca, gb',
            'states': '',
            'postal_patterns': '',
        }

        response = self.client.post(self.url, data)

        session = self.client.session
        wizard_data = session['zone_wizard_data']

        self.assertEqual(wizard_data['countries'], ['US', 'CA', 'GB'])

    def test_step2_post_handles_whitespace(self):
        """Test step 2 POST handles whitespace in inputs"""
        data = {
            'countries': '  US ,  CA  , MX  ',
            'states': '',
            'postal_patterns': '  ^10\\d{3}$  ,  ^11\\d{3}$  ',
        }

        response = self.client.post(self.url, data)

        session = self.client.session
        wizard_data = session['zone_wizard_data']

        # Should trim whitespace
        self.assertEqual(wizard_data['countries'], ['US', 'CA', 'MX'])
        self.assertIn(r'^10\d{3}$', wizard_data['postal_code_patterns'])


class ZoneWizardStep3Test(TestCase):
    """Test Zone Wizard Step 3 - Review & Create"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            is_staff=True,
        )
        self.client.login(username='admin', password='testpass123')
        self.url = reverse('shipping:zone_wizard_step3')

        # Set up complete session data
        session = self.client.session
        session['zone_wizard_data'] = {
            'name': 'Complete Test Zone',
            'description': 'Test description',
            'priority': 10,
            'is_active': True,
            'countries': ['US', 'CA'],
            'states': {'US': ['CA', 'NY']},
            'postal_code_patterns': [r'^9\d{4}$'],
        }
        session.save()

    def test_step3_get_requires_staff(self):
        """Test step 3 requires staff login"""
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_step3_get_renders_template(self):
        """Test step 3 GET renders correct template"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/shipping/zone_wizard/step3_review.html')

    def test_step3_get_displays_all_data(self):
        """Test step 3 GET displays all wizard data"""
        response = self.client.get(self.url)

        self.assertIn('zone_data', response.context)
        zone_data = response.context['zone_data']

        self.assertEqual(zone_data['name'], 'Complete Test Zone')
        self.assertEqual(zone_data['description'], 'Test description')
        self.assertEqual(zone_data['priority'], 10)
        self.assertTrue(zone_data['is_active'])
        self.assertEqual(zone_data['countries'], ['US', 'CA'])
        self.assertEqual(zone_data['states'], {'US': ['CA', 'NY']})
        self.assertEqual(zone_data['postal_code_patterns'], [r'^9\d{4}$'])

    def test_step3_post_creates_zone(self):
        """Test step 3 POST creates shipping zone"""
        initial_count = ShippingZone.objects.count()

        response = self.client.post(self.url)

        # Should create zone and redirect to changelist
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/admin/shipping/shippingzone/' in response.url)

        # Check zone was created
        self.assertEqual(ShippingZone.objects.count(), initial_count + 1)

        zone = ShippingZone.objects.latest('created_at')
        self.assertEqual(zone.name, 'Complete Test Zone')
        self.assertEqual(zone.description, 'Test description')
        self.assertEqual(zone.priority, 10)
        self.assertTrue(zone.is_active)
        self.assertEqual(zone.countries, ['US', 'CA'])
        self.assertEqual(zone.states, {'US': ['CA', 'NY']})
        self.assertEqual(zone.postal_code_patterns, [r'^9\d{4}$'])
        self.assertEqual(zone.created_by, self.user)

    def test_step3_post_clears_session(self):
        """Test step 3 POST clears wizard session data"""
        response = self.client.post(self.url)

        # Session should be cleared
        session = self.client.session
        self.assertNotIn('zone_wizard_data', session)

    def test_step3_post_minimal_zone(self):
        """Test step 3 POST creates minimal zone"""
        session = self.client.session
        session['zone_wizard_data'] = {
            'name': 'Minimal Zone',
            'description': '',
            'priority': 0,
            'is_active': False,
            'countries': [],
            'states': {},
            'postal_code_patterns': [],
        }
        session.save()

        response = self.client.post(self.url)

        zone = ShippingZone.objects.latest('created_at')
        self.assertEqual(zone.name, 'Minimal Zone')
        self.assertEqual(zone.description, '')
        self.assertFalse(zone.is_active)
        self.assertEqual(zone.countries, [])


class ZoneWizardAjaxValidationTest(TestCase):
    """Test Zone Wizard AJAX validation endpoints"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            is_staff=True,
        )
        self.client.login(username='admin', password='testpass123')

    def test_validate_country_code_requires_staff(self):
        """Test country validation requires staff login"""
        self.client.logout()
        url = reverse('shipping:validate_country_code')
        response = self.client.post(url, {'country_code': 'US'})

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_validate_country_code_valid(self):
        """Test country validation with valid code"""
        url = reverse('shipping:validate_country_code')
        response = self.client.post(url, {'country_code': 'US'})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertTrue(data['valid'])
        self.assertEqual(data['code'], 'US')
        self.assertIn('name', data)

    def test_validate_country_code_lowercase(self):
        """Test country validation normalizes lowercase"""
        url = reverse('shipping:validate_country_code')
        response = self.client.post(url, {'country_code': 'us'})

        data = json.loads(response.content)

        self.assertTrue(data['valid'])
        self.assertEqual(data['code'], 'US')

    def test_validate_country_code_invalid(self):
        """Test country validation with invalid code"""
        url = reverse('shipping:validate_country_code')
        response = self.client.post(url, {'country_code': 'XX'})

        data = json.loads(response.content)

        self.assertFalse(data['valid'])

    def test_validate_postal_pattern_requires_staff(self):
        """Test postal pattern validation requires staff login"""
        self.client.logout()
        url = reverse('shipping:validate_postal_pattern')
        response = self.client.post(url, {'pattern': r'^\d{5}$'})

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_validate_postal_pattern_valid(self):
        """Test postal pattern validation with valid regex"""
        url = reverse('shipping:validate_postal_pattern')
        response = self.client.post(url, {'pattern': r'^\d{5}$'})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertTrue(data['valid'])
        self.assertEqual(data['pattern'], r'^\d{5}$')

    def test_validate_postal_pattern_invalid(self):
        """Test postal pattern validation with invalid regex"""
        url = reverse('shipping:validate_postal_pattern')
        response = self.client.post(url, {'pattern': '[invalid(regex'})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertFalse(data['valid'])
        self.assertIn('error', data)

    def test_validate_postal_pattern_complex(self):
        """Test postal pattern validation with complex regex"""
        url = reverse('shipping:validate_postal_pattern')
        complex_pattern = r'^[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z]\s?\d[ABCEGHJ-NPRSTV-Z]\d$'

        response = self.client.post(url, {'pattern': complex_pattern})

        data = json.loads(response.content)

        self.assertTrue(data['valid'])


class ZoneWizardNavigationTest(TestCase):
    """Test Zone Wizard navigation and flow"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            is_staff=True,
        )
        self.client.login(username='admin', password='testpass123')

    def test_complete_wizard_flow(self):
        """Test complete wizard flow from step 1 to zone creation"""
        # Step 1
        step1_url = reverse('shipping:zone_wizard_step1')
        response = self.client.post(step1_url, {
            'name': 'Flow Test Zone',
            'description': 'Testing complete flow',
            'priority': '15',
            'is_active': 'on',
        })
        self.assertEqual(response.status_code, 302)

        # Step 2
        step2_url = reverse('shipping:zone_wizard_step2')
        response = self.client.post(step2_url, {
            'countries': 'US, CA',
            'states': json.dumps({'US': ['CA', 'NY']}),
            'postal_patterns': r'^9\d{4}$',
        })
        self.assertEqual(response.status_code, 302)

        # Step 3
        step3_url = reverse('shipping:zone_wizard_step3')
        response = self.client.post(step3_url)
        self.assertEqual(response.status_code, 302)

        # Verify zone created
        zone = ShippingZone.objects.latest('created_at')
        self.assertEqual(zone.name, 'Flow Test Zone')
        self.assertEqual(zone.priority, 15)
        self.assertEqual(zone.countries, ['US', 'CA'])

    def test_step2_without_step1_data(self):
        """Test step 2 without completing step 1"""
        # Clear any session data
        session = self.client.session
        session.pop('zone_wizard_data', None)
        session.save()

        step2_url = reverse('shipping:zone_wizard_step2')
        response = self.client.get(step2_url)

        # Should redirect to step 1 with a warning message
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('shipping:zone_wizard_step1'))

    def test_back_navigation(self):
        """Test backward navigation preserves data"""
        # Complete step 1
        step1_url = reverse('shipping:zone_wizard_step1')
        self.client.post(step1_url, {
            'name': 'Back Nav Test',
            'priority': '5',
            'is_active': 'on',
        })

        # Go to step 2
        step2_url = reverse('shipping:zone_wizard_step2')
        response = self.client.get(step2_url)

        # Should show step 1 data
        zone_data = response.context['zone_data']
        self.assertEqual(zone_data['name'], 'Back Nav Test')
