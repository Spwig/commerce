<p align="center">
  <a href="README.md">English</a> |
  <strong>Français</strong> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <a href="README.zh-Hant.md">繁體中文</a> |
  <a href="README.pt.md">Português</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ar.md">العربية</a> |
  <a href="README.hi.md">हिन्दी</a> |
  <a href="README.id.md">Bahasa Indonesia</a> |
  <a href="README.it.md">Italiano</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.tr.md">Türkçe</a> |
  <a href="README.vi.md">Tiếng Việt</a> |
  <a href="README.th.md">ไทย</a>
</p>

<p align="center">
  <img src="https://spwig.com/images/logo.svg" alt="Spwig" width="200">
</p>

<h1 align="center">Spwig</h1>

<p align="center">
  <strong>Le e-commerce auto-hébergé pour les marchands qui veulent maîtriser leur boutique.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">Site web</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">Documentation</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">Communauté</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/fr/marketplace">Marketplace</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/fr/demos">Démos en direct</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Qu'est-ce que Spwig ?

Spwig est une plateforme e-commerce complète : catalogue, panier, tunnel
de commande, commandes, clients, paiements, expédition, thèmes,
constructeur de pages, API admin, POS, abonnements, fidélité, blog, SEO —
toute la pile. Construite avec **Django 5**, **PostgreSQL** et **Redis**,
livrée sous forme d'un ensemble de conteneurs Docker, elle tourne sur un
VPS à 5 $ ou sur votre propre matériel.

Contrairement aux plateformes hébergées, **vous êtes propriétaire du
code, de la base de données et des données clients.** Aucun frais par
transaction. Aucun verrouillage. Si vous souhaitez la forker et suivre
votre propre voie, la licence l'autorise explicitement.

<br />

## Éditions

Même binaire. Un fichier de licence signé active ou désactive les
fonctionnalités à l'exécution. Community est ce que vous obtenez par
défaut lorsque vous lancez `docker compose up` ; pour passer à une
édition supérieure, il suffit de coller une clé dans l'admin.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| E-commerce complet, thèmes, constructeur de pages, interface POS | ✓ | ✓ | ✓ |
| Fournisseurs de paiement de votre choix | ✓ | ✓ | ✓ |
| Fournisseurs d'expédition de votre choix | ✓ | ✓ | ✓ |
| Accès à la marketplace (thèmes premium + intégrations) | ✓ | ✓ | ✓ |
| Autocomplétion d'adresses hébergée par Spwig | Gratuit · limité | Limite supérieure | Limite maximale |
| GeoIP hébergé par Spwig (localisation des visiteurs) | Gratuit · limité | Limite supérieure | Limite maximale |
| Notifications push (application admin iOS) | Gratuit · limité | Limite supérieure | Limite maximale |
| Point de vente (prise en charge du terminal POS) | ✓ | ✓ | ✓ |
| Passerelle e-mail hébergée avec IP réputées + DKIM | – | ✓ | ✓ |
| Support prioritaire | – | ✓ | ✓ |
| SSO entreprise (Azure AD, Okta) | – | – | ✓ |

<br />

## Démarrage rapide

### Option 1 — Installation en une ligne (recommandée)

L'[installeur Spwig](https://github.com/Spwig/spwig) met tout en place
en une seule commande : Docker, PostgreSQL, Redis, MinIO, TLS via
Cloudflare ou auto-signé, assistant au premier démarrage, utilisateur
admin. Images signées récupérées depuis `registry.spwig.com`.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

Les mises à jour se font depuis l'admin — voir [UPGRADING.md](UPGRADING.md).

### Option 2 — Depuis les sources

Vous voulez compiler depuis ce dépôt, bidouiller le code ou distribuer
un fork :

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

Boutique sur `http://localhost`, admin sur `http://localhost/fr/admin/`.
L'édition Community s'active automatiquement au premier démarrage — pas
d'aller-retour avec un serveur de licences, aucune clé requise. Mettez
à jour ensuite avec `git pull` et `docker compose build`.

<br />

## Fonctionnalités

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>Boutique et tunnel de commande</h3>
      <p>Rendu côté serveur par défaut — temps de premier octet rapide,
      fonctionne sans JavaScript, pensé mobile d'abord (80 % du trafic
      vient de petits écrans). Mode headless optionnel via le
      <a href="https://github.com/Spwig/headless-sdk">Spwig headless
      SDK</a> et les <a href="https://github.com/Spwig/react">composants
      React</a>.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/storefront-product.webp" alt="Storefront product page">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/page-builder.webp" alt="Page builder">
    </td>
    <td width="50%" valign="top">
      <h3>Constructeur de pages</h3>
      <p>Les marchands construisent les pages de leur boutique à partir
      de widgets réutilisables — sections héros, grilles de produits,
      témoignages, intégrations — et prévisualisent en direct dans
      l'admin. Les widgets s'installent depuis la marketplace ou depuis
      votre propre dépôt de composants.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Gestion des commandes et des clients</h3>
      <p>Chaque commande, remboursement, renouvellement d'abonnement,
      téléchargement numérique et point de contact client au même
      endroit. Opérations en masse, rôles d'équipe à permissions
      restreintes, exports CSV/XLSX, application admin mobile (iOS)
      avec notifications push.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/order-management.webp" alt="Order management">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/branding-builder.webp" alt="Branding builder">
    </td>
    <td width="50%" valign="top">
      <h3>Thèmes et identité visuelle</h3>
      <p>Les design tokens (couleurs, typographie, espacements) pilotent
      chaque surface — boutique comme admin. Changez un token, tout se
      met à jour. Les thèmes vivent dans
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      et s'installent via la marketplace ; créez le vôtre avec le
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a>.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>Point de vente</h3>
      <p>Terminal POS complet pour les commerçants physiques :
      lecture de codes-barres, paiements fractionnés, impression de
      reçus, intégration du tiroir-caisse, écran face client, mode
      hors ligne. L'édition Community embarque le code, mais l'interface
      admin affiche un appel à mise à niveau — retirez-le si vous
      forkez, c'est parfaitement OK.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/pos-terminal.webp" alt="POS terminal">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/developer-portal.webp" alt="Developer portal">
    </td>
    <td width="50%" valign="top">
      <h3>Écosystème de fournisseurs</h3>
      <p>Tout ce qui dialogue avec un système externe — paiements,
      expédition, taux de change, traduction, GeoIP, SMS, e-mail — est
      un fournisseur enfichable. Créez le vôtre avec les
      <a href="https://github.com/Spwig/provider-sdks">provider SDKs</a>,
      publiez sur la marketplace, ou hébergez un registre privé.</p>
    </td>
  </tr>
</table>

<br />

## Architecture

- **Mono-locataire.** Chaque installation correspond à une boutique, un
  marchand, un Django Site. Les marchands multi-boutiques déploient une
  installation Spwig par boutique.
- **Monolithe modulaire.** Pas un maillage de microservices. Un unique
  processus Django gère la boutique + l'admin + l'API REST + les
  workers Celery. Simple à déployer, à comprendre et à forker.
- **Verrous de fonctionnalités à l'exécution.** Community/Pro/Enterprise
  tournent tous le même binaire. Une licence signée bascule les
  drapeaux — aucun code n'est retiré.

Visite complète : [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## Communauté et support

- **Discussions.** Questions ouvertes, idées, partages :
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **Forum communautaire.** [community.spwig.com](https://community.spwig.com)
  — fils de discussion approfondis, recettes de bonnes pratiques,
  vitrines d'extensions.
- **Rapports de bugs.** [Issues](https://github.com/Spwig/commerce/issues)
  avec les étapes de reproduction. Voir [SECURITY.md](SECURITY.md) pour
  la divulgation des vulnérabilités.
- **Support commercial.** Disponible pour les licences Pro et Enterprise.

<br />

## Contribuer

Nous utilisons le **DCO** (Developer Certificate of Origin) — chaque
commit est signé avec `git commit -s`. Aucune paperasse, aucun CLA.
Guide complet dans [CONTRIBUTING.md](CONTRIBUTING.md).

Les notes destinées aux assistants de code IA travaillant sur ce dépôt
se trouvent dans [CLAUDE.md](CLAUDE.md).

<br />

## Écosystème

Projets open-source apparentés dans l'[organisation Spwig](https://github.com/Spwig) :

| Dépôt | De quoi il s'agit |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | Ce dépôt — la plateforme centrale (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | Installeur en une ligne |
| [Spwig/components](https://github.com/Spwig/components) | Thèmes, intégrations et utilitaires (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | SDK pour créer des thèmes (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | SDK pour créer des fournisseurs de paiement / expédition / etc. (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | SDK client headless / API (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | Bibliothèque de composants React (Apache-2.0) |

<br />

## Licence

Spwig est sous [AGPL-3.0-or-later](LICENSE). Vous pouvez l'exécuter, le
modifier, le distribuer, le proposer sous forme de service hébergé —
tout cela est permis. Les versions modifiées proposées sur un réseau
doivent mettre leur code source à disposition de leurs utilisateurs.
C'est tout l'intérêt de l'AGPL par rapport à la GPL.

Les intégrations de fournisseurs bâties avec les SDK sont sous
Apache-2.0 : construire une intégration propriétaire de paiement /
expédition / SMS par-dessus les SDK ne déclenche donc pas l'AGPL.
C'est intentionnel — nous voulons un écosystème de fournisseurs florissant.

<br />

## Confidentialité et télémétrie

Spwig envoie un ping anonyme par jour à `updates.spwig.com/api/v1/telemetry/` :

- UUID d'installation (généré au premier démarrage, stocké localement)
- Version de Spwig
- Édition (community / pro / enterprise / trial / dev)
- Pays (résolu à partir de l'IP à l'entrée ; l'IP elle-même n'est pas stockée)
- Comptes agrégés des feature flags (fournisseurs de paiement
  configurés, thèmes installés) — jamais de données brutes clients ou
  commandes

**Désactivez** avec `SPWIG_TELEMETRY=0` dans votre environnement. Cela
bascule `settings.SPWIG_TELEMETRY_ENABLED` et la tâche périodique
quotidienne devient inopérante.

<br />

<p align="center">
  <sub>
    Conçu avec soin à Singapour.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">communauté</a>
  </sub>
</p>
