---
title: Règles de visibilité
---

# Règles de visibilité

Les règles de visibilité vous permettent d'afficher ou de masquer des parties de votre boutique en fonction de la personne qui visite et de son emplacement. Vous pouvez verrouiller des **éléments de page**, des **éléments de menu** et des **widgets de l'en-tête/pied de page** selon les mêmes conditions : le marché ou la région du client, la langue ou la devise qu'ils utilisent, l'heure de la journée, ou des signaux par visiteur comme le fait d'être connecté.

Tout est construit à partir de **groupes de règles** : un ensemble nommé et réutilisable d'une ou plusieurs conditions. Vous créez un groupe de règles une fois (par exemple, « marché de la Nouvelle-Zélande » ou « membres connectés ») et puis vous y attachez n'importe quel élément, élément de menu ou widget que vous souhaitez contrôler. Un élément sans groupe de règles attaché est toujours visible.

## Comment la visibilité est-elle déterminée

Lorsqu'un élément possède plusieurs groupes de règles, l'élément est affiché si **n'importe quel** groupe attaché correspond (ils s'utilisent avec OU). Dans un seul groupe, vous choisissez si **tous** ou **n'importe lequel** de ses critères doit correspondre.

Les règles appartiennent à deux familles, et Spwig les gère différemment afin que votre magasin reste rapide et convivial pour les moteurs de recherche :

- **Règles de marché** — conditions basées sur la région/marché, la langue, la devise et l'heure. Ces règles sont déterminées sur le serveur pour chaque URL de marché, donc la même page est livrée identiquement à chaque visiteur (et à chaque moteur de recherche) à cet adresse. Cela rend les pages mémorisables et sécurisées pour le référencement.
- **Règles par visiteur** — statut de connexion, contenu du panier, appareil et localisation précise. Ces règles dépendent du visiteur individuel, donc Spwig les résout en privé pour chaque personne après le chargement de la page. Elles ne sont jamais intégrées dans une page partagée, mémorisée.

Si vous désactivez un groupe de règles, il cesse simplement d'être appliqué - l'élément auquel il était attaché revient à être visible. Désactiver un groupe n'est pas un moyen de cacher quelque chose.

## Créer et attacher des règles

Il y a deux façons de travailler avec des groupes de règles.

### Les attacher là où vous concevez

Partout où vous pouvez verrouiller du contenu, vous verrez un **contrôle de visibilité** (l'icône de l'œil) : 

- **Éditeur de pages** — sélectionnez un élément, ouvrez ses propriétés et utilisez le contrôle de visibilité.
- **Éditeur de menu** — sélectionnez un élément de menu et ouvrez l'onglet **Visibilité**. Cela fonctionne sur **n'importe quel** élément, y compris un élément de sous-menu (menu déroulant) imbriqué dans un autre - une règle sur un enfant n'empêche que cet enfant, laissant le reste du menu intact.
- **Éditeur d'en-tête et de pied de page** — sélectionnez un widget et ouvrez la section **Groupes de règles de visibilité** de ses paramètres.

Les règles qui dépendent du visiteur individuel - s'ils sont connectés, ce qui se trouve dans leur panier ou leur appareil - sont résolues pour chaque client sans ralentir votre magasin ou affecter les moteurs de recherche. Votre boutique reste rapide et mémorisable, et chaque visiteur voit uniquement la navigation destinée à lui.

Dans l'éditeur de visibilité vous pouvez : 

- **Attacher** n'importe quel groupe de règles existant en cochant les cases.
- **Règle rapide** — créer un groupe de règles simple sur place (par exemple, « uniquement les membres », un seul marché, une devise, un appareil ou une valeur minimale du panier) et l'attacher en une seule étape.
- **Gérer les groupes de règles** — passer à l'éditeur complet pour des règles avancées.

Cliquez sur **Appliquer** et l'élément est verrouillé immédiatement.

### Créer des règles avancées

Pour tout ce qui est plus complexe - combiner plusieurs conditions, imbriquer des groupes, ou utiliser des opérateurs précis - allez à **Conception → Règles de visibilité** (groupes de règles). Là, vous pouvez assembler des règles avec la logique ET/OU et les réutiliser à travers l'ensemble de votre magasin.

## Conditions courantes

Préservez tous les formats de markdown, les chemins d'images, les blocs de code et les termes techniques.

| Condition | Utilisez-le pour… |
|-----------|------------------|
| **Région/marché** | Afficher un bloc uniquement aux visiteurs d’un marché spécifique (par exemple, la Nouvelle-Zélande) |
| **Devise sélectionnée** | Afficher des notes sur les prix ou des offres uniquement lorsqu’une devise spécifique est active |
| **Langue sélectionnée** | Afficher du contenu uniquement dans une langue spécifique |
| **Date/heure/jour/horaires d’ouverture** | Faire défiler un panneau pendant une fenêtre de soldes ou uniquement pendant les heures d’ouverture |
| **Statut de connexion** | Afficher du contenu réservé aux membres, ou un message de demande d’inscription pour les invités |
| **Type d’appareil** | Afficher ou masquer quelque chose sur mobile, tablette ou ordinateur de bureau |
| **Valeur du panier/articles** | Afficher un message pour la livraison gratuite une fois que le panier dépasse une limite |

## Aperçu

Dans l’aperçu du constructeur de pages, vous pouvez **apercevoir en tant que marché** et **apercevoir en tant qu'utilisateur** (connecté ou invité, avec un panier d'exemple) pour voir exactement ce que chaque audience verrait — y compris les règles propres à chaque utilisateur qui s'appliquent normalement en toute discrétion.

## Conseils

- Créez un petit ensemble de groupes de règles bien nommés (« Marché Nouvelle-Zélande », « Membres », « Réservé aux appareils mobiles ») et réutilisez-les partout — c’est plus facile à gérer qu’une règle unique.
- Les règles de marché sont le choix le plus sûr pour tout ce que vous souhaitez indexer par les moteurs de recherche, car le résultat est le même pour tous les utilisateurs d’une URL de marché donnée.
- Si un élément disparaît de manière inattendue, vérifiez ses groupes de règles associés — un élément n’est masqué que lorsqu’il a un groupe actif et que aucun de ses groupes ne correspond à l'utilisateur actuel.