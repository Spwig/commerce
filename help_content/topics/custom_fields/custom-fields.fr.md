---
title: Champs personnalisés
---

Les champs personnalisés vous permettent d'ajouter des données supplémentaires aux Produits, Catégories, Commandes et Profils clients sans modifier tout code. Utilisez-les pour stocker des informations spécifiques à votre entreprise, telles que des identifiants d'API externes, des emplacements de entrepôt, des données de conformité ou tout attribut que votre magasin nécessite.

## Accès aux Champs Personnalisés

Accédez à **Paramètres > Champs personnalisés** dans le menu latéral d'administration.

![Page des champs personnalisés](/static/core/admin/img/help/custom-fields/custom-fields-page.webp)

## Concepts Clés

### Groupes de Champs

Les champs sont organisés en **groupes** — des collections logiques qui apparaissent ensemble en tant que section. Par exemple, un groupe « Informations d'expédition » pourrait contenir des champs pour l'emplacement de l'entrepôt, les dimensions du colis et la classification hazmat.

### Définitions de Champ

Chaque définition de champ contrôle :
- **Nom** : L'étiquette affichée dans les formulaires
- **Slug** : La clé lisible par machine utilisée dans le stockage JSON et les réponses API
- **Type de champ** : Le type d'entrée rendu (texte, nombre, liste déroulante, etc.)
- **Validation** : Des règles comme min/max, longueur maximale, regex ou choix autorisés
- **Visibilité** : Si le champ s'affiche sur le site de vente

### Types de Champ Pris en Charge

| Type | Description | Utilisation typique |
|------|-------------|-------------|
| **Texte** | Champ de texte à une seule ligne | Identifiant d'API externe, code de marque |
| **Zone de texte** | Texte à plusieurs lignes | Notes de traitement particulier |
| **Nombre** | Valeurs entières | Quantité minimale de commande |
| **Décimal** | Valeurs décimales | Poids à remplacer, dimension personnalisée |
| **Oui/Non** | Case à cocher | Est fragile, nécessite une signature |
| **Date** | Sélecteur de date | Date de sortie, date d'expiration |
| **Date et heure** | Sélecteur de date et d'heure | Disponibilité planifiée |
| **URL** | Adresse web | Lien du fournisseur, URL de fiche technique |
| **Email** | Adresse e-mail | Contact du fabricant |
| **Liste déroulante** | Liste à choix unique | Type de matériau, pays d'origine |
| **Liste à choix multiples** | Liste à choix multiples | Certifications, balises |
| **Couleur** | Sélecteur de couleur | Couleur de marque, couleur d'étiquette |

## Gestion des Champs Personnalisés

### Création d'un Groupe de Champ

1. Ouvrez **Paramètres > Champs personnalisés**
2. Sélectionnez l'onglet modèle (Produits, Catégories, Commandes ou Profils clients)
3. Cliquez sur **Ajouter un groupe**
4. Entrez un **Nom de groupe** (par exemple, « Intégrations externes »)
5. Activez **Afficher sur le site de vente** si les clients doivent voir ces champs
6. Cliquez sur **Enregistrer le groupe**

### Ajout d'un Champ à un Groupe

1. Sur la carte du groupe, cliquez sur **Ajouter un champ**
2. Entrez un **Nom de champ** — le slug est généré automatiquement
3. Choisissez le **Type de champ**
4. Définissez éventuellement un **Texte d'aide** et une **Valeur par défaut**
5. Configurez les options de validation (varient selon le type de champ) :
   - Texte : longueur maximale, motif regex
   - Nombre/Décimal : valeurs minimales et maximales
   - Liste déroulante : définir la liste des choix
6. Définissez les options du champ :
   - **Obligatoire** : Les commerçants doivent remplir ce champ lors de l'enregistrement
   - **Afficher sur le site de vente** : Afficher la valeur sur la page destinée aux clients
   - **Traduisible** : Permettre la traduction de la valeur (texte/zone de texte uniquement)
7. Cliquez sur **Enregistrer le champ**

### Édition et Réorganisation

- Cliquez sur l'**icône de crayon** de tout groupe ou champ pour l'éditer
- Faites glisser la **poignée de prise** pour réorganiser les groupes ou les champs au sein d'un groupe
- Les modifications prennent effet immédiatement sur tous les formulaires pertinents

### Suppression de Groupes et de Champs

- Cliquez sur l'**icône de corbeille** d'un groupe ou d'un champ pour le supprimer
- Les suppressions sont des **suppressions douces** — les données sont conservées dans la base de données mais masquées des formulaires
- Cela protège les données existantes contre la perte accidentelle

## Utilisation des Champs Personnalisés dans les Formulaires

Une fois que vous avez défini des champs personnalisés pour un modèle, un onglet **Champs personnalisés** apparaît automatiquement sur le formulaire d'édition correspondant.

### Produits et Catégories

1. Ouvrez tout produit ou catégorie pour l'édition
2. Cliquez sur l'onglet **Champs personnalisés**
3. Remplissez les champs selon vos besoins
4. Cliquez sur **Enregistrer** — les valeurs sont stockées avec l'enregistrement

### Commandes

Les valeurs des champs personnalisés des commandes s'affichent comme une **section en lecture seule** sur la page des détails de la commande. Les champs personnalisés des commandes sont généralement définis via l'API ou à la caisse.

### Profils clients

1. Ouvrez un profil client
2. Cliquez sur l'onglet **Champs personnalisés**
3. Remplissez les champs et enregistrez-les

## Accès API

### Liste des Définitions de Champ

Récupérez toutes les définitions de champs personnalisés pour un modèle :

```
GET /api/custom-fields/definitions/?model=product&app=catalog
```

**Réponse :**
```json
[
  {
    "id": 1,
    "name": "External API ID",
    "slug": "external_api_id",
    "field_type": "text",
    "is_required": false,
    "group": { "name": "External Integrations" }
  }
]
```

### Lire les Valeurs des Champs Personnalisés

Les valeurs des champs personnalisés sont incluses dans l'objet JSON `custom_fields` sur les réponses API des modèles :

```json
{
  "id": 42,
  "name": "Blue Widget",
  "custom_fields": {
    "external_api_id": "API-12345",
    "is_fragile": true
  }
}
```

### Écrire les Valeurs des Champs Personnalisés

Incluez `custom_fields` lors de la création ou de la mise à jour d'un enregistrement via l'API :

```json
{
  "custom_fields": {
    "external_api_id": "API-67890",
    "warehouse_location": "WH-A3"
  }
}
```

Les valeurs sont validées selon les définitions de champ. Les valeurs invalides renvoient une erreur `400` avec des détails.

### Interroger par des Champs Personnalisés

Les champs personnalisés sont indexés pour des requêtes rapides de la base de données. Filtrez les enregistrements en utilisant des filtres de requête de base de données :

```
GET /api/products/?custom_fields__warehouse_location=WH-A3
```

## Affichage sur le Site de Vente

### Pour les Développeurs de Thèmes

Utilisez le tag de modèle `render_custom_fields` pour afficher les champs personnalisés sur le site de vente :

```python
{% load custom_fields_tags %}

{# Afficher tous les champs visibles sur le site de vente #}
{% render_custom_fields product %}

{# Obtenir une valeur de champ spécifique #}
{% get_custom_field product "warehouse_location" as location %}
<p>Expédié depuis : {{ location }}</p>
```

Seuls les champs ayant **Afficher sur le site de vente** activé à la fois au niveau du groupe et du champ seront rendus.

## Bonnes Pratiques

- **Utilisez des noms descriptifs** — les noms de champ apparaissent dans les formulaires et sur le site de vente
- **Définissez un texte d'aide** — guidez les commerçants sur ce qu'ils doivent entrer dans chaque champ
- **Groupez les champs liés** — maintenez les formulaires organisés et intuitifs
- **Utilisez des valeurs par défaut** — réduisez l'entrée de données en définissant des valeurs sensibles
- **Soyez sélectif concernant la visibilité sur le site de vente** — n'affichez que les champs qui ont un sens pour les clients
- **Utilisez des slugs dans les intégrations** — les slugs sont des identifiants stables ; les noms de champ peuvent changer

## Dépannage

**L'onglet Champs Personnalisés ne s'affiche pas :**
- Vérifiez qu'au moins un groupe de champ actif existe pour ce modèle
- Vérifiez que la classe d'administration inclut le `CustomFieldsAdminMixin`
- Nettoyez le cache et actualisez la page

**Les valeurs des champs ne s'enregistrent pas :**
- Assurez-vous que les champs obligatoires sont remplis
- Vérifiez les règles de validation (min/max, motifs regex, choix autorisés)
- Vérifiez que le champ est actif et non supprimé de manière douce

**L'API renvoie des custom_fields vides :**
- Confirmez que le modèle a le `CustomFieldsMixin`
- Vérifiez que les définitions de champ existent pour le type de contenu correct
- Assurez-vous que le sérialiseur inclut le `CustomFieldsSerializerMixin`

## Sujets Liés

- [Ajout de Produits](#)
- [Paramètres du Magasin](#)