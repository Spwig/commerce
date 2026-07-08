---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
उपलब्ध अपडेट: {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 उपलब्ध अपडेट
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          एक नई संस्करण उपलब्ध है
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          आपके Spwig स्टोर के लिए {{ component_name }} के एक नए संस्करण के उपलब्ध है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              अपडेट विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कम्पोनेंट:</strong> {{ component_name }}<br/>
              <strong>वर्तमान संस्करण:</strong> {{ current_version }}<br/>
              <strong>नई संस्करण:</strong> {{ new_version }}<br/>
              <strong>रिलीज़ तिथि:</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          क्या नया है:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ भेदभावपूर्ण परिवर्तन
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अपडेट करें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            पूरा चेंजलॉग देखें
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 अपडेट उपलब्ध

एक नई संस्करण उपलब्ध है

आपके Spwig स्टोर के लिए {{ component_name }} के एक नए संस्करण के उपलब्ध है।

अपडेट विवरण:
- कम्पोनेंट: {{ component_name }}
- वर्तमान संस्करण: {{ current_version }}
- नई संस्करण: {{ new_version }}
- रिलीज़ तिथि: {{ release_date }}

क्या नया है:
{{ changelog }}

{% if breaking_changes %}
⚠️ भेदभावपूर्ण परिवर्तन:
{{ breaking_changes }}
{% endif %}

अपडेट करें: {{ update_url }}
पूरा चेंजलॉग देखें: {{ changelog_url }}