---
title: Suivi des affiliés & Liens
---

Le suivi des affiliés alimente tout le système de commissions en reliant les achats des clients aux affiliés qui les ont référencés. Ce guide explique comment fonctionnent les liens de suivi, les données que Spwig enregistre lorsqu'un client clique sur ces liens, et comment le système d'attribution basé sur les cookies détermine quel affilié gagne chaque commission.

Comprendre les mécanismes de suivi vous aide à résoudre les problèmes d'attribution, à analyser les performances des liens et à éduquer vos affiliés sur la manière dont ils peuvent maximiser leurs conversions.

## Qu'est-ce qu'un lien de suivi ?

Un lien de suivi est un URL unique qui redirige les clients vers votre boutique tout en enregistrant l'identité de l'affiliate dans un cookie. Chaque affilié peut créer plusieurs liens de suivi pointant vers différentes destinations — la page d'accueil, des produits spécifiques, des pages de collections ou des pages d'atterrissage.

Format d'exemple de lien de suivi:
```
https://yourstore.com/affiliate/track/a2b7f8c4d1e9/
```

Ce lien redirige vers la destination tout en définissant un cookie de suivi qui associe les achats futurs à l'affiliate qui possède le code de lien `a2b7f8c4d1e9`.

Les affiliés génèrent ces liens depuis leur tableau de bord du portail. Ils copient l'URL complète et la partagent dans des articles de blog, des réseaux sociaux, des emails ou tout autre canal où ils atteignent des clients potentiels.

## Composants des liens de suivi

Chaque lien de suivi contient ces éléments:

| Composant | Exemple | Description |
|-----------|---------|-------------|
| **URL de base** | `https://yourstore.com` | Votre domaine de boutique |
| **Chemin de suivi** | `/affiliate/track/` | Point de terminaison de suivi de Spwig |
| **Code de lien** | `a2b7f8c4d1e9` | Identifiant unique généré automatiquement à 12 caractères |
| **Destination** | Définie lors de la création du lien | Où le client atterrit après la redirection (page d'accueil, produit, etc.) |

Lorsqu'un affilié crée un lien, Spwig génère automatiquement le code unique à 12 caractères. L'affiliate n'a jamais besoin de créer ou de modifier manuellement ce code — il choisit simplement la destination et Spwig gère le reste.

### Étiquettes de lien (optionnelles)

Les affiliés peuvent ajouter une étiquette à chaque lien pour leur propre organisation:
- "Lien de la bio Instagram"
- "Description de YouTube"
- "Campagne de courriel Black Friday"

Les étiquettes aident les affiliés à suivre lesquels canaux promotionnels performent le mieux. Elles sont visibles uniquement pour l'affiliate et vous — les clients ne voient jamais l'étiquette.

## Fonctionnement du suivi

Le processus de suivi et d'attribution suit cinq étapes de clic à commission:

### 1. Client clique sur le lien

Un client potentiel clique sur le lien de suivi de l'affiliate depuis tout canal promotionnel (publication de réseaux sociaux, article de blog, newsletter électronique).

### 2. Clic enregistré

Le point de terminaison de suivi de Spwig enregistre les détails du clic:
- Adresse IP
- User agent (navigateur et appareil)
- Référent HTTP (d'où vient le clic)
- Horodatage
- Identifiant de session

Données apparaissent dans le **Clics** administrateur à **Affilié > Clics** pour l'analyse et la détection de fraude.

### 3. Cookie défini

Le système de suivi définit un cookie dans le navigateur du client avant de le rediriger. Le cookie contient:
- ID de l'affiliate (qui doit gagner la commission)
- ID du programme (quelle structure de commission s'applique)
- Code de lien (quel lien spécifique a été cliqué)

### 4. Client achète

Le client navigue dans votre boutique et termine un achat. Cela peut se produire immédiatement ou des jours/semaines plus tard, tant qu'il achète avant l'expiration du cookie.

### 5. Commission créée

À la caisse, Spwig vérifie le cookie de l'affiliate. Si trouvé et toujours valide (dans la fenêtre de durée du cookie), le système crée un enregistrement de commission avec le statut **En attente** lié à l'affiliate, au programme et à la commande.

## Attribution basée sur les cookies

Le cookie de suivi est le mécanisme central qui relie les achats aux affiliés. Comprendre comment fonctionnent les cookies vous aide à définir des fenêtres d'attribution optimales et à résoudre les problèmes de suivi.

### Structure du cookie

| Propriété | Valeur |
|----------|-------|
| **Nom** | `aff_{program_id}` (par exemple, `aff_7` pour l'ID de programme 7) |
| **Valeur** | JSON contenant l'ID de l'affiliate, le code de lien, l'horodatage |
| **Domaine** | Votre domaine de boutique |
| **Chemin** | `/` (accès site-wide) |
| **Durée** | Durée de vie du cookie du programme (1 à 365 jours) |
| **HttpOnly** | `true` (empêche l'accès JavaScript pour la sécurité) |
| **SameSite** | `Lax` (permet le suivi depuis les référents externes) |
| **Secure** | `true` sur les sites HTTPS (recommandé) |

### Fenêtre de durée de vie du cookie

La durée de vie du cookie détermine combien de temps les clients ont pour effectuer un achat après avoir cliqué sur un lien d'affiliate. Cette fenêtre est définie par programme à **Marketing > Programmes d'Affiliés** lors de la création ou de la modification d'un programme.

Durées de vie de cookie standard de l'industrie:
- **7 jours**: Produits de décision rapide (produits alimentaires, billets d'événement)
- **30 jours**: E-commerce standard (la configuration la plus courante)
- **60–90 jours**: Achats considérés (meubles, électronique, produits B2B)
- **365 jours**: Cycles de vente longs (biens de luxe, services à forte valeur)

Si un client clique sur un lien d'affiliate le 1er janvier et que votre durée de vie de cookie est de 30 jours, tout achat qu'il effectue jusqu'au 30 janvier crédite cet affilié. Les achats effectués le 31 janvier ou plus tard ne génèrent pas de commission car le cookie a expiré.

### Modèle d'attribution du dernier clic

Spwig utilise **l'attribution du dernier clic** : le clic le plus récent gagne. Voici comment cela fonctionne:

**Scénario** : Un client clique sur le lien de l'affiliate A le lundi, puis sur le lien de l'affiliate B le mercredi, puis effectue un achat le vendredi.

**Résultat** : L'affiliate B gagne la commission car son lien était le clic le plus récent.

Le cookie du dernier clic remplace les cookies d'affiliate précédents. Ce modèle est simple à comprendre et empêche les commissions doubles, bien qu'il signifie qu'un seul affilié reçoit le crédit par commande (le dernier avant l'achat).

## Enregistrement des clics

Spwig enregistre chaque clic sur chaque lien d'affiliate pour fournir des analyses à la fois pour vous et l'affiliate. Les données de clic aident à mesurer les performances des liens, à détecter la fraude et à optimiser les stratégies promotionnelles.

### Données capturées par clic

Accédez à **Affilié > Clics** pour consulter tous les clics enregistrés. Chaque entrée contient:

| Champ | Description |
|-------|-------------|
| **Lien** | Quel lien de suivi a été cliqué |
| **Affilié** | Qui possède le lien |
| **Adresse IP** | IP du client (pour la détection de fraude) |
| **User Agent** | Informations sur le navigateur et l'appareil |
| **Référent** | La page où le client a cliqué sur le lien (par exemple, "https://instagram.com") |
| **ID de session** | Identifiant unique pour cette session de navigation |
| **Horodatage** | Date et heure exactes du clic |

### Limitation des taux

Pour empêcher la fraude par clic et l'abuse par bots, Spwig limite les clics à **100 par minute par adresse IP**. Si la même IP dépasse ce seuil, les clics supplémentaires sont ignorés et ne sont pas comptés.

Cette protection empêche les acteurs malveillants d'augmenter les statistiques de clics sans bloquer le trafic légitime. Les clients réels presque jamais dépassent 100 clics par minute.

### Considérations de confidentialité

Les données de clic contiennent des adresses IP et des user agents pour la détection de fraude. Assurez-vous que votre politique de confidentialité révèle que vous suivez les références d'affiliés et partagez des données de performance anonymisées avec les affiliés.

## Affichage des liens d'affiliate

Tous les liens de suivi générés par les affiliés apparaissent dans votre tableau de bord administratif pour le suivi et la gestion.

### Accès à la liste des liens

Accédez à **Affilié > Liens** pour afficher tous les liens de suivi pour tous les affiliés et programmes. La vue en liste affiche:

- **Code de lien** : L'identifiant unique à 12 caractères
- **Affilié** : Qui a créé le lien
- **Programme** : Quelle structure de commission s'applique
- **Étiquette** : Description facultative fournie par l'affiliate
- **Destination** : Où le lien redirige les clients
- **Total de clics** : Compteur de clics à vie
- **Statut actif** : Si le lien est actuellement en suivi

### Filtrage des liens

Utilisez les filtres administratifs pour affiner la liste:
- **Par affilié** : Voir tous les liens pour un partenaire spécifique
- **Par programme** : Afficher les liens promouvant une structure de commission spécifique
- **Par statut actif** : Trouver les liens désactivés

Ce filtrage vous aide à analyser la distribution des liens dans votre réseau d'affiliés et à identifier les liens les plus performants.

## Statistiques des liens

Chaque lien de suivi accumule des métriques de performance qui aident les affiliés à optimiser leurs stratégies promotionnelles et vous à identifier vos meilleurs partenaires.

### Cliquez sur un enregistrement de lien pour afficher les statistiques détaillées:

| Métrique | Description | Calcul |
|--------|-------------|-------------|
| **Total de clics** | Tous les clics enregistrés depuis la création du lien | Compteur d'enregistrements de clics |
| **Clics (7 jours)** | Indicateur d'activité récente | Clics des 7 derniers jours |
| **Conversions** | Commandes attribuées à ce lien | Compteur de commissions depuis ce code de lien |
| **Taux de conversion** | Pourcentage de clics qui ont abouti à des achats | (Conversions ÷ Total de clics) × 100 |
| **Revenu total** | Somme de toutes les valeurs de commande depuis ce lien | Somme des totaux de commande pour les clics convertis |

### Utilisation des statistiques pour l'optimisation

**Pour les affiliés** : Ces chiffres montrent lesquels canaux promotionnels fonctionnent le mieux. Si un lien de bio Instagram a un taux de conversion de 5 % mais qu'un lien d'article de blog a 15 %, l'affiliate devrait se concentrer davantage sur le contenu du blog.

**Pour les marchands** : Les statistiques des liens révèlent lesquels affiliés génèrent du trafic de qualité. Un grand nombre de clics avec un faible taux de conversion suggère que l'audience de l'affiliate n'est pas adaptée à vos produits.

## Gestion des liens

Vous pouvez gérer les liens d'affiliate depuis le tableau de bord administratif pour des raisons de maintenance et de dépannage.

### Désactiver des liens

Pour empêcher un lien spécifique de suivre de nouveaux clics tout en conservant les données historiques:

1. Accédez à **Affilié > Liens**
2. Cliquez sur le lien que vous souhaitez désactiver
3. Désélectionnez **Actif**
4. Cliquez sur **Enregistrer**

Les liens désactivés redirigent toujours les clients vers la destination, mais ils ne définissent pas de cookies de suivi ni n'enregistrent de clics. Cela est utile lorsque l'affiliate mène une campagne temporaire ou que vous devez désactiver un canal promotionnel spécifique.

### Modifier les détails du lien

Vous pouvez modifier:
- **Étiquette** : Mettez à jour la description fournie par l'affiliate
- **Destination** : Changez vers où le lien redirige (utile si vous déplacez une page de produit)
- **Statut actif** : Activer ou désactiver le suivi

Vous ne pouvez pas modifier le code de lien — il est permanent et lié à toutes les données de clic et de commission historiques.

### Supprimer les liens inactifs

Supprimez les liens qui ne sont plus utilisés et n'ont aucun clic ou conversion historique. Cela permet de garder votre liste de liens propre sans perdre des données analytiques précieuses.

**Avertissement** : La suppression d'un lien supprime toutes les enregistrements de clic associés. Ne supprimez les liens que s'ils n'ont aucun clic ou si vous êtes absolument certain que vous n'avez pas besoin des données historiques.

## Modèle d'attribution

Comprendre la logique d'attribution de Spwig vous aide à fixer des attentes avec les affiliés et à résoudre les désaccords sur les commissions.

### Attribution du dernier clic

Comme mentionné précédemment, Spwig utilise l'attribution du dernier clic : si un client clique sur plusieurs liens d'affiliés avant d'acheter, seul l'affiliate le plus récent gagne une commission.

**Avantages**:
- Simple à comprendre et à expliquer
- Empêche les commissions doubles
- Récompense les affiliés qui concluent la vente

**Inconvénients**:
- Les affiliés qui ont introduit le client ne reçoivent aucun crédit
- Ne reflète pas les parcours clients multi-touch
- Peut inciter à l'"hijacking de lien" (affiliés ciblant des clients à forte intention qui ont déjà été référencés par quelqu'un d'autre)

### La durée de vie du cookie détermine l'éligibilité

Seuls les achats dans la fenêtre de durée de vie du cookie génèrent des commissions. Si le cookie expire avant la fin de la commande, aucune commission n'est créée même si le client revient via un favori.

**Exemple** : Durée de vie du cookie de 30 jours
- Client clique sur le lien le 1er janvier → Cookie défini, expire le 31 janvier
- Client achète le 25 janvier → Commission créée
- Client achète le 5 février → Aucune commission (cookie expiré)

### Suivi de session

En plus du cookie, Spwig suit l'ID de session pour chaque clic. Cela permet l'attribution multi-visit dans la même session même si les cookies sont bloqués ou effacés.

Si un client clique sur un lien, charge plusieurs pages de votre boutique, puis achète — tout cela dans la même session — l'affiliate reçoit le crédit même sans cookie persistant.

## Dépannage

Problèmes de suivi courants et comment les résoudre:

### Lien ne suit pas les clics

**Symptômes** : Le compteur de clics reste à zéro malgré les rapports de l'affiliate sur le partage du lien.

**Causes et solutions**:
1. **Le lien est désactivé** : Vérifiez le statut **Actif** sur la page de détails du lien
2. **Le programme est inactif** : Accédez à **Affilié > Programmes** et vérifiez que le statut du programme est **Actif**
3. **Le compte affilié est désactivé** : Vérifiez le statut du compte affilié à **Affilié > Affiliés**
4. **Limitation des taux** : Vérifiez si la même IP génère trop de clics (trafic de bots)

### Taux de conversion faible

**Symptômes** : Beaucoup de clics mais très peu de commandes attribuées.

**Causes et solutions**:
1. **Durée de vie du cookie trop courte** : Augmentez la durée de vie du programme si vos produits nécessitent des recherches et des considérations
2. **Qualité de la page de destination** : Vérifiez la page d'atterrissage — est-elle mobile-friendly ? Charge-t-elle rapidement ? Le produit est-il en stock ?
3. **Inadéquation de l'audience** : L'audience de l'affiliate peut ne pas être adaptée à vos produits
4. **Navigateur bloquant les cookies** : Certains outils de confidentialité bloquent les cookies tiers, bien que Spwig utilise des cookies premiers tiers qui sont moins susceptibles d'être bloqués

### Enregistrements de clics en double

**Symptômes** : Même client génère plusieurs enregistrements de clics en succession rapide.

**Cause** : Cela est un comportement normal. Chaque chargement de page du lien de suivi crée un enregistrement de clic. Si un client clique, la page charge lentement, et il clique à nouveau, vous verrez plusieurs enregistrements.

**Solution** : Aucune action nécessaire. Le limiteur de taux empêche l'abuse (100 clics/minute/IP), et les clics en double provenant de la même session n'affectent pas l'attribution — un seul cookie est défini.

## Conseils

- **Testez le suivi avant le lancement** — Créez un compte affilié de test, générez un lien de suivi, cliquez-y dans un navigateur incognito et effectuez un achat de test. Vérifiez que la commission apparaît avec l'attribution correcte à l'affiliate.
- **Éduquez les affiliés sur la durée de vie du cookie** — Assurez-vous que les affiliés comprennent qu'ils ne gagnent de commissions que sur les achats dans la fenêtre du cookie. Cela les aide à fixer des attentes réalistes et à se concentrer sur le trafic à forte intention.
- **Surveillez les modèles de clics pour la fraude** — Des clics anormalement élevés provenant d'une seule IP ou des clics sans chaîne d'agent utilisateur peuvent indiquer un trafic de bots. Examinez soigneusement ces affiliés avant d'approuver les commissions.
- **Utilisez des étiquettes de lien de manière cohérente** — Encouragez les affiliés à étiqueter leurs liens par canal (Instagram, Blog, Email) afin que vous puissiez tous deux analyser lesquels canaux promotionnels génèrent les meilleures conversions.
- **Considérez des durées de vie de cookie plus longues pour les produits à forte valeur** — Si votre valeur moyenne de commande est élevée et que les clients effectuent généralement des recherches avant d'acheter, prolongez la durée de vie du cookie à 60–90 jours pour capturer ces conversions différées.
- **Vérifiez les données de référent pour des informations sur les canaux** — Le champ de référent montre d'où proviennent les clics. Si vous voyez beaucoup de clics provenant de "instagram.com" ou "youtube.com", vous savez lesquels réseaux sociaux vos affiliés utilisent le plus efficacement.