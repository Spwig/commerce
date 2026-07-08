---
slug: platform-updates
title_i18n_key: Platform Updates
category: extensions
component: component_updates
keywords:
  - platform update
  - component update
  - update channel
  - stable channel
  - beta channel
  - check for updates
  - install update
  - version history
  - rollback
  - upgrade platform
  - component registry
  - update log
  - auto update
  - lock component
  - security update
url_patterns:
  - /admin/component_updates/componentregistry/
  - /admin/management/systemmetrics/check-updates/
related:
  - platform-settings
published: true
---

Your Spwig installation is built from a collection of components — themes, widgets, integrations, page builder elements, and provider connections — each with its own version that can be updated independently. The Component Registry gives you a central view of everything installed, shows which components have updates waiting, and lets you install or roll back updates at any time.

![Component Registry Overview](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Understanding the component registry

Navigate to **Extensions > Component Registry** to see every component installed on your store. Each row shows:

- **Name** — the component's display name
- **Type** — what kind of component it is (theme, widget, integration, etc.)
- **Current version** — the version currently running on your store
- **Update status** — whether an update is available
- **Channel** — which update channel the component follows
- **Auto Update** — whether updates install automatically
- **Locked** — whether the component is frozen at its current version

The dashboard at the top of the page shows summary counts: total components installed, how many have updates available, and how many are up to date.

### Component types

| Type | What it is |
|------|------------|
| Theme | Your store's visual design |
| Widget | Reusable page builder blocks |
| Page Builder Element | Custom elements for the page builder |
| Page Builder Utility | Editor tools and utilities |
| Header / Footer Template | Header and footer layouts |
| Shipping Provider | Carrier integrations (FedEx, UPS, etc.) |
| Email Provider | Email delivery services |
| Payment Provider | Payment gateway integrations |
| Exchange Rate Provider | Currency rate data sources |
| Translation Provider | AI translation services |
| Language Pack | Interface translation files |

## Update channels

Every component follows an update channel that controls which releases it receives. You can assign each component to a different channel based on how much risk you are comfortable with.

| Channel | Description | Best for |
|---------|-------------|----------|
| **Stable** | Production-ready, thoroughly tested releases | All components on live stores |
| **Beta** | Pre-release builds for testing new features before they go stable | Non-critical components you want to preview |
| **Development** | Latest features, may be unstable | Testing environments only |
| **Security** | Critical security patches only, delivered with highest priority | Components where stability is paramount |

To change a component's channel, click on its name to open the detail view, then select a new value in the **Update Channel** field and save.

## Checking for updates

Spwig checks for updates automatically at the interval configured in your update server settings (default: every 24 hours). To check immediately:

1. Navigate to **Extensions > Component Registry**
2. Click the **Check for Updates** button at the top of the page
3. The system contacts the Spwig update server and refreshes the update status for all components
4. Components with available updates are highlighted, and the **Updates Available** count updates

You can also trigger an update check for individual components using the **Check for Updates** action from the list's action menu.

## Installing updates

### Updating a single component

1. Navigate to **Extensions > Component Registry**
2. Find the component you want to update — components with available updates show an update indicator next to their version
3. Click the **Install Update** button on that component's row
4. Confirm the update when prompted
5. The update downloads, verifies, and installs — a progress indicator shows each stage
6. Once complete, the component's **Current Version** updates to the new version number

### Updating multiple components

1. Select the checkboxes next to the components you want to update
2. Choose **Install updates** from the **Action** dropdown
3. Click **Go** to proceed
4. Updates are installed in dependency order — components that others depend on update first

### What happens during an update

The update process runs through these stages:

1. **Checking** — confirms the update is available and your license is valid
2. **Downloading** — retrieves the package from the Spwig update server
3. **Verifying** — checks the package integrity against a SHA-256 checksum
4. **Extracting** — unpacks the new files
5. **Deploying** — activates the new version
6. **Health check** — verifies the component is working after the update

If any stage fails, the system automatically attempts to restore the previous version.

## Platform-level updates

In addition to individual components, Spwig can receive platform-level updates that update the core store engine. These updates go through a more thorough process including database migrations and a brief maintenance window.

Platform update history is visible in the **Platform Updates** section of the registry. Each entry shows the version transition (e.g., `v1.3.2 → v1.3.3`), the status, and the duration of the update process.

Security updates are flagged separately and, if **Auto Install Security Updates** is enabled in your update server configuration, install automatically without requiring manual action.

## Viewing version history

To see all previously installed versions of a component:

1. Click on the component name to open its detail view
2. Scroll to the **Component Versions** section at the bottom of the page
3. Each version entry shows the version number, when it was installed, the installation method, and its health status

The system keeps the last three installed versions available for rollback. Versions beyond that are automatically removed.

## Rolling back a component

If an update causes problems, you can roll back to a previous version:

1. Open the component's detail view
2. Scroll to the **Rollback** section
3. Select the version you want to restore
4. Click **Roll Back to this Version**

Only versions marked **Rollback Available** can be restored. The rollback log entry records who initiated the rollback and when.

## Locking components

Locking a component prevents any updates from being installed, including automatic ones. This is useful when you have customizations or integrations that depend on a specific version.

1. Open the component's detail view
2. Check the **Locked** checkbox in the **Lock & Freeze** section
3. Enter a reason in **Lock Reason** so your team understands why it is frozen
4. Save the record

Locked components are shown with a lock indicator in the registry list. To unlock, uncheck **Locked** and save.

## Reading update logs

The update log records every install, update, rollback, and health check operation:

1. Open a component's detail view
2. The **Update Logs** are visible inline at the bottom of the page
3. Each entry shows: the action taken, start and end times, old and new versions, whether it was automatic or manual, and any error messages if the operation failed

Log entries with a **Failed** status include the full error message to help with troubleshooting.

## Enabling auto-updates

You can allow Spwig to install updates automatically as they become available:

1. Open the component's detail view
2. Check **Auto Update** in the **Version & Update Status** section
3. Save the record

With auto-update enabled, the system installs updates during the next scheduled check cycle. Security updates follow the global **Auto Install Security Updates** setting regardless of individual component settings.

## Tips

- Always update on the **Stable** channel for themes and payment providers — these are the most customer-facing components and stability matters most
- Lock a component before making custom modifications to it, and record the reason clearly so future team members know not to update it
- Check the **Release Notes** on the component's version entry before installing a major version bump — breaking changes are flagged there
- After an update, browse to the affected area of your store to confirm everything looks and works as expected before declaring the update complete
- If auto-update is enabled on a component, monitor the **Update Logs** periodically to ensure automatic updates are completing successfully
