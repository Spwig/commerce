---
title: Zones de livraison
---

Les zones de livraison définissent des régions géographiques pour des tarifs de livraison ciblés – regroupez des pays, des états ou des codes postaux en zones, puis reliez des méthodes de livraison à des zones spécifiques pour un contrôle précis des tarifs. Les zones utilisent un système de correspondance basé sur la priorité lorsque les adresses correspondent à plusieurs zones (la zone avec la plus haute priorité gagne). Ce système permet des stratégies de tarification sophistiquées : facturer plus cher pour les zones reculées, offrir une livraison gratuite dans le pays, ou proposer des tarifs réduits pour des régions spécifiques.

Utilisez les zones lorsque vous avez besoin de coûts de livraison différents pour différentes zones géographiques, allant d'une simple distinction entre national et international à une tarification hiérarchisée complexe à plusieurs régions.

## Compréhension des zones de livraison

**Qu'est-ce qu'une zone** : Une région géographique nommée définie par des codes de pays, des états/provinces et des motifs de codes postaux.

**Fonctionnement des zones** : 
1. Le client saisit son adresse de livraison lors du paiement
2. Le système évalue toutes les zones actives
3. Les zones correspondant à l'adresse du client deviennent des candidats
4. Si plusieurs zones correspondent, la zone avec la plus haute priorité gagne
5. Les méthodes de livraison liées à la zone gagnante sont affichées
6. Les méthodes non liées à aucune zone (ou liées à une zone correspondante) sont affichées

**Composants d'une zone** : 
- **Nom** : Identifiant de la zone (ex. : "Domestique", "UE", "Zones reculées")
- **Pays** : Liste des codes de pays inclus (vide = tous les pays)
- **États/Provinces** : Restrictions d'état par pays (optionnel)
- **Motifs de codes postaux** : Motifs regex pour la correspondance des codes postaux (optionnel)
- **Priorité** : Un nombre plus élevé = une priorité plus élevée lorsqu'il y a plusieurs zones correspondantes


## Logique de correspondance des zones

Les zones utilisent une **réduction progressive** pour correspondre aux adresses : 

### Niveau 1 : Correspondance par pays

**Liste de pays vide** → La zone correspond à TOUS les pays

**Liste de pays fournie** → Le pays de l'adresse doit être dans la liste

Exemple : 
```
Zone : "Domestique"
Countries: ["US"]
→ Correspond : Toute adresse des États-Unis
→ Non correspond : Canada, Royaume-Uni, etc.
```

### Niveau 2 : Correspondance par état/province

**Aucun état défini** → La zone correspond à TOUS les états des pays autorisés

**États définis pour des pays spécifiques** → L'état de l'adresse doit correspondre

Exemple : 
```
Zone : "West Coast"
Countries: ["US"]
States: {"US": ["CA", "OR", "WA"]}
→ Correspond : Adresses de Californie, Oregon, Washington
→ Non correspond : New York, Texas, etc.
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
→ Non correspond : 94102 (San Francisco)
```

**Exemples de motifs regex** : 
- `^90[0-9]{3}$` - Zone de Los Angeles (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Format des codes postaux canadiens (K1A 0B1)
- `^SW[0-9]{1,2}` - Codes postaux du Royaume-Uni commençant par SW


## Sélection des zones basée sur la priorité

Lorsqu'une adresse correspond à plusieurs zones, la **priorité** détermine quelle zone s'applique : 

**Fonctionnement de la priorité** : 
- Un nombre plus élevé = une priorité plus élevée
- Si l'adresse correspond à des zones avec une priorité 100 et 50, la priorité 100 gagne
- Seules les méthodes de livraison de la zone gagnante sont disponibles

**Cas d'utilisation** : 

**Scénario 1 : Spécifique remplace général** 
```
Zone A : "Remote Alaska"
  Countries: ["US"]
  States: {"US": ["AK"]}
  Priority: 100

Zone B : "Domestic USA"
  Countries: ["US"]
  Priority: 50

Address: Anchorage, AK
→ Correspond à toutes les deux zones
→ Priorité 100 gagne
→ La zone "Remote Alaska" s'applique (coût de livraison plus élevé)
```

**Scénario 2 : Code postal remplace état** 
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
→ Correspond à toutes les deux zones
→ Priorité 100 gagne
→ "Manhattan Premium" s'applique (service de livraison premium)
```


## Création de zones de livraison

**Workflow étape par étape** : 

1. **Accédez aux zones**
   - Allez dans Paramètres > Livraison > Zones de livraison
   - Cliquez sur "Ajouter une zone de livraison"

2. **Configuration de base**
   - **Nom** : Identifiant descriptif (ex. : « Union européenne », « Côte Ouest », « Zones éloignées »)
   - **Priorité** : Définir l'importance relative (100 pour spécifique, 50 pour général, 1 pour la zone par défaut)
   - **Actif** : Activer/désactiver

3. **Définir la couverture géographique**

   **Option A : Tous les pays** (laisser la liste de pays vide)
   - La zone correspond à toutes les adresses à l'échelle mondiale
   - Utiliser pour les zones par défaut ou de secours

   **Option B : Pays spécifiques**
   - Cliquez sur « Ajouter un pays »
   - Sélectionnez les pays depuis le menu déroulant (US, CA, UK, etc.)
   - Répétez pour tous les pays inclus

   **Option C : États/Provinces spécifiques**
   - Après avoir ajouté les pays, cliquez sur « Ajouter des États » pour chaque pays
   - Sélectionnez les états depuis le menu déroulant
   - Exemple : US → CA, OR, WA pour la Côte Ouest

   **Option D : Modèles de codes postaux** (avancé)
   - Entrez des modèles regex (un par ligne)
   - Testez les modèles avec des codes postaux d'exemple
   - Cliquez sur « Valider les modèles » pour vérifier la syntaxe

4. **Lier aux méthodes d'expédition**
   - Les méthodes peuvent être liées lors de l'édition de la méthode (pas dans la configuration de la zone)
   - Ou liez les zones aux méthodes existantes : Éditer la Méthode → Zones d'expédition → Sélectionner les zones

5. **Définir la priorité d'affichage**
   - Les zones à plus haute priorité remplacent les zones à plus basse priorité lorsqu'il y a plusieurs correspondances
   - Recommandé : Zones spécifiques (100), Zones régionales (50), Zone par défaut (1)

6. **Activer la zone**
   - Activer « Actif » = Oui
   - Enregistrer

---

## Configurations de zones courantes

### Configuration 1 : National vs International

**Objectif** : Tarifs différents pour le national par rapport à tous les autres pays.

```
Zone 1 : « National »
  Pays : [Votre code de pays]
  Priorité : 50

Zone 2 : « International »
  Pays : [Laissez vide ou sélectionnez tous les autres pays]
  Priorité : 1
```

**Méthodes d'expédition** : 
- « Standard national » → Lien vers la zone nationale
- « Expédition internationale » → Lien vers la zone internationale

---

### Configuration 2 : Zones internationales multi-régionales

**Objectif** : Tarifs différents pour l'UE, l'Amérique du Nord, l'Asie et le reste du monde.

```
Zone 1 : « Union européenne »
  Pays : [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Priorité : 100

Zone 2 : « Amérique du Nord »
  Pays : [US, CA, MX]
  Priorité : 100

Zone 3 : « Asie-Pacifique »
  Pays : [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Priorité : 100

Zone 4 : « Reste du monde »
  Pays : [Laissez vide]
  Priorité : 1
```

**Méthodes d'expédition** : 
- « Expédition UE » → Zone UE
- « Expédition Amérique du Nord » → Zone Amérique du Nord
- « Expédition Asie-Pacifique » → Zone Asie-Pacifique
- « Standard international » → Zone Reste du monde

---

### Configuration 3 : Surcoût pour les zones éloignées

**Objectif** : Ajouter un surcoût pour les codes postaux éloignés dans la zone nationale.

```
Zone 1 : « Éloigné national »
  Pays : [US]
  Modèles postaux : [«^99[0-9]{3}$», «^96[7-9][0-9]{2}$»]  # Alaska, Hawaï
  Priorité : 100

Zone 2 : « National standard »
  Pays : [US]
  Priorité : 50
```

**Méthodes d'expédition** : 
- « Expédition éloignée » → Zone éloignée nationale (coût plus élevé)
- « Expédition standard » → Zone nationale standard

---

### Configuration 4 : Zones spécifiques par État

**Objectif** : Tarifs différents pour chaque région des États-Unis.

```
Zone 1 : « Côte Ouest »
  Pays : [US]
  États : {«US» : [«CA», «OR», «WA»]}
  Priorité : 100

Zone 2 : « Côte Est »
  Pays : [US]
  États : {«US» : [«NY», «NJ», «CT», «MA», «PA»]}
  Priorité : 100

Zone 3 : « Midwest »
  Pays : [US]
  États : {«US» : [«IL», «IN», «OH», «MI», «WI»]}
  Priorité : 100

Zone 4 : « Sud »
  Pays : [US]
  États : {«US» : [«TX», «FL», «GA», «NC», «SC»]}
  Priorité : 100

Zone 5 : « Autres États des États-Unis »
  Pays : [US]
  Priorité : 50
```

---

## Exemples de modèles de codes postaux

Les codes postaux utilisent **regex** (expressions régulières) pour le matching des modèles :

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


Tous les codes postaux canadiens :  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$",
  "Ontario (K, L, M, N, P) :    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$",
  "Quebec (G, H, J) :           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$",
  "### Royaume-Uni (Codes postaux)",
  "**Format** : AA1A 1AA ou A1A 1AA",
  "London (E, EC, N, NW, SE, SW, W, WC) :  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}",
  "Manchester (M) :                        ^M[0-9]{1,2}",
  "Birmingham (B) :                        ^B[0-9]{1,2}",
  "### Australie (Codes postaux)",
  "**Format** : 4 chiffres (ex. 2000)",
  "Nouvelle-Galles-du-Sud (1000-2999) :  ^[12][0-9]{3}$",
  "Victoria (3000-3999, 8000-8999) :  ^[38][0-9]{3}$",
  "Queensland (4000-4999, 9000-9999) :  ^[49][0-9]{3}$",
  "### Test des motifs",
  "**Avant d'enregistrer les motifs**, testez avec des codes postaux connus :",
  "1. Entrez le motif : `^90[0-9]{3}$`",
  "2. Entrée de test : "90210" → Doit correspondre",
  "3. Entrée de test : "10001" → Ne doit pas correspondre",
  "4. Entrée de test : "9021" → Ne doit pas correspondre (seulement 4 chiffres)",
  "Utilisez des testeurs de regex en ligne (regex101.com) pour valider les motifs complexes.",
  "---",
  "## Résumé de la couverture des zones",
  "Les zones affichent **résumé de la couverture** dans la vue de liste d'administration, montrant ce qui est inclus :",
  "**Exemples** :",
  "- "Tous les pays" → Aucune restriction de pays",
  "- "US, CA, MX" → 3 pays",
  "- "US (CA, OR, WA)" → États-Unis avec 3 états",
  "- "US (90xxx-91xxx)" → États-Unis avec des motifs de codes postaux",
  "**Utiliser le résumé pour** :",
  "- Vérifier rapidement la couverture des zones sans ouvrir",
  "- Identifier les chevauchements ou les lacunes dans la couverture",
  "- Auditer la configuration des zones d'un coup d'œil",
  "---",
  "## Liens des zones aux méthodes d'expédition",
  "Les zones et les méthodes ont **une relation many-to-many** :",
  "**À partir du côté Méthode** (Recommandé) :",
  "1. Modifier la méthode d'expédition",
  "2. Faire défiler jusqu'à la section "Zones d'expédition"",
  "3. Sélectionner les zones applicables (sélection multiple)",
  "4. Enregistrer la méthode",
  "**À partir du côté Zone** :",
  "- Les zones ne se lient pas directement aux méthodes",
  "- Le lien est toujours effectué depuis la configuration de la méthode",
  "**Comportement Méthode-Zone** :",
  "**Aucune zone liée** → Méthode disponible pour TOUS les adresses",
  "**Zones liées** → Méthode uniquement disponible si l'adresse du client correspond à au moins une zone liée",
  "**Exemple** :",
  "```,
  "Méthode : "Standard national"",
  "Zones liées : ["USA national"]",
  "→ Affichée uniquement aux adresses des États-Unis",
  "Méthode : "Express international"",
  "Zones liées : ["EU", "Asie-Pacifique", "Reste du monde"]",
  "→ Affichée à toutes les adresses non américaines",
  "```",
  "---",
  "## Test de correspondance des zones",
  "Avant de mettre en ligne, testez la configuration des zones :",
  "1. **Créer des commandes de test**",
  "- Utiliser des adresses dans différentes zones",
  "- Vérifier les correspondances de zones correctes",
  "2. **Vérifier la résolution de la priorité**",
  "- Utiliser une adresse qui correspond à plusieurs zones",
  "- Vérifier que la zone de plus haute priorité gagne",
  "- Confirmer l'apparition des méthodes d'expédition attendues",
  "3. **Tester les cas limites**",
  "- Codes postaux frontaliers (ex. 90999 vs 91000)",
  "- Limites de départements",
  "- Adresses internationales avec des codes postaux similaires",
  "4. **Utiliser l'outil de prévisualisation des zones** (si disponible)",
  "- Entrer une adresse de test",
  "- Voir quelles zones correspondent",
  "- Voir la résolution de la priorité",
  "---",
  "## Dépannage",
  "**Problème 1 : Aucune méthode d'expédition disponible à la caisse**",
  "**Causes** :",
  "- L'adresse du client ne correspond à aucune zone",
  "- Toutes les méthodes sont liées à des zones qui ne correspondent pas",
  "- Aucune méthode n'existe sans restrictions de zone",
  "**Solution** :",
  "- Créer une zone de secours (tous les pays, priorité 1)",
  "- OU supprimer les restrictions de zone d'au moins une méthode",
  "- Vérifier les motifs de pays/département/code postal des zones",
  "---",
  "**Problème 2 : Correspondance de zone incorrecte**",
  "**Causes** :",
  "- Une zone de priorité inférieure est sélectionnée malgré une zone de priorité supérieure qui correspond",
  "- Erreur de syntaxe dans le motif de code postal (le motif échoue silencieusement)",
  "- Mismatch des codes de département (CA vs California)",
  "**Solution** :",
  "- Vérifier les valeurs de priorité (plus grand nombre = plus haute priorité)",
  "- Tester les motifs de code postal avec un validateur de regex",
  "- Utiliser des codes de département à deux lettres (CA, pas California)",
  "---",
  "**Problème 3 : Méthode inattendue affichée**",
  "**Causes** :",
  "- La méthode n'a aucune zone liée (disponible partout)",
  "- Plusieurs zones correspondent, mais une zone inattendue a une priorité plus élevée",
  "- La couverture des zones chevauche accidentellement",
  "**Solution** :",
  "- Réviser les zones liées à la méthode",
  "- Vérifier la priorité des zones correspondantes",
  "- Auditer le résumé de la couverture des zones pour les chevauchements",
  "---",
  "## Conseils",
  "Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques.

- **Commencez avec 2 zones** - Nationale et Internationale, étendez si nécessaire
- **Utilisez la priorité avec soin** - Zones spécifiques 100, régionales 50, zone par défaut 1
- **Testez soigneusement les motifs postaux** - Les erreurs de regex échouent en silence, ce qui empêche les zones de correspondre
- **Documentez la logique des zones** - Ajoutez des notes à la description de la zone pour expliquer l'intention de couverture
- **Évitez un nombre excessif de zones** - Trop de zones complique la configuration ; utilisez des promotions d'expédition pour les scénarios complexes
- **Utilisez les codes des états, pas les noms** - "CA" et non "California", "NY" et non "New York"
- **Créez une zone par défaut** - Tous les pays, priorité 1, assure que toujours au moins une option d'expédition est disponible
- **Surveillez la performance des zones** - Si nombreux clients voient "aucune expédition disponible", auditez la couverture des zones
- **Mettez à jour les zones pour de nouvelles régions** - Ajoutez des pays à la zone UE lorsque de nouveaux membres rejoignent
- **Utilisez des noms descriptifs** - "UE (Excluant le Royaume-Uni)" est préférable à "Zone 3"
- **Testez avec des adresses réelles** - Utilisez les adresses réelles des clients lors des tests, et non des adresses inventées