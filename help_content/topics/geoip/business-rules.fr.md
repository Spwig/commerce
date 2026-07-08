---
title: Règles commerciales basées sur la localisation
---

Les règles commerciales basées sur la localisation vous permettent d'agir automatiquement lorsqu'un visiteur arrive d'un pays, d'une région ou d'un type d'appareil spécifique. Vous pouvez utiliser des règles pour définir une devise pour les clients d'une région particulière, rediriger les visiteurs vers une page localisée, afficher un bandeau promotionnel ou restreindre l'accès à certains contenus.

Les règles sont évaluées dans l'ordre de priorité chaque fois qu'une session de visiteur est établie. Lorsqu'une règle correspond, ses actions configurées sont exécutées immédiatement.

## Fonctionnement des règles commerciales

Chaque règle est composée de deux parties :

- **Conditions** — les critères qui doivent être remplis pour déclencher la règle (ex. : " le visiteur vient d'Allemagne ")
- **Actions** — ce qui se produit lorsque toutes les conditions correspondent (ex. : " définir la devise sur EUR ")

Les conditions et les actions sont stockées sous forme d'objets JSON dans le formulaire de règle. Spwig évalue toutes les règles actives dans l'ordre de priorité (les numéros les plus bas en premier) et applique celles qui correspondent.

## Accéder aux règles commerciales

Accédez à **Customers > Business Rules** pour voir toutes vos règles configurées. La liste affiche le nom de chaque règle, son statut, sa priorité, le nombre de fois où elle a été déclenchée et la dernière fois qu'elle a été déclenchée.

Cliquez sur une règle pour la consulter ou la modifier, ou cliquez sur **+ Ajouter une règle commerciale** pour en créer une nouvelle.

## Créer une règle commerciale

### Étape 1 : informations de base

Remplissez les détails d'identification de la règle :

- **Nom** — un nom clair et descriptif (ex. : `Définir EUR pour la zone euro`)
- **Description** — notes optionnelles expliquant l'objectif de la règle
- **Actif** — cochez cette case pour activer la règle ; décochez-la pour la suspendre sans la supprimer
- **Priorité** — les numéros plus bas s'exécutent en premier ; utilisez `10`, `20`, `30` pour laisser de la place aux règles futures

### Étape 2 : définir les conditions

Dans le champ **Conditions**, entrez un objet JSON qui décrit quand la règle doit être déclenchée. Toutes les conditions de l'objet doivent être vraies pour que la règle corresponde.

#### Clés de condition disponibles

| Condition | Format | Exemple |
|-----------|--------|---------|
| `country_in` | Tableau de codes de pays ISO | `["DE", "FR", "IT"]` |
| `country_not_in` | Tableau de codes de pays ISO | `["US", "CA"]` |
| `region_in` | Tableau de noms de régions | `["Bavaria", "Catalonia"]` |
| `region_not_in` | Tableau de noms de régions | `["Quebec"]` |
| `is_mobile` | Booléen | `true` |
| `is_vpn` | Booléen | `false` |

#### Exemples de conditions

Visiteurs venant d'Allemagne, de France ou d'Italie :
```json
{
  "country_in": ["DE", "FR", "IT"]
}
```

Visiteurs venant des États-Unis et utilisant un appareil mobile :
```json
{
  "country_in": ["US"],
  "is_mobile": true
}
```

Visiteurs venant en dehors de l'Union européenne :
```json
{
  "country_not_in": ["AT","BE","BG","CY","CZ","DE","DK","EE","ES","FI","FR","GR","HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"]
}
```

### Étape 3 : définir les actions

Dans le champ **Actions**, entrez un objet JSON décrivant ce qui doit se produire lorsqu'une règle est déclenchée.

#### Clés d'action disponibles

| Action | Format | Description |
|--------|--------|-------------|
| `set_currency` | Chaîne de code de devise | Définir une devise pour le visiteur |
| `set_language` | Chaîne de code de langue | Définir la langue d'affichage |
| `show_banner` | Booléen | Déclencher un bandeau promotionnel |
| `redirect_to` | Chaîne de chemin d'URL | Rediriger le visiteur vers une autre URL |

#### Exemples d'actions

Définir la devise sur Euro :
```json
{
  "set_currency": "EUR"
}
```

Rediriger vers une page d'accueil localisée :
```json
{
  "redirect_to": "/de/"
}
```

Définir à la fois la devise et la langue :
```json
{
  "set_currency": "GBP",
  "set_language": "en"
}
```

## Exemples pratiques

### Exemple : règle de devise pour la zone euro

**Scénario :** Afficher automatiquement les prix en euros aux visiteurs provenant de pays de la zone euro.

| Champ | Valeur |
|-------|-------|
| Nom | `Zone euro — Définir EUR` |
| Priorité | `10` |
| Actif | Coché |
| Conditions | `{"country_in": ["AT","BE","DE","ES","FI","FR","GR","IE","IT","LU","NL","PT"]}` |
| Actions | `{"set_currency": "EUR"}` |

### Exemple : règle de devise du Royaume-Uni

**Scénario :** Afficher les prix en GBP aux visiteurs provenant du Royaume-Uni.

| Champ | Valeur |
|-------|-------|
| Nom | `UK — Set GBP` |
| Priorité | `20` |
| Actif | Coché |
| Conditions | `"{\"country_in\": [\"GB\"]}"` |
| Actions | `"{\"set_currency\": \"GBP\"}"` |

### Exemple : rediriger vers une section du magasin localisé

**Scénario :** Envoyer les visiteurs en Australie vers une page dédiée australienne.

| Champ | Valeur |
|-------|-------|
| Nom | `Australia — Redirect` |
| Priorité | `30` |
| Actif | Coché |
| Conditions | `"{\"country_in\": [\"AU\"]}"` |
| Actions | `"{\"redirect_to\": \/au\/}"` |

## Tester les règles

Vous pouvez vérifier si une règle correspond au profil de visiteur attendu sans avoir à attendre le trafic réel :

1. Dans la liste des règles d'entreprise, sélectionnez la règle à l'aide de sa case à cocher
2. Ouvrez le menu déroulant **Action** et choisissez **Test selected rules**
3. Cliquez sur **Go**

Spwig évaluera la règle par rapport à un profil de visiteur basé aux États-Unis et indiquera s'il y a correspondance et quelles actions auraient été déclenchées.

## Surveillance de l'activité des règles

La colonne **Triggered** dans la liste des règles indique combien de fois chaque règle a été déclenchée. Cliquez sur une règle pour voir l'horodatage **Last Triggered** dans la section Statistiques.

Utilisez l'action **Reset statistics** pour remettre à zéro les compteurs de déclenchement si vous souhaitez commencer à mesurer à partir d'une date spécifique après avoir apporté des modifications à une règle.

## Conseils

- Définissez des priorités avec des écarts (10, 20, 30) plutôt que des numéros consécutifs (1, 2, 3) afin d'insérer de nouvelles règles plus tard sans avoir à renuméroter tout
- Les règles s'appliquent dans l'ordre de priorité et toutes les règles correspondantes sont appliquées — si deux règles définissent toutes deux la devise, l'action de la règle à priorité plus basse (numéro plus élevé) sera appliquée en dernier
- Utilisez le commutateur **Is Active** pour suspendre temporairement une règle pendant des promotions sans supprimer la configuration
- Testez toujours une nouvelle règle avant de l'activer dans un environnement en production pour vous assurer que les conditions sont correctes
- La détection des VPN (`"is_vpn": true`) est disponible si vous souhaitez appliquer un traitement différent aux visiteurs masquant leur emplacement, mais gardez à l'esprit que certains clients légitimes utilisent des VPN pour la confidentialité