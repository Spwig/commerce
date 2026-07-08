---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
Willkommen bei {{ blog_name }}! 🎉

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Willkommen bei {{ blog_name }}!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Vielen Dank, dass Sie sich angemeldet haben! Wir freuen uns, Ihnen unsere neuesten Inhalte mitzuteilen.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              Was Sie erwarten können:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ Neue Beiträge werden Ihnen per E-Mail zugestellt<br/>
              ✓ Exklusive Inhalte nur für Abonnenten<br/>
              ✓ {{ publish_frequency }} Updates<br/>
              ✓ Kein Spam, Sie können sich jederzeit abmelden
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Los geht's mit dem Lesen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Schauen Sie sich unsere beliebtesten Artikel an:
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
              {{ post.reading_time }} min read
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Lesen Sie jetzt →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Alle Artikel erkunden
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Ihre Abonnementverwaltung: <a href="{{ preferences_url }}">E-Mail-Präferenzen</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 WILLKOMMEN BEI {{ blog_name }}!

Hi {{ subscriber_name }},

Vielen Dank, dass Sie sich angemeldet haben! Wir freuen uns, Ihnen unsere neuesten Inhalte mitzuteilen.

WAS SIE ERWARTEN KÖNNEN:
✓ Neue Beiträge werden Ihnen per E-Mail zugestellt
✓ Exklusive Inhalte nur für Abonnenten
✓ {{ publish_frequency }} Updates
✓ Kein Spam, Sie können sich jederzeit abmelden

START MIT DEM LESEN - BELIEBTE ARTIKEL:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} min read)
  {{ post.url }}
{% endfor %}

Alle Artikel erkunden: {{ blog_url }}

Ihre Abonnementverwaltung: {{ preferences_url }}