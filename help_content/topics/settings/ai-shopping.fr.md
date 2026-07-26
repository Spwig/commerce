---
title: Achat par IA
---

L'Achat par IA permet aux assistants d'achat basés sur l'IA de trouver vos produits et, lorsqu'on le permet, d'acheter pour le compte d'un client dans votre magasin. Il est **désactivé par défaut** — l'activer est un choix délibéré, et jusqu'à ce que vous ne l'activiez pas, votre magasin ne révèle rien à ces assistants.

## Activer l'option

Ouvrez **Paramètres → Achat par IA** et activez **Commerce agentique activé**. À partir de ce moment, les assistants qui prennent en charge le Protocole de Commerce Universel pourront découvrir votre magasin et lire votre catalogue. Rien ne change concernant votre magasin normal.

## Tableau de bord de préparation

En haut de la page Achat par IA, une seule question est répondue en une seule phrase : **les assistants IA peuvent-ils vraiment acheter dans votre magasin en ce moment ?**

- **« Les assistants IA peuvent acheter dans votre magasin »** — tout ce qui est nécessaire à un achat est en place.
- **« Les assistants IA peuvent parcourir votre magasin, mais ne peuvent pas encore acheter »** — votre magasin est discoverable, mais quelque chose manque avant qu'un achat ne puisse être finalisé (généralement un fournisseur de paiement connecté).
- **« Arrêt d'urgence activé »** ou **« Commerce agentique désactivé »** — rien n'est envoyé aux assistants.

En dessous du verdict, vous trouverez une liste de vérification courte — fournisseur de paiement connecté, livraison pouvant être cotée, produits visibles aux assistants — avec une indication à côté de tout ce qui nécessite encore une attention. Les compteurs montrent combien de produits les assistants peuvent vendre, combien vous avez cachés d'eux, combien d'assistants ont visité, et combien vous avez bloqués.

La liste de vérification reflète votre configuration **en temps réel** : connectez un fournisseur de paiement ou ajoutez une méthode d'expédition et le verdict se mettra à jour la prochaine fois que vous ouvrirez la page.

## Arrêt d'urgence

L'**Arrêt d'urgence** est un interrupteur distinct du principal. Utilisez-le pour arrêter immédiatement toutes les activités des assistants — par exemple, si quelque chose semble anormal — sans avoir à modifier votre configuration. Effacez-le pour reprendre. Pensez à l'interrupteur principal comme étant « cette fonctionnalité est-elle configurée » et à l'arrêt d'urgence comme étant « arrêtez tout maintenant ».

## Ce que les assistants peuvent faire

Deux niveaux d'accès, contrôlés séparément :

- **Lecture** (découverte et navigation) est à risque faible. Un assistant peut trouver votre magasin et lire les détails des produits.
- **Paiement** (réellement acheter) est plus risqué et reste fermé aux assistants non vérifiés, sauf si vous le permettez.

Un magasin peut être discoverable sans être achetable — une façon utile de commencer.

## Cacher des produits spécifiques

Chaque produit a un paramètre **Visible pour les agents d'achat par IA** (activé par défaut). Désactivez-le pour garder un produit particulier caché aux assistants tout en le laissant visible sur votre boutique — pratique pour des articles que vous préférez vendre uniquement via votre propre site.

## Gérer les assistants individuels

Lorsqu'un assistant effectue un achat — ou tente de le faire — Spwig le note sous **Achat par IA → Identités des agents**. Chaque entrée affiche le domicile vérifié de l'assistant (le répertoire avec lequel il signe) et le nombre de requêtes qu'il a effectuées. Le nom et le logo que présente un assistant sont affichés uniquement comme des détails *revendiqués* — traitez-les comme une étiquette, pas comme une preuve d'identité ; le domicile vérifié est la partie sur laquelle vous pouvez vous fier.

Les nouveaux assistants commencent **limités** : ils peuvent effectuer des transactions, mais dans des limites. Pour en bloquer un, sélectionnez-le et choisissez **Bloquer les assistants sélectionnés** — les paiements en cours s'arrêtent et l'assistant ne peut plus acheter, tandis que tout paiement déjà effectué reste inchangé. **Débloquer les assistants sélectionnés** le ramène à l'état limité (jamais directement à l'état illimité — lever les limites est toujours une étape distincte et délibérée).

## Enregistrement des activités

**Achat par IA → Événements des agents** est un enregistrement à preuve de tampering de ce que les assistants ont fait — chaque demande vérifiée, chaque tentative bloquée, chaque modification que vous avez effectuée. Il est en lecture seule et ne peut être modifié ou supprimé, donc il constitue votre trace de preuve si un achat effectué par un assistant est jamais contesté.

## Remarque concernant les plateformes d'assistants

Les entreprises qui gèrent ces assistants (et les règles pour apparaître sur elles) sont nouvelles et changent souvent.

Certaines exigent que vous postulez ou que vous remplissiez des conditions régionales avant que vos produits ne puissent être achetés via elles.


Spwig rend votre boutique prête ; que donné assistant vous liste ou non dépend de cet assistant.