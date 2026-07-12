---
title: Aperçu du POS
---

<!-- screenshots-needed:
- url: /en/admin/pos/
  filename: pos-dashboard-overview.webp
  description: The POS dashboard landing page — full page at 1440x900
- url: /en/admin/
  filename: admin-sidebar-pos-group.webp
  description: Admin sidebar zoomed to the "Point of Sale" group, showing the expanded submenu with all items visible
-->

Spwig POS est un point de vente basé sur le navigateur qui permet à votre personnel de passer des commandes en magasin sur n'importe quelle tablette ou ordinateur portable — sans nécessiter de matériel ou de logiciel dédié. Puisque Spwig POS fonctionne sur la même plateforme que votre boutique en ligne, votre catalogue de produits, les niveaux de stock, les comptes clients et l'historique des commandes sont toujours synchronisés sur tous les canaux. Une vente effectuée en magasin réduit immédiatement le stock et apparaît dans vos rapports de commandes aux côtés des commandes en ligne.

Spwig POS est inclus dans toutes les éditions — Communautaire, Pro et Entreprise — sans coût supplémentaire. Il n'y a rien à déverrouiller ou à mettre à niveau.

![Tableau de bord du POS](/static/core/admin/img/help/pos/pos-dashboard-overview.webp)

## Où se trouve le POS dans l'administration

Dans la barre latérale, faites défiler jusqu'au groupe **Point de vente**. Cliquez sur **Tableau de bord du POS** pour ouvrir la zone de gestion du POS à l'adresse `/admin/pos/`. À partir de là, vous pouvez surveiller vos terminaux, consulter les dernières shifts et accéder à toutes les sections de configuration du POS via le sous-menu :

- **Tableau de bord du POS** — Aperçu de l'état des terminaux, des shifts actifs et des ventes récentes via le POS
- **Terminaux** — Terminaux POS enregistrés et leurs paramètres
- **Shifts** — Enregistrements de shifts ouverts et fermés avec des données de conciliation en espèces
- **Groupes de magasins** — Groupes de localisations physiques partageant des paramètres régionaux
- **Modèles de reçus** — Mise en page de reçus personnalisée par magasin ou groupe
- **Diapositives de promotion** — Images promotionnelles affichées sur l'écran client lorsqu'il est inactif
- **Fournisseurs de terminaux** — Connexions aux services de paiement (ex. Stripe Terminal, Square)
- **Lecteurs de cartes** — Dispositifs physiques de lecteur de cartes appairés à vos terminaux
- **Lancer le POS** — Ouvre l'interface du POS dans un nouvel onglet

![Barre latérale d'administration — groupe Point de vente](/static/core/admin/img/help/pos/admin-sidebar-pos-group.webp)

## L'application du terminal POS

Vos caissiers travaillent dans l'interface du POS, qui s'exécute en tant qu'application web progressive (PWA) à l'adresse `/pos/` sur le domaine de votre boutique. Elle peut être installée sur une tablette ou un ordinateur portable comme une application native — elle fonctionnera depuis l'écran d'accueil et continuera à fonctionner en mode hors ligne si la connexion internet est temporairement perdue.

L'interface du POS est séparée du backend d'administration. Votre personnel se connecte à `/pos/` avec ses identifiants de boutique, et non au principal backend d'administration. L'administration est l'endroit où vous configurez et surveillez tout ; l'application POS est l'endroit où les ventes ont lieu.

L'écran destiné aux clients s'exécute à l'adresse `/pos/display/` — un second écran ou tablette tourné vers le client, affichant le panier actuel, les prix et les diapositives promotionnelles entre les transactions.

## Terminologie clé

Comprendre ces termes rend le reste de la documentation du POS plus facile à suivre.

Preserve all markdown formatting, image paths, code blocks, and technical terms.

| Terme | Définition |
|------|---------------|
| **Groupe de magasin** | Une collection nommée de lieux physiques partageant des paramètres régionaux tels que la devise, la langue et le fuseau horaire. Par exemple, "New Zealand Stores" ou "Singapore Region". |
| **Emplacement de magasin** | Un magasin individuel ou une succursale. Dans Spwig, les emplacements de magasin sont des enregistrements de entrepôt marqués comme emplacements de vente au détail. |
| **Terminal de caisse** | Un appareil (tablette, ordinateur portable) enregistré à un emplacement de magasin. Chaque terminal a son propre nom, code de liaison et affectation facultative d'un lecteur de carte. |
| **Lecteur de carte** | L'appareil de paiement attaché à un terminal de caisse — par exemple, un lecteur Stripe S700 ou une machine à carte Adyen. Il traite les paiements sans contact et par carte à puce et code PIN. |
| **Fournisseur de paiement** | Le service derrière le lecteur de carte — Stripe Terminal, Square, Adyen et autres. Vous configurez un fournisseur de paiement par magasin et connectez vos lecteurs de carte via celui-ci. |
| **Journée de caisse** | Une période d'ouverture/fermeture à un terminal. Un caissier ouvre une journée de caisse au début de leur session (en entrant le solde de caisse initial) et la ferme à la fin, en comptant l'argent dans le tiroir. Les rapports de journée de caisse montrent les ventes totales, les remboursements et toute variation d'argent. |
| **Écran client** | Un deuxième écran ou tablette orienté vers le client qui affiche le contenu du panier en temps réel, le total et des diapositives promotionnelles lorsque le terminal est inactif. Il se connecte à un terminal de caisse via un court code de liaison. |
| **Code de liaison** | Un code de 8 caractères utilisé pour lier un nouvel appareil à un enregistrement de terminal dans l'administration. Lorsque vous enregistrez un terminal, vous entrez son code de liaison la première fois que vous ouvrez `/pos/` sur cet appareil. |
| **Panier mis en pause** | Une transaction suspendue enregistrée afin que le caissier puisse servir un autre client et revenir plus tard à la vente originale. Les paniers mis en pause sont stockés par terminal et expirent après 24 heures. |

## Comment l'inventaire et les commandes sont liés

Chaque produit que vous vendez via la caisse provient de votre catalogue principal. Le stock est déduit de l'entrepôt auquel le terminal est assigné, afin que la disponibilité en ligne et en magasin reste précise. Les commandes de caisse apparaissent dans **Orders** à côté de vos commandes en ligne, avec un badge POS pour les distinguer. Les comptes clients créés au comptoir sont les mêmes comptes utilisés sur votre boutique en ligne — si un client a déjà acheté en ligne, le caissier peut le trouver par nom ou courriel et attacher la commande en magasin à son compte.

## Hiérarchie des paramètres

Les paramètres de caisse s'appliquent de général à spécifique, donc vous n'avez besoin de configurer que ce qui diffère à chaque niveau :

1. **Défaut du site** — La devise, la langue et le fuseau horaire globaux de votre magasin depuis **Settings > Store Settings**
2. **Groupe de magasin** — Remplace la devise, la langue ou le fuseau horaire pour tous les emplacements du groupe
3. **Emplacement de magasin** — Remplacement supplémentaire pour une succursale spécifique (défini dans son enregistrement d'entrepôt)
4. **Terminal** — Remplacements au niveau de l'appareil pour une caisse spécifique

Si vous gérez un magasin à un seul emplacement, vous pouvez ignorer les groupes de magasin et permettre à tout d'hériter des paramètres par défaut de votre site.

## Ce que vous pouvez faire depuis l'administration POS

| Tâche | Où |
|------|-------|
| Enregistrer un nouveau dispositif POS | **Point of Sale > Terminals** |
| Connecter un fournisseur de paiement (Stripe, Square, etc.) | **Point of Sale > Terminal Providers** |
| Associer un lecteur de carte physique à un terminal | **Point of Sale > Card Readers** |
| Vérifier ou fermer une journée de caisse ouverte | **Point of Sale > Shifts** |
| Personnaliser le format de votre reçu | **Point of Sale > Receipt Templates** |
| Ajouter des images promotionnelles à l'écran client | **Point of Sale > Promo Slides** |
| Organiser les succursales par région | **Point of Sale > Store Groups** |
| Lancer l'interface du caissier | **Point of Sale > Open POS** (s'ouvre dans un nouvel onglet) |

## Conseils

- Vous n'avez pas besoin d'un groupe de magasin si vous faites fonctionner un seul emplacement.

# Groupe de magasins

Les groupes de magasins sont utiles lorsque vous avez plusieurs succursales avec des paramètres régionaux différents — par exemple, des magasins dans différents pays utilisant différentes devises.
- Donnez à chaque terminal un nom clair et descriptif (par exemple, "Guichet avant" ou "Caisse du café") afin que les rapports de shift et les reçus soient faciles à lire.
- Configurez votre modèle de reçu avant votre premier shift — vous pouvez personnaliser le logo, l'adresse du magasin, le message d'en-tête, et même ajouter un code QR qui renvoie à une page de commentaires ou à un programme de fidélité.
- L'écran client à `/pos/display/` fonctionne sur tout appareil avec un navigateur.

Un tablette ou moniteur de secours suffit — aucun achat de matériel supplémentaire n'est requis.
- Si un lecteur de carte devient hors ligne pendant une période chargée, le POS peut accepter l'espèce et les paiements par carte saisis manuellement en tant que solution de secours, afin que les ventes puissent continuer sans interruption.
- Les rapports de shift POS sont liés au caissier qui les a ouverts, ce qui rend simple le règlement de l'argent liquide à la fin de chaque session.