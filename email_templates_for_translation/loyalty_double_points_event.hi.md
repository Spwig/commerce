---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 अब डबल अंक ईवेंट शुरू हो गया! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 2X अंक ईवेंट!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          वफादारी सदस्यों के लिए विशेष!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          बड़ा कमाएं! एक सीमित समय के लिए, आप हर खरीदारी पर {{ points_multiplier }}X अंक कमाएंगे।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              {{ points_multiplier }}X अंक कमाएं
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              सभी खरीदारी पर<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          उदाहरण अर्जित:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              $50 खर्च करें → {{ example_points_normal }} अंक सामान्य रूप से अर्जित करें
              <strong style="color: #047857;">इस ईवेंट के दौरान → {{ example_points_bonus }} अंक अर्जित करें! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              $100 खर्च करें → {{ example_points_normal_2 }} अंक सामान्य रूप से अर्जित करें
              <strong style="color: #047857;">इस ईवेंट के दौरान → {{ example_points_bonus_2 }} अंक अर्जित करें! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          आपका वर्तमान बैलेंस:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>अंक:</strong> {{ current_points }} अंक<br/>
          <strong>टियर:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          अब खरीदें और {{ points_multiplier }}X अंक कमाएं
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          ईवेंट {{ event_end }} पर समाप्त होगा - ना छोड़ें!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 2X अंक ईवेंट!
{{ event_start }} - {{ event_end }}

वफादारी सदस्यों के लिए विशेष!

हेलो {{ customer_name }},

बड़ा कमाएं! एक सीमित समय के लिए, आप हर खरीदारी पर {{ points_multiplier }}X अंक कमाएंगे।

{{ points_multiplier }}X अंक कमाएं
सभी खरीदारी पर
{{ event_start }} - {{ event_end }}

उदाहरण अर्जित:
- $50 खर्च करें → {{ example_points_normal }} अंक सामान्य रूप से अर्जित करें
  इस ईवेंट के दौरान → {{ example_points_bonus }} अंक अर्जित करें! 🎉

- $100 खर्च करें → {{ example_points_normal_2 }} अंक सामान्य रूप से अर्जित करें
  इस ईवेंट के दौरान → {{ example_points_bonus_2 }} अंक अर्जित करें! 🎉

आपका वर्तमान बैलेंस:
- अंक: {{ current_points }} अंक
- टियर: {{ loyalty_tier }}

अब खरीदें और {{ points_multiplier }}X अंक कमाएं: {{ shop_url }}

ईवेंट {{ event_end }} पर समाप्त होगा - ना छोड़ें!
