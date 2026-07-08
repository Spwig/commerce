---
title: Colis de livraison
---

# Colis de livraison

Les colis de livraison définissent des tailles prédéfinies de boîtes et d'enveloppes pour le calcul des tarifs et l'emballage automatique – spécifiez les dimensions internes (espace utilisable), l'épaisseur des parois (dimensions externes pour les API des transporteurs), les limites de poids et le coût d'emballage. Les transporteurs utilisent les dimensions externes pour calculer le poids dimensionnel afin d'obtenir des devis de tarifs précis. Les colis ont un ordre de priorité pour les algorithmes d'emballage automatique qui sélectionnent automatiquement des combinaisons optimales de colis pour correspondre aux articles du panier.

Configurez les colis lors de l'utilisation des API des transporteurs pour les tarifs en temps réel ou lorsque vous avez besoin de calculs précis du poids dimensionnel.

## Configuration des emballages

Chaque colis définit :

**Dimensions**:
- **Longueur intérieure** : Espace utilisable à l'intérieur (cm)
- **Largeur intérieure** : Espace utilisable à l'intérieur (cm)
- **Hauteur intérieure** : Espace utilisable à l'intérieur (cm)
- **Épaisseur des parois** : Épaisseur du matériau d'emballage (cm)

**Dimensions externes** (calculées automatiquement):
```
Longueur extérieure = Longueur intérieure + (2 × Épaisseur des parois)
Largeur extérieure = Largeur intérieure + (2 × Épaisseur des parois)
Hauteur extérieure = Hauteur intérieure + (2 × Épaisseur des parois)
```

**Poids & Coût**:
- **Poids net** : Poids du colis vide (grammes)
- **Poids maximal** : Capacité maximale de charge (grammes)
- **Coût** : Coût du matériau d'emballage (pour l'optimisation des coûts)

**Propriétés**:
- **Nom** : Identifiant du colis (ex. : "Petite boîte", "Grande enveloppe")
- **Type** : Boîte ou Enveloppe
- **Priorité** : Ordre de sélection d'emballage automatique (plus bas = plus haute priorité)
- **Actif** : Basculer la disponibilité

---

## Pourquoi les dimensions externes comptent

Les transporteurs calculent le **poids dimensionnel** à partir des dimensions externes :

**Formule du poids dimensionnel**:
```
Poids dimensionnel = (Longueur × Largeur × Hauteur) / Diviseur

Diviseurs courants:
- DHL : 5000
- FedEx/UPS : 5000 (national), 6000 (international)
```

**Exemple**:
```
Petite boîte:
Intérieur : 20cm × 15cm × 10cm
Épaisseur des parois : 0,5cm
Extérieur : 21cm × 16cm × 11cm

Poids dimensionnel = (21 × 16 × 11) / 5000 = 0,74kg

Si le poids réel = 0,5kg → Le transporteur facture à 0,74kg (poids dimensionnel plus élevé)
```

**Pourquoi la précision compte** : Dimensions inexactes → devis de tarifs incorrects → client facturé trop cher ou trop peu.

---

## Tailles d'emballages courantes

### Petite enveloppe rembourrée

```
Intérieur : 25cm × 18cm × 2cm
Épaisseur des parois : 0,3cm
Poids maximal : 500g
Type : Enveloppe
Utilisation : Documents, livres, bijoux
```

### Petite boîte

```
Intérieur : 20cm × 15cm × 10cm
Épaisseur des parois : 0,5cm
Poids maximal : 5kg
Type : Boîte
Utilisation : Petits appareils électroniques, cosmétiques, accessoires
```

### Moyenne boîte

```
Intérieur : 30cm × 25cm × 20cm
Épaisseur des parois : 0,5cm
Poids maximal : 15kg
Type : Boîte
Utilisation : Vêtements, chaussures, articles de cuisine
```

### Grande boîte

```
Intérieur : 45cm × 35cm × 30cm
Épaisseur des parois : 0,6cm
Poids maximal : 30kg
Type : Boîte
Utilisation : Articles en vrac, plusieurs produits, grands appareils électroniques
```

---

## Algorithme d'emballage automatique

Le système sélectionne automatiquement les colis pour les articles du panier :

**Fonctionnement**:
1. Calculer le volume total des articles du panier
2. Trier les colis par priorité (numéro le plus bas en premier)
3. Essayer de placer les articles dans un seul colis
4. Si cela ne marche pas, essayer la taille de colis suivante
5. Si aucun colis ne convient, combiner plusieurs colis
6. Optimiser en fonction du paramètre `optimize_for`

**Modes d'optimisation**:
- **Coût** : Minimiser le coût d'emballage
- **Volume** : Minimiser l'espace perdu
- **Nombre** : Minimiser le nombre de colis

**Exemple**:
```
Articles du panier:
- Article A : 10cm × 8cm × 5cm, 200g
- Article B : 15cm × 12cm × 8cm, 400g

Colis (par priorité):
1. Petite boîte (20×15×10, priorité=1)
2. Moyenne boîte (30×25×20, priorité=2)

Algorithme:
Essayer Petite boîte : Les deux articles tiennent
Résultat : 1× Petite boîte (optimisé pour le nombre)
```

---

## Priorité des colis

**La priorité détermine l'ordre d'emballage**:

Priorité 1 (la plus haute) : Les petits colis sont essayés en premier
Priorité 10 : Les grands colis sont utilisés en dernier recours

**Stratégie**:
- Petits colis = numéros de priorité bas (1-3)
- Moyens colis = priorité moyenne (4-6)
- Grands colis = numéros de priorité élevés (7-10)

**Pourquoi** : Commencer par le plus petit colis, augmenter si nécessaire → minimise les coûts de livraison.

---

## Précision de l'épaisseur des parois

Mesurez l'emballage réel : 

**Comment mesurer**:
1. Prenez une boîte vide
2. Mesurez les dimensions intérieures (intérieures)
3. Mesurez les dimensions extérieures (extérieures)
4. Calculer : `(Extérieur - Intérieur) / 2 = Épaisseur des parois`

**Exemple**:
```
Largeur intérieure : 20cm
Largeur extérieure : 21cm
Épaisseur des parois : (21 - 20) / 2 = 0,5cm
```

**Épaisseurs courantes**:
- Enveloppe rembourrée : 0,2-0,4cm
- Carton à paroi simple : 0,4-0,6cm
- Carton à paroi double : 0,8-1,0cm

---

## Création d'un emballage prédéfini

**Étapes à suivre**:

1. **Paramètres > Livraison > Colis de livraison**
2. Cliquez sur "Ajouter un colis de livraison"
3. Entrez un nom (ex. : "Moyenne boîte")
4. Sélectionnez le type (Boîte ou Enveloppe)
5. Entrez les dimensions intérieures (L × W × H en cm)
6. Entrez l'épaisseur des parois (cm)
7. Le système calcule automatiquement les dimensions externes
8. Entrez le poids net (poids du colis vide en grammes)
9. Entrez le poids maximal (capacité de charge en grammes)
10. Optionnel : Entrez le coût (pour l'optimisation des coûts)
11. Définissez la priorité (1-10)
12. Activez = Oui
13. Enregistrer

---

## Test de sélection des colis

**Test manuel**:
1. Ajoutez des produits au panier de test
2. Procédez au paiement
3. Sélectionnez une méthode de livraison en temps réel (utilise les colis)
4. Vérifiez que le devis de tarif est raisonnable
5. Vérifiez la réponse du transporteur (les logs API montrent les colis sélectionnés)

**Prévisualisation d'emballage automatique**:
- Certains comptes de fournisseurs de livraison affichent la décomposition des colis
- Vérifiez quels colis ont été sélectionnés pour le panier
- Vérifiez l'emballage optimal

---

## Conseils

- **Mesurez précisément** - Dimensions inexactes → tarifs des transporteurs incorrects
- **Incluez l'épaisseur des parois** - Critique pour le poids dimensionnel
- **Commencez par 3-4 tailles** - Petites, moyennes, grandes couvrent la plupart des cas
- **Définissez des poids max réalistes** - Capacité de la boîte, pas une limite théorique
- **Utilisez la priorité avec soin** - Petites boîtes priorité 1, grandes boîtes priorité 10
- **Testez avec des produits réels** - Vérifiez que l'emballage automatique sélectionne les bonnes tailles
- **Mettez à jour lors du changement d'emballage** - Nouveau fournisseur = ré-mesurer les dimensions
- **Tenez compte des articles spéciaux** - Les articles fragiles peuvent nécessiter des tailles de boîte spécifiques
- **Gardez les emballages actifs au minimum** - Trop d'options ralentissent l'algorithme d'emballage automatique
- **Documentez l'emballage** - Notez quels produits correspondent à quels emballages
