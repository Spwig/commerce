---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
¡Bienvenido a {{ blog_name }}! 🎉

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 ¡Bienvenido a {{ blog_name }}!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ¡Gracias por suscribirte! Estamos emocionados de compartir nuestro contenido más reciente contigo.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              ¿Qué puedes esperar:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ Nuevos artículos entregados a tu bandeja de entrada<br/>
              ✓ Contenido exclusivo para suscriptores<br/>
              ✓ {{ publish_frequency }} actualizaciones<br/>
              ✓ Sin spam, puedes darte de baja en cualquier momento
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Comienza a leer:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Revisa nuestros artículos más populares:
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
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Leer ahora →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Explorar todos los artículos
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Administrar tu suscripción: <a href="{{ preferences_url }}">Preferencias de correo electrónico</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 ¡BIENVENIDO A {{ blog_name }}!

Hola {{ subscriber_name }},

¡Gracias por suscribirte! Estamos emocionados de compartir nuestro contenido más reciente contigo.

¿QUÉ PUEDES ESPERAR:
✓ Nuevos artículos entregados a tu bandeja de entrada
✓ Contenido exclusivo para suscriptores
✓ {{ publish_frequency }} actualizaciones
✓ Sin spam, puedes darte de baja en cualquier momento

COMIENZA A LEER - ARTÍCULOS POPULARES:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} min read)
  {{ post.url }}
{% endfor %}

Explorar todos los artículos: {{ blog_url }}

Administrar su suscripción: {{ preferences_url }}

