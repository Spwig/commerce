---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
Tipps, um das Beste aus {{ store_name }} zu machen

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
          Tipps zum Einstieg
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Nutzen Sie Ihr Spwig-Shop optimal
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hallo {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Jetzt, da <strong>{{ store_name }}</strong> online ist, hier sind einige Tipps, um das Beste aus Ihrem Shop zu machen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Ihr Aussehen anpassen
        </mj-text>
        <mj-text font-size="14px">
          Besuchen Sie <strong>Design > Theme Einstellungen</strong>, um ein Theme auszuwählen, Ihr Logo hochzuladen und Ihre Markenfarben festzulegen. Ihr Online-Shop aktualisiert sich sofort, damit Sie Änderungen in Echtzeit vorabsehen können.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Ihre Produkte hinzufügen
        </mj-text>
        <mj-text font-size="14px">
          Gehen Sie zu <strong>Katalog > Produkte</strong>, um mit dem Hinzufügen Ihrer Artikel zu beginnen. Sie können Produktvarianten (Größe, Farbe) erstellen, Preise festlegen, Lager verwalten und hochwertige Bilder hochladen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Zahlungsmethoden einrichten
        </mj-text>
        <mj-text font-size="14px">
          Gehen Sie zu <strong>Einstellungen > Zahlungsdienste</strong>, um Stripe, PayPal oder eine andere Zahlungsmethode zu verknüpfen. Sie können mehrere Anbieter aktivieren, damit Ihre Kunden auf ihre bevorzugte Art zahlen können.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Versand konfigurieren
        </mj-text>
        <mj-text font-size="14px">
          Unter <strong>Einstellungen > Versand</strong> können Sie Ihre Versandzonen und -gebühren einrichten. Sie können feste Gebühren, gewichtsbasierte oder kostenlose Versandregeln für verschiedene Regionen erstellen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Ihre SEO optimieren
        </mj-text>
        <mj-text font-size="14px">
          Spwig generiert automatisch Sitemaps und Metatags. Besuchen Sie <strong>Einstellungen > SEO</strong>, um Ihre Seitentitel, Beschreibungen und sozialen Teilenbilder anzupassen, damit Kunden Ihren Shop finden können.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Zum Admin-Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Tipps zum Einstieg - {{ store_name }}

Hallo {{ name|default:'there' }},

Jetzt, da {{ store_name }} online ist, hier sind einige Tipps, um das Beste aus Ihrem Shop zu machen.

1. Ihr Aussehen anpassen
Besuchen Sie Design > Theme Einstellungen, um ein Theme auszuwählen, Ihr Logo hochzuladen und Ihre Markenfarben festzulegen.

2. Ihre Produkte hinzufügen
Gehen Sie zu Katalog > Produkte, um mit dem Hinzufügen Ihrer Artikel zu beginnen, mit Varianten, Preisen und Bildern.

3. Zahlungsmethoden einrichten
Gehen Sie zu Einstellungen > Zahlungsdienste, um Stripe, PayPal oder eine andere Zahlungsmethode zu verknüpfen.

4. Versand konfigurieren
Unter Einstellungen > Versand können Sie Ihre Versandzonen und -gebühren für verschiedene Regionen einrichten.

5. Ihre SEO optimieren
Besuchen Sie Einstellungen > SEO, um Ihre Seitentitel, Beschreibungen und sozialen Teilenbilder anzupassen, damit Kunden Ihren Shop finden können.

Zum Admin-Panel: {{ admin_url }}

Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}