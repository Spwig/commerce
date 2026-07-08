---
template_type: admin_report_daily_sales
category: Admin Reports
---

# Email Template: admin_report_daily_sales

## Subject
📊 दैनिक बिक्री रिपोर्ट - {{ report_date }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 दैनिक बिक्री रिपोर्ट
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          बिक्री सारांश - {{ report_date }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कुल राजस्व:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>आदेश:</strong> {{ order_count }}<br/>
              <strong>औसत आदेश मूल्य:</strong> {{ avg_order_value }}<br/>
              <strong>रूपांतरण दर:</strong> {{ conversion_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ब्राउज़र:</strong> {{ visitor_count }}<br/>
              <strong>नए ग्राहक:</strong> {{ new_customers }}<br/>
              <strong>वापसी ग्राहक:</strong> {{ returning_customers }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          शीर्ष उत्पाद:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.sales }} बिक्री ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          विस्तृत रिपोर्ट देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 दैनिक बिक्री रिपोर्ट

बिक्री सारांश - {{ report_date }}

कार्यप्रदर्शन:
- कुल राजस्व: {{ total_revenue }}
- आदेश: {{ order_count }}
- औसत आदेश मूल्य: {{ avg_order_value }}
- रूपांतरण दर: {{ conversion_rate }}%

आवागमन:
- ब्राउज़र: {{ visitor_count }}
- नए ग्राहक: {{ new_customers }}
- वापसी ग्राहक: {{ returning_customers }}

शीर्ष उत्पाद:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.sales }} बिक्री ({{ product.revenue }})
{% endfor %}

विस्तृत रिपोर्ट देखें: {{ full_report_url }}