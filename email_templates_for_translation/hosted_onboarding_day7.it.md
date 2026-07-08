---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
Metti in Atto le Tue Vendite - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Iniziare: Marketing & Crescita
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Porta traffico e vendite a {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Ciao {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Ora che <strong>{{ store_name }}</strong> prende forma, è il momento di concentrarsi sul traffico e sulla crescita delle vendite. Ecco cinque suggerimenti di marketing per iniziare.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Crea il tuo primo codice sconto
        </mj-text>
        <mj-text font-size="14px">
          Offri uno sconto di lancio per attrarre i tuoi primi clienti. Vai a <strong>Marketing > Codici Sconto</strong> per creare sconti percentuali o fissi con limiti di utilizzo e date di scadenza opzionali.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configura la Riacquisizione dei Carrelli Abbandonati
        </mj-text>
        <mj-text font-size="14px">
          Recupera automaticamente le vendite perse. Abilita le email di riacquisizione dei carrelli abbandonati sotto <strong>Marketing > Carrelli Abbandonati</strong> per ricordare ai clienti gli articoli che hanno lasciato.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Connetti i tuoi account di Social Media
        </mj-text>
        <mj-text font-size="14px">
          Collega i tuoi profili di social media al tuo negozio in modo che i clienti possano trovarti e seguirti. Aggiungi i link social sotto <strong>Impostazioni > Social Media</strong> per mostrarli nel piè di pagina del tuo negozio.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configura il Tracciamento di Google Analytics
        </mj-text>
        <mj-text font-size="14px">
          Capisci da dove provengono i tuoi visitatori e come interagiscono con il tuo negozio. Aggiungi il tuo ID di tracciamento di Google Analytics sotto <strong>Impostazioni > Analytics</strong> per iniziare a raccogliere i dati.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Crea un Form di Iscrizione alla Newsletter
        </mj-text>
        <mj-text font-size="14px">
          Costruisci la tua lista email fin dal primo giorno. Aggiungi un form di iscrizione alla newsletter al tuo negozio per catturare gli indirizzi email dei visitatori. Utilizza questi contatti per promozioni, lanci di prodotti e interazione con i clienti.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Vai al Marketing" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Iniziare: Marketing & Crescita - {{ store_name }}

Ciao {{ name|default:'there' }},

Ora che {{ store_name }} prende forma, è il momento di concentrarsi sul traffico e sulla crescita delle vendite. Ecco cinque suggerimenti di marketing per iniziare.

1. Crea il tuo primo codice sconto
Offri uno sconto di lancio per attrarre i tuoi primi clienti. Vai a Marketing > Codici Sconto per creare sconti con limiti di utilizzo e date di scadenza opzionali.

2. Configura la Riacquisizione dei Carrelli Abbandonati
Recupera automaticamente le vendite perse. Abilita le email di riacquisizione dei carrelli abbandonati sotto Marketing > Carrelli Abbandonati.

3. Connetti i tuoi account di Social Media
Collega i tuoi profili di social media al tuo negozio. Aggiungi i link social sotto Impostazioni > Social Media.

4. Configura il Tracciamento di Google Analytics
Capisci da dove provengono i tuoi visitatori. Aggiungi il tuo ID di tracciamento di Google Analytics sotto Impostazioni > Analytics.

5. Crea un Form di Iscrizione alla Newsletter
Costruisci la tua lista email fin dal primo giorno. Aggiungi un form di iscrizione alla newsletter per catturare gli indirizzi email dei visitatori per promozioni e interazione.

Vai al Marketing: {{ admin_url }}

Hai bisogno di aiuto? Contatta {{ support_email }}