---
template_type: admin_report_monthly_review
category: Admin Reports
---

# Email Template: admin_report_monthly_review

## Subject
📊 Revisión Mensual de Negocios - {{ month_name }} {{ year }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Revisión Mensual de Negocios
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ month_name }} {{ year}} Rendimiento
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Ingresos:</strong> <span style="font-size: 24px; color: #059669;">
                {{ total_revenue }}
              </span><br/>
              <strong>Crecimiento:</strong> {{ revenue_growth }}<br/>
              <strong>Órdenes:</strong> {{ total_orders }}<br/>
              <strong>Nuevos clientes:</strong> {{ new_customers }}<br/>
              <strong>CLV:</strong> {{ customer_lifetime_value }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Logros clave:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ achievements }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver informe completo
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 REVISIÓN MENSUAL DE NEGOCIOS

{{ month_name }} {{ year }} Rendimiento

FINANCIAS:
- Ingresos: {{ total_revenue }}
- Crecimiento: {{ revenue_growth }}
- Órdenes: {{ total_orders }}
- Nuevos clientes: {{ new_customers }}
- CLV: {{ customer_lifetime_value }}

LOGROS CLAVE:
{{ achievements }}

Ver informe completo: {{ full_report_url }}