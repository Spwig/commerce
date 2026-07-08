---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
🎉 Bienvenue sur {{ blog_name }} !

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Bienvenue sur {{ blog_name }}!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merci d'avoir souscrit ! Nous sommes ravis de partager notre contenu le plus récent avec vous.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              Ce que vous pouvez attendre :
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ Des nouveaux articles livrés dans votre boîte de réception<br/>
              ✓ Du contenu exclusif réservé aux abonnés<br/>
              ✓ {{ publish_frequency }} mise(s) à jour<br/>
              ✓ Aucun spam, vous pouvez vous désinscrire à tout moment
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Démarrer la lecture :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Découvrez nos articles les plus populaires :
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
              {{ post.reading_time }} min de lecture
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Lire maintenant →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Explorer tous les articles
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Gérer votre abonnement : <a href="{{ preferences_url }}">Préférences de messagerie</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 BIENVENUE SUR {{ blog_name }} !

Bonjour {{ subscriber_name }},

Merci d'avoir souscrit ! Nous sommes ravis de partager notre contenu le plus récent avec vous.

CE QUE VOUS POUVEZ ATTENDRE :
✓ Des nouveaux articles livrés dans votre boîte de réception
✓ Du contenu exclusif réservé aux abonnés
✓ {{ publish_frequency }} mise(s) à jour
✓ Aucun spam, vous pouvez vous désinscrire à tout moment

DÉMARRER LA LECTURE - ARTICLES POPULAIRES :
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} min de lecture)
  {{ post.url }}
{% endfor %}

Explorer tous les articles : {{ blog_url }}

Gérer votre abonnement : {{ preferences_url }}