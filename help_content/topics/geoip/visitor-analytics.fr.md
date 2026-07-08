---
title: Analyse des visiteurs
---

L'analyse des visiteurs vous donne une vision claire de la manière dont les clients circulent dans votre magasin. Vous pouvez voir quelles pages attirent le plus de visites, comment le trafic global évolue au fil du temps, quels appareils vos clients utilisent, et comment les nouveaux visiteurs se comparent aux visiteurs existants — tout cela sans avoir besoin d'outils d'analyse externes.

## Aperçu des écrans d'analyse

Votre magasin suit automatiquement l'activité des visiteurs une fois que le système GeoIP est actif. Les données sont organisées en trois vues, chacune vous donnant un niveau différent de détail.

### Résumé du trafic quotidien

Accédez à **Clients > Statistiques de trafic quotidien** pour voir le trafic global de votre magasin pour chaque jour. Chaque ligne représente un jour du calendrier et affiche :

| Colonne | Ce que cela vous indique |
|--------|-------------------|
| **Date** | Le jour auquel le trafic a été enregistré |
| **Total des vues** | Toutes les vues de pages, y compris les bots |
| **Visiteurs uniques** | Visiteurs distincts (par session) |
| **Vues de bots** | Vues provenant de crawlers et d'outils automatisés |
| **Nouveaux visiteurs** | Sessions sans historique antérieur |
| **Visiteurs existants** | Sessions de visiteurs déjà vus |
| **Vues sur ordinateur** | Vues provenant de navigateurs de bureau |
| **Vues mobiles** | Vues provenant d'appareils mobiles |
| **Vues tablettes** | Vues provenant d'appareils tablettes |

Utilisez la navigation hiérarchique des dates en haut de la liste pour sauter rapidement à un mois ou une année spécifique. Les totaux sont mis à jour quotidiennement via un processus en arrière-plan automatisé, donc les chiffres du jour en cours apparaîtront le lendemain matin.

### Statistiques par page

Accédez à **Clients > Statistiques de page quotidienne** pour voir le trafic détaillé par page individuelle. Chaque ligne affiche un chemin d'URL pour un jour, donc vous pouvez comparer les performances de pages spécifiques au fil du temps.

| Colonne | Ce que cela vous indique |
|--------|-------------------|
| **Date** | Le jour auquel ces statistiques s'appliquent |
| **Chemin URL** | Le chemin de page normalisé (par exemple, `/products/blue-widget`) |
| **Vues** | Total des vues pour cette page ce jour-là |
| **Visiteurs uniques** | Visiteurs distincts ayant consulté cette page |
| **Vues de bots** | Vues provenant de bots sur cette page |
| **Entrées** | Le nombre de sessions qui ont commencé sur cette page (c'était leur page d'accueil) |

Utilisez le champ de recherche **Chemin URL** pour trouver des statistiques pour une page spécifique. Par exemple, recherchez `/products/` pour voir tout le trafic des pages produits, ou recherchez un slug de produit spécifique pour vous concentrer sur un seul article.

### Événements de vues de pages individuelles

Accédez à **Clients > Vues de pages** pour obtenir un journal brut de chaque navigation de page suivie. C'est un enregistrement en lecture seule — vous ne pouvez pas ajouter ou modifier d'entrées. Utilisez-le pour investiguer des sessions spécifiques ou pour vérifier que le suivi est correctement enregistré.

Chaque enregistrement affiche :
- **Chemin URL** — la page visitée
- **Session** — un identifiant court pour la session du visiteur
- **Source** — si la visite provient du frontend headless ou du magasin en ligne standard
- **Est un bot** — si le visiteur a été identifié comme trafic automatisé
- **Est une page d'entrée** — si cette page était la première de leur session
- **Horodatage** — l'heure exacte de la visite

Vous pouvez filtrer par **Est un bot**, **Source** et **Est une page d'entrée** à l'aide des filtres du volet latéral, et naviguer par date en utilisant la hiérarchie de dates en haut.

## Lire les tendances du trafic

Le résumé du trafic quotidien est votre meilleur outil pour détecter des tendances. Recherchez des motifs tels que :

- **Pic de trafic** après avoir lancé une promotion ou envoyé un courriel marketing
- **Croissance progressive** sur les semaines et les mois à mesure que votre magasin gagne en visibilité organique
- **Patterns de week-end vs. jours ouvrés** pour comprendre quand vos clients sont les plus actifs
- **Répartition mobile vs. bureau** pour décider si vous devez prioriser des modifications de conception optimisées pour mobile

Les colonnes **Nouveaux visiteurs** et **Visiteurs existants** ensemble vous indiquent comment vous retenez les clients. Un magasin sain voit généralement un mélange des deux — une forte proportion de nouveaux visiteurs suggère une forte acquisition, tandis qu'une part plus élevée de visiteurs existants suggère que la fidélité des clients commence à se développer.

La vue des statistiques par page, triée par nombre de vues dans l'ordre descendant (par défaut), affiche immédiatement les pages qui génèrent le plus de trafic un jour donné.

Recherchez :

- **Pages à forte entrée, faible nombre de vues** — pages qui attirent des visiteurs via le référencement ou les publicités, mais qui ne retiennent pas l'attention
- **Pages à forte visibilité avec nombreux visiteurs uniques** — pages populaires qui méritent d'être régulièrement mises à jour
- **Pages de produits avec un nombre croissant de vues** — produits qui pourraient gagner en visibilité via le référencement

### Exemple : trouver le trafic d'un produit

Pour vérifier combien de trafic votre produit best-seller a reçu la semaine dernière :

1. Accédez à **Customers > Daily Page Stats**
2. Utilisez la hiérarchie de dates pour sélectionner la semaine pertinente
3. Dans la zone de recherche, entrez le slug de l'URL du produit (par exemple, `/blue-widget`)
4. Examinez les **Vues**, **Visiteurs uniques** et **Entrées** au cours des jours affichés

## Données sur la localisation des visiteurs

Accédez à **Customers > Visitor Locations** pour voir une vue au niveau des sessions de l'endroit où vos visiteurs se trouvent. Chaque enregistrement représente une session de visiteur et inclut :

- Pays et ville (déterminés automatiquement par le système GeoIP)
- Type d'appareil (ordinateur de bureau, mobile, tablette)
- Préférences de devise et de langue sélectionnées par le visiteur
- Attributions de campagne UTM (source, medium, nom de campagne)
- Drapeaux indiquant le trafic des bots et des administrateurs

Vous pouvez filtrer les visiteurs par pays, type d'appareil, source UTM et s'ils étaient des bots ou du personnel administrateur. Utilisez le filtre **Is Bot** réglé sur false pour vous concentrer sur le trafic des clients réels, et le filtre **Is Admin Traffic** pour exclure vos propres sessions de test de l'analyse.

## Conseils

- Les vues des bots sont suivies séparément et exclues automatiquement des comptes de visiteurs uniques — vos chiffres de trafic reflètent l'activité réelle des clients
- La colonne **Entrées** dans les statistiques par page vous indique les pages qui agissent comme la porte d'entrée de votre magasin via le référencement et les publicités ; optimiser ces pages a le plus grand impact
- Filtrez les localisations des visiteurs par **Source UTM** pour mesurer combien de trafic un canal de marketing spécifique (par exemple, une newsletter par e-mail ou une publicité Google) envoie réellement
- Les statistiques quotidiennes sont agrégées la nuit — si vous avez besoin de vérifier le trafic de la même journée, utilisez directement le journal des vues de page
- La répartition des appareils dans le résumé quotidien vous aide à prioriser votre travail de conception ; si plus de la moitié de vos visites proviennent de mobiles, assurez-vous que vos pages de produits et votre processus de paiement ont une apparence excellente à l'écran petit