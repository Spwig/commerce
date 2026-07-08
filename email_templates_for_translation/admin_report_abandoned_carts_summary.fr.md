---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 Rapport des paniers abandonnés - {{ abandoned_count }} paniers ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Rapport des paniers abandonnés
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Résumé de l'abandon de panier
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Période :</strong> {{ report_period }}<br/>
              <strong>Paniers abandonnés :</strong> {{ abandoned_count }}<br/>
              <strong>Valeur abandonnée :</strong> <span style="font-size: 18px; color: #dc2626;">{{ abandoned_value }}</span><br/>
              <strong>Taux d'abandon :</strong> {{ abandonment_rate }}%<br/>
              <strong>Taux de récupération :</strong> {{ recovery_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Top Reasons (if tracked):
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ top_reasons }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir les détails
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 RAPPORT DES PANIERS ABANDONNÉS

Résumé de l'abandon de panier

MÉTRIQUES:
- Période : {{ report_period }}
- Paniers abandonnés : {{ abandoned_count }}
- Valeur abandonnée : {{ abandoned_value }}
- Taux d'abandon : {{ abandonment_rate }}%
- Taux de récupération : {{ recovery_rate }}%

TOP REASONS:
{{ top_reasons }}

Voir les détails: {{ full_report_url }}