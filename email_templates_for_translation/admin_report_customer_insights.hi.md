---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 ग्राहक अंतर्दृष्टि - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 ग्राहक अंतर्दृष्टि
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ग्राहक विश्लेषण
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कुल ग्राहक:</strong> {{ total_customers }}<br/>
              <strong>नए ग्राहक:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>रिटेन्शन दर:</strong> {{ retention_rate }}%<br/>
              <strong>औसत CLV:</strong> {{ avg_clv }}<br/>
              <strong>दुहरा खरीद दर:</strong> {{ repeat_purchase_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अंतर्दृष्टि:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ insights }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          विवरण रिपोर्ट देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
👥 ग्राहक अंतर्दृष्टि

ग्राहक विश्लेषण

मीट्रिक्स:
- कुल ग्राहक: {{ total_customers }}
- नए ग्राहक: {{ new_customers }} ({{ new_customer_rate }}%)
- रिटेन्शन दर: {{ retention_rate }}%
- औसत CLV: {{ avg_clv }}
- दुहरा खरीद दर: {{ repeat_purchase_rate }}%

अंतर्दृष्टि:
{{ insights }}

विवरण रिपोर्ट देखें: {{ full_report_url }}