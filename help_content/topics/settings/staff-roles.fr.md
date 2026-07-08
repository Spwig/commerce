---
title: Rôles et autorisations du personnel
---

Les rôles de personnel vous permettent de contrôler exactement ce que chaque membre de l'équipe peut voir et faire — tant dans le panneau d'administration que sur le terminal POS. Définissez des rôles avec des autorisations spécifiques, puis attribuez-les aux membres du personnel. Un utilisateur peut avoir plusieurs rôles, et ses autorisations effectives sont la combinaison de tous les rôles assignés.

![Rôles de personnel](/static/core/admin/img/help/staff-roles/role-list.webp)

## Comment ça fonctionne

1. Vous créez des **rôles** qui définissent un ensemble d'autorisations (par exemple, "Gestionnaire de commandes", "Caissier")
2. Chaque rôle contrôle deux types d'accès : **autorisations du panneau d'administration** et **autorisations POS**
3. Vous **attribuez des rôles** aux membres du personnel depuis leur page de profil
4. Les autorisations effectives d'un membre du personnel sont l'**union** de tous ses rôles — si un rôle accorde un accès, l'utilisateur l'obtient
5. Les autorisations sont **mises en cache** pour des performances optimisées et sont automatiquement actualisées lors du changement de rôles

## Rôles prédéfinis

Spwig inclut 7 rôles prédéfinis qui couvrent les structures d'équipe les plus courantes. Ces rôles ne peuvent pas être supprimés, mais vous pouvez créer des rôles personnalisés pour des besoins plus spécifiques.

| Rôle | Accès | Description |
|------|--------|-------------|
| **Propriétaire du magasin** | Admin + POS | Accès complet à tout. Pour l'administrateur principal du magasin. |
| **Gestionnaire de magasin** | Admin + POS | Opérations quotidiennes — accès complet aux produits, commandes, clients, marketing et recherche. Seulement en lecture pour la conception, les e-mails, les paiements et les paramètres. |
| **Rédacteur de contenu** | Admin | Gère les pages, les articles de blog, la conception et les médias. Seulement en lecture pour les produits. |
| **Gestionnaire de commandes** | Admin | Gère les commandes, l'expédition, les retours et le service client. Seulement en lecture pour les produits. |
| **Gestionnaire de marketing** | Admin | Gère les promotions, les bons de réduction, l'affiliation, la fidélité et les programmes de parrainage. Seulement en lecture pour les produits, les clients et les médias. |
| **Caissier** | POS uniquement | Personnel POS de première ligne. Peut traiter les ventes et vérifier les soldes des cartes-cadeaux. Aucun remboursements, réductions ou gestion de trésorerie. |
| **Caissier senior** | POS uniquement | Personnel POS expérimenté. Peut traiter les remboursements, appliquer des réductions (jusqu'à 25 %), gérer l'argent liquide et fermer les shifts. |

## Créer un rôle personnalisé

Accédez à **Paramètres > Rôles du personnel** et cliquez sur **Ajouter un rôle**.

### Paramètres généraux

| Paramètre | Description |
|---------|-------------|
| **Nom d'affichage** | Le nom du rôle affiché dans l'administration (par exemple, "Personnel de stock") |
| **Description** | Une explication brève de l'utilité de ce rôle |
| **Ordre de tri** | Contrôle l'ordre d'affichage dans la liste des rôles |
| **Icône** | Choisissez parmi 20 icônes pour identifier visuellement le rôle |
| **Couleur de badge** | Couleur utilisée pour les badges de rôle (Bleu, Vert, Orange, Rouge, Vert foncé, Gris) |
| **Panneau d'administration** | Activez/désactivez si ce rôle accorde un accès au backend d'administration |
| **Terminals POS** | Activez/désactivez si ce rôle accorde un accès aux terminaux POS |

### Catégories d'autorisation d'administration

L'onglet des autorisations d'administration organise toutes les fonctionnalités de la plateforme en 13 catégories. Pour chaque catégorie, vous définissez l'un des trois niveaux d'accès suivants :

- **Aucun** — Aucun accès à cette zone (les éléments de menu sont cachés)
- **Vue** — Accès en lecture seule (peut voir les données mais ne peut pas les modifier)
- **Complet** — Accès complet (peut consulter, créer, modifier et supprimer)

![Catégories d'autorisation](/static/core/admin/img/help/staff-roles/permission-categories.webp)

| Catégorie | Ce que cela contrôle |
|----------|-----------------|
| **Catalogue de produits** | Produits, catégories, marques, attributs, stock, entrepôts, actifs numériques |
| **Commandes et expédition** | Commandes, remboursements, retours, expéditions, configuration d'expédition |
| **Clients** | Profils clients, segments, analyses |
| **Contenu et pages** | Pages, articles de blog, annonces, formulaires |
| **Conception et thème** | Thèmes, modèles d'en-tête/pied de page, menus, tokens de conception, CSS personnalisé |
| **Marketing et promotions** | Promotions, bons de réduction, affiliation, fidélité, parrainages, flux de produits |
| **Bibliothèque multimédia** | Images, vidéos, dossiers, balises |
| **Système de courriel** | Comptes courriel, modèles, file d'attente d'envoi |
| **Paiements et facturation** | Fournisseurs de paiement, transactions, webhooks, abonnements, taux de change |
| **Recherche** | Paramètres de recherche, synonymes, redirections, analyses |
| **Paramètres du magasin** | Paramètres du site, géolocalisation, mappages de pays, règles d'entreprise |
| **Gestion POS** | Terminaux POS, shifts, mouvements de trésorerie, modèles de reçus |
| **Utilisateurs et rôles** | Comptes utilisateurs du personnel, rôles, jetons API |

Lorsqu'un utilisateur a plusieurs rôles, le **niveau d'accès le plus élevé** s'applique. Par exemple, si le Rôle A accorde "Vue" aux Produits et le Rôle B accorde "Complet", l'utilisateur obtient un accès "Complet".

### Drapeaux d'autorisation POS

Si le rôle accorde un accès POS, l'onglet Autorisations POS vous permet d'affiner exactement ce qu'un opérateur POS peut faire. Ces autorisations sont distinctes des autorisations d'administration et sont vérifiées directement sur le terminal POS.

![Autorisations POS](/static/core/admin/img/help/staff-roles/pos-permissions.webp)

| Groupe | Autorisation | Description |
|-------|-----------|-------------|
| **Général** | Accès POS | Peut utiliser le système POS |
| **Ventes et réductions** | Réductions manuelles | Peut appliquer des réductions manuelles au niveau des articles ou du panier |
| | Pourcentage maximal de réduction | Le pourcentage maximal de réduction autorisé (0–100) |
| | Révision des prix | Peut modifier les prix des produits au comptoir |
| **Remboursements et annulations** | Traiter les remboursements | Peut traiter les remboursements sur les commandes POS |
| | Annuler les commandes | Peut annuler les commandes POS du shift en cours |
| **Cartes-cadeaux** | Émettre des cartes-cadeaux | Peut émettre de nouvelles cartes-cadeaux au comptoir |
| | Vérifier le solde des cartes-cadeaux | Peut consulter les soldes des cartes-cadeaux |
| **Gestion de trésorerie** | Gestion de trésorerie | Peut effectuer des opérations de mise et de retrait d'argent liquide |
| | Ouvrir le tiroir-caisse | Peut ouvrir le tiroir-caisse sans achat |
| | Fermer les shifts | Peut fermer les shifts et effectuer une conciliation de trésorerie |
| **Rapports** | Voir les rapports POS | Peut consulter les rapports de shift et les résumés de ventes |
| **Stock** | Ajustements de stock | Peut ajuster les niveaux de stock (réception, dommages, recomptage, retour) |

Pour les autorisations booléennes, si **n'importe quel** des rôles d'un utilisateur l'active, l'utilisateur l'obtient. Pour le Pourcentage maximal de réduction, la **valeur la plus élevée** parmi tous les rôles s'applique.

## Gestion des membres du personnel

Accédez à **Paramètres > Gestion du personnel** pour consulter et gérer votre équipe.

### Liste du personnel

La liste du personnel affiche tous les utilisateurs ayant un accès au personnel. Pour chaque membre, vous pouvez voir :
- **Nom et courriel**
- **Rôles assignés** (affichés sous forme de badges colorés)
- **Type d'accès** — Admin uniquement, POS uniquement, ou Les deux
- **Statut 2FA** — Si l'authentification à deux facteurs est activée
- **Statut Actif/Inactif**

Utilisez les filtres pour affiner par rôle, type d'accès ou statut 2FA.

### Attribution de rôles aux membres du personnel

1. Cliquez sur un membre du personnel pour ouvrir son profil
2. Dans la section **Rôles**, vous verrez des cartes pour chaque rôle disponible
3. Cliquez sur le bouton d'activation de n'importe quelle carte de rôle pour l'attribuer ou la supprimer
4. Les modifications prennent effet immédiatement — aucun bouton Enregistrer n'est nécessaire
5. Le résumé **Autorisations effectives** ci-dessous affiche le résultat combiné de tous les rôles attribués

### Ajouter un nouveau membre du personnel

1. Accédez à **Paramètres > Gestion du personnel** et cliquez sur **Ajouter un membre du personnel**
2. Entrez l'adresse e-mail, le prénom et le nom de famille de l'utilisateur
3. Définissez un mot de passe temporaire
4. Attribuez un ou plusieurs rôles
5. L'utilisateur peut maintenant se connecter avec l'accès fourni par ses rôles

## Dupliquer des rôles

Pour créer un nouveau rôle basé sur un existant :

1. Ouvrez le rôle que vous souhaitez copier
2. Cliquez sur **Dupliquer le rôle** en bas de la page
3. Un nouveau rôle est créé avec toutes les mêmes autorisations
4. Renommez-le et ajustez les autorisations comme nécessaire
5. Enregistrez le nouveau rôle

Cela est utile lorsque vous avez besoin d'un rôle similaire à un existant avec de légères différences — par exemple, un "Gestionnaire junior" basé sur "Gestionnaire de magasin" mais avec moins d'autorisations.

## Comment les autorisations sont appliquées

### Panneau d'administration

- **Visibilité du menu** — Les sections du menu latéral sont cachées pour les catégories où l'utilisateur a un accès "Aucun"
- **Accès aux pages** — Tenter de visiter une page restreinte affiche une erreur d'autorisation
- **Restrictions d'action** — Avec un accès "Vue", les boutons de modification et de suppression sont cachés et les actions d'enregistrement sont bloquées
- **Bypass superutilisateur** — Les comptes superutilisateurs ont toujours un accès complet, indépendamment des attributions de rôles

### Terminal POS

- **Portail de connexion** — Seuls les utilisateurs ayant au moins un rôle avec "Terminals POS" activé peuvent se connecter au POS
- **Basculages de fonctionnalité** — Les boutons et actions POS (remboursement, réduction, annulation, etc.) sont affichés ou masqués en fonction des autorisations POS combinées de l'utilisateur
- **Plafond de réduction** — Le Pourcentage maximal de réduction impose une limite stricte sur la taille des réductions qu'un opérateur POS peut appliquer
- **Application des autorisations côté serveur** — Toutes les autorisations POS sont vérifiées côté serveur au niveau de l'API, et non seulement dans l'interface utilisateur

## Conseils

- **Commencez par les rôles prédéfinis** — Les 7 rôles intégrés couvrent la plupart des structures d'équipe. Créez des rôles personnalisés uniquement lorsque vous avez besoin de contrôles d'accès plus spécifiques.
- **Utilisez la fonction de duplication** — Lorsque vous avez besoin d'un rôle similaire à un existant, dupliquez-le et ajustez-le plutôt que de le créer à partir de zéro.
- **Attribuez plusieurs rôles si nécessaire** — Un membre du personnel qui gère à la fois les commandes et le marketing peut être attribué aux rôles "Gestionnaire de commandes" et "Gestionnaire de marketing". Les autorisations s'appliquent automatiquement.
- **Séparez l'accès administration et POS** — Les caissiers n'ont généralement pas besoin d'accès administration, et le personnel de bureau n'a pas besoin d'accès POS. Utilisez les bascules d'accès pour garder les choses propres.
- **Définissez des limites de réduction pour le personnel POS** — Le Pourcentage maximal de réduction empêche les caissiers d'appliquer des réductions excessives. Définissez-le à 0 pour interdire les réductions, ou un plafond raisonnable comme 10–25 % pour le personnel expérimenté.
- **Révisez régulièrement les rôles** — À mesure que votre équipe grandit, vérifiez les attributions de rôles pour vous assurer que le personnel a l'accès minimum nécessaire pour son travail. Supprimez les rôles lorsque les personnes changent de poste.
- **Activez l'authentification à deux facteurs pour les rôles sensibles** — Le personnel ayant accès aux paiements, aux paramètres ou à la gestion des utilisateurs devrait avoir l'authentification à deux facteurs activée pour la sécurité.