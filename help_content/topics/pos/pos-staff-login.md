---
slug: pos-staff-login
title_i18n_key: POS Staff Login & Biometric Sign-In
category: point-of-sale
component: pos_app
keywords:
  - pos login
  - pos staff access
  - biometric login
  - fingerprint login
  - webauthn
  - passkey
  - face recognition pos
  - touch id pos
  - pos register sign in
  - staff account pos
  - pos permissions
  - assign staff terminal
  - pos staff account
  - biometric unlock
  - pos fast login
  - pos credential
  - is_staff
published: true
url_patterns:
  - /admin/accounts/staffmember/
  - /admin/pos_app/posterminal/
related:
  - staff-roles
  - managing-pos-terminals
  - pos-staff-discounts
  - getting-started-with-pos
---

Every person who serves customers at a POS register needs a staff account with the right permissions. This topic explains how to create that account, assign the staff member to a terminal, and then set up biometric sign-in so they can unlock the register with a fingerprint, face scan, or hardware passkey instead of typing a password every time.

For PIN codes, discount limits, and terminal lock settings, see [POS Staff Discounts & Terminal Security](pos-staff-discounts).

## What a staff member needs to use a POS terminal

To log into a POS terminal, a person needs:

1. A **staff account** — a Spwig user with the **Staff status** flag enabled.
2. A **role that includes POS access** — roles control what a staff member can do inside the admin. A role with POS permissions is required to access the register.
3. **Assignment to the terminal** — the terminal must list them as an assigned staff member, or they must be assigned at the store location level.

## Creating a POS-eligible staff account

Navigate to **Staff & Accounts > Staff Members** (or go to `/admin/accounts/staffmember/`).

1. Click **+ Add Staff Member**.
2. Fill in the staff member's **first name**, **last name**, and **email address**.
3. Set a temporary password and ask the staff member to change it on first login.
4. Make sure **Staff status** is ticked — this is what allows them to log into the admin and the POS application.
5. Click **Save**.

> **Note:** Do not tick **Superuser status** for regular cashiers or supervisors. Superuser status bypasses all permission checks and should be reserved for the store owner.

### Assigning a role with POS access

Staff accounts by themselves have no permissions — roles grant the specific capabilities. After creating the account, open the staff member's record and go to the **Roles** section. Assign a role that includes POS access.

For a full explanation of how roles work and which permissions to include, see [Staff Roles](staff-roles).

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: staff-user-list.webp
  description: Staff member list showing a POS-eligible user with their role badge
-->

![Staff member list](/static/core/admin/img/help/pos-staff-login/staff-user-list.webp)

## Assigning staff to a terminal

Settings follow a cascade: **Site default → Store group → Store location → Individual terminal**. For most stores, the right place to assign staff is at the terminal level.

1. Navigate to **POS > Terminals** (or go to `/admin/pos_app/posterminal/`).
2. Open the terminal you want to configure.
3. Go to the **Staff Assignment** tab.
4. In the **Assigned staff** field, search for and add the staff member.
5. Click **Save**.

Staff members who appear in the **Assigned staff** list for a terminal are able to select their name on that terminal's login screen. Staff not assigned to any terminal can still log in by typing their email directly.

> **Tip:** If your store has many staff rotating across terminals, assign them at the store location (warehouse) level rather than terminal by terminal. Any staff member assigned to the location automatically has access to all terminals at that location.

## Logging in at the POS register

When a cashier opens the POS application (`/pos/`) on a terminal, they see a staff selection screen. The login flow works as follows:

1. The cashier taps or clicks their name in the list (or types their email if they are not listed).
2. They enter their password.
3. They are logged in and the register opens for their shift.

For PIN-based unlock (after the terminal locks during a shift), see [POS Staff Discounts & Terminal Security](pos-staff-discounts).

## Biometric login

Biometric sign-in lets a cashier touch a fingerprint sensor, glance at a face camera, or tap a hardware key instead of typing a password. On a busy register this saves several seconds per shift and avoids mistakes during peak hours.

Spwig uses the **WebAuthn** browser standard for biometric sign-in. A "WebAuthn credential" is a device-bound key pair: the private key is stored in the device's secure hardware and never leaves it. The POS application communicates with that hardware through the browser.

### Devices and browsers that support biometric login

WebAuthn is supported by all modern browsers — Chrome, Edge, Firefox, and Safari — on devices that have compatible hardware. Common setups that work well:

| Device | Authenticator |
|--------|---------------|
| iPad (Touch ID) | Fingerprint via Safari or Chrome |
| Android tablet | Fingerprint or face via Chrome |
| Windows tablet or PC | Windows Hello (fingerprint, face, or PIN) |
| Any device + security key | USB, NFC, or Bluetooth FIDO2 key (e.g. YubiKey) |
| iPhone (Face ID) | Face via Safari |

The POS application will only show the biometric sign-in option when the browser has confirmed that a credential is enrolled for the current user on that device.

### How enrolment works

Enrolment happens at the POS terminal, not in the admin. The staff member must complete a normal password login first, then choose to set up biometric sign-in from within the POS application. The browser then prompts them to verify their identity using the device's biometric sensor (or a passkey saved in their account on iOS/macOS/Windows). Once confirmed, the credential is stored and biometric login is available for future shifts on that device.

A single staff member can enrol on multiple devices — for example, a personal tablet and a shared register — and each device holds its own credential.

> **Note:** The exact wording of the enrolment prompt ("Register biometric", "Set up fingerprint sign-in", etc.) comes from the POS application and may vary by browser and device.

### Signing in with a biometric

Once enrolled, the cashier's name on the login screen will show a biometric sign-in button (fingerprint icon or similar). The cashier:

1. Taps their name on the terminal's login screen.
2. Taps **Sign in with fingerprint** (or equivalent).
3. Touches the sensor or looks at the camera.
4. The terminal unlocks immediately.

If biometric verification fails (finger not recognised, face obscured), the cashier falls back to entering their password.

### Revoking a credential

If a device is lost, stolen, or a staff member leaves, you should remove their biometric credentials immediately.

1. Navigate to **Staff & Accounts > Staff Members**.
2. Open the staff member's record.
3. Scroll to the **POS Settings** section.
4. In the **Biometric Unlock** row, click **Remove All**.
5. Confirm the action.

This removes all enrolled WebAuthn credentials for that staff member across every device. The next time they try to use biometric sign-in on any terminal, they will be required to log in with their password instead.

> **Important:** Removing credentials here does not block the staff member from logging in with their password. To fully revoke access, also deactivate their staff account or remove them from the terminal's assigned staff list.

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: webauthn-credential-list.webp
  description: Staff member change form showing the POS Settings section with biometric credential count and Remove All button
-->

## Security notes

- **Credentials are hardware-bound.** The private key never leaves the device's secure element. If a tablet is stolen, an attacker cannot extract the biometric key — they would still need to bypass the device's own lock screen before the browser would release the key.
- **Losing a device does not leak a password.** WebAuthn replaces the password for that device; the staff member's password is separate and unaffected.
- **Revoke promptly when staff leave.** Remove biometric credentials and deactivate the staff account in the same session when offboarding a staff member.
- **The biometric itself is never transmitted.** The fingerprint or face scan is processed entirely by the device hardware. Spwig only receives a signed challenge response, not any biometric data.

## Troubleshooting

### The "Sign in with fingerprint" button is not showing

The biometric option only appears when:
- The staff member has a credential enrolled on this specific device.
- The browser supports WebAuthn (all modern browsers do — update if on an older version).

If the button is missing, the staff member has not yet enrolled on this device. They should log in with their password and set up biometric sign-in through the POS application.

### Enrolment failed

Common reasons:
- **Browser permission denied.** The browser asked for permission to access the authenticator and the staff member declined. They need to try again and tap **Allow** when prompted.
- **No compatible authenticator found.** The device does not have a fingerprint sensor, face camera, or security key attached. Check the device hardware.
- **Duplicate credential.** The staff member may have already enrolled on this device. Existing credentials are excluded during re-registration to avoid duplicates.

### Biometric worked on one device but not another

Each device stores its own credential. Enrolling on an iPad does not automatically work on a second iPad. The staff member must complete enrolment separately on each device they will use.

### Cross-device passkeys

Some operating systems (iOS 16+, macOS Ventura+, Windows 11 with a Microsoft account) can sync passkeys across devices through iCloud Keychain or Windows Hello. If the staff member enrolled using a synced passkey, it may work across multiple devices automatically. Behaviour depends on the operating system and browser, not Spwig.

## Tips

- Set up biometric sign-in on shared registers before staff arrive for their shift — the two-minute enrolment process is much smoother when done without customers waiting.
- Assign a role with limited POS permissions to cashiers and a separate manager role to supervisors. Keep their accounts distinct from the store owner account.
- When a staff member changes devices (new tablet, new phone), have them enrol on the new device first, then revoke the old credential from the admin if the device is no longer in use.
- For stores with high staff turnover, review the **Assigned staff** list on each terminal periodically and remove staff who no longer work at the location.
- If you use hardware security keys (YubiKey or similar), one key can be enrolled on multiple terminals without any change to the admin — simply plug the key in and complete enrolment on each terminal.
