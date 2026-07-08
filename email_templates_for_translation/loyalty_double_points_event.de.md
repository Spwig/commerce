---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 Doppelte Punkte-Event jetzt starten! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 2X PUNKTE-EVENT!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Exklusiv für Treuekunden!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Mach dich bereit, große Punkte zu verdienen! Für eine begrenzte Zeit erhälst du {{ points_multiplier }}X Punkte bei jedem Kauf.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              Erhalte {{ points_multiplier }}X Punkte
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              Bei allen Käufen<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Beispielhafte Gewinne:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Ausgaben von $50 → Erhalte {{ example_points_normal }} Punkte normalerweise<br/>
              <strong style="color: #047857;">Während dieses Events → Erhalte {{ example_points_bonus }} Punkte! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Ausgaben von $100 → Erhalte {{ example_points_normal_2 }} Punkte normalerweise<br/>
              <strong style="color: #047857;">Während dieses Events → Erhalte {{ example_points_bonus_2 }} Punkte! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Dein aktueller Kontostand:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Punkte:</strong> {{ current_points }} Punkte<br/>
          <strong>Kundenstufe:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Jetzt einkaufen & {{ points_multiplier }}X Punkte verdienen
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          Das Event endet {{ event_end }} - Verpassen Sie es nicht!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 2X PUNKTE-EVENT!
{{ event_start }} - {{ event_end }}

Exklusiv für Treuekunden!

Hi {{ customer_name }},

Mach dich bereit, große Punkte zu verdienen! Für eine begrenzte Zeit erhälst du {{ points_multiplier }}X Punkte bei jedem Kauf.

ERHALTE {{ points_multiplier }}X PUNKTE
Bei allen Käufen
{{ event_start }} - {{ event_end }}

BEISPIELHAFTEN GEWINNE:
- Ausgaben von $50 → Erhalte {{ example_points_normal }} Punkte normalerweise
  Während dieses Events → Erhalte {{ example_points_bonus }} Punkte! 🎉

- Ausgaben von $100 → Erhalte {{ example_points_normal_2 }} Punkte normalerweise
  Während dieses Events → Erhalte {{ example_points_bonus_2 }} Punkte! 🎉

DEIN AKTUELLER KONTOSTAND:
- Punkte: {{ current_points }} Punkte
- Kundenstufe: {{ loyalty_tier }}

Jetzt einkaufen & {{ points_multiplier }}X Punkte verdienen: {{ shop_url }}

Das Event endet {{ event_end }} - Verpassen Sie es nicht!