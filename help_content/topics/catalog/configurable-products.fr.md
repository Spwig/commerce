---
title: "Produits Configurables"
---

Les produits configurables permettent aux clients de construire leur propre produit en choisissant des options parmi differents emplacements de configuration. C'est ideal pour les articles fabriques sur commande comme les PC sur mesure, les coffrets cadeaux personnalises ou les meubles sur mesure ou chaque composant est un produit reel de votre catalogue.

![Product configurator admin](/static/core/admin/img/help/configurable-products/product-configurator.webp)

## Comment ca Fonctionne

Un produit configurable est compose d'**emplacements** (categories de choix) et d'**options** (les produits reels que les clients peuvent choisir). Par exemple, un PC sur mesure pourrait avoir des emplacements pour Processeur, Carte Graphique, RAM et Stockage — chaque emplacement contenant plusieurs options de produit parmi lesquelles choisir.

## Strategies de Tarification

Choisissez comment le prix final est calcule :

| Strategie | Description |
|-----------|-------------|
| **Somme des Composants** | Prix final = total de tous les prix des options selectionnees. Pas de prix de base necessaire. |
| **Prix de Base + Ajustements** | Commencez avec le prix de base du produit, puis ajoutez/soustrayez des ajustements de prix par option. |
| **Prix Fixe** | Un prix unique quel que soit les options selectionnees par le client. |

## Configuration d'un Produit Configurable

### Etape 1 : Creer le Produit

1. Naviguez vers **Produits > Tous les Produits** et cliquez sur **+ Ajouter un Produit**
2. Definissez le **Type de Produit** sur **Produit Configurable**
3. Choisissez votre **Strategie de Tarification** (Somme des Composants est la plus courante)
4. Remplissez le nom du produit, la description et les autres details de base
5. Enregistrez le produit

### Etape 2 : Ajouter des Emplacements de Configuration

Apres l'enregistrement, basculez vers l'onglet **Configuration** pour configurer vos emplacements.

1. Cliquez sur **+ Ajouter un Emplacement** pour creer une nouvelle categorie de configuration
2. Pour chaque emplacement, configurez :
   - **Nom** — Ce que le client voit (ex., "Processeur", "Couleur")
   - **Icone** — Classe d'icone Font Awesome pour l'identification visuelle
   - **Obligatoire** — Si le client doit faire une selection
   - **Selections Min/Max** — Combien d'options le client peut choisir (par defaut : exactement 1)
   - **Ordre de Tri** — Controle l'ordre dans lequel les emplacements apparaissent dans l'assistant de configuration

### Etape 3 : Ajouter des Options a Chaque Emplacement

Chaque emplacement a besoin d'options de produit pour que les clients choisissent :

1. Cliquez sur **Gerer les Options** sur un emplacement
2. Recherchez et ajoutez des produits existants de votre catalogue
3. Pour chaque option, configurez :
   - **Ajustement de Prix** — Montant a ajouter ou soustraire (utilise avec la tarification Prix de Base + Ajustements)
   - **Par Defaut** — Preselectionner cette option lorsque le configurateur se charge
   - **Populaire** — Afficher un badge "Populaire" pour aider les clients a decider
   - **Quantite** — Combien d'unites de ce composant sont incluses
   - **Tags de Compatibilite** — Tags utilises pour la generation par lot de regles de compatibilite

**Conseil :** Les produits composants peuvent etre masques de la vitrine en cochant **Masquer de la Vitrine** dans l'onglet Informations de Base du produit composant. Cela les garde disponibles comme options du configurateur sans encombrer votre catalogue de produits.

### Etape 4 : Definir les Regles de Compatibilite

Les regles de compatibilite empechent les clients de selectionner des combinaisons incompatibles :

| Type de Regle | Description |
|---------------|-------------|
| **Requiert** | Lorsque l'option A est selectionnee, seules les options listees sont disponibles dans l'emplacement cible |
| **Exclut** | Lorsque l'option A est selectionnee, les options listees sont masquees de l'emplacement cible |

Pour ajouter des regles :

1. Faites defiler jusqu'a la section **Regles de Compatibilite** dans l'onglet Configuration
2. Cliquez sur **+ Ajouter une Regle**
3. Selectionnez l'**option source** (le declencheur)
4. Choisissez le **type de regle** (Requiert ou Exclut)
5. Selectionnez l'**emplacement cible** et les **options affectees**

Vous pouvez egalement generer automatiquement des regles a partir des tags de compatibilite assignes aux options, ce qui est plus rapide lorsque vous gerez de nombreuses combinaisons.

### Etape 5 : Creer des Preselections (Optionnel)

Les preselections sont des configurations pre-construites qui offrent aux clients un point de depart rapide :

1. Faites defiler jusqu'a la section **Preselections de Configuration**
2. Cliquez sur **+ Ajouter une Preselection**
3. Donnez a la preselection un nom et une description (ex., "Build Gaming", "Starter Budget")
4. Selectionnez les options pour chaque emplacement
5. Telechargez optionnellement une image d'apercu et marquez-la comme **En Vedette**

Les clients peuvent commencer a partir d'une preselection puis personnaliser les emplacements individuels selon leurs preferences.

## Experience Client

Lorsqu'un client consulte un produit configurable sur votre vitrine :

1. **Interface d'Assistant** — Les emplacements sont presentes comme des etapes, guidant le client a travers chaque choix
2. **Filtrage** — Les options incompatibles sont automatiquement masquees selon les regles de compatibilite
3. **Badges Populaire** — Les options marquees comme populaires affichent un badge pour faciliter la prise de decision
4. **Preselections** — Les preselections en vedette apparaissent comme options de demarrage rapide
5. **Mises a Jour du Prix** — Le prix total se met a jour en temps reel a mesure que les options sont selectionnees
6. **Resume** — Une etape de revision montre toutes les options selectionnees avant l'ajout au panier

## Conseils

- Commencez avec la strategie de tarification "Somme des Composants" — c'est la plus intuitive pour les clients et la plus facile a maintenir.
- Utilisez les regles de compatibilite pour empecher les configurations invalides plutot que de vous fier aux connaissances du client.
- Creez 2-3 preselections pour vos configurations les plus populaires afin de reduire la fatigue decisionnelle.
- Masquez les produits composants de la vitrine s'ils ne doivent etre disponibles qu'a travers le configurateur.
- Testez le flux complet de configuration sur le frontend apres la mise en place pour vous assurer que toutes les regles fonctionnent comme prevu.
