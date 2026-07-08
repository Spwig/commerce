---
template_type: pos_daily_z_report
category: POS
---

# Email Template: pos_daily_z_report

## Subject
📊 Rapport quotidien Z - {{ report_date }} - {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Rapport quotidien Z
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Rapport de réglement de fin de journée
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Résumé quotidien pour {{ location_name }} du {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Résumé des ventes:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total des ventes:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_sales }}</span><br/>
              <strong>Transactions:</strong> {{ transaction_count }}<br/>
              <strong>Articles vendus:</strong> {{ items_sold }}<br/>
              <strong>Vente moyenne:</strong> {{ average_sale }}<br/>
              <strong>Taxes collectées:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Méthodes de paiement:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} transactions)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Résumé des shifts:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total des shifts:</strong> {{ shift_count }}<br/>
              <strong>Terminals utilisés:</strong> {{ terminal_count }}<br/>
              <strong>Cashiers actifs:</strong> {{ cashier_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% for terminal in terminal_stats %}
        <mj-spacer height="15px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ terminal.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Ventes: {{ terminal.sales }} | Transactions: {{ terminal.transactions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ajustements et remises:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Remises accordées:</strong> {{ discounts_total }}<br/>
              <strong>Remboursements émis:</strong> {{ refunds_total }}<br/>
              <strong>Annulations:</strong> {{ voids_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cash_variance != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Variance totale de trésorerie: {{ cash_variance }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              {{ variance_note }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Produits les plus vendus:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.quantity }} vendus ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir le rapport complet
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 RAPPORT QUOTIDIEN Z

Rapport de réglement de fin de journée

Résumé quotidien pour {{ location_name }} du {{ report_date }}.

RÉSUMÉ DES VENTES:
- Total des ventes: {{ total_sales }}
- Transactions: {{ transaction_count }}
- Articles vendus: {{ items_sold }}
- Vente moyenne: {{ average_sale }}
- Taxes collectées: {{ tax_collected }}

MÉTHODES DE PAIEMENT:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} transactions)
{% endfor %}

RÉSUMÉ DES SHIFTS:
- Total des shifts: {{ shift_count }}
- Terminals utilisés: {{ terminal_count }}
- Cashiers actifs: {{ cashier_count }}

DÉCOMPOSITION DES TERMINAUX:
{% for terminal in terminal_stats %}
{{ terminal.name }}: {{ terminal.sales }} | {{ terminal.transactions }} transactions
{% endfor %}

AJUSTEMENTS & REMISES:
- Remises accordées: {{ discounts_total }}
- Remboursements émis: {{ refunds_total }}
- Annulations: {{ voids_total }}

{% if cash_variance != 0 %}
⚠️ VARIANCE TOTALE DE TRÉSORERIE: {{ cash_variance }}
{{ variance_note }}
{% endif %}

TOP SELLING PRODUCTS:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.quantity }} vendus ({{ product.revenue }})
{% endfor %}

Voir le rapport complet: {{ full_report_url }}