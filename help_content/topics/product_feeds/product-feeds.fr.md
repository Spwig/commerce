---
title: Fournisseurs de flux de produits
---

Les flux de produits vous permettent d'exporter votre catalogue vers des plateformes de commerce telles que Google Shopping et Facebook Catalog. Une fois connecté, vos données de produit sont automatiquement synchronisées selon un planning, afin que vos publicités reflètent toujours vos prix actuels, stocks et détails de produit.

Votre magasin utilise un système de composants fournisseurs pour les flux. Chaque fournisseur de flux (Google, Facebook ou d'autres) est installé en tant que composant, puis connecté via un compte fournisseur. Vous pouvez exécuter plusieurs fournisseurs de flux en même temps - par exemple, un flux pour Google Shopping et un autre distinct pour Facebook.

## Connexion à un fournisseur de flux

Avant de synchroniser votre catalogue, vous devez installer et connecter au moins un composant fournisseur.

### Installation d'un composant fournisseur

Les composants fournisseurs sont disponibles sur le marché des composants Spwig. L'administrateur de votre magasin les installe via le système de mise à jour des composants. Une fois un composant fournisseur installé, il apparaît comme option lors de la création d'un compte fournisseur.

### Création d'un compte fournisseur

1. Accédez à **Marketing > Fournisseurs de flux**
2. Cliquez sur **+ Ajouter un compte fournisseur**
3. Remplissez le formulaire :

**Section Informations sur le fournisseur :**
- **Site** — sélectionnez votre magasin (il n'y en a qu'un seul)
- **Composant fournisseur** — choisissez le fournisseur de flux installé (par exemple, Google Shopping, Facebook Catalog)
- **Nom du compte** — un nom descriptif tel que `Google Shopping — Principal` ou `Facebook Catalog — États-Unis`

**Section Configuration :**
- **Actif** — cochez pour activer la génération de flux et la synchronisation
- **Principal** — cochez si c'est votre fournisseur de flux principal pour ce type de plateforme
- **Priorité** — contrôle l'ordre de tri dans la liste (les nombres plus bas apparaissent en premier)
- **Configuration** — paramètres spécifiques au fournisseur (voir ci-dessous)

4. Cliquez sur **Enregistrer**

## Options de configuration du flux

Le champ **Configuration** accepte un objet JSON avec les options suivantes :

| Option | Valeurs | Description |
|--------|--------|-------------|
| `sync_interval` | `hourly`, `daily`, `weekly`, `manual` | Fréquence à laquelle le flux est automatiquement régénéré |
| `format_preference` | `xml`, `csv`, `json` | Format de sortie (la plupart des plateformes préfèrent XML) |
| `include_variants` | `true` / `false` | Inclure les variantes de produit comme des entrées de flux distinctes |
| `target_country` | Code du pays, par exemple `"US"` | Pays cible pour le flux |
| `content_language` | Code de langue, par exemple `"en"` | Langue des données de produit |

#### Exemple de configuration pour un flux XML quotidien ciblant les États-Unis :

```json
{
  "sync_interval": "daily",
  "format_preference": "xml",
  "include_variants": true,
  "target_country": "US",
  "content_language": "en"
}
```

## Filtre des produits inclus dans le flux

Vous pouvez contrôler exactement quels produits sont inclus en ajoutant une section `product_filter` à la configuration :

```json
{
  "product_filter": {
    "status": ["published"],
    "in_stock_only": true,
    "categories": [1, 5, 12]
  }
}
```

| Option de filtre | Description |
|---------------|-------------|
| `status` | Ne comprendre que les produits avec ces statuts. Utilisez `["published"]` pour ne comprendre que les produits actifs. |
| `in_stock_only` | Mettez à `true` pour exclure les produits en rupture de stock |
| `categories` | Limiter aux ID de catégories spécifiques |
| `brands` | Limiter aux ID de marques spécifiques |

Vous pouvez également exclure des produits spécifiques par leurs ID en utilisant `exclude_products` :

```json
{
  "exclude_products": [42, 87, 103]
}
```

## Surveillance de l'état de synchronisation

La liste des comptes fournisseurs affiche à l'œil nu l'état de synchronisation de chaque flux connecté :

- **EN ATTENTE** — aucune synchronisation n'a encore eu lieu, ou le flux attend la génération
- **EN COURS DE SYNCHRONISATION** — une synchronisation est en cours
- **RÉUSSIE** — la dernière synchronisation s'est terminée sans erreur
- **ERREUR** — la dernière synchronisation a échoué ; le message d'erreur est affiché sur la page de détails du compte

La liste affiche également le nombre de produits dans le flux actuel et l'heure de la dernière synchronisation.

## Visualisation des flux générés

Accédez à **Marketing > Flux de produits** pour voir les fichiers de flux générés. Chaque entrée représente une capture d'écran d'un flux généré et affiche :

- **Compte Fournisseur** — à quel compte fournisseur appartient ce flux
- **Format** — XML, CSV ou JSON
- **Nombre de Produits** — nombre de produits inclus
- **Taille** — taille du fichier du flux généré
- **Généré le** — date de création
- **Expire le** — date d'expiration de cette version mise en cache
- **Statut** — si le flux est toujours valide ou s'il a expiré
- **Nombre de Téléchargements** — combien de fois ce flux a été téléchargé

Les flux sont en lecture seule dans l'admin — ils sont générés automatiquement par le processus de synchronisation.

## Affichage de l'historique de synchronisation

Accédez à **Marketing > Historique des Synchronisations de Flux** pour consulter l'historique complet de chaque tentative de synchronisation pour tous vos comptes de flux. Chaque entrée de journal enregistre :

- Le compte fournisseur qui a été synchronisé
- Le type de synchronisation (Complexe, Incrémentale, Manuelle ou Planifiée)
- Statut (Succès, Succès Partiel, Échec, etc.)
- Produits synchronisés, échoués et ignorés
- Durée de la synchronisation
- Toute message d'erreur

Le tableau de bord du journal de synchronisation en haut de la page affiche des statistiques globales : nombre total de synchronisations, taux de succès et durée moyenne de synchronisation. Utilisez les filtres **Compte** et **Type de Synchronisation** pour affiner à un flux spécifique.

### À faire en cas d'échec de synchronisation

1. Accédez à **Marketing > Historique des Synchronisations de Flux** et trouvez l'entrée échouée
2. Cliquez sur l'entrée de journal pour afficher le **Message d'Erreur** et **Détails de l'Erreur** complets
3. Les causes courantes incluent :
   - Des champs de produit requis manquants (titre, prix, image)
   - Des identifiants API invalides ou expirés — réinstallez le composant fournisseur pour actualiser les identifiants
   - Des erreurs réseau lors de la connexion à l'API du fournisseur
4. Une fois le problème résolu, la prochaine synchronisation planifiée s'exécutera automatiquement, ou vous pouvez déclencher une synchronisation manuelle depuis le compte fournisseur

## Conseils

- Définissez `"sync_interval": "daily"` pour la plupart des cas d'utilisation — Google et Facebook n'exigent pas de mises à jour plus fréquentes à moins que vous n'ayez une volatilité de prix très élevée
- Incluez toujours `"in_stock_only": true` dans votre filtre de produit pour éviter d'annoncer des produits que les clients ne peuvent pas acheter
- Utilisez un nom de compte descriptif qui inclut la plateforme et le marché cible (par exemple, `Google Shopping — UK`) pour faciliter la gestion de plusieurs flux
- Le nombre de **Produits dans le Flux** affiché sur le compte fournisseur vous indique immédiatement si moins de produits que prévu sont inclus — vérifiez vos paramètres de filtre de produit si le nombre semble faible
- Marquez un compte comme **Flux Principal** pour chaque type de fournisseur ; certains outils de rapport utilisent cela pour identifier votre flux principal
- Vérifiez le journal de synchronisation après toute modification en masse de votre catalogue de produits pour confirmer que les données mises à jour ont été correctement prises en compte