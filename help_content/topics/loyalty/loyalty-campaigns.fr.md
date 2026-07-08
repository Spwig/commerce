---
title: Campagnes de fidélisation
---

Les campagnes de fidélisation vous permettent de mettre en place des promotions limitées dans le temps et des récompenses automatisées qui dépassent les règles de cumul habituelles. Utilisez-les pour proposer des week-ends avec des points doubles, récompenser les clients à leur anniversaire, récupérer les clients inactifs ou offrir des bonus ciblés à des groupes spécifiques de membres.

Chaque campagne définit un déclencheur ou un calendrier, les membres auxquels elle s'applique et les actions à entreprendre. Une fois active, une campagne se déclenche automatiquement — vous la configurez une seule fois et Spwig gère le reste.

## Types de campagnes

| Type | Quand elle se déclenche |
|------|------------------------|
| **Déclenchée par un événement** | Lorsqu'un événement spécifique se produit (par exemple, un achat est effectué, un anniversaire est détecté) |
| **Planifiée** | Sur un calendrier récurrent (quotidien, hebdomadaire, mensuel) |
| **Manuelle** | Seulement lorsque vous l'exécutez explicitement depuis l'admin |
| **Comportementale** | Lorsqu'un client correspond à un modèle de comportement (par exemple, navigation sans achat) |

## Créer une campagne

Accédez à **Promotions > Campagnes de fidélisation** et cliquez sur **+ Ajouter une campagne de fidélisation**.

### Étape 1 : informations de base

- **Nom** — un nom clair et descriptif visible uniquement dans l'admin (par exemple, `Bonus d'anniversaire — 200 points`)
- **Slug** — généré automatiquement à partir du nom ; utilisé internement
- **Description** — notes optionnelles sur l'objectif de la campagne
- **Type de campagne** — sélectionnez le type à partir du tableau ci-dessus

### Étape 2 : déclencheur ou planification

**Pour les campagnes déclenchées par un événement**, définissez l'**Événement de déclenchement** qui déclenche la campagne. Les déclencheurs disponibles incluent :

| Déclencheur | Description |
|-------------|-------------|
| Commande passée | Se déclenche lorsqu'un membre termine une commande |
| Première commande | Se déclenche à la première commande d'un membre |
| Anniversaire du client | Se déclenche à l'anniversaire d'un membre |
| Anniversaire de l'adhésion | Se déclenche chaque année à l'anniversaire de l'adhésion d'un membre |
| Panier abandonné | Se déclenche lorsqu'un panier est abandonné sans passer à la caisse |
| Promotion de niveau | Se déclenche lorsqu'un membre passe à un niveau supérieur |
| Points sur le point d'expirer | Se déclenche lorsqu'un membre a des points sur le point d'expirer |
| Inactif depuis 90 jours | Se déclenche lorsqu'un membre n'a pas acheté depuis 90 jours |
| Avis soumis | Se déclenche lorsqu'un membre soumet un avis sur un produit |
| Référence convertie | Se déclenche lorsqu'un client référencé effectue un achat |

Vous pouvez ajouter des **Conditions de déclenchement** sous forme d'objet JSON pour filtrer davantage les moments où la campagne se déclenche. Par exemple, pour ne déclencher que les commandes supérieures à 100 $ :

```json
{
  "min_order_amount": 100
}
```

**Pour les campagnes planifiées**, définissez le **Type de planification** (Quotidien, Hebdomadaire, Mensuel ou Cron personnalisé) et configurez l'heure dans le champ **Configuration de la planification** :

```json
{
  "hour": 9,
  "minute": 0
}
```

### Étape 3 : actions

Le champ **Actions** définit ce qui se produit lorsqu'une campagne se déclenche. Entrez un tableau JSON d'objets d'action. L'action la plus courante est l'attribution de points bonus :

```json
[
  {
    "type": "award_points",
    "points": 200,
    "description": "Bonus d'anniversaire — merci d'être membre !"
  }
]
```

D'autres actions disponibles incluent l'envoi d'une notification par e-mail ou l'attribution d'un badge. Consultez la documentation de votre composant fournisseur pour obtenir la liste complète.

### Étape 4 : ciblage

Contrôlez les membres auxquels s'applique la campagne à l'aide des champs de ciblage :

- **Cibler tous les membres** — coché par défaut ; la campagne s'applique à chaque membre actif de fidélisation
- **Cibler un segment** — restreindre la campagne aux membres d'un segment spécifique (voir [Segments](#managing-member-segments) ci-dessous)
- **Cibler les niveaux** — restreindre la campagne aux membres de niveaux de fidélisation spécifiques

### Étape 5 : limites et délais de refroidissement

- **Nombre maximal de déclenchements par membre** — combien de fois le même membre peut bénéficier de cette campagne. Définissez à `1` pour des bonus uniques comme un cadeau d'anniversaire. Laissez vide pour une limite illimitée.
- **Délai de refroidissement (en jours)** — nombre minimum de jours entre les déclenchements de campagne pour le même membre. Par exemple, définissez à `365` pour empêcher une campagne d'anniversaire de se déclencher plus d'une fois par an.

### Étape 6 : dates de la campagne

Définissez la **Date de début** et la **Date de fin** pour rendre la campagne limitée dans le temps. Laissez les deux vides pour une campagne en cours.

Les campagnes peuvent être dans l'un des états suivants :

| État | Description |
|------|-------------|
| **Brouillon** | Créé mais pas encore actif ; en toute sécurité pour le configurer et le tester |
| **Actif** | En cours d'exécution et déclenchera lorsqu'il y aura des conditions remplies |
| **Suspendu** | Arrêté temporairement sans perdre la configuration |
| **Terminé** | Passé sa date de fin ; ne déclenche plus |
| **Archivé** | Caché de la liste active mais conservé pour les archives |

Après avoir rempli tous les champs, cliquez sur **Enregistrer**. Ensuite, changez l'état en **Actif** pour démarrer la campagne.

## Exemples pratiques

### Exemple : double points le week-end

**Scénario :** Attribuer 2x points sur tous les achats effectués pendant un week-end spécifique.

| Champ | Valeur |
|-------|-------|
| Nom | `Double Points Weekend — Mars` |
| Type de campagne | Basé sur un déclencheur |
| Événement de déclencheur | Commande passée |
| Actions | `["{\"type\": \"award_points_multiplier\", \"multiplier\": 2.0}"]` |
| Date de début | Vendredi soir |
| Date de fin | Dimanche minuit |
| Cibler tous les membres | Coché |

### Exemple : bonus d'anniversaire

**Scénario :** Donner 200 points bonus à chaque membre de fidélisation à son anniversaire.

| Champ | Valeur |
|-------|-------|
| Nom | `Birthday Bonus` |
| Type de campagne | Basé sur un déclencheur |
| Événement de déclencheur | Anniversaire du client |
| Actions | `["{\"type\": \"award_points\", \"points\": 200, \"description\": \"Happy birthday from us!\"}"]` |
| Nombre maximum de déclencheurs par membre | 1 |
| Délai de refroidissement (en jours) | 365 |
| Cibler tous les membres | Coché |

### Exemple : campagne de rachat

**Scénario :** Envoyer 100 points bonus aux membres qui n'ont pas acheté depuis 90 jours.

| Champ | Valeur |
|-------|-------|
| Nom | `90-Day Win-Back Bonus` |
| Type de campagne | Basé sur un déclencheur |
| Événement de déclencheur | Inactif pendant 90 jours |
| Actions | `["{\"type\": \"award_points\", \"points\": 100, \"description\": \"We miss you — here are some bonus points\"}"]` |
| Nombre maximum de déclencheurs par membre | 1 |
| Délai de refroidissement (en jours) | 180 |
| Cibler tous les membres | Coché |

## Gestion des segments de membres

Les segments vous permettent de cibler des campagnes sur des groupes spécifiques de membres de fidélisation. Accédez à **Promotions > Segments de fidélisation** pour les gérer.

### Types de segments

| Type | Description |
|------|-------------|
| **Basé sur des règles** | Appartenance déterminée par des règles (par exemple, membres avec plus de 1 000 points) |
| **Calcul dynamique** | Appartenance calculée à la demande à partir de critères en temps réel |
| **Affectation manuelle** | Les membres sont ajoutés au segment manuellement |

### Créer un segment

1. Accédez à **Promotions > Segments de fidélisation** et cliquez sur **+ Ajouter un segment de fidélisation**
2. Remplissez :
   - **Nom** — nom descriptif (par exemple, `High-Value Customers`, `Silver Tier Members`)
   - **Slug** — généré automatiquement
   - **Type de critère** — comment l'appartenance est déterminée
   - **Configuration des critères** — objet JSON définissant les règles d'appartenance
3. Cliquez sur **Enregistrer**

#### Exemple : segment pour les membres avec plus de 500 points

```json
{
  "min_available_points": 500
}
```

#### Exemple : segment uniquement pour les membres du niveau Or

```json
{
  "tier_slugs": ["gold"]
}
```

La colonne **Nombre de membres** dans la liste des segments indique combien de membres correspondent actuellement. Cliquez sur un segment et utilisez l'action **Rafraîchir le nombre de membres** pour le recalculer si vos données ont changé.

## Suivi des performances des campagnes

### Historique d'exécution des campagnes

Accédez à **Promotions > Exécutions de campagne** pour voir un historique de chaque fois qu'une campagne a été déclenchée pour un membre. Chaque enregistrement d'exécution affiche quelle campagne a été exécutée, pour quel membre et le résultat.

### Examiner la portée d'une campagne

Ouvrez tout enregistrement de campagne pour voir le compte **Nombre de déclencheurs** et quand la campagne s'est dernièrement déclenchée. Cela vous donne une vue d'ensemble rapide du nombre de membres qui ont bénéficié de la campagne.

## Conseils

Conservez tout le formatage markdown, les chemins d'image, les blocs de code et les termes techniques.

- Créez d'abord des campagnes en statut **Brouillon** afin de pouvoir vérifier toutes les paramètres avant qu'elles ne soient publiées
- Utilisez **Max Triggers Per Member** pour toutes les campagnes de bonus à usage unique (anniversaire, premier achat, inscription) afin d'éviter que les clients ne gagnent le bonus plus d'une fois
- Combinez un **Target Segment** avec une campagne basée sur un déclencheur pour lancer des promotions exclusives aux niveaux — par exemple, des points doubles sur les achats uniquement pour les membres Or et Platine
- Définissez une valeur **Cooldown Days** pour les campagnes de rattachement afin que les membres ne soient pas submergés s'ils effectuent un petit achat puis deviennent inactifs à nouveau peu de temps après
- La liste des campagnes est votre meilleur outil pour suivre les promotions actives — vérifiez-la avant de lancer de nouvelles offres pour vous assurer que les campagnes ne s'accumulent pas accidentellement
- Archivez les campagnes terminées au lieu de les supprimer afin d'avoir un historique des promotions que vous avez lancées et de quand