---
template_type: blog_digest_weekly
category: Blog
---

# Email Template: blog_digest_weekly

## Subject
هذا الأسبوع في {{ blog_name }}: {{ post_count }} مقالة جديدة

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📰 ملخص أسبوعي
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحبًا {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          إليك ما نشرناه هذا الأسبوع - {{ post_count }} مقالة جديدة{{ post_count|pluralize }} فقط لك!
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
              بواسطة {{ post.author }} | {{ post.reading_time }} دقيقة للقراءة
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ post.excerpt }}
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }}; font-weight: bold;">اقرأ المزيد →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endfor %}

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          عرض جميع المنشورات
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          تلقيك ملخصات أسبوعية من {{ blog_name }}.<br/>
          <a href="{{ unsubscribe_url }}">الغاء الاشتراك</a> | <a href="{{ preferences_url }}">تفضيلات البريد الإلكتروني</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📰 ملخص أسبوعي
{{ week_start }} - {{ week_end }}

مرحبًا {{ subscriber_name }},

إليك ما نشرناه هذا الأسبوع - {{ post_count }} مقالة جديدة{{ post_count|pluralize }} فقط لك!

{% for post in posts %}
{{ post.title }}
بواسطة {{ post.author }} | {{ post.reading_time }} دقيقة للقراءة
{{ post.excerpt }}
اقرأ المزيد: {{ post.url }}

{% endfor %}

عرض جميع المنشورات: {{ blog_url }}

---

تلقيك ملخصات أسبوعية من {{ blog_name }}.
الغاء الاشتراك: {{ unsubscribe_url }}
تفضيلات البريد الإلكتروني: {{ preferences_url }}