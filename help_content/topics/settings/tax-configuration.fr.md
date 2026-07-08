---
title: Configuration des taxes
---

Les taux de taxes définissent les taxes sur les ventes, la TVA et autres taxes de consommation appliquées à la caisse en fonction de l'emplacement du client et du type de produit — configurez des taux au niveau du pays/état/ville avec des exemptions éventuelles par catégorie de produit. Spwig prend en charge les taxes composées (taxe sur taxe), la sélection de taux basée sur la priorité et des groupes de paramètres de taxes prédéfinis pour un réglage rapide des systèmes fiscaux régionaux (TVA de l'UE, TVA des États-Unis). Les taux peuvent exempter certains types de produits (nourriture, livres, biens numériques) ou des catégories pour se conformer aux lois fiscales locales.

Utilisez la configuration des taxes pour garantir la conformité légale aux exigences de collecte des taxes dans vos juridictions de vente.

## Configuration des taux de taxes

Chaque taux de taxe définit :

**Portée géographique**:
- Pays (obligatoire)
- État/Province (facultatif)
- Ville (facultatif)
- Modèle de code postal (facultatif, regex)

**Détails du taux**:
- **Taux de taxe** : Pourcentage (ex. 8,5 %)
- **Nom** : Nom d'affichage (ex. « Taxe sur les ventes de Californie »)
- **Priorité** : La priorité la plus élevée gagne lorsqu'il y a plusieurs taux correspondants
- **Actif** : Basculer sans suppression

**Exemptions**:
- **Types de produits exonérés** : Biens numériques, biens physiques, services
- **Catégories exonérées** : Catégories de produits spécifiques (Nourriture, Livres, Médecine)

**Taxe composée**:
- **Est composée** : Appliquez ce taux sur les taxes précédentes (taxe sur taxe)
- Exemple : La PST du Québec s'applique sur la TVA

---

## Scénarios fiscaux courants

### TVA des États-Unis (niveau État)

```
Nom : Taxe sur les ventes de Californie
Pays : États-Unis
État : CA
Taux : 7,25 %
Priorité : 50
```

### TVA de l'UE (niveau pays)

```
Nom : TVA du Royaume-Uni
Pays : GB
Taux : 20 %
Priorité : 50

Nom : TVA allemande
Pays : DE
Taux : 19 %
Priorité : 50
```

### TVA canadienne (GST/PST composée)

```
Taux 1 : TVA fédérale
Pays : CA
Taux : 5 %
Priorité : 100
Est composée : Non

Taux 2 : PST du Québec
Pays : CA
État : QC
Taux : 9,975 %
Priorité : 50
Est composée : Oui  (s'applique au sous-total + TVA)
```

### Taxe au niveau de la ville

```
Nom : Taxe sur les ventes de Seattle
Pays : États-Unis
État : WA
Ville : Seattle
Taux : 10,1 %
Priorité : 100
```

---

## Exonérations fiscales

### Exonérations par type de produit

Exonérer des types de produits entiers :

- **Biens numériques** : Logiciels, e-books, musique
- **Biens physiques** : Produits tangibles
- **Services** : Conseil, installation

Exemple : La TVA de l'UE ne s'applique pas aux biens numériques pour les consommateurs (dans certains cas)

### Exonérations par catégorie

Exonérer des catégories de produits spécifiques :

- Nourriture et épicerie (souvent exonérée ou taux réduit)
- Livres et matériel pédagogique
- Produits médicaux et médicaments
- Vêtements (certaines juridictions)

Configuration : 
```
Nom : Taxe sur les ventes de Californie
Taux : 7,25 %
Catégories exonérées : ["Nourriture et boissons", "Médicaments sur ordonnance"]
```

---

## Groupes de paramètres de taxes prédéfinis

Charger rapidement des configurations de taxes courantes : 

**Prédéfini de TVA des États-Unis** : 
- Tous les 50 États + DC
- Taux au niveau État
- Mises à jour automatiques lors des changements de taux

**Prédéfini de TVA de l'UE** : 
- Tous les 27 États membres de l'UE
- Taux standard de TVA
- Logique de recouvrement inverse pour les B2B

**Pour utiliser les paramètres prédéfinis** : 
1. Paramètres > Panier > Paramètres de taxes
2. Sélectionner le groupe de paramètres prédéfinis (ex. « TVA des États-Unis 2026 »)
3. Cliquez sur « Charger le paramètre prédéfini »
4. Les taux sont importés automatiquement
5. Personnaliser si nécessaire

---

## Résolution des priorités

Lorsque plusieurs taux correspondent, la priorité la plus élevée s'applique : 

Exemple : 
```
Client à Seattle, WA : 

Taux A : Fédéral des États-Unis (Priorité 1) - 0 %
Taux B : État de Washington (Priorité 50) - 6,5 %
Taux C : Ville de Seattle (Priorité 100) - 3,6 %

Résultat : Taux de Seattle (10,1 % au total) s'applique
```

---

## Options d'affichage des taxes

Configurez dans Paramètres > Panier > Paramètres des taxes : 

- **Les prix incluent la taxe** : Afficher les prix avec la taxe incluse (style UE)
- **Afficher la taxe séparément** : Afficher la taxe comme élément de ligne (style US)
- **Arrondir la taxe** : Par article ou par commande
- **Libellé de la taxe** : Personnaliser l'étiquette (« TVA », « Taxe sur les ventes », « TVA fédérale »)

---

## Test de la configuration fiscale

Avant de lancer : 

1. Créer des commandes de test provenant de différentes juridictions
2. Vérifier que le taux de taxe correct est appliqué
3. Vérifier que les exemptions fonctionnent pour les catégories exclues
4. Tester le calcul de la taxe composée
5. Vérifier les éléments de taxe sur les factures

---

## Notes de conformité

- **États-Unis** : Les règles de nexus exigent la collecte de taxes dans les États où vous avez une présence physique ou un nexus économique
- **UE** : Les entreprises inscrites à la TVA doivent collecter la TVA auprès des clients de l'UE
- **Canada** : La TVA/HST/PST varie selon la province
- **Consulter un expert fiscal** : Les lois fiscales changent fréquemment, vérifier les exigences actuelles

---

## Conseils

- **Utilisez les paramètres fiscaux prédéfinis** - Plus rapide que l'entrée manuelle, mise à jour automatique
- **Surveillez les seuils de nexus** - Suivez les ventes par État pour le nexus économique des États-Unis
- **Définissez correctement la priorité** - Ville > État > Pays
- **Testez la taxe composée** - Vérifiez que les calculs correspondent aux montants attendus
- **Mettez à jour annuellement** - Les taux de taxes changent, relisez chaque janvier
- **Documentez les exemptions** - Conservez des registres des raisons pour lesquelles les catégories sont exemptées
- **Utilisez des noms descriptifs** - « Taxe sur les ventes de Californie 2026 » est meilleur que « Taxe 1 »
- **Activez la taxe par défaut** - Plus sûr que d'oublier d'appliquer la taxe

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.