---
title: Avis sur les produits
---

Les avis des clients permettent de noter un produit et d'écrire sur leur expérience. Les avis que vous approuvez s'affichent sur la page du produit dans votre boutique, où ils aident les autres acheteurs à décider de ce qu'ils veulent acheter. Spwig vous donne un contrôle total sur les avis qui seront publiés : rien n'est publié avant que vous ne l'ayez approuvé.

Les avis sont situés sous **Produits > Avis** dans la barre latérale, qui s'ouvre en tant que groupe : le lien du haut vous amène au **Tableau de bord des avis**, et **Modérer les avis** vous amène directement à la liste des avis.

## Le tableau de bord des avis

Accédez à **Produits > Avis** pour ouvrir le tableau de bord — une vue d'ensemble d'une seule page de la performance des avis dans votre magasin.

![Tableau de bord des avis](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

En haut, six cartes KPI résument votre activité d'avis :

| Carte | Ce qu'elle affiche |
|---|---|
| **Avis totaux** | Tous les avis jamais soumis, approuvés ou non |
| **Note moyenne** | La moyenne des notes étoiles sur chaque avis |
| **En attente de modération** | Les avis en attente de votre approbation ou de votre rejet |
| **Taux d'approbation** | La part de tous les avis que vous avez approuvés |
| **Achats vérifiés** | La part des avis laissés par des clients ayant une commande confirmée pour ce produit |
| **Nouveaux (30 jours)** | Les avis soumis au cours des 30 derniers jours |

Sous les KPI, trois graphiques vous donnent plus de détails :

- **Répartition des notes** — un graphique en barres de la quantité d'avis qui tombent dans chaque note (1 à 5). Un groupe d'avis à 1 étoile ici mérite d'être investigué immédiatement.
- **Volume des avis (12 semaines)** — un graphique en courbe des comptes d'avis semaine après semaine, afin de repérer les pics après une promotion ou une baisse qui nécessite de l'attention.
- **Canal d'achat des commentateurs** — un graphique en camembert du canal marketing (direct, courriel, recherche payante, réseaux sociaux organiques, etc.) qui a conduit à l'**achat** derrière chaque avis. Cela réutilise vos données d'attribution et est vraiment utile pour voir quels canaux attirent des clients qui vont ensuite laisser des avis — mais ce n'est pas un enregistrement de la manière dont le client a trouvé le formulaire d'avis lui-même. Spwig ne suit pas cela séparément ; voir « Ce que le parcours fait et ne fait pas » plus bas dans ce guide.

Deux listes complètent le tableau de bord :

- **Produits les plus commentés** — vos produits les plus commentés, chacun avec son compte d'avis et sa note moyenne, qui mène directement vers le produit.
- **En attente de modération** — vos derniers avis en attente, afin de pouvoir accéder directement à tout ce qui nécessite une décision sans quitter le tableau de bord.

## La liste des avis

Cliquez sur **Modérer les avis** (ou **Produits > Avis > Modérer les avis**) pour voir chaque avis sous forme de carte, avec des filtres au-dessus de la liste.

![Liste des avis produits avec des filtres et des cartes d'avis en attente](/static/core/admin/img/help/product-reviews/review-list.webp)

Chaque carte affiche la miniature du produit, le titre de l'avis, la note étoile, un badge **Approuvé**/**En attente**, un badge **Achat vérifié** lorsqu'il est pertinent, un aperçu du commentaire, et qui l'a rédigé ainsi que la date.

### Filtrer les avis

Utilisez le panneau de filtre pour réduire la liste :

- **Recherche** — correspond au nom du produit, au nom d'utilisateur client ou au titre de l'avis
- **Note** — n'affiche que les avis avec une note étoile spécifique (utile pour investiguer les plaintes à 1 étoile)
- **Approbation** — séparez rapidement les avis approuvés des avis en attente
- **Vérifié** — filtrez les avis provenant de clients ayant une commande confirmée pour ce produit

Le filtrage s'effectue instantanément sans recharger la page.

## Approuver et rejeter les avis

Les avis ne sont pas visibles sur votre boutique jusqu'à ce que vous les approuviez. Vous pouvez approuver ou rejeter les avis individuellement ou en vrac.

### Actions en vrac

1. Dans la liste des avis, cochez les cases à côté des avis que vous souhaitez traiter
2. Sélectionnez **Approuver les avis sélectionnés** ou **Rejeter les avis sélectionnés** dans la liste déroulante des actions
3. Cliquez sur **Aller**

C'est le moyen le plus rapide de traiter un ensemble d'avis nouveaux.

### Avis individuel

1.

Cliquez sur l'icône de modification sur une carte d'avis, ou sur son titre, pour ouvrir l'avis
2.

Conservez toutes les formattages markdown, les chemins d'images, les blocs de code et les termes techniques.

Sur l'onglet **Aperçu**, cochez ou décochez **Approuvé**
3.

Cliquez sur le bouton coche dans l'en-tête pour enregistrer

## La page d'édition de l'aperçu

Ouvrir un aperçu vous donne une vue de type tableau de bord centrée sur cet aperçu unique — une en-tête avec le nom du produit, la note, un badge **Approuvé**/**En attente**, un badge **Acheteur vérifié** lorsqu'il s'applique, qui a rédigé l'aperçu et à quelle date, ainsi qu'une ligne de statistiques (**Note**, **Votes utiles**, **Commandes clients**, **Dépense sur la vie**). Ci-dessous, les détails sont organisés en quatre onglets.

![Page d'édition de l'aperçu — Onglet Aperçu avec galerie d'images](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### Onglet Aperçu

C'est ici que vous modérez l'aperçu lui-même :

- **Images de l'aperçu** — si le client a ajouté des photos, elles s'affichent ici sous forme de galerie de vignettes ; cliquez sur n'importe quelle vignette pour ouvrir l'image en taille réelle dans un nouvel onglet. Les aperçus avec des photos sont un signal de confiance fort pour les acheteurs, donc cela vaut le coup d'y jeter un coup d'œil avant d'approuver.
- **Note**, **Titre**, **Commentaire** — le contenu soumis par le client
- **Approuvé** — contrôler si l'aperçu est visible sur votre magasin
- **Acheteur vérifié** — signale que l'aperçu provient d'un acheteur confirmé ; Spwig le définit automatiquement lorsqu'une commande livrée pour le produit existe (voir l'onglet **Achats**), mais vous pouvez le remplacer ici si nécessaire
- **Images** — la liste d'origine des URLs d'images derrière la galerie ci-dessus ; vous n'avez normalement pas besoin de les modifier, mais elles restent éditable pour les cas particuliers (par exemple, supprimer une photo d'un aperçu à plusieurs images)

Vous ne pouvez pas modifier le texte de l'aperçu — approuver ou rejeter, et gérer les images, est l'étendue de ce que vous contrôlez ici.

### Onglet Client et Parcours

![Page d'édition de l'aperçu — Onglet Client et Parcours](/static/core/admin/img/help/product-reviews/review-edit-customer-tab.webp)

Cet onglet vous donne un aperçu de la personne ayant rédigé l'aperçu : commandes totales, nombre de commentaires qu'ils ont rédigés, leur note moyenne donnée, combien de temps ils sont clients, et leurs coordonnées, avec un lien pour ouvrir leur enregistrement client complet.

En dessous se trouve le **parcours des canaux de trafic** — les canaux, campagnes et référents qui ont amené ce client dans votre magasin, tirés de vos données d'attribution et affichés sous forme de timeline.

#### Ce que le « parcours » dit et ne dit pas

Lisez cette timeline comme le **parcours d'arrivée et d'achat** du client — comment ils ont trouvé votre magasin et ont acheté. Ce n'est **pas** un enregistrement de la visite pendant laquelle ils ont rédigé cet aperçu. Spwig ne suit pas où se trouvait le client, ou quel appareil ou session ils ont utilisés, au moment où ils ont soumis l'aperçu. Si la timeline montre « Email > soins de la peau d'été » trois semaines avant la date de l'aperçu, cela vous indique que la campagne email a probablement conduit à l'achat — cela ne dit rien sur le fait qu'ils soient revenus depuis un résultat de recherche, un signet, ou un email de suivi pour réellement rédiger l'aperçu. Traitez cet onglet comme un contexte marketing utile, et non comme une trace littérale de la soumission de l'aperçu.

### Onglet Achat

![Page d'édition de l'aperçu — Onglet Achat](/static/core/admin/img/help/product-reviews/review-edit-purchase-tab.webp)

Cet onglet liste chaque commande dans laquelle le client a acheté le produit évalué — numéro de commande, date, total, statut, et le canal d'achat pour cette commande. Si l'une de ces commandes a atteint un statut livré (expédié ou livré), vous verrez une note de confirmation que c'est une commande vérifiée — le même signal qui définit automatiquement **Acheteur vérifié** sur l'onglet Aperçu.

Si aucune commande correspondante n'apparaît ici, le client a soit acheté le produit avant que votre magasin ne suive les commandes dans Spwig, soit ils n'ont jamais réellement acheté — à noter avant de décider de la valeur à accorder à l'aperçu.

### Onglet Avancé

Des métadonnées que vous n'avez rarement besoin de modifier : **Nombre d'utilisateurs utiles** (combien de clients ont marqué l'aperçu comme utile), la provenance de l'importation si l'aperçu a été migré d'une autre plateforme, et les horodatages de création/mise à jour.

## Conseils

Conservez toutes les formattages markdown, les chemins d'images, les blocs de code, et les termes techniques.

- Vérifiez d'abord la liste **En attente de modération** sur le tableau de bord — c'est le moyen le plus rapide de voir ce qui nécessite une décision sans ouvrir la liste complète des avis
- Un groupe de critiques à 1 étoile sur le même produit dans le graphique **Répartition des notes** est un signe clair pour investiguer sur l'emballage, la qualité du produit ou votre texte de présentation
- Utilisez le filtre **Vérifié** lors de la prise de décision sur les avis douteux — les retours des clients ayant une commande confirmée ont plus de poids dans tout litige
- Approuvez les avis rapidement, y compris les critiques négatives — un avis négatif visible sans réponse peut sembler plus mauvais qu'une plainte traitée, et les avis qui s'affichent lentement découragent les clients de laisser des retours futurs
- Ne lisez pas trop en détail le **Parcours provenant du trafic** ou le graphique **Canal d'achat des commentateurs** du tableau de bord — ils décrivent comment le client est arrivé et a acheté, pas comment il est arrivé pour écrire l'avis
- Les avis accompagnés de photos méritent une attention particulière avant d'être approuvés ; les photos de produits provenant de clients réels sont l'un des contenus les plus convaincants sur votre vitrine