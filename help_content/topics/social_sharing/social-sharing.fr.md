---
title: Partage social
---

Les boutons de partage social permettent aux clients de partager vos produits, articles de blog et pages vers les réseaux sociaux directement depuis votre boutique en ligne. Vous contrôlez les plateformes affichées, l'apparence des boutons, leur emplacement et si l'activité de partage est suivie et comptée.

## Configuration des paramètres de partage social

Tout le comportement de partage social est contrôlé depuis une seule page de paramètres. Accédez à **Marketing > Paramètres de partage social** (la page redirige automatiquement vers le formulaire de paramètres — il n'y a qu'un seul enregistrement de paramètres).

### Emplacement : où apparaissent les boutons

La section **Emplacement** contrôle les types de contenu qui affichent automatiquement les boutons de partage.

| Paramètre | Description |
|---------|-------------|
| **Activer sur les produits** | Afficher les boutons de partage sur les pages de détails des produits |
| **Activer sur les catégories** | Afficher les boutons de partage sur les pages de liste des catégories |
| **Activer sur les articles de blog** | Afficher les boutons de partage sur les pages d'articles de blog |
| **Activer sur les pages personnalisées** | Afficher les boutons de partage sur les pages personnalisées de la boutique |

Cochez les types de contenu sur lesquels vous souhaitez que les boutons apparaissent. Vous pouvez activer toute combinaison — par exemple, uniquement les produits et les articles de blog.

**Position de l'emplacement** contrôle l'endroit sur la page où les boutons sont affichés :

| Option | Description |
|--------|-------------|
| **En dessous du contenu** (par défaut) | Affiché après le contenu principal |
| **Au-dessus du contenu** | Affiché avant le contenu principal |
| **Barre latérale** | Affiché dans la barre latérale de la page |
| **Flottant (fixe)** | Reste collé au côté de l'écran lorsque le visiteur fait défiler |

### Apparence : comment les boutons ressemblent

La section **Apparence** contrôle les plateformes affichées et la mise en forme des boutons.

**Plateformes activées** — laissez vide pour afficher toutes les plateformes prises en charge, ou entrez un tableau JSON pour restreindre les plateformes affichées :

```json
["facebook", "twitter", "pinterest", "whatsapp", "email"]
```

Plateformes prises en charge : `facebook`, `twitter`, `linkedin`, `pinterest`, `whatsapp`, `telegram`, `email`

**Style du bouton** : 

| Style | Description |
|-------|-------------|
| **Icône seule** (par défaut) | Affiche uniquement l'icône de la plateforme |
| **Icône + Étiquette** | Affiche l'icône et le nom de la plateforme |
| **Étiquette seule** | Affiche uniquement le nom de la plateforme en texte |

**Taille du bouton** — choisissez **Petit**, **Moyen** (par défaut) ou **Grand** pour correspondre à la conception de votre boutique en ligne.

**Direction de mise en page** — arrangez les boutons **Horizontalement** (par défaut, côte à côte) ou **Verticalement** (empilés).

**Afficher le titre** — lorsque coché, un titre "Partager" apparaît au-dessus du groupe de boutons.

**Visibilité mobile** contrôle l'affichage des boutons sur les petits écrans : 

| Option | Description |
|--------|-------------|
| **Toujours afficher** (par défaut) | Les boutons sont visibles sur tous les appareils |
| **Cacher sur mobile** | Les boutons sont cachés sur les appareils mobiles |
| **Uniquement sur mobile** | Les boutons sont affichés uniquement sur les appareils mobiles |

### Paramètres de suivi

**Afficher les comptes de partage** — lorsque coché, un badge de comptage apparaît sur chaque bouton pour indiquer combien de fois cette plateforme a été partagée. Les comptes sont mis à jour en temps réel à mesure que les partages sont enregistrés.

**Suivre les partages** — lorsque coché, chaque clic de partage est enregistré dans l'analyse des partages. Désactiver cela arrête l'enregistrement de nouveaux enregistrements mais n'efface pas les données existantes. Le suivi attribue également des badges de fidélité aux clients qui partagent (si le programme de fidélité est actif).

Cliquez sur **Enregistrer** en bas du formulaire pour appliquer vos modifications. Les paramètres prennent effet immédiatement.

## Consulter l'activité de partage

### Événements de partage individuels

Accédez à **Marketing > Partages sociaux** pour voir un journal de chaque événement de partage enregistré. Chaque entrée affiche :

- **Plateforme** — quel réseau social a été utilisé (affiché sous forme de badge coloré)
- **Contenu partagé** — le type et le nom du contenu partagé (par exemple, `produit: Blue Widget`)
- **Utilisateur** — le client qui a partagé, ou "Anonyme" pour les visiteurs non connectés
- **Type d'appareil** — ordinateur de bureau, mobile ou tablette
- **Partagé à** — la date et l'heure du partage

Le journal des partages est en lecture seule — les entrées sont créées automatiquement lorsque les clients cliquent sur les boutons de partage.

Utilisez les filtres **Platform** et **Device Type** pour explorer les modèles de partage, et la hiérarchie des dates pour examiner des périodes temporelles spécifiques.

### Partages par contenu

Accédez à **Marketing > Share Counts** pour voir les totaux agrégés de partages groupés par élément de contenu et plateforme. Cette vue permet facilement d'identifier vos produits et publications les plus partagés.

Chaque entrée affiche :
- **Content** — le type et le nom de l'élément (par exemple, `product: Blue Widget`)
- **Platform** — le réseau social
- **Share Count** — le nombre total de partages enregistrés sur cette plateforme
- **Last Updated** — quand le compte a été recalculé pour la dernière fois

La liste est triée par nombre de partages descendant, donc votre contenu le plus viral apparaît en haut. Les compteurs de partages sont mis à jour automatiquement chaque fois qu'un nouvel événement de partage est enregistré — il n'est pas nécessaire de les actualiser manuellement.

## Comprendre comment les partages sont suivis

Lorsqu'un client clique sur un bouton de partage, Spwig enregistre :

1. La plateforme sur laquelle ils ont partagé
2. Le contenu partagé (produit, article de blog, page, etc.)
3. S'ils étaient connectés (si oui, le partage est lié à leur compte pour l'intégration de fidélité)
4. Le type d'appareil
5. L'URL partagée

Le compte de partage pour cette plateforme et cet élément de contenu est ensuite incrémenté automatiquement. Si **Show Share Counts** est activé, le compte mis à jour apparaît sur le bouton la prochaine fois que la page est chargée.

## Intégration de fidélité

Si votre programme de fidélité est actif et que **Track Shares** est activé, les clients connectés gagnent des badges de fidélité lorsqu'ils partagent du contenu. Le badge de partage social fait partie des règles basées sur l'action du programme de fidélité.

Pour configurer l'attribution de points pour les partages, accédez à **Customers > Loyalty Rules** et cherchez des règles du type **Action-Based** avec le type d'action **Social Share**.

## Conseils

- Activez d'abord le partage sur les produits et les articles de blog — ce sont les types de contenu les plus susceptibles d'être partagés de manière organique par les clients
- Pinterest est particulièrement utile pour les catégories de produits visuels comme la mode, la décoration de la maison et la nourriture — priorisez-la dans la liste `enabled_platforms` pour ces magasins
- Le partage via WhatsApp génère une forte conversion à partir de recommandations chaleureuses, surtout sur mobile ; envisagez d'utiliser le mode d'affichage **Mobile Only** pour WhatsApp tout en maintenant d'autres plateformes visibles sur tous les appareils
- Si vous remarquez que les compteurs de partage sont gonflés, vérifiez si le trafic de test (des sessions administrateur) a été compté avant que le drapeau **Is Admin Traffic** ne soit pleinement fonctionnel — vous pouvez réinitialiser les compteurs en supprimant les entrées des analyses de partage
- Examinez la liste des Partages Mensuels pour identifier vos produits les plus partagés et les mettre en avant plus visiblement sur votre page d'accueil ou dans vos e-mails de marketing