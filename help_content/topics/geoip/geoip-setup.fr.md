---
title: Configuration GeoIP
---

Le GeoIP permet à votre magasin de détecter automatiquement l'origine de chaque visiteur en se basant sur son adresse IP. Cela active des fonctionnalités basées sur la localisation à travers votre magasin — de l'affichage de la bonne devise par défaut, à l'exécution de règles commerciales géographiques, en passant par l'analyse des données au niveau du pays.

Votre magasin est préconfiguré avec le service GeoIP de Spwig, donc la détection géographique fonctionne dès la mise en place. Vous pouvez également connecter des fournisseurs supplémentaires pour une plus grande précision, utiliser une base de données que vous téléchargez vous-même, ou vous appuyer sur les en-têtes d'un CDN pour des recherches sans latence.

## Fonctionnement des fournisseurs

Accédez à **Clients > Fournisseurs GeoIP** pour voir les fournisseurs configurés pour votre magasin. Chaque fournisseur gère les recherches d'adresses IP vers des localisations en utilisant une méthode différente. Lorsqu'un visiteur arrive, votre magasin interroge les fournisseurs actifs dans l'ordre de priorité et utilise le premier résultat réussi.

Plusieurs fournisseurs peuvent être actifs en même temps — les fournisseurs avec un numéro de priorité plus bas sont testés en premier. Si le fournisseur de plus haute priorité échoue ou ne renvoie aucune donnée, le suivant est testé automatiquement.

### Types de fournisseurs disponibles

| Fournisseur | Description |
|----------|-------------|
| **Spwig GeoIP** | Recherche basée en cloud par le service Spwig. Aucune configuration requise. |
| **MaxMind GeoLite2** | Base de données hors ligne de MaxMind. Haute précision. Nécessite une clé de licence gratuite. |
| **DB-IP Lite** | Base de données hors ligne de DB-IP. Téléchargez-la depuis leur site web. |
| **IP2Location LITE** | Base de données hors ligne d'IP2Location. Nécessite une inscription gratuite. |
| **En-têtes de bord CDN** | Lit les en-têtes de localisation injectés par votre CDN (par exemple, Cloudflare). Aucune latence. |
| **Indices du navigateur** | Utilise l'heure/la langue fournis par le navigateur comme signal de localisation non contraignant. |
| **Fournisseur personnalisé** | Un composant de fournisseur installé depuis le marché des composants Spwig. |

## Ajouter un fournisseur

### Utilisation du service GeoIP de Spwig (par défaut)

Le fournisseur GeoIP de Spwig est ajouté automatiquement lors d'une nouvelle installation. Vérifiez qu'il apparaît dans la liste et que **Actif** est coché. Aucune configuration supplémentaire n'est nécessaire.

### Ajouter une base de données MaxMind GeoLite2

MaxMind propose une base de données gratuite hors ligne qui fournit des résultats précis sans envoyer des recherches à un service externe.

1. Enregistrez-vous pour un compte gratuit sur maxmind.com et générez une clé de licence
2. Accédez à **Clients > Fournisseurs GeoIP** et cliquez sur **+ Ajouter un fournisseur GeoIP**
3. Remplissez le formulaire :
   - **Nom** : `MaxMind GeoLite2` (ou tout autre nom descriptif)
   - **Type de fournisseur** : MaxMind GeoLite2
   - **Actif** : coché
   - **Priorité** : `1` (plus bas que la priorité par défaut de Spwig pour l'essayer en premier, ou plus haut pour l'utiliser comme secours)
   - **Clé de licence** : collez votre clé de licence MaxMind
   - **URL de la base de données** : l'URL de téléchargement depuis votre tableau de bord du compte MaxMind
4. Cliquez sur **Enregistrer**

Après l'enregistrement, sélectionnez le fournisseur dans la liste et utilisez l'action **Mettre à jour les bases de données du fournisseur sélectionné** pour vérifier que l'URL de la base de données est accessible.

### Ajouter des en-têtes de bord CDN

Si votre magasin est derrière un CDN qui injecte des en-têtes de géolocalisation (par exemple, `CF-IPCountry` de Cloudflare), vous pouvez utiliser ces en-têtes pour une détection instantanée du pays sans latence.

1. Accédez à **Clients > Fournisseurs GeoIP** et cliquez sur **+ Ajouter un fournisseur GeoIP**
2. Définissez **Type de fournisseur** sur **En-têtes de bord CDN**
3. Définissez **Priorité** sur `0` (priorité la plus élevée, car les en-têtes sont la source la plus rapide)
4. Dans le champ **Configuration**, spécifiez quel en-tête votre CDN utilise :
   ```json
   {
     "header_name": "CF-IPCountry"
   }
   ```
5. Cliquez sur **Enregistrer**

## Tester un fournisseur

Après avoir ajouté un fournisseur, vous pouvez vérifier qu'il fonctionne correctement :

1. Dans la liste des fournisseurs GeoIP, sélectionnez le fournisseur à l'aide de sa case à cocher
2. Ouvrez le menu déroulant **Action** et choisissez **Tester les fournisseurs sélectionnés**
3. Cliquez sur **Aller**

Spwig enverra une recherche de test pour une adresse IP connue (le DNS public de Google, `8.8.8.8`) et vous montrera le résultat. Un test réussi affichera le pays renvoyé et le temps de réponse en millisecondes.

## Définir la priorité du fournisseur

Lorsque plusieurs fournisseurs sont activés, le champ **Priority** (Priorité) détermine lequel est essayé en premier.

Les nombres plus bas indiquent une priorité plus élevée.

Par exemple, pour utiliser d'abord les en-têtes du CDN (plus rapide) et revenir sur Spwig GeoIP en cas d'échec :

| Fournisseur | Priorité |
|------------|----------|
| CDN Edge Headers | 0 |
| Spwig GeoIP | 10 |

Vous pouvez modifier la priorité directement dans la liste — la colonne **Priority** (Priorité) est modifiable en ligne.

## Surveillance des performances des fournisseurs

Chaque enregistrement de fournisseur suit ses propres statistiques de précision :

- **Total Lookups** — nombre total de recherches d'adresses IP effectuées
- **Successful Lookups** — recherches qui ont renvoyé un résultat
- **Failed Lookups** — recherches qui n'ont renvoyé aucune donnée ou une erreur
- **Average Response (ms)** — temps de réponse moyen en millisecondes
- **Accuracy** — pourcentage de recherches réussies

Si un fournisseur affiche un taux de précision faible ou des temps de réponse élevés, envisagez d'ajuster sa priorité ou de le désactiver au profit d'une option mieux performante.

## Mappages par pays

Accédez à **Customers > Country Mappings** (Clients > Mappages par pays) pour configurer les paramètres par défaut par pays pour la devise, la langue, l'impôt et l'expédition. Chaque entrée de pays contrôle :

- **Default Currency** — devise pré-sélectionnée pour les visiteurs de ce pays
- **Default Language** — langue affichée aux visiteurs de ce pays
- **Tax Rate** — pourcentage d'impôt par défaut appliqué pour ce pays
- **Is EU Member** / **Requires VAT** — utilisé pour la logique de conformité fiscale de l'UE
- **Shipping Zone** — relie le pays à une zone d'expédition
- **Supports COD** — active le paiement à la livraison (COD) pour ce pays

Vous pouvez modifier directement les champs **Is Active** (Actif), **Default Currency** (Devise par défaut) et **Default Language** (Langue par défaut) dans la liste sans avoir à ouvrir chaque enregistrement.

## Conseils

- Le fournisseur Spwig GeoIP fonctionne immédiatement sans configuration — ajoutez uniquement des fournisseurs supplémentaires si vous avez besoin d'une plus grande précision ou d'une utilisation hors ligne
- Si vous utilisez Cloudflare, le fournisseur CDN Edge Headers est le meilleur choix : il n'ajoute aucune latence et ne compte pas contre aucun quota d'API
- Gardez uniquement les fournisseurs que vous utilisez réellement activés — avoir plusieurs fournisseurs actifs n'améliore pas la précision si le premier réussit déjà
- Vérifiez les statistiques de précision hebdomadairement et désactivez tout fournisseur dont le taux de réussite est inférieur à 80 %
- Les mappages par pays sont utilisés comme paramètres par défaut ; les clients peuvent toujours modifier manuellement leur devise et leur langue sur le site de vente