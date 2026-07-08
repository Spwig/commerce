---
template_type: subscription_plan_downgraded
category: Subscriptions
---

# Email Template: subscription_plan_downgraded

## Subject
आपका सदस्यता योजना {{ new_plan_name }} में बदल गई है

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          योजना बदल गई
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सदस्यता योजना अपडेट करें
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपकी सदस्यता योजना {{ new_plan_name }} में बदल गई है।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              योजना बदल गई विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>पुरानी योजना:</strong> {{ old_plan_name }}<br/>
              <strong>नई योजना:</strong> {{ new_plan_name }}<br/>
              <strong>बदल गई:</strong> {{ downgrade_date }}<br/>
              <strong>लागू:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          क्या बदल गई है:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ plan_changes }}
        </mj-text>

        {% if features_lost %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              अब उपलब्ध नहीं होने वाली सुविधाएं:
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ features_lost }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          बिलिंग जानकारी:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>नई कीमत:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>लागू तिथि:</strong> {{ effective_date }}<br/>
              <strong>अगली बिलिंग तिथि:</strong> {{ next_billing_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 आपके खाते में आपकी पुरानी योजना के अप्रयुक्त भाग के लिए {{ credit_amount }} क्रेडिट लागू किया गया है।
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          अपना विचार बदल गए?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color_secondary|default:'#6b7280' }}" align="center">
          आप किसी भी समय {{ old_plan_name }} में अपग्रेड कर सकते हैं।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ upgrade_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          योजना अपग्रेड करें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          मेरी सदस्यता देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
योजना बदल गई

सदस्यता योजना अपडेट करें

हेलो {{ customer_name }},

आपकी सदस्यता योजना {{ new_plan_name }} में बदल गई है।

योजना बदल गई विवरण:
- पुरानी योजना: {{ old_plan_name }}
- नई योजना: {{ new_plan_name }}
- बदल गई: {{ downgrade_date }}
- लागू: {{ effective_date }}

क्या बदल गई है:
{{ plan_changes }}

{% if features_lost %}
अब उपलब्ध नहीं होने वाली सुविधाएं:
{{ features_lost }}
{% endif %}

बिलिंग जानकारी:
- नई कीमत: {{ new_price }} / {{ billing_period }}
- लागू तिथि: {{ effective_date }}
- अगली बिलिंग तिथि: {{ next_billing_date }}

{% if credit_applied %}
💰 आपके खाते में आपकी पुरानी योजना के अप्रयुक्त भाग के लिए {{ credit_amount }} क्रेडिट लागू किया गया है।
{% endif %}

अपना विचार बदल गए?
आप किसी भी समय {{ old_plan_name }} में अपग्रेड कर सकते हैं।

योजना अपग्रेड करें: {{ upgrade_url }}
मेरी सदस्यता देखें: {{ account_url }}