---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
🎉 {{ blog_name }} में आपका स्वागत है! 

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 {{ blog_name }} में आपका स्वागत है!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          सदस्यता लेने के लिए धन्यवाद! हम आपके साथ हमारी नवीनतम सामग्री साझा करने के लिए उत्सुक हैं।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              क्या आपके अपेक्षा करते हैं:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ अपने ईमेल डिलीवरी के लिए नई पोस्ट्स <br/>
              ✓ विशिष्ट सदस्य-केवल सामग्री <br/>
              ✓ {{ publish_frequency }} अपडेट्स <br/>
              ✓ कोई स्पैम नहीं, कभी भी अनसब्स्क्राइब करें
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          पढ़ना शुरू करें:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          हमारे सबसे लोकप्रिय लेखों की जांच करें:
        </mj-text>

        <mj-spacer height="15px" />

        {% for post in popular_posts %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ post.featured_image }}" alt="{{ post.title }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ post.title }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ post.reading_time }} मिनट पढ़ें
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">अब पढ़ें →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          सभी लेख खोजें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          अपनी सदस्यता का प्रबंधन करें: <a href="{{ preferences_url }}">ईमेल पसंद</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ blog_name }} में आपका स्वागत है!

हेलो {{ subscriber_name }},

सदस्यता लेने के लिए धन्यवाद! हम आपके साथ हमारी नवीनतम सामग्री साझा करने के लिए उत्सुक हैं।

क्या आपके अपेक्षा करते हैं:
✓ अपने ईमेल डिलीवरी के लिए नई पोस्ट्स
✓ विशिष्ट सदस्य-केवल सामग्री
✓ {{ publish_frequency }} अपडेट्स
✓ कोई स्पैम नहीं, कभी भी अनसब्स्क्राइब करें

पढ़ना शुरू करें - लोकप्रिय लेख:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} मिनट पढ़ें)
  {{ post.url }}
{% endfor %}

सभी लेख खोजें: {{ blog_url }}

अपनी सदस्यता का प्रबंधन करें: {{ preferences_url }}

