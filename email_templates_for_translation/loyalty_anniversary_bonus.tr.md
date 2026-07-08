---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} YIL{{ years_as_member|pluralize }} - Teşekkürler!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} YIL{{ years_as_member|pluralize }} BERABER!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bugün, sadakat programımıza katıldığınızdan beri {{ years_as_member }} yil{{ years_as_member|pluralize }}. Teşekkürler değerli üyem olmaya!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Doğum Günü Bonusu
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Puan
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              {{ years_as_member }} yil{{ years_as_member|pluralize }} kutlamak için eklenmiştir!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ years_as_member }}-Yıl Yolculuğunuz:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>Üyelik Tarihi:</strong> {{ member_since }}<br/>
          <strong>Toplam Sipariş:</strong> {{ total_orders }}<br/>
          <strong>Kazanılan Puanlar:</strong> {{ lifetime_points }} puan<br/>
          <strong>Mevcut Katman:</strong> {{ loyalty_tier }}<br/>
          <strong>Toplam Tasarruf:</strong> {{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Sadakat Panelinizi Görüntüleyin
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          {{ years_as_member }} harika yil{{ years_as_member|pluralize }} için teşekkür ederiz!<br/>
          Çok daha fazlası için kadeh kırıyoruz 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} YIL{{ years_as_member|pluralize|upper }} BERABER!

Merhaba {{ customer_name }},

Bugün, sadakat programımıza katıldığınızdan beri {{ years_as_member }} yil{{ years_as_member|pluralize }}. Teşekkürler değerli üyem olmaya!

DOĞUM GÜNLÜĞÜ BONUSU:
{{ bonus_points }} Puan
{{ years_as_member }} yil{{ years_as_member|pluralize }} kutlamak için eklenmiştir!

{{ years_as_member }}-YIL YOLCUĞUNUZ:
- Üyelik Tarihi: {{ member_since }}
- Toplam Sipariş: {{ total_orders }}
- Kazanılan Puanlar: {{ lifetime_points }} puan
- Mevcut Katman: {{ loyalty_tier }}
- Toplam Tasarruf: {{ total_savings }}

Sadakat panelinizi görüntüleyin: {{ loyalty_dashboard_url }}

{{ years_as_member }} harika yil{{ years_as_member|pluralize }} için teşekkür ederiz!
Çok daha fazlası için kadeh kırıyoruz 🥂