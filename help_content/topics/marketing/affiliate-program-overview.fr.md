---
title: Aperçu du programme d'affiliation
---

Le programme d'affiliation Spwig vous permet de recruter des partenaires qui promeuvent vos produits en échange de commissions. Ce canal de marketing étend votre portée via des influenceurs, des blogueurs, des créateurs de contenu et des ambassadeurs de marque qui partagent des liens de suivi uniques avec leur public. Lorsqu'une personne clique sur un lien d'affiliation et effectue un achat, l'affilié gagne une commission et vous gagnez un client.

Ce résumé explique ce qu'est le programme d'affiliation, à qui il s'adresse et comment les commerçants l'utilisent pour créer un réseau de partenaires qui génère des ventes.

![Tableau de bord du commerçant](/static/core/admin/img/help/affiliate-program-overview/merchant-dashboard.webp)

## Concepts clés

Comprendre ces termes fondamentaux vous aidera à configurer et à gérer votre programme d'affiliation:

| Terme | Définition |
|------|------------|
| **Affilié** | Un partenaire qui promeut vos produits et gagne des commissions sur les ventes qu'il génère |
| **Programme** | Une structure de commission avec des taux, des règles et des paramètres (vous pouvez créer plusieurs programmes) |
| **Lien de suivi** | Un URL unique contenant le code de l'affilié (par exemple, `yourstore.com/?ref=CODE`) |
| **Commission** | Le paiement que reçoit un affilié pour une vente générée, calculé en fonction des règles du programme |
| **Durée de vie du cookie** | La durée (en jours) pendant laquelle le cookie de suivi persiste après que le client a cliqué sur un lien d'affiliation |
| **Paiement** | Un paiement en bloc qui règle plusieurs commissions approuvées à la fois |
| **Tableau de bord du commerçant** | Votre interface d'administration pour gérer les programmes, les affiliés, les commissions et les paiements |
| **Portail des affiliés** | Le tableau de bord public où les affiliés consultent leurs revenus, obtiennent des liens de suivi et demandent des paiements |

## Fonctionnement

Le workflow d'affiliation suit quatre étapes principales:

### 1. Postuler
Les affiliés découvrent votre programme et soumettent des candidatures via le portail des affiliés public à `/affiliate/` sur votre boutique. Vous pouvez activer l'**approbation automatique** pour les programmes ouverts ou le **révision manuelle** pour les partenariats invités uniquement.

### 2. Approuver
Vous examinez les candidatures en attente dans **Marketing > Affiliés**. Vérifiez le site web, la présence sur les réseaux sociaux et l'adéquation du public de chaque candidat avant d'approuver. Une fois approuvé, l'affilié reçoit ses identifiants de connexion et peut accéder à son tableau de bord.

### 3. Promouvoir
Les affiliés approuvés obtiennent des liens de référence uniques depuis leur portail. Ils partagent ces liens dans des articles de blog, des réseaux sociaux, des lettres d'information par e-mail, ou là où ils interagissent avec leur public. Spwig définit un cookie de suivi lorsqu'une personne clique sur le lien.

### 4. Gagner
Lorsqu'un client référencé achète un produit dans la durée de vie du cookie, Spwig crée un enregistrement de commission. Vous examinez et approuvez les commissions dans **Marketing > Commissions**, puis traitez les paiements lorsque les affiliés atteignent le seuil minimum de paiement.

## Aperçu du workflow du commerçant

En tant que commerçant, vous gérez l'ensemble du cycle de vie du programme depuis votre panneau d'administration:

### Création de programmes
Commencez par créer un ou plusieurs programmes d'affiliation à **Marketing > Programmes d'affiliation**. Chaque programme a sa propre structure de commission, durée de vie du cookie et paramètres d'approbation. Vous pouvez créer des programmes distincts pour les influenceurs (commission plus élevée) par rapport aux partenaires généraux (commission plus basse).

### Examen des candidatures
Les nouvelles candidatures d'affiliation apparaissent à **Marketing > Affiliés** avec un statut **En attente**. Examinez chaque candidature pour vérifier que le partenaire est un bon choix pour votre marque. Approuvez pour activer leur compte ou refusez avec une raison.

### Approbation des commissions
Lorsque les affiliés génèrent des ventes, les commissions apparaissent à **Marketing > Commissions** avec un statut **En attente**. Vérifiez la commande liée pour confirmer qu'elle est légitime (pas une auto-référence, pas une commande retournée), puis approuvez ou refusez en conséquence.

### Traitement des paiements
Une fois que les affiliés ont accumulé des commissions approuvées au-delà du seuil minimum de paiement, traitez les paiements en bloc à **Marketing > Paiements**. Spwig s'intègre avec PayPal et Airwallex pour des paiements automatisés, ou vous pouvez enregistrer des virements bancaires manuels.

## Aperçu du workflow des affiliés

Comprendre comment les affiliés vivent votre programme vous aide à concevoir une meilleure onboarding et un meilleur support:

### Postuler
Les affiliés visitent votre portail des affiliés, lisent les détails du programme (taux de commission, durée de vie du cookie, conditions de paiement), et soumettent une candidature avec leurs informations de contact et leurs canaux de promotion.

### Créer des liens
Après l'approbation, les affiliés se connectent à leur tableau de bord pour générer des liens de suivi. Ils peuvent créer des liens généraux pour la boutique ou des liens vers des produits/catégories spécifiques qu'ils souhaitent promouvoir.

### Promouvoir
Les affiliés partagent leurs liens de suivi là où ils interagissent avec des clients potentiels — articles de blog, vidéos YouTube, histoires Instagram, lettres d'information par e-mail, ou sites de comparaison.

### Demander des paiements
Les affiliés suivent leurs revenus en temps réel via le tableau de bord du portail des affiliés. Lorsque leur solde approuvé atteint le seuil minimum de paiement, ils peuvent demander un paiement.

## Où trouver chaque fonctionnalité

| Fonctionnalité | Emplacement dans l'administration | Description |
|---------|---------------|-------------|
| **Programmes** | Marketing > Programmes d'affiliation | Créer et configurer les structures de commission |
| **Affiliés** | Marketing > Affiliés | Examiné les candidatures, gérer les comptes des affiliés |
| **Commissions** | Marketing > Commissions | Examiné et approuver les commissions en attente |
| **Paiements** | Marketing > Paiements | Traiter les paiements en bloc vers les affiliés |
| **Paramètres** | Marketing > Paramètres des affiliés | Paramètres globaux, fournisseurs de paiement, personnalisation du portail |
| **Tableau de bord** | Marketing > Tableau de bord des affiliés | Aperçu analytique avec les clics, commandes et totaux de commissions |

Le portail destiné aux affiliés est automatiquement disponible à `/affiliate/` sur l'URL publique de votre boutique.

## Cas d'utilisation courants

Voici quatre méthodes éprouvées que les commerçants utilisent pour utiliser le programme d'affiliation Spwig afin de développer leur entreprise:

### Partenariats avec des influenceurs
Partenaires avec des influenceurs de réseaux sociaux qui ont des publics engagés dans votre niche. Offrez des taux de commission plus élevés (15–20%) pour attirer des influenceurs de qualité qui peuvent générer un trafic significatif. Utilisez des liens de suivi pour mesurer le ROI de chaque partenariat.

### Ambassadeurs de marque
Créez un réseau de clients fidèles qui deviennent des ambassadeurs de marque. Offrez à ces clients fidèles des comptes d'affiliation afin qu'ils puissent gagner des commissions lorsqu'ils font référence des amis et de la famille. Cela fonctionne particulièrement bien pour les produits de niche avec des communautés passionnées.

### Créateurs de contenu
Recrutez des blogueurs, des YouTubers et des podcasters qui créent des guides d'achat, des critiques ou du contenu de comparaison. Les affiliés avec du contenu éternel peuvent générer des références cohérentes mois après mois.

### Réseaux de recommandations
Permettez aux clients existants de rejoindre votre programme et de gagner des commissions en partageant les produits qu'ils aiment. Cela crée une boucle virale où les clients satisfaits deviennent des promoteurs, attirant de nouveaux clients qui peuvent également devenir des affiliés.

## Conseils

- **Commencez par un seul programme** — Créez un programme de partenaire général avec un taux de commission de 10 % et une durée de vie du cookie de 30 jours. Vous pouvez ajouter des programmes spécialisés plus tard une fois que vous comprendrez les partenaires qui performent le mieux.
- **Fixez des attentes claires** — Documentez votre processus d'approbation, les délais de commission et l'horaire de paiement dans le portail des affiliés. La transparence construit la confiance et réduit les demandes de support.
- **Surveillez les fraudes** — Examinez attentivement les commissions pour des signes rouges comme les auto-références (les affiliés achètent via leurs propres liens), des taux de retour anormalement élevés ou des schémas de clics suspects. Rejetez immédiatement les commissions frauduleuses.
- **Communiquez régulièrement** — Envoyez des mises à jour mensuelles à vos affiliés avec des nouvelles du programme, des points clés du calendrier de promotion et des reconnaissances des meilleurs performeurs. Une communication active maintient les affiliés engagés et promeut.
- **Optimisez pour mobile** — La plupart des affiliés partagent des liens sur les réseaux sociaux où la majorité des clics proviennent de dispositifs mobiles. Testez votre flux de paiement sur les téléphones pour garantir une expérience fluide pour les clients référencés.
- **Fournissez des actifs créatifs** — Facilitez la promotion de vos produits par les affiliés en leur fournissant des images de bannières, des photos de produits et des copies prêtes à l'emploi qu'ils peuvent utiliser dans leur contenu.