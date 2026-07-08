---
template_type: blog_digest_weekly
category: Blog
---

# Email Template: blog_digest_weekly

## Subject
सप्ताहांत {{ blog_name }} पर: {{ post_count }} नई लेख

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📰 साप्ताहिक समाचार संकलन
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          यहां हमारे द्वारा इस सप्ताह प्रकाशित कुछ है - {{ post_count }} नई लेख{{ post_count|pluralize }} आपके लिए!
        </mj-text>

        <mj-spacer height="30px" />

        {% for post in posts %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          {% if post.featured_image %}
          <mj-column width="35%">
            <mj-image src="{{ post.featured_image }}" alt="{{ post.title }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
          {% else %}
          <mj-column width="100%">
          {% endif %}
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" line-height="1.3">
              {{ post.title }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              द्वारा {{ post.author }} | {{ post.reading_time }} मिनट पढ़ें
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ post.excerpt }}
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }}; font-weight: bold;">अधिक पढ़ें →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endfor %}

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          सभी पोस्ट देखें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          आप {{ blog_name }} से साप्ताहिक समाचार संकलन प्राप्त कर रहे हैं।<br/>
          <a href="{{ unsubscribe_url }}">सदस्यता रद्द करें</a> | <a href="{{ preferences_url }}">ईमेल प्राथमिकताएं</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📰 साप्ताहिक समाचार संकलन
{{ week_start }} - {{ week_end }}

हेलो {{ subscriber_name }},

यहां हमारे द्वारा इस सप्ताह प्रकाशित कुछ है - {{ post_count }} नई लेख{{ post_count|pluralize }} आपके लिए!

{% for post in posts %}
{{ post.title }}
द्वारा {{ post.author }} | {{ post.reading_time }} मिनट पढ़ें
{{ post.excerpt }}
अधिक पढ़ें: {{ post.url }}

{% endfor %}

सभी पोस्ट देखें: {{ blog_url }}

---
आप {{ blog_name }} से साप्ताहिक समाचार संकलन प्राप्त कर रहे हैं।
सदस्यता रद्द करें: {{ unsubscribe_url }}
ईमेल प्राथमिकताएं: {{ preferences_url }}