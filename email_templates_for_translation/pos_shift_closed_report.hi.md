---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 शिफ्ट रिपोर्ट: {{ terminal_name }} - {{ shift_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Shift Closed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Shift Summary Report
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Shift closed on {{ terminal_name }} by {{ cashier_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Shift Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Cashier:</strong> {{ cashier_name }}<br/>
              <strong>Started:</strong> {{ shift_started }}<br/>
              <strong>Ended:</strong> {{ shift_ended }}<br/>
              <strong>Duration:</strong> {{ shift_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sales Summary:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Sales:</strong> {{ total_sales }}<br/>
              <strong>Transactions:</strong> {{ transaction_count }}<br/>
              <strong>Items Sold:</strong> {{ items_sold }}<br/>
              <strong>Average Sale:</strong> {{ average_sale }}<br/>
              <strong>Tax Collected:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Payment Breakdown:
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
          Cash Reconciliation:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Opening Cash:</strong> {{ opening_cash }}<br/>
              <strong>Cash Sales:</strong> {{ cash_sales }}<br/>
              <strong>Expected Cash:</strong> {{ expected_cash }}<br/>
              <strong>Counted Cash:</strong> {{ counted_cash }}<br/>
              <strong>Difference:</strong> <span style="color: {{ cash_difference_color }};">{{ cash_difference }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        {% if discrepancy_amount != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Cash Discrepancy: {{ discrepancy_amount }}
            </mj-text>
            {% if discrepancy_note %}
            <mj-text font-size="14px" color="#92400e">
              Note: {{ discrepancy_note }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Full Report
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 शिफ्ट बंद

शिफ्ट समारह रिपोर्ट

शिफ्ट {{ terminal_name }} द्वारा {{ cashier_name }} पर बंद कर दिया गया।

शिफ्ट विवरण:
- टर्मिनल: {{ terminal_name }}
- कैशियर: {{ cashier_name }}
- शुरू: {{ shift_started }}
- समाप्त: {{ shift_ended }}
- अवधि: {{ shift_duration }}

बिक्री समारह:
- कुल बिक्री: {{ total_sales }}
- लेनदेन: {{ transaction_count }}
- बेचे गए आइटम: {{ items_sold }}
- औसत बिक्री: {{ average_sale }}
- एकत्रित कर: {{ tax_collected }}

भुगतान विस्तार:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} लेनदेन)
{% endfor %}

कैश रिकॉन्सिलिएशन:
- खोले गए कैश: {{ opening_cash }}
- कैश बिक्री: {{ cash_sales }}
- अपेक्षित कैश: {{ expected_cash }}
- गिने गए कैश: {{ counted_cash }}
- अंतर: {{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ कैश अंतर: {{ discrepancy_amount }}
{% if discrepancy_note %}नोट: {{ discrepancy_note }}{% endif %}
{% endif %}

पूरा रिपोर्ट देखें: {{ shift_report_url }}