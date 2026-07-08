---
title: Personnalisation des modèles de reçus
---

Les modèles de reçus contrôlent l'apparence et le contenu des reçus thermiques imprimés à vos terminaux de caisse. Personnalisez le texte d'en-tête et de pied de page, ajoutez votre logo, configurez les champs de conformité (numéros d'identification fiscale, numéros d'enregistrement commercial) et incluez des codes QR promotionnels. Les modèles prennent en charge la ciblage par portée - créez un modèle par défaut pour tous les magasins, des modèles spécifiques à un groupe pour les régions, ou des modèles spécifiques à un magasin pour des emplacements individuels. Le système utilise les règles de priorité des portées pour déterminer quel modèle s'applique lors de l'impression d'un reçu.

Utilisez les modèles de reçus pour maintenir la cohérence de la marque, respecter les exigences de conformité régionales et améliorer l'engagement des clients grâce à des éléments promotionnels.

![Liste des modèles de reçus](/static/core/admin/img/help/receipt-template-customization/receipt-list.webp)

## Principes de base des modèles de reçus

Les modèles de reçus définissent la structure et le contenu des reçus imprimés à partir d'imprimantes thermiques ESC/POS. Chaque modèle spécifie :

**Configuration physique**:
- Largeur du papier (58mm ou 80mm)
- Image du logo (en noir et blanc pour l'impression thermique)
- Taille et espacement des polices

**Sections de contenu**:
- Texte d'en-tête (nom du magasin, adresse, informations de contact)
- Données de transaction dynamiques (articles, prix, totaux, méthodes de paiement)
- Texte de pied de page (politique de retour, message de remerciement, réseaux sociaux)
- Champs de conformité (numéros d'identification fiscale, numéros d'enregistrement commercial)
- Code QR promotionnel avec étiquette

**Ciblage par portée**:
- Modèle par défaut (s'applique à tous les magasins sauf s'il est remplacé)
- Modèle de groupe (s'applique à tous les magasins d'un groupe)
- Modèle de magasin (s'applique à un magasin spécifique/entrepôt)

## Règles de priorité des portées

Lorsqu'un terminal imprime un reçu, le système sélectionne un modèle en utilisant cette hiérarchie (priorité la plus élevée à la plus basse) :

| Priorité | Portée | Exemple | Cas d'utilisation |
|----------|-------|---------|----------|
| **1** | Spécifique au magasin | Modèle du magasin de Paris | Exigences spécifiques de conformité fiscale en France |
| **2** | Spécifique au groupe | Modèle des magasins européens | Affichage de la TVA pour toutes les localisations de l'UE |
| **3** | Par défaut | Modèle global | Fallback pour tous les magasins non configurés |

**Fonctionnement**:
1. Vérifiez si le magasin a un modèle dédié (spécifique à l'entrepôt)
2. Si non, vérifiez si le groupe du magasin a un modèle de groupe
3. Si non, utilisez le modèle par défaut

**Exemple**:
- Modèle par défaut : "Reçu standard" (aucune attribution de portée)
- Modèle de groupe : "Reçu de l'UE" (attribué au groupe des magasins européens) - inclut l'enregistrement de la TVA
- Modèle de magasin : "Reçu de Paris" (attribué à l'entrepôt de Paris) - inclut le numéro SIRET français

**Résultat**:
- Terminal du magasin de Paris : Utilise "Reçu de Paris" (le plus spécifique)
- Terminal du magasin de Berlin (dans le groupe des magasins européens, aucun modèle de magasin) : Utilise "Reçu de l'UE" (niveau de groupe)
- Terminal du magasin de New York (aucun groupe, aucun modèle de magasin) : Utilise "Reçu standard" (fallback par défaut)

## Configuration de la largeur du papier

Les imprimantes thermiques de reçus utilisent soit une largeur de papier de 58mm soit de 80mm. Choisissez en fonction de votre matériel d'imprimante : 

| Largeur du papier | Caractères par ligne | Meilleur pour | Utilisation typique |
|------------------|---------------------|----------------|------------------|
| **58mm** | ~32 caractères | Petite empreinte, portable | Camions de nourriture, caisses enregistreuses mobiles, kiosques |
| **80mm** | ~48 caractères | Commerce standard | La plupart des magasins de détail, restaurants |

**Impossible de mélanger les largeurs** : Tous les terminaux utilisant le même modèle doivent avoir la même largeur d'imprimante. Si vous avez des types d'imprimantes mixtes, créez des modèles séparés pour chaque largeur.

**Limites de taille du logo** : 
- **58mm** : Largeur maximale 384 pixels (recommandé : 350px)
- **80mm** : Largeur maximale 576 pixels (recommandé : 550px)

Les logos dépassant la largeur maximale sont automatiquement réduits, ce qui peut réduire la qualité.

## Configuration du logo

Les logos de reçu doivent être **en noir et blanc** (uniquement noir et blanc) pour la compatibilité avec les imprimantes thermiques : 

**Exigences du logo** : 
- Format de fichier : PNG, JPG ou WebP
- Mode de couleur : Noir et blanc (pixels noirs sur fond blanc)
- Dimensions recommandées : 
  - Papier 58mm : 350px de largeur × 100-150px de hauteur
  - Papier 80mm : 550px de largeur × 150-200px de hauteur
- Taille du fichier : <100KB (les imprimantes thermiques ont une mémoire limitée)

**Création de logos en noir et blanc** : 
1. Commencez par votre logo régulier (en couleur ou en niveaux de gris)
2. Utilisez un éditeur d'images pour le convertir en noir et blanc pur (aucun gris)
3. Augmentez le contraste pour garantir que les éléments noirs sont solides
4. Exportez en tant que PNG avec fond transparent ou blanc

**Positionnement du logo** : 
- Toujours centré horizontalement
- Imprimé en haut du reçu (au-dessus du texte d'en-tête)
- Suivi d'un espace automatique (évite l'encombrement avec le contenu)

**Sélection du logo** : 
- Cliquez sur **Parcourir la bibliothèque multimédia** dans le formulaire de modèle
- Sélectionnez l'actif de logo en noir et blanc
- L'aperçu montre comment le logo apparaîtra sur le reçu

**Aucun logo** : Laissez le champ du logo vide si vous préférez une marque uniquement textuelle (le texte d'en-tête peut inclure le nom du magasin).

## Texte d'en-tête

Le texte d'en-tête apparaît immédiatement après le logo (ou en haut si aucun logo n'est présent). Contenu typique : 

**Nom du magasin et adresse** : 
```
Your Store Name
123 Main Street
City, State 12345
Phone: (555) 123-4567
```

**Heures d'ouverture** : 
```
Lundi-Vendredi : 9h-21h
Samedi-Dimanche : 10h-18h
```

**Slogan ou devise** : 
```
Produits de qualité, service exceptionnel
```

**Formatage** : 
- Utilisez des sauts de ligne pour séparer les informations
- Alignement au centre automatique
- Gardez les lignes sous la limite de caractères pour la largeur du papier (32 caractères pour 58mm, 48 pour 80mm)

**Variables disponibles** (optionnel) : 
- `{store_name}` - Remplacé par le nom de l'entrepôt
- `{order_date}` - Remplacé par la date de la transaction
- `{order_number}` - Remplacé par l'ID de commande

La plupart des commerçants utilisent du texte statique plutôt que des variables pour la cohérence de l'en-tête.

## Texte de pied de page

Le texte de pied de page apparaît après les détails de la transaction (articles, totaux, paiement). Contenu typique : 

**Politique de retour** : 
```
Retours dans les 30 jours avec le reçu
Crédit de magasin ou échange uniquement
```

**Message de remerciement** : 
```
Merci d'avoir acheté chez nous !
Suivez-nous @yourstore
```

**Service client** : 
```
Questions ? Appelez (555) 123-4567
ou envoyez un e-mail à support@yourstore.com
```

**Conseils de formatage** : 
- Placez les informations les plus importantes en premier (politique de retour, contact)
- Utilisez des sauts de ligne pour la lisibilité
- Pensez à ajouter une ligne de séparation (`---`) entre les sections

## Champs de conformité

Beaucoup de juridictions exigent des informations spécifiques sur les reçus : 

**Étiquette du numéro d'identification fiscale** - Étiquette personnalisable pour le numéro d'identification fiscal : 
- États-Unis : "Tax ID" ou "EIN"
- Union européenne : "VAT Number" ou "VAT Reg No"
- Canada : "GST/HST Number"
- Australie : "ABN"

**Valeur du numéro d'identification fiscal** - Le numéro d'identification réel : 
- Entré une seule fois dans le modèle, apparaît sur tous les reçus
- Exemple : "VAT Number: GB123456789"

**Étiquette du numéro d'enregistrement commercial** - Étiquette personnalisable pour l'enregistrement commercial : 
- France : "SIRET"
- Allemagne : "Handelsregister"
- Royaume-Uni : "Company Registration Number"

**Valeur du numéro d'enregistrement commercial** - Le numéro d'enregistrement réel : 
- Exemple : "SIRET: 123 456 789 00010"

**Afficher "Powered by Spwig"** - Basculer pour afficher ou cacher la marque "Powered by Spwig" : 
- Activé par défaut (soutient le développement de la plateforme)
- Désactiver pour les opérations sans marque blanche

**Exemples de conformité par région** : 

**Union européenne** : 
- Étiquette du numéro d'identification fiscal : "VAT Number"
- Valeur du numéro d'identification fiscal : "GB123456789"
- Afficher le numéro d'enregistrement de l'entreprise si requis par le pays

**États-Unis** : 
- Aucune exigence générale de numéro d'identification fiscal sur les reçus (varie selon l'État)
- Peut inclure l'EIN pour les transactions B2B

**France (spécifique)** : 
- Numéro SIRET obligatoire sur tous les reçus
- Étiquette du numéro d'enregistrement commercial : "SIRET"
- Valeur du numéro d'enregistrement commercial : "123 456 789 00010"

**Australie** : 
- Numéro ABN recommandé pour les entreprises enregistrées au GST
- Étiquette du numéro d'identification fiscal : "ABN"

Vérifiez les exigences locales pour les reçus avant de mettre en ligne.

## Promotions via code QR

Incluez un code QR en bas des reçus pour stimuler l'engagement des clients : 

**URL du code QR** - Destination lors du balayage : 
- Demande d'avis : `https://yourstore.com/reviews/leave-review`
- Programme de fidélité : `https://yourstore.com/loyalty/join`
- Réduction pour achat suivant : `https://yourstore.com/discount/THANKYOU`
- Réseaux sociaux : `https://instagram.com/yourstore`
- Page d'accueil du site : `https://yourstore.com`

**Étiquette du code QR** - Texte affiché au-dessus du code QR : 
- "Balayez pour laisser un avis et obtenir 10% de réduction sur votre prochain achat"
- "Rejoignez notre programme de fidélité - Balayez ici"
- "Suivez-nous sur Instagram - Balayez pour vous connecter"
- "Notez votre expérience"

**Meilleures pratiques pour les codes QR** : 
- Utilisez des URLs courtes (les URLs longues créent des codes denses et difficiles à balayer)
- Testez le code QR avec plusieurs caméras de téléphone avant le déploiement
- Incluez une proposition de valeur claire dans l'étiquette (ce que le client obtient en balayant)
- Suivez les balayages de code QR pour mesurer l'efficacité (utilisez une URL avec un paramètre de suivi)

**Codes QR dynamiques** (Avancé) : 
- Utilisez un service de redirection de code QR (bit.ly, tinyurl) pour créer une URL courte
- Pointez la redirection vers des destinations différentes selon les saisons sans imprimer à nouveau les reçus
- Exemple : `https://bit.ly/yourstoreqr` → redirige vers la promotion actuelle

## Création de modèles pour différentes portées

**Modèle par défaut** (point de départ recommandé) : 
1. Accédez à **POS > Modèles de reçus**
2. Cliquez sur **+ Ajouter un modèle de reçu**
3. Laissez les champs **Entrepôt** et **Groupe de magasins** vides (cela le rend par défaut)
4. Configurez la largeur du papier correspondant à votre type d'imprimante le plus courant
5. Ajoutez un logo, un en-tête, un pied de page
6. Configurez les champs de conformité pour votre marché principal
7. Enregistrez

Ce modèle s'applique à tous les magasins sauf s'il est remplacé.

**Modèle de groupe** (pour les variations régionales) : 
1. Créez un nouveau modèle
2. Sélectionnez **Groupe de magasins** (par exemple, "Magasins européens")
3. Laissez **Entrepôt** vide
4. Ajustez les champs de conformité pour la région (par exemple, formatage de la TVA)
5. Ajustez le texte d'en-tête (par exemple, adresse régionale)
6. Enregistrez

Ce modèle s'applique à tous les magasins du groupe.

**Modèle de magasin** (pour les besoins spécifiques à un emplacement) : 
1. Créez un nouveau modèle
2. Sélectionnez **Entrepôt** (par exemple, "Magasin de Paris")
3. Ajustez tous les champs pour cet emplacement spécifique
4. Enregistrez

Ce modèle s'applique uniquement à ce magasin.

**Test des modèles** : 
- Traitez une transaction de test sur le terminal
- Imprimez le reçu
- Vérifiez la netteté du logo, l'alignement du texte, les champs de conformité, la scannabilité du code QR
- Ajustez le modèle et refaites le test si nécessaire

## Mises en page de reçus courantes

**Reçu minimal** (camions de nourriture, pop-up) : 
- Aucun logo (économie d'espace)
- En-tête : nom du magasin et numéro de téléphone uniquement
- Pied de page : message de remerciement
- Aucun code QR

**Reçu de commerce standard** : 
- Logo (marque en noir et blanc)
- En-tête : nom complet du magasin, adresse, heures d'ouverture
- Conformité : numéro d'identification fiscal
- Pied de page : politique de retour, message de remerciement
- Code QR : demande d'avis

**Reçu de commerce premium** : 
- Logo (marque complète)
- En-tête : devise, adresse, contact
- Conformité : numéro d'identification fiscal, numéro d'enregistrement commercial
- Pied de page : politique de retour, service client, réseaux sociaux
- Code QR : inscription au programme de fidélité

**Chaîne multi-emplacements** : 
- Modèle par défaut : branding corporatif, politiques standard
- Modèles de groupe : conformité régionale (TVA pour l'UE, GST pour le Canada)
- Modèles de magasin : adresse et numéro de téléphone spécifiques à l'emplacement

## Gestion de plusieurs modèles

**Conventions de nommage des modèles** : 
- Utilisez la portée dans le nom : "Modèle par défaut", "Modèle du groupe de l'UE", "Modèle du magasin de Paris" 
- Aide à identifier quel modèle s'applique où lors de la consultation de la liste

**Modifications de modèle** : 
- Les modifications s'appliquent immédiatement aux reçus futurs
- Les reçus passés (déjà imprimés) ne sont pas affectés
- Testez les modifications sur un terminal à faible trafic avant de les déployer sur tous les magasins

**Duplication de modèles** : 
- Lors de la création d'un nouveau modèle similaire à un modèle existant, dupliquez le modèle existant et modifiez-le
- Évite de commencer à partir de zéro

**Suppression de modèles** : 
- Impossible de supprimer le modèle par défaut tant que des terminaux existent (doit avoir un fallback)
- Peut supprimer les modèles de groupe/magasin (les terminaux retournent au niveau suivant de la hiérarchie)
- Confirmez qu'aucun terminal n'utilise actuellement le modèle avant de le supprimer

## Conseils

- **Commencez par 80mm si vous n'êtes pas sûr** - La largeur de papier standard convient à la plupart des détaillants ; 58mm est spécialisé
- **Testez le logo sur une imprimante réelle** - Ce qui semble bon à l'écran peut imprimer mal ; testez tôt
- **Maintenez les champs de conformité à jour** - Les numéros d'enregistrement fiscaux expirés sur les reçus créent des problèmes juridiques
- **Les codes QR avec une proposition de valeur balayent mieux** - "Balayez pour 10% de réduction" dépasse "Balayez ici" par 10 fois
- **Révisez les limites de caractères** - Le débordement de texte ruine le formatage ; comptez les caractères par ligne avant le déploiement
- **Un modèle par largeur de papier** - Neffectuez pas l'affectation d'un modèle de 80mm à un terminal avec une imprimante de 58mm (le logo ne s'adaptera pas)
- **Imprimez des reçus de test mensuellement** - Les imprimantes se dégradent avec le temps ; vérifiez que la qualité reste acceptable
- **Utilisez les variables avec parcimonie** - Le texte statique est plus fiable que les variables dynamiques (moins de points de défaillance)
- **Sauvegardez la configuration du modèle** - Prenez une capture d'écran ou exportez les paramètres du modèle avant de faire des changements majeurs (retour facile)
- **La conformité régionale varie** - Étudiez les exigences locales pour les reçus avant le déploiement ; les amendes pour non-conformité peuvent être sévères

