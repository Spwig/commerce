---
title: Import en masse de codes de réduction
---

L'assistant d'importation de codes de réduction vous permet de créer des centaines de codes de réduction en une seule fois en téléchargeant un fichier CSV ou XLSX. Cela est idéal lorsque vous avez des codes imprimés à l'avance, des codes de programmes de fidélité provenant d'un système tiers, ou simplement besoin de lancer une campagne importante sans ajouter chaque code manuellement.

![Liste de codes de réduction avec le bouton Importer](/static/core/admin/img/help/voucher-import/voucher-list-import-button.webp)

## Démarrer un import

Accédez à **Marketing > Codes de réduction** et cliquez sur le bouton **Importer** dans le coin supérieur droit de la page. Cela ouvre l'assistant d'importation en trois étapes.

## Étape 1 : Télécharger votre fichier et définir les paramètres par lot

![Formulaire de téléchargement d'import](/static/core/admin/img/help/voucher-import/import-upload.webp)

La première page comporte deux parties : le téléchargement du fichier et les paramètres de réduction par lot.

### Préparer votre fichier

Téléchargez un fichier `.csv` ou `.xlsx` d'une taille maximale de 5 Mo. Le fichier doit avoir une ligne d'en-tête comme première ligne. Le minimum requis est une seule colonne contenant les codes de réduction — toutes les autres colonnes sont optionnelles.

L'importateur reconnaît automatiquement les noms de colonnes courants. Si votre fichier utilise l'un des noms suivants, Spwig sélectionnera automatiquement la bonne correspondance sur la page suivante sans aucun clic supplémentaire :

| Votre nom de colonne | Correspond à |
|---------------------|-------------|
| `code`, `voucher_code`, `coupon_code`, `promo_code` | Code de réduction |
| `name`, `title`, `campaign` | Nom interne |
| `description`, `details`, `note` | Description destinée aux clients |
| `external_id`, `member_id`, `reference` | ID externe |

**Conseil :** Téléchargez d'abord le modèle XLSX (voir [Exporter les codes de réduction comme modèle](#exporting-vouchers-as-a-template) ci-dessous) — il utilise exactement les noms de colonnes que l'importateur attend, donc la correspondance des colonnes est automatique.

### Limites de fichier

- Taille maximale du fichier : **5 Mo**
- Nombre maximum de lignes par import : **5 000 codes**

### Définir les paramètres de réduction par lot

Chaque code du lot partagera les mêmes paramètres de réduction que vous configurez sur cette page. Remplissez les champs comme vous le feriez lors de la création d'un seul code de réduction :

**Section Réduction**

| Champ | Description |
|-------|-------------|
| **Type de réduction** | Pourcentage, Montant fixe ou Livraison gratuite |
| **Valeur de réduction** | Le pourcentage (0–100) ou le montant fixe à déduire |
| **Montant maximum de réduction** | Plafond optionnel pour les réductions en pourcentage (par exemple, plafonner une réduction de 20 % à 50 $) |
| **Portée d'application** | Panier entier, Produits spécifiques ou Catégories spécifiques |

**Section Validité**

| Champ | Description |
|-------|-------------|
| **Date de début** | Date à partir de laquelle les codes deviennent actifs (par défaut maintenant si laissée vide) |
| **Date de fin** | Date à laquelle les codes expirent (laissez vide pour aucune expiration) |
| **Jours de validité** | Alternative à la date de fin — les codes expirent après ce nombre de jours à partir de leur création |

**Section Limites d'utilisation**

| Champ | Description |
|-------|-------------|
| **Nombre maximum d'utilisations total** | Nombre total de redemptions autorisés pour tous les clients (vide = illimité) |
| **Nombre maximum d'utilisations par client** | Nombre de fois qu'un client peut utiliser tout code de ce lot |
| **Valeur minimale de commande** | Valeur minimale du panier requise avant que le code ne s'applique |

**Restrictions**

Cochez toute combinaison de :
- **Ne s'applique pas aux articles en promotion** — empêche le code de s'accumuler avec des produits déjà réduits
- **Ne peut pas être combiné avec d'autres codes de réduction** — empêche les clients d'utiliser deux codes sur le même commande
- **Ne peut pas être combiné avec des articles en promotion** — similaire à l'option ci-dessus mais ciblée sur les articles en prix promotionnel
- **Uniquement pour les nouveaux clients** — restreint le code aux clients sans commandes précédentes terminées
- **Actif immédiatement** — cochez cette case pour rendre les codes actifs dès leur importation

Lorsque vous êtes satisfait des paramètres, cliquez sur **Continuer vers l'aperçu**.

## Étape 2 : Mapper les colonnes et vérifier

![Page de mappage des colonnes et d'aperçu](/static/core/admin/img/help/voucher-import/import-preview.webp)

La page d'aperçu affiche quatre compteurs de résumé en haut :

- **Lignes analysées** — nombre total de lignes de données trouvées dans votre fichier

- **À importer** — nouveaux codes qui seront créés

- **Doublons** — codes qui existent déjà dans votre catalogue

- **À ignorer (invalides)** — lignes rejetées en raison d'erreurs de validation (code vide, code trop long, etc.)

### Mappage des colonnes

Le tableau **Mappage des colonnes** vous permet de préciser à Spwig quelle colonne de votre fichier correspond à chaque champ de coupon. Spwig détecte automatiquement les noms d'en-tête courants (voir le tableau ci-dessus), mais vous pouvez modifier tout mappage en utilisant le menu déroulant de chaque ligne.

Seule la colonne **Code de coupon** est obligatoire. Les autres champs — **Nom interne**, **Description destinée aux clients**, et **ID externe** — sont optionnels. Si vous les ignorez, Spwig utilise des valeurs par défaut sensibles (le nom interne par défaut est "Coupon importé {code}").

### Stratégie de gestion des codes en double

Si certains codes de votre fichier existent déjà dans votre catalogue, vous devez choisir comment les gérer :

| Stratégie | Ce qui se produit |

|----------|-------------|

| **Ignorer les doublons** | Les codes existants restent exactement tels quels. Seuls les nouveaux codes sont créés. |

| **Remplacer les paramètres** | Les codes existants sont mis à jour avec les paramètres de remise de ce lot. Leurs codes, les comptes d'utilisation et les dates de création sont conservés. |

| **Échouer l'importation** | L'importation entière est annulée si même un seul doublon est trouvé. Utilisez cette option lorsque vous avez besoin d'une garantie que les codes existants ne sont pas affectés. |

Les codes en double trouvés sont listés dans un panneau expansible afin que vous puissiez les consulter avant de prendre une décision.

### Tableau d'aperçu des données

Le bas de la page affiche les 20 premières lignes de votre fichier afin que vous puissiez confirmer que le mappage des colonnes semble correct avant de valider. Les lignes correspondant à des codes existants sont mises en surbrillance.

Lorsque tout semble correct, cliquez sur **Importer N coupons** pour valider le lot.

## Étape 3 : Vérifier le résultat

![Page de résultat de l'importation](/static/core/admin/img/help/voucher-import/import-result.webp)

Après la complétion de l'importation, vous verrez un résumé affichant :

- **Importés** — codes créés avec succès

- **Ignorés** — codes qui n'ont pas été créés (doublons ou lignes invalides)

- **Lignes traitées** — nombre total de lignes de votre fichier qui ont été évaluées

- **Échoués** — lignes qui ont rencontré une erreur inattendue

Cliquez sur **Voir les coupons importés** pour ouvrir la liste des coupons filtrée uniquement aux codes de ce lot, ce qui facilite la vérification du résultat ou l'activation en masse des nouveaux codes.

Si quelque chose semble incorrect — par exemple, le type de remise incorrect a été appliqué — vous pouvez utiliser la stratégie **Remplacer les paramètres** lors d'une nouvelle importation pour corriger le lot sans avoir à supprimer et recréer les codes.

Cliquez sur **Importer un autre lot** pour commencer un nouvel upload, ou sur **Retour à la liste des coupons** pour revenir à votre catalogue complet.

## Exporter les coupons comme un modèle

La liste des coupons prend en charge une action d'exportation XLSX qui génère un fichier dans le même ordre de colonnes que l'importateur s'attend. C'est la manière la plus simple d'obtenir un modèle correctement formaté :

1. Accédez à **Marketing > Coupons**

2. Sélectionnez les coupons que vous souhaitez exporter (ou sélectionnez tous)

3. Choisissez **Exporter les coupons sélectionnés vers XLSX** depuis le menu déroulant **Action**

4. Cliquez sur **Aller**

Le fichier téléchargé contient toutes les 21 colonnes que l'importateur comprend, y compris les champs qui sont au niveau du lot dans l'assistant d'importation (type de remise, dates, limites d'utilisation, etc.). Vous pouvez utiliser ce fichier comme référence ou faire un aller-retour de vos codes existants via un cycle d'édition → réimportation en utilisant la stratégie **Remplacer les paramètres**.

## Conseils

Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques.

- Téléchargez d'abord une exportation XLSX pour l'utiliser comme modèle — les noms des colonnes sont pré-formatés afin que le mappage automatique les reconnaisse sans aucun ajustement sur la page d'aperçu.
- Exécutez un petit lot de test de 5 à 10 codes avant d'importer des centaines pour vérifier que votre mappage des colonnes et les paramètres du lot sont corrects.
- Utilisez **Days valid** au lieu d'une date de fin fixe lorsque les codes seront distribués au fil du temps — la date d'expiration de chaque code commence alors à partir de la date d'importation et non d'une date du calendrier unique.
- Si vous recevez des codes d'un système de fidélité tiers, mappez la référence de membre ou de client du fournisseur à la colonne **External ID** afin de pouvoir réconcilier les rédemptions plus tard.
- Après un grand import, cliquez sur **View imported vouchers** sur la page des résultats pour filtrer la liste uniquement au nouveau lot — vous pouvez ensuite modifier en masse, activer ou désactiver les codes en groupe.
- Un import échoué (en utilisant la stratégie de duplication **Fail**) ne modifie pas votre catalogue, il est donc sûr de corriger le fichier et de réessayer autant de fois que nécessaire.