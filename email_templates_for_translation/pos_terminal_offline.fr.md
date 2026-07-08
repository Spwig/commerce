---
template_type: pos_terminal_offline
category: POS
---

# Email Template: pos_terminal_offline

## Subject
⚠️ Terminal POS hors ligne : {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ Terminal Déconnecté
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Terminal POS hors ligne
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} has gone offline and is no longer responding.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Informations sur le terminal:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Location:</strong> {{ location }}<br/>
              <strong>Last Seen:</strong> {{ last_seen }}<br/>
              <strong>Hors ligne depuis:</strong> {{ offline_since }}<br/>
              <strong>Durée:</strong> {{ offline_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Causes courantes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Problèmes de connectivité réseau<br/>
          • Terminal éteint ou redémarré<br/>
          • Crash ou blocage du logiciel<br/>
          • Pannes de service internet
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions recommandées:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Vérifiez l'alimentation et la connexion réseau du terminal<br/>
          2. Redémarrez le dispositif terminal<br/>
          3. Vérifiez la connectivité internet<br/>
          4. Vérifiez les paramètres de pare-feu et de sécurité
        </mj-text>

        {% if active_shift %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Avertissement de shift actif
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Ce terminal a un shift actif. Les données de vente ne seront pas synchronisées jusqu'à ce qu'il soit reconnecté.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_terminals_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir l'état du terminal
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Vous recevrez une autre notification lorsque le terminal se reconnectera.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ TERMINAL DÉCONNECTÉ

Terminal POS hors ligne

{{ terminal_name }} has gone offline and is no longer responding.

INFORMATIONS SUR LE TERMINAL : 
- Terminal : {{ terminal_name }}
- Emplacement : {{ location }}
- Dernière connexion : {{ last_seen }}
- Hors ligne depuis : {{ offline_since }}
- Durée : {{ offline_duration }}

CAUSES COURANTES : 
• Problèmes de connectivité réseau
• Terminal éteint ou redémarré
• Crash ou blocage du logiciel
• Pannes de service internet

ACTIONS RECOMMANDÉES : 
1. Vérifiez l'alimentation et la connexion réseau du terminal
2. Redémarrez le dispositif terminal
3. Vérifiez la connectivité internet
4. Vérifiez les paramètres de pare-feu et de sécurité

{% if active_shift %}
⚠️ AVERTISSEMENT DE SHIFT ACTIF : 
Ce terminal a un shift actif. Les données de vente ne seront pas synchronisées jusqu'à ce qu'il soit reconnecté.
{% endif %}

Voir l'état du terminal : {{ admin_terminals_url }}

Vous recevrez une autre notification lorsque le terminal se reconnectera.