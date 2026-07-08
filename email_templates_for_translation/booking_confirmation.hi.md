---
template_type: booking_confirmation
category: Bookings
---

# Email Template: booking_confirmation

## Subject
बुकिंग पुष्टि - {{ product_name }} पर {{ booking_date }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          बुकिंग पुष्टि!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          हेलो {{ customer_name }}, आपकी बुकिंग पुष्टि हो गई है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Booking Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>तारीख:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>समय:</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>संसाधन:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>मेहमान:</strong> {{ persons_display }}
        </mj-text>
        {% endif %}
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>कुल राशि:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
        {% if deposit_amount %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>जमा राशि:</strong> {{ deposit_amount }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Add to Calendar -->
    {% if ical_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=ical_url text="Add to Calendar" %}
    {% endif %}

    <!-- Manage Booking -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          कोई बदलाव करना है? अपने खाते से आप बुकिंग को <a href="{{ reschedule_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">पुनः निर्धारित कर सकते हैं</a> या <a href="{{ cancel_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">रद्द कर सकते हैं</a>।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
बुकिंग पुष्टि!

हेलो {{ customer_name }}, आपकी बुकिंग पुष्टि हो गई है।

{{ product_name }}
तारीख: {{ booking_date }}
समय: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}संसाधन: {{ resource_name }}{% endif %}
{% if persons_display %}मेहमान: {{ persons_display }}{% endif %}
{% if total_cost %}कुल राशि: {{ total_cost }}{% endif %}
{% if deposit_amount %}जमा राशि: {{ deposit_amount }}{% endif %}

{% if ical_url %}कैलेंडर में जोड़ें: {{ ical_url }}{% endif %}

कोई बदलाव करना है? अपने खाते में जाएं और बुकिंग को पुनः निर्धारित करें या रद्द करें।
{{ reschedule_url }}
{{ cancel_url }}