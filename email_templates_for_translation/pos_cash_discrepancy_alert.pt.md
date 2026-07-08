---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ Alerta de Diferença em Dinheiro: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Diferença em Dinheiro Detectada
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alerta de Variação em Dinheiro
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Uma diferença em dinheiro de {{ discrepancy_amount }} foi detectada ao fechar o turno em {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes da Diferença:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Caixa:</strong> {{ cashier_name }}<br/>
              <strong>Data do Turno:</strong> {{ shift_date }}<br/>
              <strong>Duração do Turno:</strong> {{ shift_duration }}<br/>
              <strong>Detectado:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Contagem em Dinheiro:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>Dinheiro Esperado:</strong> {{ expected_cash }}<br/>
              <strong>Dinheiro Contado:</strong> {{ counted_cash }}<br/>
              <strong>Diferença:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Dinheiro Inicial:</strong> {{ opening_cash }}<br/>
              <strong>Vendas em Dinheiro:</strong> {{ cash_sales }}<br/>
              <strong>Estornos em Dinheiro:</strong> {{ cash_refunds }}<br/>
              <strong>Dinheiro Pago:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nota do Caixa:
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
          Ações Recomendadas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Revisar histórico de transações para erros<br/>
          2. Verificar pagamentos em dinheiro não registrados<br/>
          3. Verificar se a contagem em dinheiro foi precisa<br/>
          4. Documentar a diferença nas anotações do turno<br/>
          5. Entrar em contato com o caixa, se necessário
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Relatório do Turno
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Revisar Transações
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ DIFERENÇA EM DINHEIRO DETECTADA

Alerta de Variação em Dinheiro

Uma diferença em dinheiro de {{ discrepancy_amount }} foi detectada ao fechar o turno em {{ terminal_name }}.

DETALHES DA DIFERENÇA:
- Terminal: {{ terminal_name }}
- Caixa: {{ cashier_name }}
- Data do Turno: {{ shift_date }}
- Duração do Turno: {{ shift_duration }}
- Detectado: {{ detected_at }}

CONTAGEM EM DINHEIRO:
- Dinheiro Esperado: {{ expected_cash }}
- Dinheiro Contado: {{ counted_cash }}
- Diferença: {{ discrepancy_amount }}

DECOMPOSIÇÃO:
- Dinheiro Inicial: {{ opening_cash }}
- Vendas em Dinheiro: {{ cash_sales }}
- Estornos em Dinheiro: {{ cash_refunds }}
- Dinheiro Pago: {{ cash_paid_out }}

{% if cashier_note %}
NOTA DO CAIXA:
"{{ cashier_note }}"
{% endif %}

AÇÕES RECOMENDADAS:
1. Revisar histórico de transações para erros
2. Verificar pagamentos em dinheiro não registrados
3. Verificar se a contagem em dinheiro foi precisa
4. Documentar a diferença nas anotações do turno
5. Entrar em contato com o caixa, se necessário

Ver relatório do turno: {{ shift_report_url }}
Revisar transações: {{ transaction_history_url }}
