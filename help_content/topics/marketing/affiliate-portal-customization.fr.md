---
title: Personnalisation du Portail des Affiliés
---

Le portail des affiliés Spwig est la page d'accueil publique où les affiliés potentiels apprennent à connaître votre programme et s'inscrivent. Personnaliser ce portail vous permet d'aligner les messages, la marque et les appels à l'action avec la position unique de votre magasin. Un portail bien conçu attire des affiliés de haute qualité et convertit les visiteurs en partenaires actifs.

## Qu'est-ce que le Portail des Affiliés ?

Le portail des affiliés est accessible à l'adresse `/affiliate/` sur votre domaine de magasin. Il sert à :

- **Page de découverte** — Endroit où les affiliés potentiels apprennent à connaître votre structure de commission, vos avantages et vos exigences
- **Point d'entrée d'inscription** — Formulaire d'inscription pour de nouveaux affiliés (inscription invité ou basée sur un compte)
- **Passerelle de connexion** — Les affiliés existants peuvent s'identifier pour accéder à leur tableau de bord
- **Exposition de la marque** — Reflète l'identité de votre magasin et la proposition de valeur de votre programme d'affiliation

Le portail est entièrement personnalisable via les paramètres des affiliés dans l'administration, y compris le message d'ouverture, les points forts, les flux étape par étape et les options d'inscription.

![Page d'accueil du Portail des Affiliés](/static/core/admin/img/help/affiliate-portal-customization/portal-landing.webp)

## Accès aux Paramètres

Accédez à **Marketing > Programme d'Affiliation > Paramètres du Portail** pour personnaliser le portail.

Le modèle de paramètres des affiliés est un **singleton** — vous avez exactement un enregistrement de paramètres pour votre magasin entier. Tous les champs sont **traduisibles** à l'aide du système de traduction Spwig, donc vous pouvez personnaliser les messages pour chaque langue que votre magasin prend en charge.

## Section d'Accueil

La section d'accueil est la première chose que les affiliés potentiels voient. Elle comprend :

- **Titre** — Titre principal (ex. : "Rejoignez notre programme d'affiliation")
- **Sous-titre** — Texte d'accompagnement expliquant la valeur du programme (ex. : "Gagnez des commissions en promouvant des produits premium à votre audience")
- **Statistiques** — Métriques affichées automatiquement :
  - Nombre total de programmes actifs
  - Nombre total d'affiliés actifs
  - Taux moyen de commission (calculé sur tous les programmes actifs)
- **Boutons CTA** — Générés automatiquement :
  - **Se connecter** — Pour les affiliés existants
  - **Devenir affilié** — Active le flux d'inscription

### Personnalisation du Message d'Accueil

| Champ | Valeur d'exemple | Objectif |
|-------|------------------|---------|
| **Titre d'accueil** | "Collaborez avec nous et gagnez" | Atteindre l'attention avec un titre axé sur les avantages |
| **Sous-titre d'accueil** | "Rejoignez plus de 500 affiliés qui gagnent des commissions compétitives sur chaque vente que vous faites référencer" | Fournir une preuve sociale et clarifier l'offre |

Les statistiques sont **calculées automatiquement** et se mettent à jour en temps réel en fonction de vos programmes et affiliés actifs. Vous ne pouvez pas modifier manuellement ces valeurs.

## Section des Fonctionnalités

La section des fonctionnalités met en avant **6 cartes de bénéfices personnalisables** qui expliquent pourquoi les affiliés devraient rejoindre votre programme. Chaque carte de fonctionnalité contient :

- **Icône** — Classe d'icône FontAwesome (ex. : `fa-dollar-sign`, `fa-chart-line`, `fa-headset`)
- **Titre** — Titre du bénéfice (ex. : "Commissions compétitives")
- **Description** — Explication en 1 à 2 phrases (ex. : "Gagnez jusqu'à 15 % sur chaque vente que vous faites référencer")

### Fonctionnalités par défaut

Spwig fournit des fonctionnalités par défaut lors de l'installation initiale de l'application d'affiliation :

| Icône | Titre | Description |
|------|-------|-------------|
| `fa-dollar-sign` | Commissions compétitives | Gagnez des commissions généreuses sur chaque vente que vous faites référencer |
| `fa-link` | Liens de suivi faciles | Obtenez des liens de suivi uniques qui fonctionnent n'importe où |
| `fa-chart-line` | Analytiques en temps réel | Suivez les clics, les conversions et les revenus dans votre tableau de bord |
| `fa-calendar-check` | Paiements fiables | Recevez vos paiements à temps via PayPal ou virement bancaire |
| `fa-headset` | Support dédié | Notre équipe est là pour vous aider à réussir |
| `fa-gift` | Matériel de marketing | Accédez aux bannières, images et contenus promotionnels |

### Personnalisation des Fonctionnalités

Les fonctionnalités sont stockées sous forme d'**array JSON** dans la base de données. Modifiez-les directement dans le formulaire d'administration :

```json
[
  {
    "icon": "fa-percent",
    "title": "Jusqu'à 20 % de commission",
    "description": "Gagnez des commissions d'industrie leader sur les ventes de produits premium"
  },
  {
    "icon": "fa-rocket",
    "title": "Approbation rapide",
    "description": "Obtenez une approbation en 24 heures et commencez à promouvoir immédiatement"
  },
  {
    "icon": "fa-mobile-alt",
    "title": "Tableau de bord mobile",
    "description": "Gérez vos liens et suivez vos revenus depuis n'importe quel appareil"
  }
]
```

**Référence des icônes :** Utilisez toute classe d'icône FontAwesome 5 Free. Parcourez les icônes sur [fontawesome.com/icons](https://fontawesome.com/icons) et utilisez le nom de la classe (ex. : `fa-trophy`, `fa-users`, `fa-star`).

## Section Comment ça marche

La section "Comment ça marche" affiche un **flux visuel de 4 étapes** qui explique le parcours des affiliés. Chaque étape comprend :

- **Titre** — Nom de l'étape (ex. : "S'inscrire")
- **Description** — Explication en 1 à 2 phrases de ce qui se passe

### Étapes par défaut

| Étape | Titre | Description |
|------|-------|-------------|
| 1 | S'inscrire | Créez votre compte d'affilié gratuit en quelques minutes |
| 2 | Obtenir vos liens | Générez des liens de suivi uniques pour tout produit ou page |
| 3 | Promouvoir | Partagez vos liens avec votre audience via le contenu, les réseaux sociaux ou l'e-mail |
| 4 | Gagner des commissions | Recevez vos paiements lorsque les clients achètent en utilisant vos liens de référence |

### Personnalisation des Étapes

Les étapes sont stockées sous forme d'**array JSON**. Vous pouvez les modifier dans l'administration :

```json
[
  {
    "title": "Postulez pour rejoindre",
    "description": "Soumettez votre candidature et dites-nous à propos de votre plateforme"
  },
  {
    "title": "Obtenir l'approbation",
    "description": "Notre équipe examine votre candidature dans les 24 heures"
  },
  {
    "title": "Créer des liens",
    "description": "Accédez à votre tableau de bord et générez des liens de suivi instantanément"
  },
  {
    "title": "Commencer à gagner",
    "description": "Gagnez des commissions sur chaque vente que vous faites référencer — payés mensuellement via PayPal"
  }
]
```

Le flux visuel numérote automatiquement chaque étape (1, 2, 3, 4) sur la page d'accueil.

## Section CTA

La dernière section avant le formulaire d'inscription est la **section Appel à l'action (CTA)**. Elle fournit une dernière impulsion pour encourager les inscriptions.

| Champ | Valeur d'exemple | Objectif |
|-------|------------------|---------|
| **Titre CTA** | "Prêt à commencer à gagner ?" | Question directe qui crée de l'urgence |
| **Description CTA** | "Rejoignez notre programme d'affiliation aujourd'hui et commencez à gagner des commissions sur des produits que vous aimez déjà et que vous recommandez." | Renforcez les avantages et éliminez les frottements |

La section CTA affiche automatiquement le bouton **Devenir affilié** en dessous du texte.

## Paramètres d'Inscription

Contrôlez la manière dont les nouveaux affiliés s'inscrivent et les informations qu'ils fournissent.

### Formulaire d'Inscription Personnalisé

**Champ :** `custom_form` (ForeignKey vers le formulaire FormBuilder)

Si vous avez un formulaire d'inscription personnalisé construit avec le FormBuilder de Spwig, sélectionnez-le ici. Cela vous permet de collecter des informations supplémentaires lors de l'inscription (ex. : URL du site web, taille de l'audience, canaux de promotion).

**Laissez vide** pour utiliser le formulaire d'inscription d'affilié par défaut (email, mot de passe, détails de paiement).

### Permettre l'Inscription Invité

**Champ :** `allow_guest_registration` (Booléen)

- **Coché** — Les visiteurs peuvent postuler sans créer un compte Spwig au préalable
- **Non coché** — Les visiteurs doivent s'identifier ou créer un compte client avant de postuler

**Recommandation :** Activez l'inscription invité pour réduire les frottements. Vous pouvez toujours exiger une approbation pour vérifier les affiliés avant d'activer ceux-ci.

### Exiger une Approbation

**Champ :** `require_approval` (Booléen)

- **Coché** — Les nouveaux affiliés doivent attendre une approbation manuelle avant d'accéder à leur tableau de bord
- **Non coché** — Les nouveaux affiliés sont approuvés automatiquement et peuvent créer des liens immédiatement

**Recommandation :** Activez l'approbation manuelle si vous souhaitez vérifier les affiliés pour l'adéquation avec la marque, la prévention de la fraude ou des programmes exclusifs.

### URL des Conditions Générales

**Champ :** `terms_url` (URL)

Lien optionnel vers les conditions générales de votre programme d'affiliation. Si fourni, le formulaire d'inscription affiche une case à cocher exigeant que les affiliés acceptent vos conditions avant de s'inscrire.

**Exemple :** `/pages/affiliate-terms/`

### Message de Bienvenue

**Champ :** `welcome_message` (Texte)

Message affiché aux affiliés immédiatement après une inscription réussie. Utilisez-le pour :

- Les remercier pour leur inscription
- Expliquer les étapes suivantes (ex. : "Nous examinerons votre candidature dans les 24 heures")
- Lier aux ressources pour commencer

**Exemple :**
```
Bienvenue dans notre programme d'affiliation ! Nous avons reçu votre candidature et la traiterons dans les 24 heures. Vérifiez votre e-mail pour la confirmation d'approbation et les instructions pour vous connecter.
```

## Support Multilingue

Tous les champs de texte dans les Paramètres des Affiliés sont **traduisibles** à l'aide du widget de traduction Spwig :

- Titre d'accueil
- Sous-titre d'accueil
- Fonctionnalités (JSON traduit par langue)
- Étapes Comment ça marche (JSON traduit par langue)
- Titre CTA
- Description CTA
- Message de bienvenue

### Comment la Traduction Fonctionne

Lorsque vous modifiez un champ traduisible, vous verrez un widget de traduction qui vous permet de fournir du contenu pour chaque langue activée. Pour les champs JSON (fonctionnalités, étapes), vous fournissez des objets JSON séparés par langue :

**Anglais :**
```json
[
  {"icon": "fa-dollar-sign", "title": "Competitive Commissions", "description": "Earn up to 15% on every sale"}
]
```

**Espagnol :**
```json
[
  {"icon": "fa-dollar-sign", "title": "Comisiones Competitivas", "description": "Gana hasta el 15% en cada venta"}
]
```

Le portail affiche automatiquement la version de la langue correcte en fonction des préférences de langue du visiteur.

## Prévisualiser vos Changements

Après avoir personnalisé les paramètres du portail :

1. **Enregistrez** vos modifications dans l'administration
2. Visitez `/affiliate/` sur le frontend de votre magasin (ouvrir dans un nouvel onglet)
3. **Testez le flux d'inscription** en cliquant sur "Devenir affilié"
4. **Vérifiez la cohérence de la marque** — le portail correspond-il à la conception et aux messages de votre magasin ?

Vous pouvez apporter des modifications itératives et actualiser la page pour voir les mises à jour immédiatement.

## Exemples de Personnalisation

### Scénario 1 : Magasin de Vêtements en Ligne

**Objectif :** Recruter des influenceurs et blogueurs de mode.

| Paramètre | Valeur |
|-----------|-------|
| Titre d'accueil | "Promouvoir les styles que vous aimez et gagnez" |
| Sous-titre d'accueil | "Rejoignez plus de 1 200 influenceurs qui gagnent 12 % de commissions sur chaque vente" |
| Fonctionnalité 1 | Icône : `fa-tshirt`, Titre : "Collections de Mode Sélectionnées", Description : "Promouvoir des vêtements et accessoires premium" |
| Fonctionnalité 2 | Icône : `fa-percentage`, Titre : "12 % de Commission", Description : "Taux d'industrie leader sur tous les produits" |
| Fonctionnalité 3 | Icône : `fa-camera`, Titre : "Contenu Exclusif", Description : "Accédez aux photos, vidéos et actifs de campagne de produits" |
| Permettre l'Inscription Invité | Coché |
| Exiger une Approbation | Coché (examen manuel pour l'adéquation avec la marque) |

### Scénario 2 : Programme de Partenariat SaaS B2B

**Objectif :** Recruter des consultants et agences pour des références de logiciels d'entreprise.

| Paramètre | Valeur |
|-----------|-------|
| Titre d'accueil | "Partenaires avec nous pour croître vos revenus" |
| Sous-titre d'accueil | "Gagnez 500 $ par référence d'entreprise via notre programme de partenariat B2B" |
| Fonctionnalité 1 | Icône : `fa-handshake`, Titre : "$500 par référence", Description : "Commission fixe pour les leads d'entreprises qualifiés" |
| Fonctionnalité 2 | Icône : `fa-clock`, Titre : "Cookie de 180 jours", Description : "Fenêtre d'attribution longue pour les cycles de vente complexes" |
| Fonctionnalité 3 | Icône : `fa-user-tie`, Titre : "Gestionnaire de Partenaire Dédicacé", Description : "Support de luxe pour vos clients" |
| Permettre l'Inscription Invité | Non coché (B2B nécessite un compte) |
| Exiger une Approbation | Coché (programme invité uniquement) |
| URL des Conditions Générales | `/pages/partner-program-terms/` |

## Conseils

- Personnalisez votre **titre d'accueil** pour se concentrer sur les avantages, pas sur les fonctionnalités — "Gagnez pendant que vous dormez" est plus convaincant que "Inscription au programme d'affiliation"
- Utilisez **la preuve sociale** dans le sous-titre (ex. : "Rejoignez 500+ affiliés") pour construire la confiance et la crédibilité
- Choisissez **des icônes FontAwesome** qui renforcent visuellement chaque avantage — l'icône doit communiquer instantanément la valeur
- Gardez les descriptions des fonctionnalités à **1 à 2 phrases** — le portail est sur la conversion, pas sur l'explication exhaustive
- Testez vous-même le **flux d'inscription** avant de promouvoir le portail — repérez les points de friction comme des champs de formulaire confus ou des liens cassés
- Activez **l'inscription invité** pour réduire les frottements d'inscription, puis utilisez **exiger l'approbation** pour vérifier les affiliés après leur soumission
- Utilisez le **message de bienvenue** pour fixer les attentes (timeline d'approbation, étapes suivantes, contact de support) et réduire les demandes de support
- Mettez à jour le portail **saisonnièrement** pour s'aligner sur les campagnes — mettez en avant les promotions de commissions spéciales ou les lancements de produits

Souvenez-vous : Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques exactement comme indiqué dans les règles de préservation.