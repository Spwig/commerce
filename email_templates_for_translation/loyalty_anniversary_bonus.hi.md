---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} साल साथ - धन्यवाद!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} साल साथ!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आज से आप हमारे लॉयल्टी प्रोग्राम में शामिल होने के {{ years_as_member }} साल पूरे हो रहे हैं। आपके इतने मूल्यवान सदस्य के रूप में रहने के लिए धन्यवाद!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              वर्षगांठ बॉनस
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} अंक
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              आपके {{ years_as_member }} साल साथ मनाने के लिए जोड़ा गया।
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          आपका {{ years_as_member }}-साल यात्रा:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>सदस्य: </strong>{{ member_since }}<br/>
          <strong>कुल आदेश: </strong>{{ total_orders }}<br/>
          <strong>अर्जित अंक: </strong>{{ lifetime_points }} अंक<br/>
          <strong>वर्तमान स्तर: </strong>{{ loyalty_tier }}<br/>
          <strong>कुल बचत: </strong>{{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अपने लॉयल्टी डैशबोर्ड को देखें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          {{ years_as_member }} अद्भुत साल के लिए धन्यवाद!<br/>
          आगे के अधिक से अधिक 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} साल साथ!

हेलो {{ customer_name }},

आज से आप हमारे लॉयल्टी प्रोग्राम में शामिल होने के {{ years_as_member }} साल पूरे हो रहे हैं। आपके इतने मूल्यवान सदस्य के रूप में रहने के लिए धन्यवाद!

वर्षगांठ बॉनस:
{{ bonus_points }} अंक
आपके {{ years_as_member }} साल साथ मनाने के लिए जोड़ा गया।

आपका {{ years_as_member }}-साल यात्रा:
- सदस्य: {{ member_since }}
- कुल आदेश: {{ total_orders }}
- अर्जित अंक: {{ lifetime_points }} अंक
- वर्तमान स्तर: {{ loyalty_tier }}
- कुल बचत: {{ total_savings }}

अपने लॉयल्टी डैशबोर्ड को देखें: {{ loyalty_dashboard_url }}

{{ years_as_member }} अद्भुत साल के लिए धन्यवाद!
यहां तक कि अधिक से अधिक 🥂