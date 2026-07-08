# Language Management Section Implementation Plan

## Overview
Build a comprehensive language management section for admins to configure which languages their site supports, with intelligent warnings based on available translation models.

## Database Schema

### 1. New Model: `SiteLanguage`
```python
class SiteLanguage(models.Model):
    code = models.CharField(max_length=10, unique=True)  # e.g., 'en', 'es', 'zh-CN'
    name = models.CharField(max_length=100)  # e.g., 'English', 'Spanish'
    native_name = models.CharField(max_length=100)  # e.g., 'Español', '中文'
    is_active = models.BooleanField(default=False)  # Selected for site translation
    is_default = models.BooleanField(default=False)  # Site default language

    # Model support
    m2m100_support = models.CharField(choices=['full', 'limited', 'none'])
    nllb_support = models.CharField(choices=['full', 'limited', 'none'])
    requires_nllb = models.BooleanField(default=False)

    # Ordering
    order = models.IntegerField(default=0)  # For drag-and-drop ordering

    # Metadata
    rtl = models.BooleanField(default=False)  # Right-to-left language
    date_format = models.CharField(max_length=50, default='Y-m-d')
    time_format = models.CharField(max_length=50, default='H:i:s')
```

## UI Components

### 1. Language Management Page (`/admin/translations/languages/`)
- **Two-column drag interface:**
  - Left: Available Languages (searchable, filterable by model support)
  - Right: Active Languages (drag to reorder)
- **Drag languages between columns to activate/deactivate**
- **Visual indicators:**
  - Green checkmark: Full M2M100 support
  - Orange warning: Limited M2M100 support (suggest 1.2B model)
  - Red exclamation: Requires NLLB installation
  - Blue info: External provider recommended

### 2. CSS Styling (`translations/static/translations/admin/css/languages.css`)
```css
.language-manager {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.language-list {
    min-height: 400px;
    border: 2px dashed var(--border-color);
    border-radius: 8px;
    padding: 15px;
}

.language-item {
    padding: 10px 15px;
    margin: 5px 0;
    background: var(--body-bg);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    cursor: move;
    display: flex;
    align-items: center;
    gap: 10px;
}

.language-item.dragging {
    opacity: 0.5;
}

.language-item.drag-over {
    background: var(--selected-bg);
}

.language-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.indicator-full { background: #28a745; }
.indicator-limited { background: #ffc107; }
.indicator-nllb { background: #dc3545; }
```

### 3. JavaScript Drag & Drop (`translations/static/translations/admin/js/languages.js`)
```javascript
class LanguageManager {
    constructor() {
        this.initDragAndDrop();
        this.initSearch();
        this.initFilters();
        this.loadLanguages();
    }

    initDragAndDrop() {
        // Sortable.js for drag and drop
        // Handle drag between available and active lists
        // Update order on drop
        // Show visual feedback
    }

    saveConfiguration() {
        // AJAX save active languages and order
        // Update django-parler configuration
        // Trigger model compatibility check
    }

    checkModelRequirements(languageCode) {
        // Check if language needs NLLB
        // Show appropriate warnings
        // Suggest model downloads
    }
}
```

## API Endpoints

### 1. `/api/languages/` - List all languages
```python
def languages_list_view(request):
    # Return all available languages with model support info
    # Include current active status
```

### 2. `/api/languages/activate/` - Activate/deactivate languages
```python
def languages_activate_view(request):
    # Update active languages
    # Reconfigure django-parler
    # Check model compatibility
```

### 3. `/api/languages/reorder/` - Reorder languages
```python
def languages_reorder_view(request):
    # Update language ordering
    # This affects language switcher display
```

### 4. `/api/languages/check-compatibility/` - Check model compatibility
```python
def check_language_compatibility_view(request):
    # Check which models support selected languages
    # Return warnings and suggestions
```

## Integration Points

### 1. Django-Parler Configuration
- Dynamically update `PARLER_LANGUAGES` setting
- Create migration to sync with database
- Update translation fields in models

### 2. Page Builder Integration
- Add language selector to translatable fields
- Show only active languages
- Add "Translate" button for AI translation

### 3. Model Compatibility Warnings
```python
LANGUAGE_WARNINGS = {
    'limited_m2m100': [
        'ast', 'ba', 'br', 'ceb', 'ff', 'fy', 'gd', 'ha',
        'ig', 'ilo', 'lb', 'lg', 'ln', 'mg', 'ns', 'oc',
        'or', 'ps', 'sd', 'ss', 'su', 'sw', 'tl', 'tn',
        'wo', 'xh', 'yi', 'yo', 'zu'
    ],
    'nllb_only': [
        'te_IN', 'gl_ES', 'sl_SI'  # Telugu, Galician, Slovene
    ]
}
```

## Available Languages

### M2M100 Supported Languages (100 languages)
Afrikaans (af), Amharic (am), Arabic (ar), Asturian (ast), Azerbaijani (az), Bashkir (ba), Belarusian (be), Bulgarian (bg), Bengali (bn), Breton (br), Bosnian (bs), Catalan; Valencian (ca), Cebuano (ceb), Czech (cs), Welsh (cy), Danish (da), German (de), Greek (el), English (en), Spanish (es), Estonian (et), Persian (fa), Fulah (ff), Finnish (fi), French (fr), Western Frisian (fy), Irish (ga), Gaelic; Scottish Gaelic (gd), Galician (gl), Gujarati (gu), Hausa (ha), Hebrew (he), Hindi (hi), Croatian (hr), Haitian; Haitian Creole (ht), Hungarian (hu), Armenian (hy), Indonesian (id), Igbo (ig), Iloko (ilo), Icelandic (is), Italian (it), Japanese (ja), Javanese (jv), Georgian (ka), Kazakh (kk), Central Khmer (km), Kannada (kn), Korean (ko), Luxembourgish; Letzeburgesch (lb), Ganda (lg), Lingala (ln), Lao (lo), Lithuanian (lt), Latvian (lv), Malagasy (mg), Macedonian (mk), Malayalam (ml), Mongolian (mn), Marathi (mr), Malay (ms), Burmese (my), Nepali (ne), Dutch; Flemish (nl), Norwegian (no), Northern Sotho (ns), Occitan (post 1500) (oc), Oriya (or), Panjabi; Punjabi (pa), Polish (pl), Pushto; Pashto (ps), Portuguese (pt), Romanian; Moldavian; Moldovan (ro), Russian (ru), Sindhi (sd), Sinhala; Sinhalese (si), Slovak (sk), Slovenian (sl), Somali (so), Albanian (sq), Serbian (sr), Swati (ss), Sundanese (su), Swedish (sv), Swahili (sw), Tamil (ta), Thai (th), Tagalog (tl), Tswana (tn), Turkish (tr), Ukrainian (uk), Urdu (ur), Uzbek (uz), Vietnamese (vi), Wolof (wo), Xhosa (xh), Yiddish (yi), Yoruba (yo), Chinese (zh), Zulu (zu)

### NLLB Additional Languages
- Telugu (te_IN)
- Galician (gl_ES)
- Slovene (sl_SI)

Plus enhanced support for all M2M100 languages with regional variants.

## Implementation Steps

1. **Create SiteLanguage model and migration**
2. **Populate initial language data from M2M100 and NLLB lists**
3. **Build language management view and templates**
4. **Implement drag-and-drop JavaScript**
5. **Create API endpoints for language operations**
6. **Add model compatibility checking**
7. **Integrate with django-parler configuration**
8. **Update page builder to use active languages**
9. **Add translation triggers in admin forms**
10. **Create management command to sync languages**

## Files to Create/Modify

### New Files:
- `translations/models.py` - Add SiteLanguage model
- `translations/views.py` - Add language management views
- `translations/templates/admin/translations/languages.html`
- `translations/static/translations/admin/css/languages.css`
- `translations/static/translations/admin/js/languages.js`
- `translations/management/commands/populate_languages.py`

### Modified Files:
- `translations/urls.py` - Add new endpoints
- `translations/admin.py` - Register SiteLanguage admin
- `core/settings.py` - Dynamic PARLER_LANGUAGES
- `page_builder/admin.py` - Add translation UI
- `templates/admin/translations/dashboard.html` - Add languages link

## Security Considerations
- Staff member required for all language management
- CSRF protection on all state-changing operations
- Validate language codes against known list
- Prevent deletion of default language

## Performance Considerations
- Cache active languages list
- Lazy load language data in UI
- Batch update operations
- Use select_related for language queries