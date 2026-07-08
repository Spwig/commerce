---
title: Création de programmes d'affiliation
---

Les programmes d'affiliation définissent la manière dont vos partenaires gagnent des commissions lorsqu'ils renvoient des clients vers votre magasin. Chaque programme a sa propre structure de commission, ses propres règles de suivi et ses seuils de paiement. Vous pouvez créer plusieurs programmes pour servir différents segments de partenaires d'affiliation — tels que les influenceurs, les créateurs de contenu ou les partenaires de renvoi en volume.

![Liste des programmes](/static/core/admin/img/help/creating-affiliate-programs/programs-list.webp)

## Composants d'un programme

Chaque programme d'affiliation se compose de : 

- **Nom et description** — Identifier le programme et l'expliquer aux affiliés
- **Structure de commission** — Combien les affiliés gagnent par vente (pourcentage ou montant fixe)
- **Durée de vie du cookie** — Combien de temps le suivi des renvois dure après un clic (1 à 365 jours)
- **Approbation automatique** — Si les nouveaux affiliés s'inscrivent automatiquement ou nécessitent une vérification manuelle
- **Seuil de paiement minimum** — Combien les affiliés doivent gagner avant de demander un paiement
- **Statut** — Actif, mis en pause ou archivé

## Types de commissions

Choisissez entre deux modèles de commission lors de la création de votre programme : 

| Type | Fonctionnement | Quand l'utiliser | Calcul d'exemple |
|------|-------------|-------------|---------------------|
| **Pourcentage** | L'affilié gagne un pourcentage du sous-total de la commande | Récompenses évolutives qui augmentent avec la valeur de la commande | 10 % d'une commande de 150 $ = 15 $ de commission |
| **Montant fixe** | L'affilié gagne un montant fixe par vente | Coûts prévisibles ; idéal pour les produits à volume élevé et à faible marge | 25 $ par vente, indépendamment de la valeur de la commande |

Les commissions en pourcentage s'adaptent naturellement — les affiliés gagnent plus lorsqu'ils renvoient des clients de haute valeur. Cela aligne leurs incitations avec les vôtres et est le modèle le plus courant (généralement 5 à 15 %).

Les commissions fixes s'avèrent utiles pour les services, les abonnements ou les programmes de renvoi en volume où vous souhaitez des coûts par vente prévisibles. Elles sont faciles à comprendre et à planifier, mais peuvent sous-évaluer les affiliés qui attirent des commandes importantes.

## Création d'un programme

Accédez à **Marketing > Programmes d'affiliation** et cliquez sur **+ Ajouter un programme**.

### Étapes de configuration

1. **Nom du programme**
   Entrez un nom descriptif visible par les affiliés (par exemple, « Programme de partenariat » ou « Échelon des influenceurs »).

2. **Slug**
   Un identifiant convivial pour les URL, généré automatiquement à partir du nom. Utilisé dans les URL et les références internes. Vous pouvez le personnaliser si nécessaire.

3. **Description**
   Texte optionnel expliquant les avantages et les termes du programme. Les affiliés le voient lorsqu'ils examinent les programmes auxquels ils peuvent adhérer.

4. **Type de commission**
   Sélectionnez **Pourcentage** ou **Montant fixe**.

5. **Valeur de commission**
   - Pour le pourcentage : Entrez une valeur entre 0 et 100 (par exemple, `10` pour 10 %)
   - Pour le montant fixe : Entrez le montant en dollars par vente (par exemple, `25,00` pour 25 $)

6. **Durée de vie du cookie en jours**
   Combien de jours le cookie de suivi dure (1 à 365). Voir la section ci-dessous pour des conseils.

7. **Approbation automatique des affiliés**
   - **Coché** — Les nouveaux affiliés s'inscrivent automatiquement
   - **Décoché** — Vous révisez manuellement et approuvez chaque candidature

8. **Paiement minimum**
   Le solde minimum qu'un affilié doit accumuler avant de demander un paiement (par exemple, `50,00` pour 50 $).

9. **Statut**
   Définissez-le sur **Actif** pour accepter de nouveaux affiliés et suivre les renvois.

10. **Enregistrer** le programme.

## Explication de la durée de vie du cookie

La durée de vie du cookie détermine combien de temps Spwig se souvient qu'un client a cliqué sur un lien de renvoi d'un affilié.

### Fonctionnement

1. Un client clique sur le lien d'un affilié
2. Spwig définit un cookie de suivi dans le navigateur du client
3. Si le client termine un achat **dans la durée de vie du cookie**, la commande est attribuée à l'affilié
4. Si le cookie expire avant l'achat, l'affilié ne gagne pas de commission

### Choix de la durée

| Durée | Cas d'utilisation | Scénario typique |
|----------|----------|------------------|
| **1 à 7 jours** | Achats impulsifs, ventes flash | Produits de consommation rapide, offres limitées |
| **30 jours** | Commerce électronique standard | Commerce en ligne général, recommandation par défaut |
| **60 à 90 jours** | Achats réfléchis | Articles de haute valeur, B2B, services |
| **180 jours ou plus** | Cycles de vente longs | Logiciels d'entreprise, abonnements, biens de luxe |

**La norme de l'industrie est de 30 jours.** Cela équilibre une attribution équitable aux affiliés avec des limites pratiques de suivi. Les durées plus courtes favorisent les clients qui convertissent rapidement ; les durées plus longues donnent aux clients le temps de rechercher et de revenir pour terminer leur achat.

### Note technique

La durée de vie du cookie n'affecte que **l'attribution**. Les commissions approuvées restent valides indéfiniment — la durée de vie du cookie détermine simplement si une commande est créditée à l'affilié au départ.

## Paramètres d'approbation automatique

Le paramètre d'approbation automatique contrôle si les nouvelles candidatures d'affiliés nécessitent une vérification manuelle.

### Quand activer l'approbation automatique

- **Programmes publics** — Vous souhaitez développer rapidement votre base d'affiliés sans bouchons
- **Produits à faible risque** — Le risque de fraude ou de marque est minimal
- **Programmes à volume élevé** — Vous prévoyez beaucoup de candidatures et ne pouvez pas vérifier chacune manuellement

### Quand demander une vérification manuelle

- **Programmes sur invitation** — Vous ne souhaitez accepter que des partenaires pré-vérifiés
- **Programmes premium** — Taux de commission élevé ou avantages exclusifs
- **Produits sensibles à la marque** — Vous devez vous assurer que les affiliés correspondent à vos valeurs de marque
- **Prévention de la fraude** — Vous souhaitez filtrer les comptes suspects

### Considérations de sécurité

Vérifier manuellement les affiliés aide à prévenir : 
- Les schémas de renvoi par soi-même (les affiliés créant des comptes fictifs pour gagner des commissions)
- Les violations de marque (les affiliés soumissionnant vos termes de marque dans les publicités payantes)
- La désalignement de marque (les affiliés promouvant vos produits dans des contextes inappropriés)

Pour la plupart des magasins, commencer avec **l'approbation manuelle** est plus sûr. Vous pouvez toujours activer l'approbation automatique plus tard une fois que vous avez établi des schémas de confiance.

## Seuil de paiement minimum

Le seuil de paiement minimum empêche les coûts administratifs liés au traitement de nombreux petits paiements.

### Pourquoi définir un seuil minimum

- **Réduit les frais de transaction** — Les processeurs de paiement facturent par transaction, donc regrouper les paiements économise de l'argent
- **Simplifie la comptabilité** — Moins d'événements de paiement signifie moins de travail de conciliation
- **Norme de l'industrie** — La plupart des programmes d'affiliation ont des seuils (25 $ à 100 $)

### Seuils typiques

| Seuil | Cas d'utilisation |
|-----------|----------|
| **25 $ à 50 $** | Programmes à volume élevé où les affiliés atteignent rapidement le seuil |
| **50 $ à 100 $** | Seuil standard pour la plupart des programmes |
| **100 $ à 200 $** | Programmes premium ou paiements internationaux avec des frais de traitement élevés |

### Équilibre de la satisfaction des affiliés

Fixer le seuil **trop haut** irrite les affiliés qui peuvent attendre des mois pour recevoir leur premier paiement. Fixer le seuil **trop bas** crée une charge administrative et réduit vos marges avec des frais.

**Recommandation :** Commencez à 50 $. Cela est suffisamment bas pour que les affiliés actifs atteignent ce seuil lors de leurs premières ventes, mais suffisamment élevé pour regrouper efficacement les paiements.

### Aucun plafond

Il n'y a pas de solde maximum — les affiliés peuvent accumuler des gains indéfiniment avant de demander un paiement. Certains affiliés préfèrent regrouper leurs demandes trimestriellement ou annuellement pour planifier leurs impôts.

## Gestion du statut du programme

Les programmes peuvent être dans l'un des trois statuts : 

| Statut | Description | Comportement |
|--------|-------------|----------|
| **Actif** | Le programme est en cours | Accepte de nouveaux affiliés, suit les renvois, calcule les commissions |
| **Mis en pause** | Désactivé temporairement | Les affiliés existants restent mais aucun nouveau compte n'est possible ; les cookies de renvoi existants fonctionnent toujours |
| **Archivé** | Fermé définitivement | Aucun nouveau affilié, aucun nouveau renvoi suivi ; les données historiques sont conservées pour les rapports |

### Quand mettre un programme en pause

- Vous révisez les taux de commission ou les termes
- Vous dépassez votre budget pour les paiements aux affiliés ce trimestre
- Vous testez une nouvelle structure de programme et souhaitez empêcher les nouveaux affiliés de s'inscrire au programme ancien

Les programmes mis en pause honorent toujours les cookies de suivi existants et les commissions en attente — vous empêchez simplement les nouveaux affiliés de s'inscrire.

### Quand archiver un programme

- Vous avez remplacé le programme par une nouvelle structure
- Le programme était limité dans le temps (par exemple, campagne saisonnière)
- Vous fusionnez plusieurs programmes en un seul

Les programmes archivés restent dans la base de données pour les rapports historiques mais sont supprimés des vues de gestion active.

## Exemples de programmes

### Exemple 1 : Programme d'influenceur (Pourcentage)

| Champ | Valeur |
|-------|-------|
| Nom | Programme d'influenceur |
| Type de commission | Pourcentage |
| Valeur de commission | 10 |
| Durée de vie du cookie en jours | 30 |
| Approbation automatique | Décoché (vérification manuelle) |
| Seuil de paiement minimum | 50,00 |
| Statut | Actif |

**Cas d'utilisation :** Recruter des influenceurs de réseaux sociaux et des créateurs de contenu. La commission de 10 % s'adapte à la valeur de la commande, récompensant les affiliés qui attirent des clients à forte dépense. L'approbation manuelle garantit que vous vérifiez chaque influenceur auprès de son public et de son alignement de marque.

### Exemple 2 : Programme de renvoi en volume (Montant fixe)

| Champ | Valeur |
|-------|-------|
| Nom | Programme de partenaires de renvoi |
| Type de commission | Montant fixe |
| Valeur de commission | 25,00 |
| Durée de vie du cookie en jours | 7 |
| Approbation automatique | Coché |
| Seuil de paiement minimum | 100,00 |
| Statut | Actif |

**Cas d'utilisation :** Collaborer avec des sites de deals, des agrégateurs de coupons et des réseaux de renvoi qui génèrent un volume élevé. La commission fixe de 25 $ maintient les coûts prévisibles, et la courte durée de vie du cookie (7 jours) cible les clients rapides. L'approbation automatique est activée car ces partenaires utilisent généralement un service auto-géré.

### Exemple 3 : Partenaire premium (Pourcentage élevé)

| Champ | Valeur |
|-------|-------|
| Nom | Échelon de partenaire premium |
| Type de commission | Pourcentage |
| Valeur de commission | 15 |
| Durée de vie du cookie en jours | 90 |
| Approbation automatique | Décoché |
| Seuil de paiement minimum | 200,00 |
| Statut | Actif |

**Cas d'utilisation :** Programme exclusif pour les affiliés performants ou les partenaires stratégiques. Une commission plus élevée (15 %) récompense leur trafic de qualité, et la durée de vie du cookie de 90 jours accommode les cycles de réflexion plus longs. Approbation manuelle uniquement — c'est un échelon sur invitation.

## Conseils

- Commencez avec une **commission en pourcentage** (5 à 15 %) pour la plupart des programmes — c'est plus facile à expliquer aux affiliés et s'adapte naturellement à la valeur de la commande.
- Utilisez une **durée de vie du cookie de 30 jours** comme base — c'est la norme de l'industrie et équilibre une attribution équitable avec des limites pratiques de suivi.
- Activez **l'approbation manuelle** initialement pour vérifier les affiliés, puis basculez vers l'approbation automatique une fois que vous avez établi des schémas de confiance et des contrôles contre la fraude.
- Fixez votre **seuil de paiement minimum** à 50 $ à 100 $ pour équilibrer la satisfaction des affiliés (pas trop élevé pour atteindre) avec l'efficacité administrative (pas trop nombreux de petits paiements).
- Créez **des programmes distincts** pour différents segments d'affiliés (influenceurs, sites de contenu, agrégateurs de deals) afin de suivre les performances et d'ajuster les commissions indépendamment.
- Surveillez régulièrement le **tableau de bord d'analyse** pour identifier les affiliés performants et ajuster les taux de commission pour retenir les meilleurs partenaires.

Souvenez-vous : Conservez tout le formatage markdown, les chemins d'image, les blocs de code et les termes techniques exactement comme indiqué dans les règles de préservation.