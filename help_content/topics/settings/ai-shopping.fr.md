---
title: Achats intelligents
---

L'achat intelligent permet aux assistants d'achat intelligents de trouver vos produits et, si vous le permettez, d'acheter dans votre magasin au nom d'un client. Il est **désactivé par défaut** - le fait de l'activer est une décision délibérée, et tant que vous ne le faites pas, votre magasin ne met rien à disposition de ces assistants.

## Comment l'activer

Ouvrez **Paramètres → Achat intelligent** et passez **l'achat agissant activé** à on. À partir de ce point, les assistants qui soutiennent le protocole universel de commerce peuvent découvrir votre magasin et consulter votre catalogue. Rien de votre boutique normale ne change.

## Tableau de bord de préparation

Le haut de la page Achat intelligent répond à une question en une phrase : **les assistants intelligents peuvent-ils acheter dans votre magasin maintenant ?**

- **« Les assistants intelligents peuvent acheter dans votre magasin »** — tout ce qui est nécessaire pour un achat est en place.
- **« Les assistants intelligents peuvent parcourir votre magasin, mais ne peuvent pas encore acheter »** — votre magasin est trouvable, mais quelque chose manque avant qu'un achat ne puisse être finalisé (généralement un fournisseur de paiement connecté).
- **« Arrêt d'urgence activé »** ou **« Achat agissant désactivé »** — rien n'est envoyé aux assistants.

Sous le verdict, vous verrez une courte liste de vérification - fournisseur de paiement connecté, la livraison peut être facturée, les produits sont visibles par les assistants - avec un indice à côté de tout ce qui a encore besoin d'attention. Les compteurs montrent combien de produits les assistants peuvent vendre, combien vous avez caché d'eux, combien d'assistants ont visité, et combien vous avez bloqués.

La liste de vérification reflète votre configuration **en temps réel** : connectez un fournisseur de paiement ou ajoutez une méthode d'expédition et le verdict s'actualisera la prochaine fois que vous ouvrerez la page.

## L'arrêt d'urgence

L'**arrêt d'urgence** est un interrupteur séparé du principal. Utilisez-le pour arrêter immédiatement toute activité des assistants - par exemple, si quelque chose semble faux - sans modifier votre configuration. Réinitialisez-le pour reprendre. Pensez à l'interrupteur principal comme à « ce paramètre est-il configuré ? » et à l'arrêt d'urgence comme à « arrêtez tout maintenant ».

## Ce que les assistants peuvent faire

Deux niveaux d'accès, contrôlés séparément :

- **Lecture** (découverte et navigation) est à faible risque. Un assistant peut trouver votre magasin et lire les détails des produits.
- **Achats** (acheter réellement) est à haut risque et reste fermé aux assistants non vérifiés, sauf si vous le permettez.

Un magasin peut être trouvable sans être achetable - une bonne façon de commencer.

## Masquer des produits spécifiques

Chaque produit dispose d'un paramètre **Visible par les agents d'achat intelligents** (activé par défaut). Désactivez-le pour empêcher un produit particulier d'être vu par les assistants tout en restant sur votre boutique, pratique pour les articles que vous préférez vendre uniquement via votre site.

## Gérer les assistants individuels

Lorsqu'un assistant achète d'abord - ou essaie de le faire - Spwig le note sous **Achat intelligent → Identités d'agents**. Chaque entrée montre la maison vérifiée de l'assistant (le répertoire avec lequel il s'authentifie), son niveau de confiance, et le nombre de demandes qu'il a effectuées. Le nom et le logo que présente un assistant ne sont affichés que comme des détails *allégués* - à traiter comme une étiquette, et non comme une preuve d'identité ; la maison vérifiée est la partie qui peut être considérée comme fiable.

Chaque assistant se situe dans l'une des trois catégories de niveau de confiance :

| Niveau de confiance | Ce que cela signifie |
|---|---|
| **Plafonné (vérifié, limité)** | Le niveau par défaut pour un nouvel assistant. Spwig a enregistré son identité, et il porte le plafond de valeur de commande, le plafond de dépense, et les restrictions de paiement définis sur sa politique (voir ci-dessous). |
| **Vérifié (limites supprimées)** | Une décision délibérée de votre part de faire confiance à cet assistant. Ses plafonds de valeur de commande et de dépense quotidienne sont supprimés. |
| **Bloqué** | L'assistant ne peut plus acheter dans votre magasin. Les commandes en cours sont annulées, bien que tout paiement déjà effectué reste inchangé. |

Pour arrêter un assistant, sélectionnez-le dans la liste et choisissez **Bloquer les assistants sélectionnés**. **Débloquer les assistants sélectionnés** le ramène toujours à **Plafonné** - jamais directement à Vérifié - car lever les plafonds est une étape séparée, délibérée.

Pour supprimer entièrement les plafonds d'un assistant, sélectionnez-le et choisissez **Promouvoir en vérifié (supprimer les plafonds)**.

Cela efface sa valeur maximale de commande et sa limite de dépense quotidienne, et passe l'assistant en état Vérifié.

Un assistant bloqué est ignoré - d'abord débloquez-le, puis promuez-le.

Traitez cela comme une décision de confiance réelle : ne promuez qu'un assistant en lequel vous êtes certain, car la vérification supprime les barrières de sécurité dont dispose un nouvel assistant.

## Définir les limites d'un assistant

Ouvrez la page de détail d'un assistant et utilisez la section **Policy (limites et offres autorisées)** pour définir ce qu'il est autorisé à faire :

| Champ | Ce qu'il contrôle |
|---|---|
| **Valeur maximale de commande** | La plus grande commande que cet assistant peut passer. Laissez vide s'il n'y a pas de plafond. |
| **Plafond de dépense quotidienne** | Le montant maximum que cet assistant peut dépenser sur l'ensemble de ses commandes en une journée. Laissez vide s'il n'y a pas de plafond. |
| **Autoriser les codes de réduction** | Si l'assistant peut appliquer des codes de réduction lors du règlement. |
| **Autoriser les cartes-cadeaux** | Si l'assistant peut utiliser des cartes-cadeaux. |
| **Autoriser les biens numériques** | Si l'assistant peut acheter des produits numériques. |
| **Taux de limite (par minute)** | Le nombre de demandes que l'assistant peut envoyer à votre magasin par minute. |

Un nouvel assistant démarre avec des plafonds de valeur de commande et de dépense, et les codes de réduction, les cartes-cadeaux et les biens numériques sont désactivés - le paramètre par défaut délibérément prudent. Modifiez l'une de ces colonnes et enregistrez ; chaque modification est enregistrée dans **Agent Events** avec les valeurs avant et après, vous permettant ainsi d'avoir une trace de qui a modifié quoi et à quel moment. La promotion d'un assistant en Vérifié efface sa valeur maximale de commande et son plafond de dépense quotidienne pour vous - vous n'avez pas besoin de les vider manuellement d'abord.

## Le registre d'activité

**IA Shopping → Agent Events** est un registre indiquant ce que les assistants ont fait, de manière non modifiable - chaque demande vérifiée, chaque tentative bloquées, chaque modification que vous avez effectuée. C'est un registre en lecture seule, qui ne peut pas être modifié ou supprimé, donc il constitue votre preuve si un achat effectué par un assistant est jamais contesté.

## Remarque concernant les plateformes d'assistants

Les sociétés gérant ces assistants (et les règles pour y figurer) sont nouvelles et changent souvent. Certaines exigent que vous fassiez une demande ou que vous répondiez à des conditions régionales avant que vos produits ne puissent être achetés via elles. Spwig met votre magasin prêt ; le fait qu'un assistant donné vous affiche dépend de cet assistant.