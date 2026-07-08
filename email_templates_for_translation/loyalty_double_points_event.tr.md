---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 2X Puan Olayı Şimdi Başladı! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 2X PUAN Olayı!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Loyalite Üyeleri İçin Özel!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Büyük puanlar kazanmaya hazırsınız! Sınırlı süreliğine, her alışverişinizde {{ points_multiplier }}X puan kazanacaksınız.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              {{ points_multiplier }}X Puan Kazan
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              Tüm alışverişlerde<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Örnek Kazançlar:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              $50 harcayın → {{ example_points_normal }} puan normalde kazanırsınız<br/>
              <strong style="color: #047857;">Bu olay sırasında → {{ example_points_bonus }} puan kazanırsınız! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              $100 harcayın → {{ example_points_normal_2 }} puan normalde kazanırsınız<br/>
              <strong style="color: #047857;">Bu olay sırasında → {{ example_points_bonus_2 }} puan kazanırsınız! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mevcut Bakiyeniz:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Puanlar:</strong> {{ current_points }} puan<br/>
          <strong>Derece:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Şimdi Alışveriş Yap & {{ points_multiplier }}X Puan Kazan
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          Olay {{ event_end }} tarihinde sona eriyor - Kaçmayın!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 2X Puan Olayı!
{{ event_start }} - {{ event_end }}

Loyalite Üyeleri İçin Özel!

Merhaba {{ customer_name }},

Büyük puanlar kazanmaya hazırsınız! Sınırlı süreliğine, her alışverişinizde {{ points_multiplier }}X puan kazanacaksınız.

{{ points_multiplier }}X Puan Kazan
Tüm alışverişlerde
{{ event_start }} - {{ event_end }}

Örnek Kazançlar:
- $50 harcayın → {{ example_points_normal }} puan normalde kazanırsınız
  Bu olay sırasında → {{ example_points_bonus }} puan kazanırsınız! 🎉

- $100 harcayın → {{ example_points_normal_2 }} puan normalde kazanırsınız
  Bu olay sırasında → {{ example_points_bonus_2 }} puan kazanırsınız! 🎉

Mevcut Bakiyeniz:
- Puanlar: {{ current_points }} puan
- Derece: {{ loyalty_tier }}

Şimdi alışveriş yap & {{ points_multiplier }}X puan kazan: {{ shop_url }}

Olay {{ event_end }} tarihinde sona eriyor - Kaçmayın!