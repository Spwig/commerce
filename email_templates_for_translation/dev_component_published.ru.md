---
template_type: dev_component_published
category: Developer Portal
---

# Email Template: dev_component_published

## Subject
{{ component_name }} v{{ version }} теперь доступен на Spwig Marketplace!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Success Accent -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="50px 20px">
      <mj-column>
        <mj-text font-size="36px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Теперь доступно!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="15px">
          Ваш компонент теперь доступен на Spwig Marketplace
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Здравствуйте, {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          Ваш компонент теперь доступен и доступен всем продавцам Spwig на рынке!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Component Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>Компонент:</strong> {{ component_name }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>Тип:</strong> {{ component_type }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Версия:</strong> v{{ version }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Analytics Info -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Отслеживайте производительность вашего компонента на панели мониторинга — загрузки, рейтинги и отзывы будут отображаться, когда продавцы начнут его использовать.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Посмотреть аналитику
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig Developer Portal</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Вопросы? Свяжитесь с поддержкой разработчиков
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Здравствуйте, {{ developer_name }},

Ваш компонент теперь доступен и доступен всем продавцам Spwig на рынке!

Компонент: {{ component_name }}
Тип: {{ component_type }}
Версия: v{{ version }}

Отслеживайте производительность вашего компонента на панели мониторинга — загрузки, рейтинги и отзывы будут отображаться, когда продавцы начнут его использовать.

Посмотреть аналитику: {{ dashboard_url }}

---
Spwig Developer Portal