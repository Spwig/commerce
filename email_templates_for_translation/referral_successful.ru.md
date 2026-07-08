---
template_type: referral_successful
category: Referral Program
---

# Email Template: referral_successful

## Subject
🎉 Ваш друг {{ referee_name }} только что зарегистрировался!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Успех по рекомендации!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          {{ referee_name }} Присоединился!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          Ваша рекомендация теперь является участником
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Хорошие новости! {{ referee_name }} только что зарегистрировался, используя вашу ссылку на рекомендацию.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Как только он совершит свой первый заказ, вы оба получите вознаграждение! Мы отправим вам еще один email, когда это произойдет.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          Что будет дальше?
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. {{ referee_name }} совершает свой первый заказ<br/>
          2. Вы оба получите свои вознаграждения автоматически<br/>
          3. Вы можете использовать свое вознаграждение при любом будущем заказе
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Keep Sharing -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Продолжайте делиться, чтобы заработать больше!
        </mj-text>
        <mj-text
          background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}"
          border="2px dashed {{ theme.color.primary|default:'#2563eb' }}"
          border-radius="8px"
          padding="15px"
          font-size="14px"
          color="{{ theme.color.primary|default:'#2563eb' }}"
          align="center"
          font-family="monospace"
        >
          {{ referral_link }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_dashboard_url }}">
          Просмотреть мои рекомендации
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 Ваш друг {{ referee_name }} только что зарегистрировался!

Здравствуйте, {{ customer_name }},

Хорошие новости! {{ referee_name }} только что зарегистрировался, используя вашу ссылку на рекомендацию.

Как только он совершит свой первый заказ, вы оба получите вознаграждение! Мы отправим вам еще один email, когда это произойдет.

Что будет дальше?
1. {{ referee_name }} совершает свой первый заказ
2. Вы оба получите свои вознаграждения автоматически
3. Вы можете использовать свое вознаграждение при любом будущем заказе

Продолжайте делиться, чтобы заработать больше:
{{ referral_link }}

Просмотреть ваши рекомендации: {{ referral_dashboard_url }}

{{ shop_name }}