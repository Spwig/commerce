---
title: Segments de clients
---

Les segments de clients vous permettent de classer automatiquement vos clients en groupes significatifs en fonction de leur comportement d'achat. Une fois que les clients sont segmentés, vous pouvez utiliser ces groupes pour orienter vos efforts de marketing — par exemple, offrir des récompenses de fidélité aux clients VIP ou envoyer des campagnes de rattachement aux clients qui n'ont pas acheté depuis un certain temps.

Spwig évalue les critères de segment par rapport aux métriques de chaque client et les affecte au segment de plus haute priorité auquel ils correspondent. Cela se produit automatiquement à mesure que les données des clients sont mises à jour.

## Types de segments disponibles

Spwig dispose d'un ensemble de types de segments prédéfinis. Chaque type de segment a un identifiant interne fixe, mais vous pouvez personnaliser le nom d'affichage, la description, les critères et la couleur pour correspondre à la manière dont vous pensez à vos clients.

| Type de segment | Utilisation typique |
|---|---|
| **Client invité** | Clients qui ont passé commande sans créer de compte |
| **Nouveau client** | Clients qui ont récemment effectué leur premier achat |
| **Client régulier** | Clients ayant un historique d'achat régulier |
| **Acheteur fréquent** | Clients qui achètent souvent (intervalle court entre les commandes) |
| **Haute valeur** | Clients ayant un montant total dépensé élevé |
| **Client VIP** | Vos clients les plus précieux et les plus fidèles |
| **Chasseur de bonnes affaires** | Clients qui ont tendance à acheter pendant les soldes |
| **À risque** | Clients qui n'ont pas acheté depuis un certain temps |
| **Inactif** | Clients absents depuis une période prolongée |

## Comprendre les critères de segment

Chaque segment est défini par une combinaison de critères. Spwig vérifie ces critères par rapport aux métriques stockées de chaque client. Tous les critères d'un segment sont combinés — un client doit satisfaire toutes les conditions définies pour être éligible.

### Critères de dépense

- **Min Total dépensé** — le client doit avoir dépensé au moins ce montant sur toutes les commandes terminées
- **Max Total dépensé** — le client ne doit pas avoir dépensé plus de ce montant

Utilisez une fourchette de dépense pour identifier un niveau spécifique. Par exemple, en fixant Min à 500 $ et Max à 2 000 $, vous ciblerez les clients du niveau intermédiaire.

### Critères du nombre de commandes

- **Min Commandes** — le client doit avoir au moins ce nombre de commandes terminées
- **Max Commandes** — le client ne doit pas avoir plus de ce nombre de commandes terminées

Combiner Min Commandes avec un minimum de dépense est une méthode fiable pour définir des clients VIP : ils achètent fréquemment *et* dépensent généreusement.

### Critères de récence

- **Min Jours depuis la dernière commande** — la commande la plus récente du client doit remonter au moins à ce nombre de jours
- **Max Jours depuis la dernière commande** — la commande la plus récente du client doit être dans ce nombre de jours

Les critères de récence sont essentiels pour les segments à risque et inactifs. Par exemple, en fixant Min Jours à 90 et Max Jours à 365, vous identifierez les clients qui se sont tapis mais ne sont pas complètement perdus.

## Priorité des segments

Lorsqu'un client correspond à plus d'un segment, le segment avec la **plus haute priorité** gagne. Vous pouvez définir la priorité pour chaque segment dans la section **Paramètres d'affichage** du formulaire de segment.

Le segment **Client invité** est toujours évalué en premier, indépendamment de l'ordre de priorité, car le statut d'invité est déterminé par le type de compte plutôt que par les critères d'achat.

## Affichage et gestion des segments

Accédez à **Clients > Segments de clients** pour voir tous vos segments configurés. La liste affiche le nom d'affichage de chaque segment, le type interne, la couleur assignée, la priorité, le nombre actuel de clients correspondants et si le segment est actif.

![Liste des segments de clients](/static/core/admin/img/help/customer-segments/segments-list.webp)

### Créer ou modifier un segment

1.

Accédez à **Clients > Segments de clients**
2.

Cliquez sur un segment existant pour l'éditer, ou cliquez sur **+ Ajouter un segment de client** pour en créer un nouveau
3.

Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques.

Remplissez l'onglet **Informations sur le segment** : 
   - **Nom** — sélectionnez le type de segment interne à partir du menu déroulant
   - **Nom d'affichage** — le nom lisible par l'humain affiché dans l'admin (par exemple, "VIP Customers")
   - **Description** — une note interne brève expliquant ce que ce segment représente
4.

Définissez des critères à travers les onglets pertinents : 
   - **Critères - Dépenses** — dépense totale minimale et maximale
   - **Critères - Commandes** — nombre minimal et maximal de commandes
   - **Critères - Récence** — nombre minimal et maximal de jours depuis la dernière commande
5.

Configurez **Paramètres d'affichage** : 
   - **Couleur** — une couleur hex utilisée pour identifier visuellement ce segment dans les listes
   - **Priorité** — un nombre plus élevé signifie que ce segment est évalué en premier
   - **Actif** — décochez pour désactiver le segment sans le supprimer
6.

Cliquez sur **Enregistrer** pour appliquer les modifications

### Exemple : Configuration d'un segment VIP

Voici un exemple réaliste pour un segment VIP à haute valeur :

| Champ | Valeur |
|---|---|
| Nom | `vip` |
| Nom d'affichage | VIP Customers |
| Dépense totale minimale | $1 000 |
| Commandes minimales | 5 |
| Jours depuis la dernière commande maximale | 180 |
| Priorité | 90 |
| Couleur | `#FFD700` |

Cela signifie : un client est considéré comme VIP s'il a dépensé au moins $1 000, a passé au moins 5 commandes et a effectué un achat au cours des 6 derniers mois.

### Exemple : Configuration d'un segment à risque

| Champ | Valeur |
|---|---|
| Nom | `at_risk` |
| Nom d'affichage | À risque |
| Jours depuis la dernière commande minimale | 60 |
| Jours depuis la dernière commande maximale | 180 |
| Priorité | 30 |
| Couleur | `#FF6B35` |

## Utilisation des segments pour le marketing ciblé

Les segments sont affichés sur les profils clients à travers l'admin, donc votre équipe sait immédiatement à quel niveau appartient chaque client. Utilisez cette information pour : 

- **Mener des campagnes de coupons ciblés** — créez des coupons restreints aux clients d'un segment spécifique, puis utilisez votre système de messagerie pour les envoyer uniquement à ce groupe
- **Prioriser le support** — marquez les clients VIP ou à haute valeur afin que votre équipe puisse leur fournir un service prioritaire
- **Planifier la réengagement** — examinez régulièrement les segments À risque et Inactif pour identifier les clients qui ont besoin d'un courriel de réengagement ou d'une offre spéciale
- **Ajuster le budget marketing** — concentrez le budget d'acquisition sur les canaux qui attirent les clients à haute valeur en analysant les cohortes de segments qu'ils convertissent

## Conseils

- Commencez par les types de segments prédéfinis avant de créer des critères personnalisés — ils couvrent les besoins de segmentation les plus courants dès le départ
- Vérifiez périodiquement le nombre de clients dans chaque segment ; un segment VIP avec zéro client ou un segment À risque qui augmente rapidement méritent une investigation
- Utilisez le champ **Priorité** avec soin — si vos critères se chevauchent entre segments (par exemple, un client correspond à la fois à Frequent Buyer et High Value), le segment à plus haute priorité l'emporte
- Désactivez les segments que vous n'utilisez pas actuellement au lieu de les supprimer — vous pouvez les réactiver plus tard sans reconfigurer les critères
- Les critères de segment sont vérifiés contre les métriques client stockées, qui sont recalculées automatiquement. Si les comptages de segment semblent obsolètes, les métriques peuvent être recalculées depuis la section Métriques client de l'admin