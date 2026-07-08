# Affiliate App Translations

## Supported Languages
- **English (en)** - Primary language
- **Spanish (es)** - Español
- **French (fr)** - Français
- **German (de)** - Deutsch
- **Japanese (jp)** - 日本語
- **Portuguese (pt)** - Português
- **Chinese Simplified (zh-hans)** - 简体中文

## Translation Guidelines

### 1. Key Naming Conventions
All translation keys must follow this format:
```
{app}_{model/feature}_{field/action}_{context}
```

**Examples:**
```python
# Model fields
affiliate_program_name = "Program Name"
affiliate_commission_rate = "Commission Rate"

# Actions
affiliate_payout_approve_action = "Approve Payout"
affiliate_link_generate_action = "Generate Link"

# UI elements
affiliate_stats_clicks_label = "Total Clicks"
affiliate_portal_welcome_message = "Welcome to Affiliate Portal"

# Status labels
affiliate_commission_pending = "Pending"
affiliate_commission_approved = "Approved"
```

### 2. Using Translations in Code

#### In Python (models, views, forms)
```python
from django.utils.translation import gettext_lazy as _

class Program(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_("program name")
    )

    class Meta:
        verbose_name = _("affiliate program")
        verbose_name_plural = _("affiliate programs")
```

#### In Templates - Simple strings
```django
{% load i18n %}
<h1>{% trans "Affiliate Dashboard" %}</h1>
```

#### In Templates - With context hints
```django
{% trans "Order" context "noun" %}  {# Not the verb "to order" #}
{% trans "Program" context "affiliate program" %}
```

#### In Templates - With variables
```django
{% blocktrans with name=program.name %}
    Welcome to {{ name }}!
{% endblocktrans %}
```

#### In Templates - Pluralization
```django
{% blocktrans count counter=clicks %}
    {{ counter }} click
{% plural %}
    {{ counter }} clicks
{% endblocktrans %}
```

### 3. Generating Translation Files

#### Create .po files for all languages
```bash
# From the Spwig repo root
./shop_venv/bin/python manage.py makemessages -l es -l fr -l de -l jp -l pt -l zh-hans
```

#### Create .po files for specific app
```bash
cd affiliate
../shop_venv/bin/python ../manage.py makemessages -l es -l fr -l de -l jp -l pt -l zh-hans
```

#### Update existing .po files
```bash
./shop_venv/bin/python manage.py makemessages -a  # All languages
```

### 4. Compiling Translations
After editing .po files, compile them to .mo files:
```bash
./shop_venv/bin/python manage.py compilemessages
```

### 5. Translation File Location
```
affiliate/locale/
├── en/LC_MESSAGES/
│   ├── django.po
│   └── django.mo
├── es/LC_MESSAGES/
│   ├── django.po
│   └── django.mo
├── fr/LC_MESSAGES/
│   ├── django.po
│   └── django.mo
├── de/LC_MESSAGES/
│   ├── django.po
│   └── django.mo
├── jp/LC_MESSAGES/
│   ├── django.po
│   └── django.mo
├── pt/LC_MESSAGES/
│   ├── django.po
│   └── django.mo
└── zh-hans/LC_MESSAGES/
    ├── django.po
    └── django.mo
```

### 6. Testing Translations

#### Test specific language in browser
Add `?lang=es` to URL or set language preference in admin.

#### Test specific language in shell
```python
from django.utils import translation
translation.activate('es')
from django.utils.translation import gettext as _
print(_("affiliate program"))
```

### 7. Common Translation Keys

Here are the most commonly used translation keys in the Affiliate app:

```python
# Models
_("affiliate program")
_("affiliate")
_("tracking link")
_("click")
_("conversion")
_("commission")
_("payout")

# Fields
_("name")
_("email")
_("status")
_("amount")
_("rate")
_("created at")
_("updated at")

# Actions
_("create")
_("edit")
_("delete")
_("approve")
_("reject")
_("generate link")

# Status
_("pending")
_("approved")
_("rejected")
_("paid")
_("active")
_("inactive")

# Navigation
_("dashboard")
_("statistics")
_("links")
_("commissions")
_("payouts")
_("settings")

# Messages
_("successfully created")
_("successfully updated")
_("successfully deleted")
_("error occurred")
```

### 8. Date and Number Formatting

Django automatically handles locale-specific formatting:

```django
{% load i18n l10n %}

{# Date formatting #}
{{ program.created_at|date:"SHORT_DATE_FORMAT" }}

{# Number formatting #}
{{ commission.amount|floatformat:2 }}

{# Currency (using locale) #}
{{ payout.amount|floatformat:2 }} {{ CURRENCY_CODE }}
```

### 9. Right-to-Left (RTL) Language Support

If adding Arabic or Hebrew in the future:

```django
{% load i18n %}
<html lang="{{ LANGUAGE_CODE }}" dir="{% if LANGUAGE_BIDI %}rtl{% else %}ltr{% endif %}">
```

### 10. Translation Best Practices

✅ **DO:**
- Always mark user-facing text for translation
- Use descriptive keys: `affiliate_program_name` not `field1`
- Include context hints when meaning is ambiguous
- Test all translations before deployment
- Keep strings short and clear
- Use variables for dynamic content

❌ **DON'T:**
- Hardcode any user-facing text
- Use generic keys like `label_1`, `text_2`
- Split sentences across multiple translation strings
- Include HTML in translation strings (when possible)
- Forget to compile messages after editing .po files

### 11. Workflow Summary

1. **Write Code** with `_()` or `{% trans %}`
2. **Generate .po files**: `makemessages`
3. **Edit .po files** with translations
4. **Compile to .mo**: `compilemessages`
5. **Test** in different languages
6. **Commit** both .po and .mo files

### 12. Translation Resources

- **Django i18n docs**: https://docs.djangoproject.com/en/stable/topics/i18n/
- **gettext format**: https://www.gnu.org/software/gettext/manual/gettext.html
- **Translation tools**:
  - Poedit (https://poedit.net/)
  - Lokalize (for KDE)
  - Online: Transifex, Crowdin

### 13. Example .po File Entry

```po
#: affiliate/models.py:45
msgid "affiliate program"
msgstr "programa de afiliados"

#: affiliate/templates/affiliate/portal/dashboard.html:12
#, python-format
msgid "Welcome, %(name)s!"
msgstr "¡Bienvenido, %(name)s!"

#: affiliate/views.py:89
msgctxt "affiliate commission"
msgid "pending"
msgstr "pendiente"
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Create translations | `./shop_venv/bin/python manage.py makemessages -l es` |
| Update translations | `./shop_venv/bin/python manage.py makemessages -a` |
| Compile translations | `./shop_venv/bin/python manage.py compilemessages` |
| Test language | Add `?lang=es` to URL |
| Activate in code | `translation.activate('es')` |

---

**Last Updated**: October 19, 2025
**Maintained By**: Shop Platform Team
