---
template_type: pos_daily_z_report
category: POS
---

# Email Template: pos_daily_z_report

## Subject
📊 दैनिक Z रिपोर्ट - {{ report_date }} - {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 दैनिक Z रिपोर्ट
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          दिन के अंत में समायोजन रिपोर्ट
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ location_name }} के लिए {{ report_date }} के लिए दैनिक समारह।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          बिक्री का सारांश:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कुल बिक्री:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_sales }}</span><br/>
              <strong>लेनदेन:</strong> {{ transaction_count }}<br/>
              <strong>बिक्री वस्तुएँ:</strong> {{ items_sold }}<br/>
              <strong>औसत बिक्री:</strong> {{ average_sale }}<br/>
              <strong>वसूला टैक्स:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          भुगतान विधियाँ:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}</strong>: {{ payment.amount }} ({{ payment.count }} लेनदेन)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          शिफ्ट का सारांश:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कुल शिफ्ट:</strong> {{ shift_count }}<br/>
              <strong>उपयोग किए गए टर्मिनल:</strong> {{ terminal_count }}<br/>
              <strong>सक्रिय कैशियर:</strong> {{ cashier_count }}
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
              बिक्री: {{ terminal.sales }} | लेनदेन: {{ terminal.transactions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          समायोजन एवं छूट:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>दिया गया छूट:</strong> {{ discounts_total }}<br/>
              <strong>वापसी जारी की गई:</strong> {{ refunds_total }}<br/>
              <strong>रद्द कर दिया गया:</strong> {{ voids_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cash_variance != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ कुल नकद अंतर: {{ cash_variance }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              {{ variance_note }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          शीर्ष बिक्री वाली वस्तुएँ:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.quantity }} बिक्री ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          पूरा रिपोर्ट देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 दैनिक Z रिपोर्त

दिन के अंत में समायोजन रिपोर्त

{{ location_name }} के लिए {{ report_date }} के लिए दैनिक समारह।

बिक्री का सारांश:
- कुल बिक्री: {{ total_sales }}
- लेनदेन: {{ transaction_count }}
- बिक्री वस्तुएँ: {{ items_sold }}
- औसत बिक्री: {{ average_sale }}
- वसूला टैक्स: {{ tax_collected }}

भुगतान विधियाँ:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} लेनदेन)
{% endfor %}

शिफ्ट का सारांश:
- कुल शिफ्ट: {{ shift_count }}
- उपयोग किए गए टर्मिनल: {{ terminal_count }}
- सक्रिय कैशियर: {{ cashier_count }}

टर्मिनल विभाजन:
{% for terminal in terminal_stats %}
{{ terminal.name }}: {{ terminal.sales }} | {{ terminal.transactions }} लेनदेन
{% endfor %}

समायोजन एवं छूट:
- दिया गया छूट: {{ discounts_total }}
- वापसी जारी की गई: {{ refunds_total }}
- रद्द कर दिया गया: {{ voids_total }}

{% if cash_variance != 0 %}
⚠️ कुल नकद अंतर: {{ cash_variance }}
{{ variance_note }}
{% endif %}

शीर्ष बिक्री वाली वस्तुएँ:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.quantity }} बिक्री ({{ product.revenue }})
{% endfor %}

पूरा रिपोर्त देखें: {{ full_report_url }}