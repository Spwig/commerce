---
template_type: blog_post_published
category: Blog
---

# Email Template: blog_post_published

## Subject
नई पोस्ट: {{ post_title }} - {{ shop_name }} ब्लॉग

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📝 नई ब्लॉग पोस्ट
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हमने एक नई पोस्ट प्रकाशित की है जिसे हम आपको पसंद करेंगे!
        </mj-text>

        <mj-spacer height="30px" />

        {% if featured_image %}
        <mj-image src="{{ featured_image }}" alt="{{ post_title }}" border-radius="8px" />
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" line-height="1.3">
          {{ post_title }}
        </mj-text>

        <mj-spacer height="15px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          द्वारा {{ author_name }} | {{ publish_date }} | {{ reading_time }} मिनट पढ़ें
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ post_excerpt }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ post_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          पूरा लेख पढ़ें
        </mj-button>

        <mj-spacer height="30px" />

        {% if related_posts %}
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          आपको शायद इसके बारे में भी पढ़ना चाहिए:
        </mj-text>

        {% for post in related_posts %}
        <mj-spacer height="15px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ post.title }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ post.excerpt }}
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">अधिक पढ़ें →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}
        <mj-spacer height="30px" />
        {% endif %}

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          आप इसे {{ blog_name }} के सदस्यता लेने के कारण प्राप्त कर रहे हैं।<br/>
          <a href="{{ unsubscribe_url }}">ब्लॉग अपडेट से अनसबस्क्राइब करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 नई ब्लॉग पोस्ट

हेलो {{ subscriber_name }},

हमने एक नई पोस्ट प्रकाशित की है जिसे हम आपको पसंद करेंगे!

{{ post_title }}
द्वारा {{ author_name }} | {{ publish_date }} | {{ reading_time }} मिनट पढ़ें

{{ post_excerpt }}

पूरा लेख पढ़ें: {{ post_url }}

{% if related_posts %}
आपको शायद इसके बारे में भी पढ़ना चाहिए:
{% for post in related_posts %}
- {{ post.title }}
  {{ post.url }}
{% endfor %}
{% endif %}

---
आप इसे {{ blog_name }} के सदस्यता लेने के कारण प्राप्त कर रहे हैं।
ब्लॉग अपडेट से अनसबस्क्राइब करें: {{ unsubscribe_url }}