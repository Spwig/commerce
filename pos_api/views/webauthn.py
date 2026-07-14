import base64

from django.core import signing
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, extend_schema
from fido2.server import Fido2Server
from fido2.webauthn import (
    AttestationObject,
    AttestedCredentialData,
    AuthenticatorData,
    CollectedClientData,
    PublicKeyCredentialRpEntity,
    PublicKeyCredentialUserEntity,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from admin_api.authentication import MobileTokenAuthentication
from pos_api.permissions import IsStaffUser

CHALLENGE_MAX_AGE = 300  # 5 minutes


def _get_rp(request):
    """Build relying party from request hostname."""
    host = request.get_host().split(":")[0]
    return PublicKeyCredentialRpEntity(name="Spwig POS", id=host)


def _get_server(request):
    return Fido2Server(_get_rp(request))


def _b64encode(data):
    """Encode bytes to URL-safe base64 without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64decode(s):
    """Decode URL-safe base64 (with or without padding)."""
    s += "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)


def _build_credentials(queryset):
    """Build AttestedCredentialData list from WebAuthnCredential queryset."""
    return [
        AttestedCredentialData.from_ctap1(
            bytes(cred.credential_id),
            bytes(cred.public_key),
        )
        for cred in queryset
    ]


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


@extend_schema(
    summary=_("Begin WebAuthn registration"),
    description=_(
        "Generate registration options for biometric enrollment. Returns challenge and credential creation options."
    ),
    responses={200: OpenApiResponse(description=_("Registration options"))},
    tags=["POS - WebAuthn"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def webauthn_register_begin(request):
    """Generate WebAuthn registration options."""
    from pos_app.models import WebAuthnCredential

    server = _get_server(request)
    user = request.user

    # Existing credentials to exclude (prevent re-registration)
    existing = WebAuthnCredential.objects.filter(user=user)
    credentials = _build_credentials(existing)

    user_entity = PublicKeyCredentialUserEntity(
        name=user.email,
        id=str(user.pk).encode(),
        display_name=user.get_full_name() or user.email,
    )

    options, state = server.register_begin(
        user_entity,
        credentials=credentials,
        user_verification=UserVerificationRequirement.PREFERRED,
        resident_key_requirement=ResidentKeyRequirement.DISCOURAGED,
    )

    # Sign the state for stateless round-trip
    signed_state = signing.dumps(state, salt="webauthn-register")

    # Serialize options to JSON-friendly format
    pk = options.public_key
    return Response(
        {
            "success": True,
            "state": signed_state,
            "options": {
                "rp": {"id": pk.rp.id, "name": pk.rp.name},
                "user": {
                    "id": _b64encode(pk.user.id),
                    "name": pk.user.name,
                    "displayName": pk.user.display_name,
                },
                "challenge": _b64encode(pk.challenge),
                "pubKeyCredParams": [
                    {"type": p.type.value, "alg": p.alg} for p in pk.pub_key_cred_params
                ],
                "timeout": pk.timeout or 60000,
                "excludeCredentials": [
                    {"type": c.type.value, "id": _b64encode(c.id)}
                    for c in (pk.exclude_credentials or [])
                ],
                "authenticatorSelection": {
                    "userVerification": "preferred",
                    "residentKey": "discouraged",
                },
                "attestation": (pk.attestation.value if pk.attestation else "none"),
            },
        }
    )


@extend_schema(
    summary=_("Complete WebAuthn registration"),
    description=_("Verify attestation and store credential for biometric unlock."),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "state": {"type": "string", "description": "Signed state from register_begin"},
                "credential": {"type": "object", "description": "Browser credential response"},
                "device_name": {"type": "string"},
            },
            "required": ["state", "credential"],
        }
    },
    responses={
        200: OpenApiResponse(description=_("Credential registered")),
        400: OpenApiResponse(description=_("Verification failed")),
    },
    tags=["POS - WebAuthn"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def webauthn_register_complete(request):
    """Verify attestation and store credential."""
    from pos_app.models import WebAuthnCredential

    signed_state = request.data.get("state", "")
    credential_data = request.data.get("credential", {})
    device_name = request.data.get("device_name", "")

    try:
        state = signing.loads(signed_state, salt="webauthn-register", max_age=CHALLENGE_MAX_AGE)
    except (signing.BadSignature, signing.SignatureExpired):
        return Response(
            {
                "success": False,
                "error": {"code": "INVALID_STATE", "message": "Challenge expired or invalid."},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        client_data_bytes = _b64decode(credential_data["response"]["clientDataJSON"])
        att_object_bytes = _b64decode(credential_data["response"]["attestationObject"])
    except (KeyError, Exception):
        return Response(
            {
                "success": False,
                "error": {"code": "INVALID_CREDENTIAL", "message": "Invalid credential data."},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    server = _get_server(request)

    try:
        auth_data = server.register_complete(
            state,
            CollectedClientData(client_data_bytes),
            AttestationObject(att_object_bytes),
        )
    except Exception as e:
        return Response(
            {"success": False, "error": {"code": "VERIFICATION_FAILED", "message": str(e)}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Store credential
    cred_data = auth_data.credential_data
    WebAuthnCredential.objects.create(
        user=request.user,
        credential_id=cred_data.credential_id,
        public_key=bytes(cred_data.public_key),
        sign_count=auth_data.counter,
        device_name=device_name[:200] if device_name else "",
    )

    return Response({"success": True})


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------


@extend_schema(
    summary=_("Begin WebAuthn authentication"),
    description=_(
        "Generate authentication challenge for biometric unlock. "
        "Returns allowCredentials for the locked-by user and all managers. "
        "If failed_attempts >= 3, only manager credentials are included."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "locked_by_user_id": {"type": "integer"},
                "failed_attempts": {"type": "integer"},
            },
        }
    },
    responses={
        200: OpenApiResponse(description=_("Authentication options")),
        404: OpenApiResponse(description=_("No credentials registered")),
    },
    tags=["POS - WebAuthn"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def webauthn_authenticate_begin(request):
    """Generate WebAuthn authentication challenge."""
    from pos_app.models import POSStaffDiscount, WebAuthnCredential

    locked_by_user_id = request.data.get("locked_by_user_id")
    failed_attempts = request.data.get("failed_attempts", 0)
    require_manager = failed_attempts >= 3

    # Determine which user IDs have valid credentials
    user_ids = set()

    if not require_manager and locked_by_user_id:
        user_ids.add(locked_by_user_id)

    # Always include manager IDs
    manager_ids = set(
        POSStaffDiscount.objects.filter(is_manager=True).values_list("user_id", flat=True)
    )
    user_ids.update(manager_ids)

    credentials_qs = WebAuthnCredential.objects.filter(user_id__in=user_ids)
    if not credentials_qs.exists():
        return Response(
            {
                "success": False,
                "error": {
                    "code": "NO_CREDENTIALS",
                    "message": "No biometric credentials registered.",
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    # Build credential ID → user ID map for lookup in complete
    cred_user_map = {}
    for cred in credentials_qs:
        cred_user_map[bytes(cred.credential_id).hex()] = cred.user_id

    credentials = _build_credentials(credentials_qs)

    server = _get_server(request)
    options, state = server.authenticate_begin(
        credentials=credentials,
        user_verification=UserVerificationRequirement.PREFERRED,
    )

    # Attach context to state for the complete step
    state["cred_user_map"] = cred_user_map
    state["locked_by_user_id"] = locked_by_user_id
    state["failed_attempts"] = failed_attempts

    signed_state = signing.dumps(state, salt="webauthn-auth")

    pk = options.public_key
    return Response(
        {
            "success": True,
            "state": signed_state,
            "options": {
                "challenge": _b64encode(pk.challenge),
                "timeout": pk.timeout or 60000,
                "rpId": pk.rp_id,
                "allowCredentials": [
                    {"type": c.type.value, "id": _b64encode(c.id)}
                    for c in (pk.allow_credentials or [])
                ],
                "userVerification": "preferred",
            },
        }
    )


@extend_schema(
    summary=_("Complete WebAuthn authentication"),
    description=_("Verify biometric assertion and unlock terminal."),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "state": {"type": "string"},
                "credential": {"type": "object"},
                "cart_item_count": {"type": "integer"},
                "cart_total": {"type": "string"},
            },
            "required": ["state", "credential"],
        }
    },
    responses={
        200: OpenApiResponse(description=_("Authentication successful")),
        400: OpenApiResponse(description=_("Verification failed")),
    },
    tags=["POS - WebAuthn"],
)
@api_view(["POST"])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def webauthn_authenticate_complete(request):
    """Verify WebAuthn assertion and unlock."""
    from django.contrib.auth import get_user_model

    from pos_app.models import POSStaffDiscount, POSTerminal, WebAuthnCredential

    User = get_user_model()

    signed_state = request.data.get("state", "")
    credential_data = request.data.get("credential", {})
    cart_items = request.data.get("cart_item_count", 0)
    cart_total = request.data.get("cart_total")

    try:
        state = signing.loads(signed_state, salt="webauthn-auth", max_age=CHALLENGE_MAX_AGE)
    except (signing.BadSignature, signing.SignatureExpired):
        return Response(
            {
                "success": False,
                "error": {"code": "INVALID_STATE", "message": "Challenge expired or invalid."},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    cred_user_map = state.pop("cred_user_map", {})
    locked_by_user_id = state.pop("locked_by_user_id", None)
    state.pop("failed_attempts", 0)

    # Get terminal for audit logging
    terminal_uuid = request.headers.get("X-Terminal-UUID")
    terminal = None
    if terminal_uuid:
        try:
            terminal = POSTerminal.objects.get(uuid=terminal_uuid, is_active=True)
        except POSTerminal.DoesNotExist:
            pass

    # Parse client credential response
    try:
        credential_id = _b64decode(credential_data["id"])
        client_data_bytes = _b64decode(credential_data["response"]["clientDataJSON"])
        authenticator_data_bytes = _b64decode(credential_data["response"]["authenticatorData"])
        signature = _b64decode(credential_data["response"]["signature"])
    except (KeyError, Exception):
        return Response(
            {
                "success": False,
                "error": {"code": "INVALID_CREDENTIAL", "message": "Invalid credential data."},
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Rebuild credentials for verification
    creds_qs = WebAuthnCredential.objects.filter(
        user_id__in=[int(uid) for uid in cred_user_map.values()]
    )
    credentials = _build_credentials(creds_qs)

    server = _get_server(request)

    try:
        server.authenticate_complete(
            state,
            credentials,
            credential_id,
            CollectedClientData(client_data_bytes),
            AuthenticatorData(authenticator_data_bytes),
            signature,
        )
    except Exception as e:
        return Response(
            {"success": False, "error": {"code": "VERIFICATION_FAILED", "message": str(e)}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Update sign count and last used
    try:
        stored_cred = WebAuthnCredential.objects.get(credential_id=credential_id)
        stored_cred.sign_count += 1
        stored_cred.last_used_at = timezone.now()
        stored_cred.save(update_fields=["sign_count", "last_used_at"])
        auth_user = stored_cred.user
    except WebAuthnCredential.DoesNotExist:
        auth_user = request.user

    # Determine unlock type
    is_manager = POSStaffDiscount.objects.filter(user=auth_user, is_manager=True).exists()

    locked_by_user = None
    if locked_by_user_id:
        try:
            locked_by_user = User.objects.get(pk=locked_by_user_id)
        except User.DoesNotExist:
            pass

    manager_override = is_manager and (auth_user.pk != locked_by_user_id)

    # Audit log
    if terminal:
        from pos_api.views.terminal import _log_lock_event

        _log_lock_event(
            request,
            terminal,
            "unlock_biometric",
            locked_by_user=locked_by_user,
            performed_by_user=auth_user,
            manager_override=manager_override,
            cart_items=cart_items,
            cart_total=cart_total,
            unlock_method="biometric",
        )

    return Response(
        {
            "success": True,
            "unlock_type": "manager" if manager_override else "cashier",
            "user_name": auth_user.get_full_name() or auth_user.email,
        }
    )
