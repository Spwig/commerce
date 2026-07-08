---
title: Zones d'expédition
---

Les zones d'expédition définissent des régions géographiques pour des tarifs d'expédition ciblés - regroupez les pays, états ou codes postaux en zones, puis reliez les méthodes d'expédition à des zones spécifiques pour un contrôle précis des tarifs. Les zones utilisent une correspondance basée sur la priorité lorsqu'une adresse correspond à plusieurs zones (la zone avec la plus haute priorité gagne). Ce système permet des stratégies de tarification sophistiquées : facturez plus cher pour les zones reculées, proposez une livraison gratuite dans le pays, ou proposez des tarifs réduits pour des régions spécifiques.

Utilisez les zones lorsque vous avez besoin de coûts d'expédition différents pour différentes zones géographiques, allant d'une simple division nationale vs internationale à une tarification hiérarchisée multi-région complexe.

## Compréhension des zones d'expédition

**Qu'est-ce qu'une zone** : Région géographique nommée définie par des codes de pays, d'états/provinces et des motifs de codes postaux.

**Fonctionnement des zones** :
1. Le client saisit son adresse de livraison à la caisse
2. Le système évalue toutes les zones actives
3. Les zones correspondant à l'adresse du client sont des candidats
4. Si plusieurs zones correspondent, la zone avec la plus haute priorité gagne
5. Les méthodes d'expédition liées à la zone gagnante sont affichées
6. Les méthodes non liées à aucune zone (ou liées à une zone correspondante) sont affichées

**Composants d'une zone** :
- **Nom** : Identifiant de la zone (ex. : "Domestique", "UE", "Zones reculées")
- **Pays** : Liste des codes de pays inclus (vide = tous les pays)
- **États/Provinces** : Restrictions d'état par pays (optionnel)
- **Motifs de codes postaux** : Motifs regex pour la correspondance des codes postaux (optionnel)
- **Priorité** : Un nombre plus élevé = une priorité plus élevée lorsqu'il y a plusieurs zones correspondantes

---

## Logique de correspondance des zones

Les zones utilisent une **réduction progressive** pour correspondre aux adresses :

### Niveau 1 : Correspondance par pays

**Liste de pays vide** → La zone correspond à TOUS les pays

**Liste de pays fournie** → Le pays de l'adresse doit être dans la liste

Exemple : 
```
Zone : "Domestique"
Countries: ["US"]
→ Correspond : toute adresse des États-Unis
→ Aucune correspondance : Canada, Royaume-Uni, etc.
```

### Niveau 2 : Correspondance par état/province

**Aucun état défini** → La zone correspond à TOUS les états des pays autorisés

**États définis pour des pays spécifiques** → L'état de l'adresse doit correspondre

Exemple : 
```
Zone : "West Coast"
Countries: ["US"]
States: {"US": ["CA", "OR", "WA"]}
→ Correspond : adresses de Californie, Oregon, Washington
→ Aucune correspondance : New York, Texas, etc.
```

### Niveau 3 : Correspondance par code postal

**Aucun motif défini** → La zone correspond à TOUS les codes postaux des pays/états autorisés

**Motifs définis** → Le code postal de l'adresse doit correspondre à au moins un motif

Exemple : 
```
Zone : "Los Angeles Metro"
Countries: ["US"]
States: {"US": ["CA"]}
Postal Patterns: ["^90[0-9]{3}$", "^91[0-9]{3}$"]
→ Correspond : 90001, 91210, 90245
→ Aucune correspondance : 94102 (San Francisco)
```

**Exemples de motifs regex** : 
- `^90[0-9]{3}$` - Zone de Los Angeles (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Format des codes postaux canadiens (K1A 0B1)
- `^SW[0-9]{1,2}` - Codes postaux du Royaume-Uni commençant par SW

---

## Sélection de zone basée sur la priorité

Lorsqu'une adresse correspond à plusieurs zones, la **priorité** détermine quelle zone s'applique : 

**Fonctionnement de la priorité** : 
- Un nombre plus élevé = une priorité plus élevée
- Si l'adresse correspond à des zones avec une priorité 100 et 50, la priorité 100 gagne
- Seules les méthodes d'expédition de la zone gagnante sont disponibles

**Cas d'utilisation** : 

**Scénario 1 : Une zone spécifique remplace une zone générale** 
```
Zone A : "Remote Alaska"
  Countries: ["US"]
  States: {"US": ["AK"]}
  Priority: 100

Zone B : "Domestic USA"
  Countries: ["US"]
  Priority: 50

Address: Anchorage, AK
→ Correspond à toutes les zones
→ Priorité 100 gagne
→ La zone "Remote Alaska" s'applique (coût d'expédition plus élevé)
```

**Scénario 2 : Un code postal remplace un état** 
```
Zone A : "Manhattan Premium"
  Countries: ["US"]
  States: {"US": ["NY"]}
  Postal Patterns: ["^100[0-2][0-9]$"]
  Priority: 100

Zone B : "New York State"
  Countries: ["US"]
  States: {"US": ["NY"]}
  Priority: 50

Address: New York, NY 10001
→ Correspond à toutes les zones
→ Priorité 100 gagne
→ "Manhattan Premium" s'applique (service d'expédition premium)
```

---

## Création de zones d'expédition

**Workflow étape par étape** : 

1. **Naviguez vers les zones** 
   - Allez dans Paramètres > Expédition > Zones d'expédition
   - Cliquez sur "Ajouter une zone d'expédition"

2. **Configuration de base** 
   - **Nom** : Identifiant descriptif (ex. : "Union européenne", "West Coast", "Zones reculées")
   - **Priorité** : Définissez l'importance relative (100 pour spécifique, 50 pour général, 1 pour fallback)
   - **Active** : Activez/désactivez via le commutateur

3. **Définir la couverture géographique** 

   **Option A : Tous les pays** (laissez la liste de pays vide)
   - La zone correspond à toutes les adresses à l'échelle mondiale
   - Utilisez pour les zones par défaut/fallback

   **Option B : Pays spécifiques** 
   - Cliquez sur "Ajouter un pays"
   - Sélectionnez les pays depuis le menu déroulant (US, CA, UK, etc.)
   - Répétez pour tous les pays inclus

   **Option C : États/Provinces spécifiques** 
   - Après avoir ajouté les pays, cliquez sur "Ajouter des états" pour chaque pays
   - Sélectionnez les états depuis le menu déroulant
   - Exemple : US → CA, OR, WA pour West Coast

   **Option D : Motifs de codes postaux** (avancé)
   - Entrez des motifs regex (un par ligne)
   - Testez les motifs avec des codes postaux d'exemple
   - Cliquez sur "Valider les motifs" pour vérifier la syntaxe

4. **Lier aux méthodes d'expédition** 
   - Les méthodes peuvent être liées lors de la modification de la méthode (pas dans la configuration de la zone)
   - Ou liez les zones aux méthodes existantes : Éditer la méthode → Zones d'expédition → Sélectionner les zones

5. **Définir la priorité d'affichage** 
   - Les zones à haute priorité remplacent les zones à basse priorité lorsqu'il y a plusieurs correspondances
   - Recommandé : Zones spécifiques (100), Zones régionales (50), Zone par défaut (1)

6. **Activer la zone** 
   - Activez le commutateur "Active" = Oui
   - Enregistrez

---

## Configurations de zones courantes

### Configuration 1 : National vs International

**Objectif** : Tarifs différents pour le national vs tous les autres pays.

```
Zone 1 : "Domestique"
  Countries: [Votre code de pays]
  Priority: 50

Zone 2 : "International"
  Countries: [Laissez vide ou sélectionnez tous les autres pays]
  Priority: 1
```

**Méthodes d'expédition** : 
- "Standard national" → Liée à la zone nationale
- "Expédition internationale" → Liée à la zone internationale

---

### Configuration 2 : International multi-région

**Objectif** : Tarifs différents pour l'UE, l'Amérique du Nord, l'Asie et le reste du monde.

```
Zone 1 : "Union européenne"
  Countries: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Priority: 100

Zone 2 : "Amérique du Nord"
  Countries: [US, CA, MX]
  Priority: 100

Zone 3 : "Asie-Pacifique"
  Countries: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Priority: 100

Zone 4 : "Reste du monde"
  Countries: [Laissez vide]
  Priority: 1
```

**Méthodes d'expédition** : 
- "Expédition UE" → Zone UE
- "Expédition Amérique du Nord" → Zone Amérique du Nord
- "Expédition Asie-Pacifique" → Zone Asie-Pacifique
- "Standard international" → Zone Reste du monde

---

### Configuration 3 : Surcoût pour les zones reculées

**Objectif** : Ajouter un surcoût pour les codes postaux reculés dans la zone nationale.

```
Zone 1 : "Remote Domestic"
  Countries: [US]
  Postal Patterns: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Priority: 100

Zone 2 : "Standard Domestic"
  Countries: [US]
  Priority: 50
```

**Méthodes d'expédition** : 
- "Expédition reculée" → Zone Remote Domestic (coût plus élevé)
- "Expédition standard" → Zone Standard Domestic

---

### Configuration 4 : Zones spécifiques aux états

**Objectif** : Tarifs différents pour chaque région des États-Unis.

```
Zone 1 : "West Coast"
  Countries: [US]
  States: {"US": ["CA", "OR", "WA"]}
  Priority: 100

Zone 2 : "East Coast"
  Countries: [US]
  States: {"US": ["NY", "NJ", "CT", "MA", "PA"]}
  Priority: 100

Zone 3 : "Midwest"
  Countries: [US]
  States: {"US": ["IL", "IN", "OH", "MI", "WI"]}
  Priority: 100

Zone 4 : "South"
  Countries: [US]
  States: {"US": ["TX", "FL", "GA", "NC", "SC"]}
  Priority: 100

Zone 5 : "Other US States"
  Countries: [US]
  Priority: 50
```

---

## Exemples de motifs de codes postaux

Les codes postaux utilisent des **regex** (expressions régulières) pour la correspondance de motifs : 

### États-Unis (Codes ZIP)

**Format** : 5 chiffres (ex. : 90210)

```
Californie (90000-96199) :  ^9[0-6][0-9]{3}$
New York (10000-14999) :    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599) :  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999) :      ^99[5-9][0-9]{2}$
```

### Canada (Codes postaux)

**Format** : A1A 1A1 (lettre-chiffre-lettre espace chiffre-lettre-chiffre)

```
Tous les codes postaux canadiens :  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$
Ontario (K, L, M, N, P) :    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$ 
Québec (G, H, J) :           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$ 
```

### Royaume-Uni (Codes postaux)

**Format** : AA1A 1AA ou A1A 1AA

```
Londres (E, EC, N, NW, SE, SW, W, WC) :  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}
Manchester (M) :                        ^M[0-9]{1,2}
Birmingham (B) :                        ^B[0-9]{1,2}
```

### Australie (Codes postaux)

**Format** : 4 chiffres (ex. : 2000)

```
Nouvelle-Galles-du-Sud (1000-2999) :  ^[12][0-9]{3}$
Victoria (3000-3999, 8000-8999) :  ^[38][0-9]{3}$
Queensland (4000-4999, 9000-9999) :  ^[49][0-9]{3}$
```

### Test des motifs

**Avant d'enregistrer les motifs**, testez avec des codes postaux connus : 

1. Entrez le motif : `^90[0-9]{3}$`
2. Entrée de test : "90210" → Doit correspondre
3. Entrée de test : "10001" → Ne doit pas correspondre
4. Entrée de test : "9021" → Ne doit pas correspondre (seulement 4 chiffres)

Utilisez des testeurs de regex en ligne (regex101.com) pour valider les motifs complexes.

---

## Résumé de la couverture des zones

Les zones affichent un **résumé de la couverture** dans la vue de la liste d'administration montrant ce qui est inclus : 

**Exemples** : 
- "Tous les pays" → Aucune restriction de pays
- "US, CA, MX" → 3 pays
- "US (CA, OR, WA)" → États-Unis avec 3 états
- "US (90xxx-91xxx)" → États-Unis avec des motifs de codes postaux

**Utiliser le résumé pour** : 
- Vérifier rapidement la couverture de la zone sans ouvrir
- Repérer les chevauchements ou les lacunes dans la couverture
- Audit de la configuration de la zone en un coup d'œil

---

## Lier les zones aux méthodes d'expédition

Les zones et les méthodes ont une **relation many-to-many** : 

**À partir de la méthode** (Recommandé) : 
1. Éditer la méthode d'expédition
2. Faites défiler jusqu'à la section "Zones d'expédition"
3. Sélectionnez les zones applicables (multi-sélection)
4. Enregistrez la méthode

**À partir de la zone** : 
- Les zones ne se lient pas directement aux méthodes
- Le lien est toujours effectué à partir de la configuration de la méthode

**Comportement méthode-zone** : 

**Aucune zone liée** → Méthode disponible pour TOUS les adresses

**Zones liées** → Méthode uniquement disponible si l'adresse du client correspond à au moins une zone liée

**Exemple** : 
```
Méthode : "Standard national"
Zones liées : ["USA national"]
→ Affichée uniquement aux adresses des États-Unis

Méthode : "Expédition internationale express"
Zones liées : ["UE", "Asie-Pacifique", "Reste du monde"]
→ Affichée à toutes les adresses non des États-Unis
```

---

## Test de correspondance des zones

Avant de lancer, testez la configuration des zones : 

1. **Créer des commandes de test** 
   - Utilisez des adresses dans différentes zones
   - Vérifiez que les correspondances de zones sont correctes

2. **Vérifier la résolution de la priorité** 
   - Utilisez une adresse qui correspond à plusieurs zones
   - Vérifiez que la zone avec la plus haute priorité gagne
   - Confirmez l'apparition des méthodes d'expédition attendues

3. **Tester les cas limites** 
   - Codes postaux frontaliers (ex. : 90999 vs 91000)
   - Limites d'état
   - Adresses internationales avec des codes postaux similaires

4. **Utiliser l'outil de prévisualisation des zones** (si disponible) 
   - Entrez une adresse de test
   - Voyez les zones correspondantes
   - Voir la résolution de la priorité

---

## Dépannage

**Problème 1 : Aucune méthode d'expédition disponible à la caisse**

**Causes** : 
- L'adresse du client ne correspond à aucune zone
- Toutes les méthodes sont liées à des zones qui ne correspondent pas
- Aucune méthode n'existe sans restrictions de zones

**Solution** : 
- Créez une zone de secours (tous les pays, priorité 1)
- OU supprimez les restrictions de zones d'au moins une méthode
- Vérifiez les motifs de pays/états/codes postaux des zones

---

**Problème 2 : Correspondance de zone incorrecte**

**Causes** : 
- Une zone de priorité plus bas est sélectionnée malgré une zone de priorité plus élevée correspondante
- Erreur de syntaxe dans le motif de code postal (le motif échoue silencieusement)
- Mismatch de code d'état (CA vs Californie)

**Solution** : 
- Vérifiez les valeurs de priorité (un nombre plus élevé = une priorité plus élevée)
- Testez les motifs de code postal avec un validateur de regex
- Utilisez les codes d'état à deux lettres (CA, pas Californie)

---

**Problème 3 : Méthode inattendue affichée**

**Causes** : 
- La méthode n'a aucune zone liée (disponible partout)
- Plusieurs zones correspondent, mais une zone inattendue a une priorité plus élevée
- La couverture des zones chevauche accidentellement

**Solution** : 
- Révisez les zones liées à la méthode
- Vérifiez la priorité des zones correspondantes
- Audit du résumé de la couverture des zones pour détecter les chevauchements

---

## Conseils

- **Commencez avec 2 zones** - Nationale et Internationale, étendez si nécessaire
- **Utilisez la priorité avec soin** - Zones spécifiques 100, régionales 50, fallback 1
- **Testez les motifs de code postal de manière approfondie** - Les erreurs de regex échouent silencieusement, empêchant les zones de correspondre
- **Documentez la logique des zones** - Ajoutez des notes à la description de la zone pour expliquer l'intention de couverture
- **Évitez les zones excessives** - Trop de zones compliquent la configuration ; utilisez des règles d'expédition pour les scénarios complexes
- **Utilisez les codes d'état, pas les noms** - "CA" pas "Californie", "NY" pas "New York"
- **Créez une zone de secours** - Tous les pays, priorité 1, assurez-vous qu'au moins une option d'expédition est toujours disponible
- **Surveillez les performances des zones** - Si nombreux clients voient "aucune expédition disponible", auditez la couverture des zones
- **Mettez à jour les zones pour de nouvelles régions** - Ajoutez des pays à la zone UE lorsqu' de nouveaux membres rejoignent
- **Utilisez des noms descriptifs** - "UE (Excluant le Royaume-Uni)" est meilleur que "Zone 3"
- **Testez avec des adresses réelles** - Utilisez les adresses réelles des clients pendant les tests, pas des adresses inventées

Souvenez-vous : Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques exactement comme indiqué dans les règles de préservation.