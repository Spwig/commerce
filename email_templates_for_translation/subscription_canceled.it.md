---
template_type: subscription_canceled
category: Subscriptions
---

# Email Template: subscription_canceled

## Subject
❌ La tua sottoscrizione {{ plan_name }} è stata annullata - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Siamo dispiaciuti di vederti andare via
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          La tua sottoscrizione è stata annullata
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Cancellation Details Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px" border="2px solid {{ theme.color.text_muted|default:'#6b7280' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
                Riepilogo Annullamento
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Piano:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Annullato il:</strong> {{ cancellation_date|date:"F d, Y" }}
              </mj-text>

              {% if access_until %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Accesso fino a:</strong> {{ access_until|date:"F d, Y" }}
              </mj-text>
              <mj-text font-size="13px" color="{{ theme.color.success|default:'#10b981' }}" padding="10px 0 5px 0">
                ✓ Hai ancora accesso ai tuoi vantaggi fino a {{ access_until|date:"F d, Y" }}
              </mj-text>
              {% else %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Stato:</strong> Annullato immediatamente
              </mj-text>
              {% endif %}
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What This Means Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Cosa Questo Significa
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          Non sarai addebitato nuovamente
        </mj-text>

        {% if access_until %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          Puoi continuare a utilizzare i tuoi vantaggi fino a {{ access_until|date:"F d, Y" }}
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          Il tuo accesso è terminato immediatamente
        </mj-text>
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          Puoi riattivare la sottoscrizione in qualsiasi momento
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Feedback Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px 15px 20px" line-height="1.6" align="center">
          Saremmo felici di ricevere il tuo feedback per aiutarci a migliorare.
        </mj-text>
        <mj-button href="{{ feedback_url }}" background-color="{{ theme.color.text_muted|default:'#6b7280' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="14px" font-weight="600" border-radius="6px" padding="12px 28px">
          Condividi Feedback
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Reactivate CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px 15px 20px" line-height="1.6" align="center">
          Cambiato idea? Puoi riattivare la tua sottoscrizione in qualsiasi momento.
        </mj-text>
        <mj-button href="{{ reactivate_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Riattiva Sottoscrizione
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Hai bisogno di aiuto? Contattaci a {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Powered by Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Siamo dispiaciuti di vederti andare via

La tua sottoscrizione è stata annullata

RIEPILOGO ANNULLAMENTO:
Plan: {{ plan_name }}
Canceled On: {{ cancellation_date|date:"F d, Y" }}
{% if access_until %}Access Until: {{ access_until|date:"F d, Y" }}

✓ Hai ancora accesso ai tuoi vantaggi fino a {{ access_until|date:"F d, Y" }}
{% else %}Status: Annullato immediatamente
{% endif %}

Cosa Questo Significa:
• Non sarai addebitato nuovamente
{% if access_until %}• Puoi continuare a utilizzare i tuoi vantaggi fino a {{ access_until|date:"F d, Y" }}
{% else %}• Il tuo accesso è terminato immediatamente
{% endif %}• Puoi riattivare la sottoscrizione in qualsiasi momento

Saremmo felici di ricevere il tuo feedback per aiutarci a migliorare.
Condividi Feedback: {{ feedback_url }}

Cambiato idea? Puoi riattivare la tua sottoscrizione in qualsiasi momento.
Riattiva Sottoscrizione: {{ reactivate_url }}

Hai bisogno di aiuto? Contattaci a {{ support_email }}

---
Powered by Spwig - https://spwig.com