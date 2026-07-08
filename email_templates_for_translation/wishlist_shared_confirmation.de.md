---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ Ihre Wunschliste wurde geteilt - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ Wunschliste erfolgreich geteilt!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihre Wunschliste mit {{ wishlist_item_count }} Artikel{{ wishlist_item_count|pluralize }} wurde erfolgreich geteilt. Andere können Ihre Wunschliste jetzt mit dem untenstehenden Link ansehen.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Teilen-Link:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Link kopieren
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Was wird geteilt:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • Der Name Ihrer Wunschliste (falls festgelegt)<br/>
          • {{ wishlist_item_count }} Produkt{{ wishlist_item_count|pluralize }}<br/>
          • Produktbezeichnungen, Bilder und Preise<br/>
          • Kauf-Links für jedes Produkt
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 Ideal zum Teilen mit Freunden und Familie für Geschenke und besondere Anlässe!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Meine Wunschliste verwalten
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Möchten Sie das Teilen beenden? Sie können den Teilen-Link jederzeit in Ihren <a href="{{ wishlist_settings_url }}">Wunschlisten-Einstellungen</a> deaktivieren.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ WISHLIST SHARED SUCCESSFULLY!

Hi {{ customer_name }},

Ihre Wunschliste mit {{ wishlist_item_count }} Artikel{{ wishlist_item_count|pluralize }} wurde erfolgreich geteilt. Andere können Ihre Wunschliste jetzt mit dem untenstehenden Link ansehen.

SHARE LINK:
{{ share_url }}

WHAT'S SHARED:
• Der Name Ihrer Wunschliste (falls festgelegt)
• {{ wishlist_item_count }} Produkt{{ wishlist_item_count|pluralize }}
• Produktbezeichnungen, Bilder und Preise
• Kauf-Links für jedes Produkt

💡 Ideal zum Teilen mit Freunden und Familie für Geschenke und besondere Anlässe!

Manage my wishlist: {{ wishlist_url }}

Möchten Sie das Teilen beenden? Sie können den Teilen-Link jederzeit in Ihren Wunschlisten-Einstellungen deaktivieren: {{ wishlist_settings_url }}