---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ नकद असंगति चेतावनी: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ नकद असंगति चेतावनी
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          नकद अंतर चेतावनी
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} पर शिफ्ट बंद करते समय {{ discrepancy_amount }} की एक नकद असंगति का पता चला।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              असंगति विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>टर्मिनल:</strong> {{ terminal_name }}<br/>
              <strong>कैशियर:</strong> {{ cashier_name }}<br/>
              <strong>शिफ्ट तिथि:</strong> {{ shift_date }}<br/>
              <strong>शिफ्ट अवधि:</strong> {{ shift_duration }}<br/>
              <strong>पता लगाया गया:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          नकद गिनती:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>अपेक्षित नकद:</strong> {{ expected_cash }}<br/>
              <strong>गिने गए नकद:</strong> {{ counted_cash }}<br/>
              <strong>असंगति:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>शुरू करें नकद:</strong> {{ opening_cash }}<br/>
              <strong>नकद बिक्री:</strong> {{ cash_sales }}<br/>
              <strong>कैश रिफंड:</strong> {{ cash_refunds }}<br/>
              <strong>नकद निकाला गया:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          कैशियर का नोट:
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
          सुझाए गए कार्रवाई:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. त्रुटियों के लिए लेनदेन ऐतिहासिक की जांच करें<br/>
          2. अपरिभाजित नकद भुगतान की जांच करें<br/>
          3. नकद गिनती की पुष्टि करें<br/>
          4. शिफ्ट नोट में असंगति को दर्ज करें<br/>
          5. आवश्यकता पड़े तो कैशियर के साथ अपडेट करें
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          शिफ्ट रिपोर्ट देखें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          लेनदेन की जांच करें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ नकद असंगति चेतावनी

नकद अंतर चेतावनी

{{ terminal_name }} पर शिफ्ट बंद करते समय {{ discrepancy_amount }} की एक नकद असंगति का पता चला।

असंगति विवरण:
- टर्मिनल: {{ terminal_name }}
- कैशियर: {{ cashier_name }}
- शिफ्ट तिथि: {{ shift_date }}
- शिफ्ट अवधि: {{ shift_duration }}
- पता लगाया गया: {{ detected_at }}

नकद गिनती:
- अपेक्षित नकद: {{ expected_cash }}
- गिने गए नकद: {{ counted_cash }}
- असंगति: {{ discrepancy_amount }}

ब्रेकडाउन:
- शुरू करें नकद: {{ opening_cash }}
- नकद बिक्री: {{ cash_sales }}
- कैश रिफंड: {{ cash_refunds }}
- नकद निकाला गया: {{ cash_paid_out }}

{% if cashier_note %}
कैशियर का नोट:
"{{ cashier_note }}"
{% endif %}

सुझाए गए कार्रवाई:
1. त्रुटियों के लिए लेनदेन ऐतिहासिक की जांच करें
2. अपरिभाजित नकद भुगतान की जांच करें
3. नकद गिनती की पुष्टि करें
4. शिफ्ट नोट में असंगति को दर्ज करें
5. आवश्यकता पड़े तो कैशियर के साथ अपडेट करें

शिफ्ट रिपोर्ट देखें: {{ shift_report_url }}
लेनदेन की जांच करें: {{ transaction_history_url }}