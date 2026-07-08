---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 Événement 2X Points - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 ÉVÉNEMENT 2X POINTS !
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Exclusif pour les Membres de la Fidélité !
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Préparez-vous à gagner GRAND ! Pour une période limitée, vous gagnerez {{ points_multiplier }}X points sur chaque achat.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              Gagnez {{ points_multiplier }}X Points
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              Sur tous les achats<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Exemples de gains :
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Dépensez 50 $ → Gagnez {{ example_points_normal }} points normalement<br/>
              <strong style="color: #047857;">Pendant cet événement → Gagnez {{ example_points_bonus }} points ! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Dépensez 100 $ → Gagnez {{ example_points_normal_2 }} points normalement<br/>
              <strong style="color: #047857;">Pendant cet événement → Gagnez {{ example_points_bonus_2 }} points ! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Votre solde actuel :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Points :</strong> {{ current_points }} points<br/>
          <strong>Niveau :</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Magasinez maintenant & gagnez {{ points_multiplier }}X Points
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          L'événement se termine {{ event_end }} - Ne manquez pas !
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 ÉVÉNEMENT 2X POINTS !
{{ event_start }} - {{ event_end }}

Exclusif pour les Membres de la Fidélité !

Bonjour {{ customer_name }},

Préparez-vous à gagner GRAND ! Pour une période limitée, vous gagnerez {{ points_multiplier }}X points sur chaque achat.

Gagnez {{ points_multiplier }}X Points
Sur tous les achats
{{ event_start }} - {{ event_end }}

EXEMPLES DE GAINS :
- Dépensez 50 $ → Gagnez {{ example_points_normal }} points normalement
  Pendant cet événement → Gagnez {{ example_points_bonus }} points ! 🎉

- Dépensez 100 $ → Gagnez {{ example_points_normal_2 }} points normalement
  Pendant cet événement → Gagnez {{ example_points_bonus_2 }} points ! 🎉

VOTRE SOLDE ACTUEL :
- Points : {{ current_points }} points
- Niveau : {{ loyalty_tier }}

Magasinez maintenant & gagnez {{ points_multiplier }}X points : {{ shop_url }}

L'événement se termine {{ event_end }} - Ne manquez pas !