---
template_type: admin_report_daily_sales
category: Admin Reports
---

# Email Template: admin_report_daily_sales

## Subject
📊 Relatório Diário de Vendas - {{ report_date }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Relatório Diário de Vendas
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Resumo das Vendas - {{ report_date }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total de Receita:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>Pedidos:</strong> {{ order_count }}<br/>
              <strong>Valor Médio do Pedido:</strong> {{ avg_order_value }}<br/>
              <strong>Taxa de Conversão:</strong> {{ conversion_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Visitantes:</strong> {{ visitor_count }}<br/>
              <strong>Novos Clientes:</strong> {{ new_customers }}<br/>
              <strong>Clientes Recorrentes:</strong> {{ returning_customers }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Produtos em Destaque:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.sales }} vendas ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Relatório Completo
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 RELATÓRIO DIÁRIO DE VENDAS

Resumo das Vendas - {{ report_date }}

DESEMPENHO:
- Total de Receita: {{ total_revenue }}
- Pedidos: {{ order_count }}
- Valor Médio do Pedido: {{ avg_order_value }}
- Taxa de Conversão: {{ conversion_rate }}%

TRÁFEGO:
- Visitantes: {{ visitor_count }}
- Novos Clientes: {{ new_customers }}
- Clientes Recorrentes: {{ returning_customers }}

PRODUTOS EM DESTAQUE:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.sales }} vendas ({{ product.revenue }})
{% endfor %}

Ver relatório completo: {{ full_report_url }}