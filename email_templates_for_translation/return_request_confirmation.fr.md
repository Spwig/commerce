---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
Demande de retour reçue - Commande n°{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          Demande de retour reçue
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          Commande n°{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nous avons reçu votre demande de retour pour la commande <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails du retour :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Raison :</strong> {{ return_reason }}<br/>
              <strong>Articles :</strong> {{ items_count }} article(s)<br/>
              <strong>Statut :</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Qu'est-ce qui arrive ensuite ?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Notre équipe examinera votre demande de retour dans les 24 à 48 heures<br/>
          2. Une fois approuvée, nous vous enverrons un étiquette de retour par e-mail<br/>
          3. Emballez les articles de manière sécurisée et joignez l'étiquette de retour<br/>
          4. Déposez le colis au point de livraison le plus proche<br/>
          5. Votre remboursement sera traité une fois que nous aurons reçu et inspecté les articles
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Si vous avez des questions, n'hésitez pas à nous contacter.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
DEMANDE DE RETOUR REÇUE
Commande n°{{ order_number }}

Bonjour {{ customer_name }},

Nous avons reçu votre demande de retour pour la commande #{{ order_number }}.

DÉTAILS DU RETOUR :
- Raison : {{ return_reason }}
- Articles : {{ items_count }} article(s)
- Statut : {{ return_status }}

QU'EST-CE QUI ARRIVE ENSUITE ?
1. Notre équipe examinera votre demande de retour dans les 24 à 48 heures
2. Une fois approuvée, nous vous enverrons un étiquette de retour par e-mail
3. Emballez les articles de manière sécurisée et joignez l'étiquette de retour
4. Déposez le colis au point de livraison le plus proche
5. Votre remboursement sera traité une fois que nous aurons reçu et inspecté les articles

Si vous avez des questions, n'hésitez pas à nous contacter.