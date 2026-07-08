---
template_type: feed_sync_success
category: Product Feeds
---

# Email Template: feed_sync_success

## Subject
✓ {{ feed_name }} synchronisé avec {{ platform_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ Synchronisation réussie
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Fichier synchronisé avec succès
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre {{ feed_name }} a été synchronisé avec succès sur {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de la synchronisation :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Fichier :</strong> {{ feed_name }}<br/>
              <strong>Plateforme :</strong> {{ platform_name }}<br/>
              <strong>Synchronisé le :</strong> {{ synced_at }}<br/>
              <strong>Produits synchronisés :</strong> {{ products_synced }}<br/>
              <strong>Durée :</strong> {{ sync_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Résumé des modifications :
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% if products_added > 0 %}• {{ products_added }} produit{{ products_added|pluralize }} ajouté<br/>{% endif %}
          {% if products_updated > 0 %}• {{ products_updated }} produit{{ products_updated|pluralize }} mis à jour<br/>{% endif %}
          {% if products_removed > 0 %}• {{ products_removed }} produit{{ products_removed|pluralize }} supprimé<br/>{% endif %}
        </mj-text>
        {% endif %}

        {% if sync_warnings %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Avertissements de synchronisation
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ sync_warnings }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if platform_url %}
        <mj-button href="{{ platform_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir sur {{ platform_name }}
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Voir les détails du fichier
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ SYNCHRONISATION RÉUSSIE

Fichier synchronisé avec succès

Votre {{ feed_name }} a été synchronisé avec succès sur {{ platform_name }}.

DÉTAILS DE LA SYNCHRONISATION :
- Fichier : {{ feed_name }}
- Plateforme : {{ platform_name }}
- Synchronisé le : {{ synced_at }}
- Produits synchronisés : {{ products_synced }}
- Durée : {{ sync_duration }}

{% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
RÉSUMÉ DES MODIFICATIONS :
{% if products_added > 0 %}• {{ products_added }} produit{{ products_added|pluralize }} ajouté{% endif %}
{% if products_updated > 0 %}• {{ products_updated }} produit{{ products_updated|pluralize }} mis à jour{% endif %}
{% if products_removed > 0 %}• {{ products_removed }} produit{{ products_removed|pluralize }} supprimé{% endif %}
{% endif %}

{% if sync_warnings %}
⚠️ AVERTISSEMENTS DE SYNCHRONISATION :
{{ sync_warnings }}
{% endif %}

{% if platform_url %}Voir sur {{ platform_name }} : {{ platform_url }}{% endif %}
Voir les détails du fichier : {{ admin_feed_url }}