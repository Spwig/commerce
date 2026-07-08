---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 छोड़े गए कार्ट रिपोर्ट - {{ abandoned_count }} कार्ट ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 छोड़े गए कार्ट रिपोर्ट
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          कार्ट छोड़ने का सारांश
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Period:</strong> {{ report_period }}<br/>
              <strong>Abandoned Carts:</strong> {{ abandoned_count }}<br/>
              <strong>Abandoned Value:</strong> <span style="font-size: 18px; color: #dc2626;">{{ abandoned_value }}</span><br/>
              <strong>Abandonment Rate:</strong> {{ abandonment_rate }}%<br/>
              <strong>Recovery Rate:</strong> {{ recovery_rate }}%
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
          View Details
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 छोड़े गए कार्ट रिपोर्ट

कार्ट छोड़ने का सारांश

मेट्रिक्स:
- अवधि: {{ report_period }}
- छोड़े गए कार्ट: {{ abandoned_count }}
- छोड़े गए मूल्य: {{ abandoned_value }}
- छोड़ने की दर: {{ abandonment_rate }}%
- पुनर्जीवन दर: {{ recovery_rate }}%

शीर्ष कारण:
{{ top_reasons }}

विवरण देखें: {{ full_report_url }}