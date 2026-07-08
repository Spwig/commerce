---
title: Groupes de magasins POS
---

Les groupes de magasins organisent plusieurs emplacements de vente au détail avec des configurations partagées. Au lieu de configurer chaque terminal individuellement, regroupez les terminaux par région, franchise ou type d'emplacement et appliquez les paramètres au niveau du groupe. Les groupes prennent en charge l'héritage des paramètres - la devise, la langue, le fuseau horaire, les modèles de reçus et le contenu promotionnel s'appliquent des groupes vers les magasins individuels. Cela simplifie la gestion pour les commerçants multi-emplacements tout en préservant la flexibilité pour les surcharges spécifiques aux magasins lorsqu'elles sont nécessaires.

Utilisez des groupes de magasins lorsque vous gérez plusieurs emplacements de vente au détail, franchises ou marchés régionaux avec des exigences opérationnelles différentes.

![Liste des groupes de magasins](/static/core/admin/img/help/pos-store-groups/storegroup-list.webp)

## Qu'est-ce qu'un groupe de magasins ?

Les groupes de magasins sont des conteneurs organisationnels pour les entrepôts et terminaux qui partagent des caractéristiques communes:

**Stratégies de regroupement courantes**:
- **Géographique** : Région du Nord, Région du Sud, Côte Ouest, Côte Est
- **Franchise** : Magasins du Franchiseur A, Magasins du Franchiseur B, Magasins de la Société Mère
- **Format** : Emplacements en centre commercial, Magasins indépendants, Magasins pop-up
- **Marché** : Magasins nationaux, Magasins européens, Magasins d'Asie-Pacifique

Les groupes ne modifient pas le fonctionnement physique des terminaux - ils fournissent une couche de configuration qui simplifie la gestion à grande échelle.

## Quand utiliser des groupes de magasins

**Un seul emplacement** - Pas besoin de groupes. Configurez directement les terminaux.

**2-3 emplacements avec les mêmes paramètres** - Les groupes sont optionnels. Peut être plus facile de configurer directement les terminaux.

**4+ emplacements** - Les groupes sont fortement recommandés. La configuration centralisée économise du temps.

**Opérations multi-pays** - Les groupes sont essentiels. Des devises, langues et fuseaux horaires différents nécessitent des surcharges au niveau du groupe.

**Opérations de franchise** - Les groupes sont critiques. Chaque franchiseur a besoin de paramètres indépendants tout en maintenant la cohérence de la marque.

## Hiérarchie d'héritage des paramètres

Spwig POS utilise une cascade de 4 niveaux de paramètres (priorité la plus élevée à la plus basse):

| Niveau | Priorité | Exemple | Cas d'utilisation |
|--------|----------|---------|------------------|
| **Terminal** | 1 (la plus élevée) | Le terminal 5 modifie la largeur du papier à 58 mm | Un seul terminal a un matériel d'imprimante unique |
| **Magasin** | 2 | Le magasin 2 modifie la devise en GBP | Emplacement au Royaume-Uni parmi des magasins principalement américains |
| **Groupe** | 3 | Groupe européen qui définit le fuseau horaire sur CET | Cohérence régionale à travers plusieurs magasins |
| **Site** | 4 (la plus basse) | Défaut mondial : USD, anglais, UTC | Valeur par défaut pour toutes les configurations non définies |

**Fonctionnement**:
- Le système vérifie d'abord les paramètres du terminal
- Si non définis, vérifie les paramètres du magasin
- Si non définis, vérifie les paramètres du groupe
- Si non définis, utilise les paramètres par défaut du site

**Exemple**:
- Défaut du site : Devise = USD, Langue = Anglais
- Groupe « Magasins européens » : Devise = EUR, Langue = non définie
- Magasin « Flagship de Paris » : Devise = non définie, Langue = Français
- Terminal « Encaisse 1 de Paris » : Devise = non définie, Langue = non définie

**Résultat pour l'encaisse 1 de Paris**:
- Devise : EUR (héritée du groupe)
- Langue : Français (héritée du magasin)

Cette cascade permet des paramètres généraux avec des surcharges ciblées là où nécessaire.

## Créer un groupe de magasins

Accédez à **POS > Groupes de magasins** et cliquez sur **+ Ajouter un groupe de magasins**:

![Formulaire d'ajout d'un groupe de magasins](/static/core/admin/img/help/pos-store-groups/storegroup-add-form.webp)

### Configuration de base

**Nom du groupe** - Étiquette descriptive (ex. : « Magasins de la Côte Ouest », « Franchises européennes », « Emplacements en centre commercial »)

**Code** - Identifiant court et unique (ex. : « WEST », « EUR », « MALL »):
- Utilisé internement pour les références
- Doit être unique à travers tous les groupes
- 2 à 10 caractères, alphanumériques
- Majuscules recommandées pour la cohérence

**Ordre de tri** - Contrôle l'ordre d'affichage dans les listes d'administration (les numéros plus bas apparaissent en premier):
- Utilisez des multiples de 10 : 10, 20, 30 (permet d'insérer de nouveaux groupes entre les existants)
- Aide à organiser logiquement les groupes (ordre géographique, ordre de taille, etc.)

### Surcharges régionales

**Surcharges de devise** - Définir une devise au niveau du groupe différente du défaut du site:
- Exemple : le groupe européen utilise EUR, le groupe Asie-Pacifique utilise JPY
- Les terminaux de ce groupe utilisent par défaut cette devise
- Affecte l'affichage des prix, la conciliation en espèces, les rapports

**Surcharges de langue** - Définir une langue au niveau du groupe différente du défaut du site:
- Exemple : les magasins français utilisent le français, les magasins allemands utilisent l'allemand
- Affecte la langue de l'interface POS, la langue des reçus (si le modèle le prend en charge)
- Le personnel voit l'interface POS dans cette langue lorsqu'ils se connectent aux terminaux du groupe

**Surcharges de fuseau horaire** - Définir un fuseau horaire au niveau du groupe différent du défaut du site:
- Exemple : les magasins de la Côte Ouest utilisent America/Los_Angeles, les magasins européens utilisent Europe/Paris
- Affecte les horodatages des shifts, la planification des rapports, la planification des diapositives promotionnelles
- Assure que les rapports de shift correspondent aux heures d'ouverture locales

**Quand surcharger**:
- **Devise** : Surchargez toujours pour les emplacements internationaux (différentes devises de paiement)
- **Langue** : Surchargez pour les marchés non anglophones (contenu destiné aux clients)
- **Fuseau horaire** : Surchargez pour les emplacements à plus de 2 heures de la devise par défaut du site (horodatages locaux précis)

## Associer des entrepôts à des groupes

Après avoir créé un groupe, affectez des entrepôts à ce groupe:

1. Accédez à **Catalogue > Entrepôts**
2. Éditez l'entrepôt représentant un emplacement de magasin
3. Définissez le champ **Groupe de magasin** sur votre groupe créé
4. Enregistrez

Tous les terminaux affectés à cet entrepôt héritent maintenant des paramètres du groupe.

**Exemple de configuration**:
- Créer un groupe : « Magasins européens » (Devise : EUR, Langue : non définie, Fuseau horaire : CET)
- Créer des entrepôts : « Magasin de Paris », « Magasin de Berlin », « Magasin de Rome »
- Affecter les trois entrepôts au groupe « Magasins européens »
- Créer des terminaux : « Encaisse 1 de Paris », « Encaisse 1 de Berlin », « Encaisse 1 de Rome »
- Chaque terminal hérite de la devise EUR et du fuseau horaire CET du groupe
- Surcharge de la langue au niveau du magasin : Paris=Français, Berlin=Allemand, Rome=Italien

## Paramètres contrôlés par les groupes

Les groupes peuvent surcharger ces paramètres:

**Paramètres opérationnels**:
- Devise (affecte l'affichage des prix et la conciliation en espèces)
- Langue (affecte la langue de l'interface POS)
- Fuseau horaire (affecte les horodatages et la planification)

**Paramètres de contenu** (via des modèles à portée limitée):
- Modèles de reçus (créer des conceptions de reçus spécifiques au groupe)
- Diapositives promotionnelles (cibler les promotions sur des groupes spécifiques)

**Non contrôlés par les groupes**:
- Configuration matérielle des terminaux (configurée par terminal)
- Affectations du personnel (configurée par terminal)
- Niveaux de stock des entrepôts (configurée par entrepôt)
- Comptes de fournisseurs de paiement (configurés au niveau du site ou par fournisseur)

## Exemples concrets

### Exemple 1 : Détaillant de mode international

**Configuration**:
- 50 magasins répartis dans 5 pays
- Chaque pays a des devises, langues et exigences fiscales différentes

**Structure de groupe**:
- Groupe : « Magasins des États-Unis » (USD, anglais, America/New_York)
  - 20 entrepôts (New York, Los Angeles, Chicago, etc.)
  - 60 terminaux
- Groupe : « Magasins du Royaume-Uni » (GBP, anglais, Europe/London)
  - 10 entrepôts (Londres, Manchester, etc.)
  - 30 terminaux
- Groupe : « Magasins de l'UE » (EUR, non défini, Europe/Paris)
  - 15 entrepôts (Paris, Berlin, Rome, etc.)
  - 45 terminaux
  - Surcharge de la langue au niveau du magasin (Paris=français, Berlin=allemand, Rome=italien)
- Groupe : « Magasins du Japon » (JPY, japonais, Asia/Tokyo)
  - 5 entrepôts (Tokyo, Osaka, etc.)
  - 15 terminaux

**Avantages**:
- Une configuration de groupe s'applique à tous les magasins de chaque marché
- Modèles de reçus limités aux groupes (format de TVA pour l'UE, impôt sur les ventes pour les États-Unis)
- Diapositives promotionnelles ciblées par région (États-Unis : Vente du Memorial Day, UE : Vente des vacances d'été)

### Exemple 2 : Chaîne de cafés

**Configuration**:
- 30 emplacements, tous dans le même pays, mais différents formats

**Structure de groupe**:
- Groupe : « Emplacements en centre commercial » (non défini, non défini, non défini)
  - 10 magasins en centre commercial
  - Diapositives promotionnelles horaires étendues (ouverts jusqu'à 21h)
  - Modèle de reçu avec code QR de validation de parking en centre commercial
- Groupe : « Magasins indépendants » (non défini, non défini, non défini)
  - 15 magasins en face de la rue
  - Diapositives promotionnelles horaires standard
  - Modèle de reçu standard
- Groupe : « Emplacements aéroportuaires » (non défini, non défini, non défini)
  - 5 magasins aéroportuaires
  - Diapositives promotionnelles 24/7
  - Modèle de reçu avec intégration de code QR d'informations sur les vols

**Avantages**:
- Contenu promotionnel différent pour différents formats
- Personnalisation du reçu selon l'emplacement
- Gestion simplifiée (mettre à jour un groupe au lieu de mettre à jour 10 magasins individuels)

### Exemple 3 : Opération de franchise

**Configuration**:
- 100 magasins, 20 différents franchiseurs

**Structure de groupe**:
- Groupe : « Franchiseur A » (non défini, non défini, non défini)
  - 10 magasins gérés par Franchiseur A
  - Informations de contact du Franchiseur A sur les reçus (via le modèle de reçu du groupe)
  - Contenu promotionnel du Franchiseur A (événements locaux, offres)
- Groupe : « Franchiseur B » (non défini, non défini, non défini)
  - 8 magasins gérés par Franchiseur B
  - Informations de contact du Franchiseur B sur les reçus
  - Contenu promotionnel du Franchiseur B
- (Répéter pour tous les franchiseurs)
- Groupe : « Magasins de la société mère » (non défini, non défini, non défini)
  - 5 magasins propriétaires de la société mère
  - Marque de la société mère et promotions

**Avantages**:
- Chaque franchiseur gère ses propres paramètres de groupe
- Cohérence de la marque maintenue via les paramètres par défaut du site
- Indépendance des franchiseurs via les surcharges de groupe

## Gestion des paramètres de groupe

**Changer les paramètres de groupe** affecte tous les terminaux de ce groupe:
- Changement de devise : Tous les terminaux du groupe basculent vers la nouvelle devise lors de la prochaine synchronisation
- Changement de langue : Tous les terminaux du groupe basculent vers la nouvelle langue lors de la prochaine synchronisation
- Changement de fuseau horaire : Tous les terminaux du groupe recalculent les horodatages lors de la prochaine synchronisation

**Considérations sur l'impact**:
- Testez les changements sur un seul terminal avant de les appliquer à l'ensemble du groupe
- Informez le personnel des changements à venir (ex. : changement de langue)
- Planifiez les changements pendant les heures creuses pour minimiser les perturbations

**Supprimer un groupe**:
- Réassignez tous les entrepôts à un autre groupe ou supprimez l'affectation du groupe
- Les terminaux perdent les paramètres du groupe et retournent aux paramètres par défaut du site
- Ne pouvez pas supprimer un groupe tant que des entrepôts y sont encore affectés

## Conseils

- **Utilisez des codes significatifs** - « WEST » est plus clair que « GRP1 » lors de la révision des configurations
- **Planifiez la hiérarchie avant de créer des groupes** - Réfléchissez à votre structure organisationnelle en premier ; la restructuration ultérieure est fastidieuse
- **Testez les paramètres de groupe avec un seul terminal** - Avant d'affecter 50 entrepôts à un groupe, testez les paramètres du groupe avec un seul terminal
- **Surchargez rarement au niveau du magasin** - Trop de surcharges au niveau du magasin annulent l'objectif des groupes
- **Documentez les objectifs des groupes** - Notez dans le nom du groupe ce qui le distingue (géographie, format, franchiseur)
- **Utilisez l'ordre de tri stratégiquement** - Classez les groupes par importance (Magasins de la société mère en premier) ou géographie (Ouest à Est) pour une navigation plus facile
- **Gardez le nombre de groupes raisonnable** - 20+ groupes suggèrent une sursegmentation ; envisagez de les regrouper
- **Les surcharges de devise sont permanentes** - Changer la devise d'un groupe pendant l'opération complique le comptabilité ; planifiez soigneusement

