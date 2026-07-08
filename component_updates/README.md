# Component Update System

A comprehensive versioning and update management system for Shop Platform components.

## Overview

The Component Update System provides centralized version control, update distribution, and rollback capabilities for all platform components including widgets, themes, utilities, elements, and templates.

### Key Features

- **🔄 Automatic Updates** - Scheduled update checks with auto-install options
- **📦 Component Versioning** - Semantic versioning (SemVer) for all components
- **⏮️ Rollback Support** - Quick rollback to previous 3 versions
- **🔒 Security** - JWT authentication with update server
- **📊 Update Channels** - Stable, beta, dev, and security release channels
- **🏥 Health Monitoring** - Post-update health checks
- **📝 Audit Trail** - Complete logging of all update operations
- **🔗 Dependency Tracking** - Automatic dependency resolution

## Architecture

### Components

1. **ComponentRegistry** - Central registry of all installed components
2. **ComponentVersion** - Version history with rollback capability
3. **UpdateChannel** - Distribution channels (stable/beta/dev/security)
4. **UpdateLog** - Audit trail of all update operations
5. **UpdateServerConfig** - Connection and authentication settings
6. **ComponentDependency** - Component dependency tracking

### Update Flow

```
1. Check for Updates
   ↓
2. Download Package (authenticated)
   ↓
3. Verify Package & Dependencies
   ↓
4. Install Update (with backup)
   ↓
5. Health Check
   ↓
6. Cleanup Old Versions (keep last 3)
```

## Usage

### Admin Interface

Access the Component Updates admin at:
```
/en/admin/component_updates/
```

#### Available Admin Actions

1. **Check for updates** - Query update server for new versions
2. **Install available updates** - Install updates for selected components
3. **Enable/Disable auto-update** - Toggle automatic updates
4. **Lock/Unlock components** - Prevent/allow updates

### Management Commands

#### Check for Updates

Check all components for available updates:
```bash
./shop_venv/bin/python manage.py check_updates
```

Check specific component:
```bash
./shop_venv/bin/python manage.py check_updates --component logo
```

Auto-install available updates:
```bash
./shop_venv/bin/python manage.py check_updates --install
```

Auto-install only for components with auto-update enabled:
```bash
./shop_venv/bin/python manage.py check_updates --install --auto-only
```

#### Rollback Component

Rollback to previous version:
```bash
./shop_venv/bin/python manage.py rollback_component logo
```

Rollback to specific version:
```bash
./shop_venv/bin/python manage.py rollback_component logo 1.0.0
```

#### Sync Components

Sync existing components to the registry:
```bash
./shop_venv/bin/python manage.py sync_components
```

### Programmatic Usage

#### Using UpdateManager Service

```python
from component_updates.services import UpdateManager
from component_updates.models import ComponentRegistry

# Initialize manager
manager = UpdateManager()

# Check for updates
result = manager.check_for_updates()
print(f"Found {result['updates_found']} updates")

# Install update for specific component
component = ComponentRegistry.objects.get(slug='logo')
manager.install_update(component)

# Rollback to previous version
manager.rollback(component)

# Check dependencies
satisfied, issues = manager.check_dependencies(component, '2.0.0')
if not satisfied:
    print(f"Dependency issues: {issues}")
```

## Configuration

### Update Server Settings

Configure in admin at: `/en/admin/component_updates/updateserverconfig/`

**Required Settings:**
- **Server URL** - Update server endpoint (default: `https://updates.spwig.com`)
- **License Key** - Your platform license key
- **Installation UUID** - Auto-generated unique identifier

**Optional Settings:**
- **Check Interval** - How often to check for updates (default: 24 hours)
- **Auto Download** - Automatically download available updates
- **Auto Install Security** - Automatically install security updates
- **Send Telemetry** - Send anonymous usage statistics

### Update Channels

Components can subscribe to different update channels:

- **Stable** - Production-ready releases (recommended)
- **Beta** - Pre-release testing versions
- **Dev** - Development snapshots
- **Security** - Critical security patches

Configure per-component in the Component Registry admin.

## Component Types

The system supports versioning and updates for:

### 1. Widgets
Package-based header/footer widgets with templates, JavaScript, and CSS.

**Installation:** Extracts to `design/widget_packages/{slug}/`

### 2. Themes
Complete theme packages with CSS, templates, and assets.

**Installation:** Extracts to `design/themes/{slug}/`

### 3. Utilities
Page builder utilities for design customization.

**Installation:** Coming soon

### 4. Elements
Page builder content elements.

**Installation:** Coming soon

### 5. Header/Footer Templates
Pre-built header and footer templates.

**Installation:** Coming soon

## Package Structure

Component packages are distributed as ZIP files with the following structure:

```
component-package.zip
├── manifest.json          # Package metadata
├── templates/            # Django templates
├── static/              # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
├── locale/              # Translations (optional)
└── README.md            # Documentation (optional)
```

### Manifest.json Schema

```json
{
  "slug": "component-slug",
  "name": "Component Name",
  "version": "1.2.0",
  "type": "widget|theme|utility|element|header_template|footer_template",
  "description": "Component description",
  "author": "Author Name",
  "license": "MIT",
  "homepage": "https://example.com",
  "requires": {
    "platform_version": ">=1.0.0",
    "dependencies": [
      {
        "type": "widget",
        "slug": "required-widget",
        "version": ">=1.0.0"
      }
    ]
  },
  "changelog": "What's new in this version"
}
```

## Security

### Authentication

- JWT-based authentication with update server
- Automatic token refresh when expired
- Installation UUID prevents unauthorized access
- License key validation

### Package Verification

- Manifest validation (slug, version, type)
- Checksum verification (SHA256)
- Dependency checks before installation
- Backup before installation (auto-restore on failure)

### Update Safety

- Components can be locked to prevent updates
- Critical updates flagged for manual review
- Three-version rollback window
- Health checks after installation
- Complete audit trail

## Health Monitoring

After each update, the system performs health checks:

- **Healthy** ✅ - Component loaded and functioning
- **Degraded** ⚠️ - Component loaded but with warnings
- **Unhealthy** ❌ - Component failed to load
- **Unknown** ❓ - Health check not yet performed

Health status is visible in:
- Component Registry admin list
- Version history
- Rollback options

## Rollback System

The system maintains the last 3 installed versions for each component.

### Automatic Rollback

If a health check fails after update, manual rollback is required (automatic rollback not yet implemented).

### Manual Rollback

**Via Admin:**
1. Go to Component Registry
2. Select component
3. View "Rollback Versions" field
4. Note the version you want
5. Use management command to rollback

**Via Command Line:**
```bash
./shop_venv/bin/python manage.py rollback_component logo 1.0.0
```

### Rollback Limitations

- Only last 3 versions are kept
- Older versions have `rollback_available=False`
- Cannot rollback locked components
- Dependencies are not automatically downgraded

## Update Logs

Complete audit trail of all update operations:

**Tracked Actions:**
- Install
- Update
- Rollback
- Uninstall
- Health Check

**Logged Information:**
- Start and completion timestamps
- Duration
- Status (in_progress, completed, failed)
- Old and new versions
- Error messages and tracebacks
- Initiated by (user or auto-update)

Access logs at: `/en/admin/component_updates/updatelog/`

## Dependency Management

Components can declare dependencies on other components:

```python
from component_updates.models import ComponentDependency, ComponentRegistry

# Add dependency
component = ComponentRegistry.objects.get(slug='mega-menu')
required = ComponentRegistry.objects.get(slug='logo')

ComponentDependency.objects.create(
    component=component,
    depends_on=required,
    version_constraint='>=1.0.0',
    is_required=True
)
```

The system validates dependencies before installation:
- Missing dependencies are reported
- Version constraints are checked
- Installation fails if required dependencies not met

## Scheduled Updates

### Using Django-Cron

Add to your cron configuration:

```python
# core/cron.py
from django_cron import CronJobBase, Schedule
from component_updates.services import UpdateManager

class CheckComponentUpdates(CronJobBase):
    RUN_EVERY_MINS = 60 * 24  # Daily

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'component_updates.check_updates'

    def do(self):
        manager = UpdateManager()
        result = manager.check_for_updates()

        # Auto-install security updates
        for update in result['updates']:
            if update.get('critical') and update['component'].auto_update:
                manager.install_update(update['component'])
```

### Using Celery

```python
# component_updates/tasks.py
from celery import shared_task
from .services import UpdateManager

@shared_task
def check_component_updates():
    manager = UpdateManager()
    return manager.check_for_updates()

@shared_task
def install_component_update(component_id, version=None):
    from .models import ComponentRegistry
    component = ComponentRegistry.objects.get(id=component_id)
    manager = UpdateManager()
    return manager.install_update(component, version)
```

## Troubleshooting

### Authentication Errors

**Problem:** `UpdateAuthenticationError: Authentication failed`

**Solutions:**
1. Check server URL is correct
2. Verify license key is valid
3. Check internet connectivity
4. Review update server logs

### Download Failures

**Problem:** `UpdateDownloadError: Download failed`

**Solutions:**
1. Check network connectivity
2. Verify sufficient disk space
3. Check file permissions
4. Review firewall settings

### Installation Errors

**Problem:** `UpdateInstallError: Installation failed`

**Solutions:**
1. Check file permissions
2. Verify component package integrity
3. Check dependencies are satisfied
4. Review installation logs in UpdateLog
5. Try rollback to previous version

### Health Check Failures

**Problem:** Component shows "Unhealthy" status

**Solutions:**
1. Check error logs
2. Verify all files extracted correctly
3. Check template syntax
4. Verify static files collected
5. Rollback to previous version

## API Reference

### UpdateManager

Main service class for managing updates.

#### Methods

**`check_for_updates(component=None)`**
- Check for available updates from server
- Args: component (optional) - specific component to check
- Returns: Dict with update information

**`download_component(component, version)`**
- Download component package from server
- Args: component, version
- Returns: Path to downloaded file

**`install_update(component, version=None)`**
- Install update for component
- Args: component, version (optional, defaults to latest)
- Returns: bool - success status

**`rollback(component, target_version=None)`**
- Rollback component to previous version
- Args: component, target_version (optional)
- Returns: bool - success status

**`check_dependencies(component, version)`**
- Check if dependencies are satisfied
- Args: component, version
- Returns: Tuple (bool, List[str]) - satisfied status and issues

## Future Enhancements

### Phase 2 (Planned)
- [ ] Enhanced dependency resolution
- [ ] Delta updates (patch-based)
- [ ] Update scheduling
- [ ] Automatic rollback on health check failure

### Phase 3 (Planned)
- [ ] CDN distribution for faster downloads
- [ ] Multi-region update servers
- [ ] Component marketplace integration
- [ ] Update approval workflows

### Phase 4 (Planned)
- [ ] A/B testing for updates
- [ ] Gradual rollout (canary deployments)
- [ ] Update analytics dashboard
- [ ] Custom update channels

## Contributing

To add update support for a new component type:

1. Add component type to `ComponentRegistry.COMPONENT_TYPES`
2. Add OneToOne field linking to component model
3. Implement `_install_{type}_package()` method in UpdateManager
4. Add health check logic in `_health_check()`
5. Update documentation

## License

This component is part of the Shop Platform and follows the platform's licensing terms.

## Support

For issues or questions:
- Check the Update Logs for error details
- Review this documentation
- Check server connection status in UpdateServerConfig
- Contact platform support with Installation UUID
