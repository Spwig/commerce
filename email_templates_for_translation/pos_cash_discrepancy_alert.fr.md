---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ Écart de trésorerie : {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Écart de trésorerie détecté
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alerte de variance de trésorerie
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Un écart de trésorerie de {{ discrepancy_amount }} a été détecté lors de la fermeture du shift sur {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de l'écart:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Caisse:</strong> {{ cashier_name }}<br/>
              <strong>Date du shift:</strong> {{ shift_date }}<br/>
              <strong>Durée du shift:</strong> {{ shift_duration }}<br/>
              <strong>Détecté:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Comptage de la trésorerie:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>Trésorerie prévue:</strong> {{ expected_cash }}<br/>
              <strong>Trésorerie comptée:</strong> {{ counted_cash }}<br/>
              <strong>Écart:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Trésorerie initiale:</strong> {{ opening_cash }}<br/>
              <strong>Ventes en espèces:</strong> {{ cash_sales }}<br/>
              <strong>Remboursements en espèces:</strong> {{ cash_refunds }}<br/>
              <strong>Trésorerie versée:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Note de la caissière:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              "{{ cashier_note }}"
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions recommandées:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Vérifier l'historique des transactions pour des erreurs<br/>
          2. Vérifier les paiements en espèces non enregistrés<br/>
          3. Vérifier que le comptage de la trésorerie était exact<br/>
          4. Documenter l'écart dans les notes du shift<br/>
          5. Suivre en cas de besoin avec la caissière
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir le rapport de shift
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Vérifier les transactions
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ÉCART DE TRÉSORERIE DÉTECTÉ

Alerte de variance de trésorerie

Un écart de trésorerie de {{ discrepancy_amount }} a été détecté lors de la fermeture du shift sur {{ terminal_name }}.

DÉTAILS DE L'ÉCART:
- Terminal: {{ terminal_name }}
- Caisse: {{ cashier_name }}
- Date du shift: {{ shift_date }}
- Durée du shift: {{ shift_duration }}
- Détecté: {{ detected_at }}

COMPTAGE DE LA TRÉSORERIE:
- Trésorerie prévue: {{ expected_cash }}
- Trésorerie comptée: {{ counted_cash }}
- Écart: {{ discrepancy_amount }}

DÉTAILS:
- Trésorerie initiale: {{ opening_cash }}
- Ventes en espèces: {{ cash_sales }}
- Remboursements en espèces: {{ cash_refunds }}
- Trésorerie versée: {{ cash_paid_out }}

{% if cashier_note %}
NOTE DE LA CAISSIÈRE:
"{{ cashier_note }}"
{% endif %}

ACTIONS RECOMMANDÉES:
1. Vérifier l'historique des transactions pour des erreurs
2. Vérifier les paiements en espèces non enregistrés
3. Vérifier que le comptage de la trésorerie était exact
4. Documenter l'écart dans les notes du shift
5. Suivre en cas de besoin avec la caissière

Voir le rapport de shift: {{ shift_report_url }}
Vérifier les transactions: {{ transaction_history_url }}

