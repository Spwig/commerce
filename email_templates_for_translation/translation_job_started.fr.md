---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 Traduction en cours : {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 Traduction en cours
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Traduction en lots en cours
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre travail de traduction en lots a été lancé et est maintenant en cours de traitement.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails du travail:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID du travail:</strong> {{ job_id }}<br/>
              <strong>Type de contenu:</strong> {{ content_type }}<br/>
              <strong>Langue source:</strong> {{ source_language }}<br/>
              <strong>Langues cibles:</strong> {{ target_languages }}<br/>
              <strong>Éléments à traduire:</strong> {{ item_count }}<br/>
              <strong>Démarré:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Estimation de la fin:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (Basé sur {{ word_count }} mots)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Qu'est-ce qui arrive ensuite:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Le service de traduction par IA traite votre contenu<br/>
          2. Les traductions sont enregistrées comme brouillons pour examen<br/>
          3. Vous recevrez un e-mail lorsque le travail sera terminé<br/>
          4. Examinez et publiez les traductions depuis votre tableau de bord administrateur
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir l'état du travail
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Vous pouvez fermer cet e-mail. Nous vous notifions quand la traduction est terminée.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 TRADUCTION EN COURS

Traduction en lots en cours

Votre travail de traduction en lots a été lancé et est maintenant en cours de traitement.

DÉTAILS DU TRAVAIL:
- ID du travail : {{ job_id }}
- Type de contenu : {{ content_type }}
- Langue source : {{ source_language }}
- Langues cibles : {{ target_languages }}
- Éléments à traduire : {{ item_count }}
- Démarré : {{ started_at }}

ESTIMATION DE LA FIN:
{{ estimated_completion }}
(Basé sur {{ word_count }} mots)

QU'ARRIVE-T-IL EN SUITE:
1. Le service de traduction par IA traite votre contenu
2. Les traductions sont enregistrées comme brouillons pour examen
3. Vous recevrez un e-mail lorsque le travail sera terminé
4. Examinez et publiez les traductions depuis votre tableau de bord administrateur

Voir l'état du travail : {{ job_status_url }}

Vous pouvez fermer cet e-mail. Nous vous notifions quand la traduction est terminée.