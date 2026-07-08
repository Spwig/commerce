---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 بدأ الآن فعالية نقاط المزدوجة! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 فعالية نقاط المزدوجة!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          حصرية للعملاء المخلصين!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          السلام عليكم {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          استعد لربح الكثير! لفترة محدودة، ستربح {{ points_multiplier }}X نقاط على كل شراء.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              ربح {{ points_multiplier }}X نقاط
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              على جميع المشتريات<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          أمثلة على الربح:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              إنفاق 50 دولارًا → ربح {{ example_points_normal }} نقاط بشكل طبيعي<br/>
              <strong style="color: #047857;">خلال هذه الفعالية → ربح {{ example_points_bonus }} نقاط! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              إنفاق 100 دولارًا → ربح {{ example_points_normal_2 }} نقاط بشكل طبيعي<br/>
              <strong style="color: #047857;">خلال هذه الفعالية → ربح {{ example_points_bonus_2 }} نقاط! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          رصيدك الحالي:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>نقاط:</strong> {{ current_points }} نقاط<br/>
          <strong>الدرجة:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          اشopper الآن واربح {{ points_multiplier }}X نقاط
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          تنتهي الفعالية {{ event_end }} - لا تفوت الفرصة!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 فعالية نقاط المزدوجة!
{{ event_start }} - {{ event_end }}

حصرية للعملاء المخلصين!

السلام عليكم {{ customer_name }},

استعد لربح الكثير! لفترة محدودة، ستربح {{ points_multiplier }}X نقاط على كل شراء.

ربح {{ points_multiplier }}X نقاط
على جميع المشتريات
{{ event_start }} - {{ event_end }}

أمثلة على الربح:
- إنفاق 50 دولارًا → ربح {{ example_points_normal }} نقاط بشكل طبيعي
  خلال هذه الفعالية → ربح {{ example_points_bonus }} نقاط! 🎉

- إنفاق 100 دولارًا → ربح {{ example_points_normal_2 }} نقاط بشكل طبيعي
  خلال هذه الفعالية → ربح {{ example_points_bonus_2 }} نقاط! 🎉

رصيدك الحالي:
- نقاط: {{ current_points }} نقاط
- الدرجة: {{ loyalty_tier }}

اشopper الآن واربح {{ points_multiplier }}X نقاط: {{ shop_url }}

تنتهي الفعالية {{ event_end }} - لا تفوت الفرصة!