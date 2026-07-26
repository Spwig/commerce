---
title: Gestion des transactions en attente et reprise du point de vente
---

<!-- screenshots-needed:
- url: /en/admin/pos_app/parkedcart/
  filename: parked-cart-list.webp
  description: Vue de la liste des paniers en attente (peut être vide après une installation fraîche — capture quand même)
  save-to: core/static/core/admin/img/help/pos/
-->

Les paniers en attente permettent à vos caissiers de suspendre une transaction et de commencer immédiatement à servir le prochain client — sans perdre un seul article ou remise. Lorsque vous êtes prêt, le panier d'origine est restauré exactement tel qu'il était et la vente reprend là où elle en était.

## Ce que faire un panier en attente fait

Lorsqu'un caissier appuie sur **Park** sur le terminal de caisse, Spwig enregistre une copie complète du panier actuel sur le serveur. Le terminal est alors vidé pour qu'une nouvelle transaction puisse commencer immédiatement. Le panier en attente est stocké et lié au terminal sur lequel il a été créé.

Rien n'est perdu dans la copie. Le panier en attente préserve :

- Chaque article et sa quantité
- Tout client qui a été associé à la vente
- Les remises manuelles appliquées au panier ou à des articles individuels

Le panier en attente reste disponible sur le même terminal pendant un maximum de **24 heures**. Après cela, Spwig l'enlève automatiquement. Les paniers qui ont déjà été restaurés sont supprimés immédiatement après leur restauration et ne comptent pas dans la fenêtre de 24 heures.

## Comment faire un panier en attente

Vous devez avoir au moins un article dans le panier avant de pouvoir le mettre en attente. Un panier vide ne peut pas être mis en attente.

1. Pendant qu'une vente est en cours, appuyez sur le bouton **Park** sur le terminal de caisse.
2. Spwig enregistre le panier et vide le terminal. Vous verrez une confirmation et le compteur de paniers en attente dans la zone des paniers en attente sera mis à jour.
3. Commencez la transaction du prochain client sur le terminal désormais vide.

Si le client a été associé à la vente avant de mettre le panier en attente, son nom apparaîtra dans la liste des paniers en attente pour une identification facile.

## Comment reprendre une transaction en attente

1. Appuyez sur la zone ou l'icône **Parked Carts** sur le terminal de caisse. Vous verrez une liste de tous les paniers actuellement en attente sur ce terminal, affichant le nom du client (s'il en a été associé), le nombre d'articles, le montant total, le caissier qui a mis le panier en attente et l'heure à laquelle il a été mis en attente.
2. Appuyez sur le panier que vous souhaitez reprendre.
3. Si votre terminal actuel contient des articles, le point de vente les supprimera avant de restaurer le panier en attente. Assurez-vous d'avoir terminé ou mis en attente la transaction actuelle avant de reprendre une autre.
4. Les articles du panier en attente, l'association au client et les remises manuelles sont tous restaurés. La vente continue normalement.

## Visibilité des paniers en attente

Les paniers en attente sont **liés au terminal** sur lequel ils ont été créés. Tout caissier connecté au même terminal peut voir et reprendre tout panier en attente sur ce terminal — il n'y a aucune restriction par caissier sur qui peut reprendre un panier en attente.

Les paniers en attente créés sur un terminal différent, même dans le même emplacement de magasin, ne sont pas visibles sur votre terminal actuel.

## Annulation d'un panier en attente depuis le point de vente

Un caissier peut supprimer un panier en attente directement depuis la liste des paniers en attente sur le terminal — appuyez sur le panier et utilisez l'option de suppression ou d'abandon. Les paniers en attente supprimés sont définitivement supprimés et ne peuvent pas être récupérés.

## Expiration automatique et nettoyage

Chaque panier en attente expire **24 heures après avoir été mis en attente**. Spwig exécute une tâche en arrière-plan qui supprime les paniers expirés qui n'ont jamais été reprises. Il n'y a rien à faire de votre côté — le nettoyage se fait automatiquement.

Si vous avez besoin de supprimer des paniers en attente avant la fenêtre de 24 heures, un caissier peut les supprimer un par un depuis la liste des paniers en attente sur le terminal.

## Postes de travail et paniers en attente

Il n'y a aucun lien rigide entre un panier en attente et le poste de travail qui était ouvert lorsqu'il a été mis en attente. Fermer un poste de travail n'efface **pas** automatiquement ou annule tout panier en attente sur ce terminal. Les paniers en attente survivent aux changements de poste de travail et restent disponibles pendant la fenêtre complète de 24 heures.

Cela signifie que :

- Un panier mis en attente à la fin d'un poste de travail matinal peut être repris par un caissier sur un poste de travail ultérieur.
- Si vous ne souhaitez pas que les paniers en attente passent d'un poste de travail à un autre, faites en sorte que les caissiers vident la liste des paniers en attente avant de fermer leur poste de travail.

## Conseils

Conservez tous les formats de mise en forme Markdown, les chemins d'image, les blocs de code et les termes techniques.

- Garez un panier dès que le client dit « Je dois juste prendre une autre chose » — c'est plus rapide que de lui demander d'attendre dans la file ou de réajouter manuellement les articles.
- Si la liste des paniers gérés s'allonge, vérifiez si un caissier précédent a laissé des transactions non résolues à la fin de son shift et nettoyez les paniers obsolètes.
- Attachez le client à la vente avant de gérer le panier — son nom apparaît dans la liste, ce qui rend beaucoup plus facile de trouver le bon panier lors de son retour.
- Les paniers gérés expirent après 24 heures, ils ne sont donc pas adaptés pour conserver des transactions pendant plusieurs jours commerciaux.
- Souvenez-vous que reprendre un panier géré effacera ce qui est actuellement dans le registre.

Terminez ou gérez la transaction active avant de prendre un autre panier géré.