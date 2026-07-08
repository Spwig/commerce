---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 Relatório de Turno: {{ terminal_name }} - {{ shift_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Turno Fechado
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Relatório Resumo do Turno
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Turno fechado no {{ terminal_name }} por {{ cashier_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Turno:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Caixa:</strong> {{ cashier_name }}<br/>
              <strong>Iniciado:</strong> {{ shift_started }}<br/>
              <strong>Encerrado:</strong> {{ shift_ended }}<br/>
              <strong>Duração:</strong> {{ shift_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Resumo das Vendas:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Vendas Totais:</strong> {{ total_sales }}<br/>
              <strong>Transações:</strong> {{ transaction_count }}<br/>
              <strong>Itens Vendidos:</strong> {{ items_sold }}<br/>
              <strong>Venda Média:</strong> {{ average_sale }}<br/>
              <strong>Taxa Coletada:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Detalhes dos Pagamentos:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} transações)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Reconciliação de Dinheiro:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Dinheiro Inicial:</strong> {{ opening_cash }}<br/>
              <strong>Vendas em Dinheiro:</strong> {{ cash_sales }}<br/>
              <strong>Dinheiro Esperado:</strong> {{ expected_cash }}<br/>
              <strong>Dinheiro Contado:</strong> {{ counted_cash }}<br/>
              <strong>Diferença:</strong> <span style="color: {{ cash_difference_color }};">{{ cash_difference }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        {% if discrepancy_amount != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Diferença de Dinheiro: {{ discrepancy_amount }}
            </mj-text>
            {% if discrepancy_note %}
            <mj-text font-size="14px" color="#92400e">
              Nota: {{ discrepancy_note }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Relatório Completo
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 TURNO FECHADO

Relatório Resumo do Turno

Turno fechado no {{ terminal_name }} por {{ cashier_name }}.

DETALHES DO TURNO:
- Terminal: {{ terminal_name }}
- Caixa: {{ cashier_name }}
- Iniciado: {{ shift_started }}
- Encerrado: {{ shift_ended }}
- Duração: {{ shift_duration }}

RESUMO DAS VENDAS:
- Vendas Totais: {{ total_sales }}
- Transações: {{ transaction_count }}
- Itens Vendidos: {{ items_sold }}
- Venda Média: {{ average_sale }}
- Taxa Coletada: {{ tax_collected }}

DETALHES DOS PAGAMENTOS:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} transações)
{% endfor %}

RECONCILIAÇÃO DE DINHEIRO:
- Dinheiro Inicial: {{ opening_cash }}
- Vendas em Dinheiro: {{ cash_sales }}
- Dinheiro Esperado: {{ expected_cash }}
- Dinheiro Contado: {{ counted_cash }}
- Diferença: {{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ DIFERENÇA DE DINHEIRO: {{ discrepancy_amount }}
{% if discrepancy_note %}Nota: {{ discrepancy_note }}{% endif %}
{% endif %}

Ver relatório completo: {{ shift_report_url }}