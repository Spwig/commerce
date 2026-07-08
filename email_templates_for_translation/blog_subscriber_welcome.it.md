---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
Benvenuto in {{ blog_name }}! 🎉

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Benvenuto in {{ blog_name }}!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grazie per l'iscrizione! Siamo entusiasti di condividere il nostro ultimo contenuto con te.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              Cosa aspettarti:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ Nuovi post inviati alla tua casella di posta<br/>
              ✓ Contenuti esclusivi per iscritti<br/>
              ✓ {{ publish_frequency }} aggiornamenti<br/>
              ✓ Nessun spam, puoi annullare l'iscrizione in qualsiasi momento
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Inizia a leggere:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Dai un'occhiata ai nostri articoli più popolari:
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
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Leggi ora →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Esplora tutti gli articoli
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Gestisci la tua iscrizione: <a href="{{ preferences_url }}">Preferenze Email</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 BENVENUTO IN {{ blog_name }}!

Ciao {{ subscriber_name }},

Grazie per l'iscrizione! Siamo entusiasti di condividere il nostro ultimo contenuto con te.

COSA ASPETTARTI:
✓ Nuovi post inviati alla tua casella di posta
✓ Contenuti esclusivi per iscritti
✓ {{ publish_frequency }} aggiornamenti
✓ Nessun spam, puoi annullare l'iscrizione in qualsiasi momento

INIZIA A LEGGERE - ARTICOLI POPOLARI:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} min read)
  {{ post.url }}
{% endfor %}

Esplora tutti gli articoli: {{ blog_url }}

Gestisci la tua iscrizione: {{ preferences_url }}