---
template_type: loyalty_points_earned
category: Loyalty Program
---

# Email Template: loyalty_points_earned

## Subject
आपने {{ points }} अंक अर्जित कर लिए!

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
          ✨ अंक अर्जित!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Points Display -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          +{{ points }}
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          अंक आपके खाते में जोड़ दिए गए हैं
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          हेलो {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          अच्छी खबर! आपने {{ points }} अंक अर्जित कर लिए {{ reason }}।
        </mj-text>

        <!-- Balance -->
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding="20px 0" />
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>कुल अंक:</strong> {{ total_points }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          अब इन्हें बदलने के लिए उपलब्ध हैं
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Rewards Suggestion -->
    {% if suggested_reward %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          🎁 अब आप इन्हें बदल सकते हैं:
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ suggested_reward }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ rewards_url }}">
          रिवॉर्ड्स ब्राउज़ करें
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
आपने {{ points }} अंक अर्जित कर लिए!

हेलो {{ customer_name }},

अच्छी खबर! आपने {{ points }} अंक अर्जित कर लिए {{ reason }}।

कुल अंक: {{ total_points }}
अब इन्हें बदलने के लिए उपलब्ध हैं

{% if suggested_reward %}आप अब इन्हें बदल सकते हैं: {{ suggested_reward }}{% endif %}

रिवॉर्ड्स ब्राउज़ करें: {{ rewards_url }}

{{ shop_name }}