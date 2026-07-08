---
template_type: loyalty_points_expiring
category: Loyalty Program
---

# Email Template: loyalty_points_expiring

## Subject
Ricordo: {{ expiring_points }} punti che scadranno presto

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}" align="center">
          ⏰ Punti che scadranno presto
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Points Display -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center">
          {{ expiring_points }}
        </mj-text>
        <mj-text font-size="18px" color="#856404" align="center">
          punti scadono in {{ days_until_expiration }} giorni
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center">
          Data di scadenza: {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Ciao {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Non lasciare che i tuoi punti vadano perduti! Hai {{ expiring_points }} punti che scadranno presto.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Riscatta ora per ottenere premi esclusivi prima che scompaiano.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Suggested Rewards -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Premi che puoi ottenere:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          Esplora il catalogo dei premi e riscatta i tuoi punti prima che scadano.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ rewards_url }}">
          Riscatta i Punti Ora
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ricordo: {{ expiring_points }} punti che scadranno presto

Ciao {{ customer_name }},

Non lasciare che i tuoi punti vadano perduti! Hai {{ expiring_points }} punti che scadranno in {{ days_until_expiration }} giorni.

Data di scadenza: {{ expiration_date }}

Riscatta ora per ottenere premi esclusivi prima che scompaiano.

Riscatta i punti: {{ rewards_url }}

{{ shop_name }}