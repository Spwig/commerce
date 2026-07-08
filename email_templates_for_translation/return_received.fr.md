---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
Nous avons reçu votre retour - Commande #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Retour reçu
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Commande #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nous avons reçu vos articles retournés pour la commande <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Quel est l'étape suivante :</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Notre équipe inspectera les articles retournés dans les 2 à 3 jours ouvrés<br/>
          2. Nous vérifierons que les articles sont dans leur état d'origine<br/>
          3. Une fois l'inspection terminée, nous traiterons votre remboursement<br/>
          4. Vous recevrez un e-mail de confirmation une fois le remboursement traité
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Le remboursement sera crédité à votre méthode de paiement originale et peut prendre 5 à 10 jours ouvrés pour apparaître sur votre compte.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merci pour votre patience !
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Retour reçu - Commande #{{ order_number }}

Bonjour {{ customer_name }},

Nous avons reçu vos articles retournés pour la commande #{{ order_number }}.

Quel est l'étape suivante :
1. Notre équipe inspectera les articles retournés dans les 2 à 3 jours ouvrés
2. Nous vérifierons que les articles sont dans leur état d'origine
3. Une fois l'inspection terminée, nous traiterons votre remboursement
4. Vous recevrez un e-mail de confirmation une fois le remboursement traité

Le remboursement sera crédité à votre méthode de paiement originale et peut prendre 5 à 10 jours ouvrés pour apparaître sur votre compte.

Merci pour votre patience !