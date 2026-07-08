"""
Customers Sync Serializer

Handles export/import of customer models (full_migration only):
- User: Django auth users (non-staff only)
- CustomerProfile: Extended profile with custom fields and preferences
- CommunicationPreference: GDPR-compliant email/SMS consent tracking
- Address: Customer shipping/billing addresses (active only)

Passwords are exported as Django hash strings and imported as-is,
so customers can continue using their existing credentials.
Staff/admin users are excluded from sync.
"""
import logging
from django.db import transaction

from .base import CollectionSyncSerializer

logger = logging.getLogger(__name__)

USER_FIELDS = [
    'email', 'username', 'first_name', 'last_name',
    'password', 'is_active', 'date_joined',
]

PROFILE_FIELDS = [
    'external_id', 'phone', 'date_of_birth',
    'company_name', 'tax_number', 'is_business_customer',
    'dashboard_layout', 'show_order_history', 'show_wishlist',
    'show_recent_products', 'show_recommendations',
    'custom_fields',
]

COMM_PREF_FIELDS = [
    'email_enabled', 'sms_enabled',
    'email_transactional', 'email_marketing',
    'sms_transactional', 'sms_marketing',
    'app_preferences',
    'email_verified', 'email_verified_at',
    'sms_verified', 'sms_verified_at',
    'consent_source', 'consent_ip',
    'consent_user_agent', 'consent_timestamp',
    'language_code',
]

ADDRESS_FIELDS = [
    'address_type', 'name', 'company',
    'address1', 'address2', 'city', 'state',
    'postal_code', 'country', 'phone',
    'is_default',
]


class CustomersSerializer(CollectionSyncSerializer):
    """Serializer for customer accounts and profiles (full_migration only).

    Models handled:
        - User: Django user accounts (customers only, not staff)
        - CustomerProfile: Extended profile data, custom fields, theme preference
        - CommunicationPreference: Email/SMS consent with GDPR audit trail
        - Address: Shipping/billing addresses (active versions only)

    Import order: Users → CustomerProfile → CommunicationPreference → Address
    (dependency-driven: user must exist before related models can reference it)
    """

    category_key = 'customers'
    natural_key_fields = ['email']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from django.contrib.auth import get_user_model
        self.model_class = get_user_model()

    # -- User key helpers --

    @staticmethod
    def _user_key(user):
        """Get a portable identifier for a user: email if available, else username."""
        return user.email if user.email else user.username

    @staticmethod
    def _resolve_user(user_key):
        """Resolve a user key (email or username) to a User instance."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not user_key:
            return None
        # Try email first (most users have one)
        user = User.objects.filter(email__iexact=user_key).first()
        if user:
            return user
        # Fall back to username match (guest users with no email)
        return User.objects.filter(username=user_key).first()

    def get_count(self):
        from django.contrib.auth import get_user_model
        from accounts.models import CustomerProfile, CommunicationPreference
        from orders.models import Address

        User = get_user_model()
        return (
            User.objects.filter(is_staff=False).count()
            + CustomerProfile.objects.filter(user__is_staff=False).count()
            + CommunicationPreference.objects.filter(user__is_staff=False).count()
            + Address.objects.filter(is_active=True, user__is_staff=False).count()
        )

    # -- Export --

    def export(self, credential_mode='redact'):
        from django.contrib.auth import get_user_model
        from accounts.models import CustomerProfile, CommunicationPreference
        from orders.models import Address

        User = get_user_model()
        items = []

        # 1. Users (non-staff only)
        for user in User.objects.filter(is_staff=False):
            data = {field: getattr(user, field) for field in USER_FIELDS}
            data['_source_pk'] = user.pk
            data['_model'] = 'User'
            items.append(data)

        # 2. CustomerProfile (non-staff users only)
        for profile in CustomerProfile.objects.select_related(
            'user', 'preferred_theme'
        ).filter(user__is_staff=False):
            data = {field: getattr(profile, field) for field in PROFILE_FIELDS}
            data['_source_pk'] = profile.pk
            data['_model'] = 'CustomerProfile'
            data['_user_email'] = self._user_key(profile.user)
            data['_preferred_theme_slug'] = (
                profile.preferred_theme.slug if profile.preferred_theme else None
            )
            items.append(data)

        # 3. CommunicationPreference (non-staff users only)
        for pref in CommunicationPreference.objects.select_related('user').filter(
            user__is_staff=False
        ):
            data = {field: getattr(pref, field) for field in COMM_PREF_FIELDS}
            data['_source_pk'] = pref.pk
            data['_model'] = 'CommunicationPreference'
            data['_user_email'] = self._user_key(pref.user)
            items.append(data)

        # 4. Address (active only, non-staff users only)
        for address in Address.objects.filter(
            is_active=True, user__is_staff=False
        ).select_related('user'):
            data = {field: getattr(address, field) for field in ADDRESS_FIELDS}
            data['_source_pk'] = address.pk
            data['_model'] = 'Address'
            data['_user_email'] = self._user_key(address.user)
            items.append(data)

        return {
            'category': self.category_key,
            'sync_type': 'collection',
            'items': items,
            'total': len(items),
        }

    # -- Import --

    def import_data(self, data, dry_run=False, sync_mode='additive'):
        if dry_run:
            return self.generate_diff(data)

        items = data.get('items', [])
        synced = 0
        skipped = 0
        failed = 0
        deleted = 0
        errors = []

        try:
            with transaction.atomic():
                # Separate items by model type
                users = [i for i in items if i.get('_model') == 'User']
                profiles = [i for i in items if i.get('_model') == 'CustomerProfile']
                comm_prefs = [i for i in items if i.get('_model') == 'CommunicationPreference']
                addresses = [i for i in items if i.get('_model') == 'Address']

                # Pass 1: Users (must exist before all related models)
                for item in users:
                    try:
                        with transaction.atomic():
                            self._import_user(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"User '{item.get('email', '?')}': {e}")
                        logger.error("Failed to import user '%s': %s", item.get('email'), e)

                # Pass 2: CustomerProfile (OneToOne with User)
                for item in profiles:
                    try:
                        with transaction.atomic():
                            self._import_profile(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"Profile '{item.get('_user_email', '?')}': {e}")
                        logger.error("Failed to import profile for '%s': %s", item.get('_user_email'), e)

                # Pass 3: CommunicationPreference (OneToOne with User)
                for item in comm_prefs:
                    try:
                        with transaction.atomic():
                            self._import_comm_pref(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"CommPref '{item.get('_user_email', '?')}': {e}")
                        logger.error("Failed to import comm pref for '%s': %s", item.get('_user_email'), e)

                # Pass 4: Address (FK to User)
                for item in addresses:
                    try:
                        with transaction.atomic():
                            self._import_address(item)
                        synced += 1
                    except Exception as e:
                        failed += 1
                        errors.append(f"Address '{item.get('name', '?')}' ({item.get('_user_email', '?')}): {e}")
                        logger.error("Failed to import address for '%s': %s", item.get('_user_email'), e)

                # Mirror mode: delete local items not in remote data
                if sync_mode == 'mirror':
                    deleted = self._delete_absent(items)

        except Exception as e:
            logger.error("Customers import failed: %s", e)
            return {'synced': 0, 'skipped': 0, 'failed': 1, 'errors': [str(e)]}

        result = {'synced': synced, 'skipped': skipped, 'failed': failed, 'errors': errors}
        if sync_mode == 'mirror':
            result['deleted'] = deleted
        return result

    def _import_user(self, item):
        """Import or update a customer user account."""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        email = item.get('email', '')
        # Match by email if available, otherwise by username (guest users)
        if email:
            existing = User.objects.filter(email__iexact=email).first()
        else:
            existing = User.objects.filter(username=item.get('username', '')).first()

        if existing:
            for field in USER_FIELDS:
                if field in item and field != 'username':
                    setattr(existing, field, item[field])
            existing.is_staff = False
            existing.is_superuser = False
            existing.save()
        else:
            username = item.get('username', email.split('@')[0])
            username = self._generate_unique_username(username, email)

            user = User(
                email=email,
                username=username,
                is_staff=False,
                is_superuser=False,
            )
            for field in USER_FIELDS:
                if field in item and field not in ('email', 'username'):
                    setattr(user, field, item[field])
            user.save()

    def _generate_unique_username(self, username, email):
        """Generate a unique username, appending numbers if necessary."""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        existing = User.objects.filter(username=username).first()
        if not existing or existing.email.lower() == email.lower():
            return username

        base = username
        counter = 1
        while User.objects.filter(username=f'{base}{counter}').exclude(
            email__iexact=email
        ).exists():
            counter += 1
        return f'{base}{counter}'

    def _import_profile(self, item):
        """Import or update a customer profile."""
        from accounts.models import CustomerProfile

        user_key = item.get('_user_email')
        user = self._resolve_user(user_key)
        if not user:
            raise ValueError(f"User '{user_key}' not found for profile import")

        profile = CustomerProfile.get_or_create_for_user(user)

        for field in PROFILE_FIELDS:
            if field in item:
                setattr(profile, field, item[field])

        # Resolve preferred_theme FK from slug
        theme_slug = item.get('_preferred_theme_slug')
        if theme_slug:
            from design.theme_models import Theme
            theme = Theme.objects.filter(slug=theme_slug).first()
            if theme:
                profile.preferred_theme = theme
            else:
                logger.warning(
                    "Preferred theme '%s' not found for user '%s', setting to None",
                    theme_slug, user_key
                )
                profile.preferred_theme = None
        else:
            profile.preferred_theme = None

        profile.save()

    def _import_comm_pref(self, item):
        """Import or update communication preferences."""
        from accounts.models import CommunicationPreference

        user_key = item.get('_user_email')
        user = self._resolve_user(user_key)
        if not user:
            raise ValueError(
                f"User '{user_key}' not found for communication preference import"
            )

        pref, _created = CommunicationPreference.get_or_create_for_user(user)

        for field in COMM_PREF_FIELDS:
            if field in item:
                setattr(pref, field, item[field])

        # Do NOT set unsubscribe_token — auto-generated on save, must be unique
        pref.save()

    def _import_address(self, item):
        """Import or update a customer address."""
        from orders.models import Address

        user_key = item.get('_user_email')
        user = self._resolve_user(user_key)
        if not user:
            raise ValueError(f"User '{user_key}' not found for address import")

        # Composite natural key match
        existing = Address.objects.filter(
            user=user,
            address_type=item.get('address_type', 'both'),
            name=item.get('name', ''),
            address1=item.get('address1', ''),
            is_active=True,
        ).first()

        if existing:
            for field in ADDRESS_FIELDS:
                if field in item:
                    setattr(existing, field, item[field])
            existing.save()
        else:
            address = Address(user=user, version=1, is_active=True)
            for field in ADDRESS_FIELDS:
                if field in item:
                    setattr(address, field, item[field])
            address.save()

    @staticmethod
    def _clean_protect_refs(user):
        """Remove PROTECT-chain objects that block User.delete() CASCADE.

        The CASCADE path User → LoyaltyMember → LoyaltyTransaction/LoyaltyRedemption
        and User → CustomerWallet → WalletTransaction both contain PROTECT FKs.
        We explicitly delete those child records so the CASCADE can proceed.
        Orders with on_delete=PROTECT are intentionally NOT cleaned — if a user
        has orders, mirror mode should skip that user rather than destroy order history.
        """
        # Loyalty: LoyaltyMember.customer → User (CASCADE)
        #   LoyaltyTransaction.member → LoyaltyMember (PROTECT)
        #   LoyaltyRedemption.member → LoyaltyMember (PROTECT)
        try:
            from loyalty.models import LoyaltyMember
            for member in LoyaltyMember.objects.filter(customer=user):
                member.transactions.all().delete()
                member.redemptions.all().delete()
        except ImportError:
            pass

        # Wallet: CustomerWallet.customer → User (CASCADE)
        #   WalletTransaction.wallet → CustomerWallet (PROTECT)
        try:
            from wallet.models import CustomerWallet
            for wallet in CustomerWallet.objects.filter(customer=user):
                wallet.transactions.all().delete()
        except ImportError:
            pass

    def _delete_absent(self, items):
        """In mirror mode, delete local items not present in remote data."""
        from django.contrib.auth import get_user_model
        from accounts.models import CustomerProfile, CommunicationPreference
        from orders.models import Address

        User = get_user_model()
        deleted_count = 0

        # Build set of remote user keys (email or username, lowercased)
        remote_keys = set()
        for i in items:
            if i.get('_model') == 'User':
                email = i.get('email', '')
                if email:
                    remote_keys.add(email.lower())
                else:
                    remote_keys.add(i.get('username', '').lower())

        def _is_remote(user):
            """Check if a user is present in the remote data."""
            if user.email:
                return user.email.lower() in remote_keys
            return user.username.lower() in remote_keys

        # 1. Addresses (FK to User, delete first)
        for address in Address.objects.filter(
            user__is_staff=False, is_active=True
        ).select_related('user'):
            if not _is_remote(address.user):
                address.delete()
                deleted_count += 1

        # 2. CommunicationPreference (OneToOne to User)
        for pref in CommunicationPreference.objects.filter(
            user__is_staff=False
        ).select_related('user'):
            if not _is_remote(pref.user):
                pref.delete()
                deleted_count += 1

        # 3. CustomerProfile (OneToOne to User)
        for profile in CustomerProfile.objects.filter(
            user__is_staff=False
        ).select_related('user'):
            if not _is_remote(profile.user):
                profile.delete()
                deleted_count += 1

        # 4. Users last — clean up PROTECT-chain objects before delete
        local_only = [
            u for u in User.objects.filter(is_staff=False)
            if not _is_remote(u)
        ]
        if local_only:
            logger.warning(
                "Mirror mode: deleting %d local-only customer users.",
                len(local_only)
            )
            for user in local_only:
                try:
                    with transaction.atomic():
                        self._clean_protect_refs(user)
                        user.delete()
                    deleted_count += 1
                except Exception as e:
                    logger.warning(
                        "Cannot delete user '%s': %s (likely has orders or other protected references)",
                        self._user_key(user), e
                    )

        return deleted_count

    # -- Diff --

    def generate_diff(self, remote_data):
        from django.contrib.auth import get_user_model
        from accounts.models import CustomerProfile, CommunicationPreference
        from orders.models import Address

        User = get_user_model()

        items = remote_data.get('items', [])
        if not items:
            return {'changes': [], 'warnings': [], 'summary': 'No data to sync'}

        changes = []
        warnings = []

        for item in items:
            model_type = item.get('_model')

            if model_type == 'User':
                email = item.get('email', '')
                if email:
                    existing = User.objects.filter(email__iexact=email).first()
                else:
                    existing = User.objects.filter(
                        username=item.get('username', '')
                    ).first()
                # Exclude password from diff (comparing hashes is misleading)
                compare_fields = [f for f in USER_FIELDS if f != 'password']
                display_name = f"User: {email or item.get('username', 'Unknown')}"

            elif model_type == 'CustomerProfile':
                user = self._resolve_user(item.get('_user_email', ''))
                existing = (
                    CustomerProfile.objects.filter(user=user).first()
                    if user else None
                )
                compare_fields = PROFILE_FIELDS
                display_name = f"Profile: {item.get('_user_email', 'Unknown')}"

            elif model_type == 'CommunicationPreference':
                user = self._resolve_user(item.get('_user_email', ''))
                existing = (
                    CommunicationPreference.objects.filter(user=user).first()
                    if user else None
                )
                compare_fields = COMM_PREF_FIELDS
                display_name = f"Preferences: {item.get('_user_email', 'Unknown')}"

            elif model_type == 'Address':
                user = self._resolve_user(item.get('_user_email', ''))
                existing = (
                    Address.objects.filter(
                        user=user,
                        address_type=item.get('address_type'),
                        name=item.get('name'),
                        address1=item.get('address1'),
                        is_active=True,
                    ).first() if user else None
                )
                compare_fields = ADDRESS_FIELDS
                display_name = (
                    f"Address: {item.get('name', 'Unknown')} "
                    f"({item.get('_user_email', '')})"
                )

            else:
                warnings.append(f"Unknown model type: {model_type}")
                continue

            if existing:
                field_changes = self._compute_field_diff(
                    existing, item, compare_fields
                )
                if field_changes:
                    changes.append({
                        'type': 'modify',
                        'model': model_type,
                        'name': display_name,
                        'changes': field_changes,
                    })
            else:
                changes.append({
                    'type': 'add',
                    'model': model_type,
                    'name': display_name,
                    'fields': {
                        k: v for k, v in item.items()
                        if not k.startswith('_') and k != 'password'
                    },
                })

        adds = sum(1 for c in changes if c['type'] == 'add')
        mods = sum(1 for c in changes if c['type'] == 'modify')
        parts = []
        if adds:
            parts.append(f'{adds} addition(s)')
        if mods:
            parts.append(f'{mods} modification(s)')

        return {
            'changes': changes,
            'warnings': warnings,
            'summary': ', '.join(parts) if parts else 'No changes',
        }

    # -- Snapshot & Restore --

    def snapshot_current(self):
        return self.export(credential_mode='skip')

    def restore_snapshot(self, snapshot):
        try:
            result = self.import_data(snapshot, dry_run=False)
            return {'restored': result.get('synced', 0), 'errors': result.get('errors', [])}
        except Exception as e:
            return {'restored': 0, 'errors': [str(e)]}
