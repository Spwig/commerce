---
title: Overview du Constructeur de Formulaires
---

Le Constructeur de Formulaires crée des formulaires personnalisés pour la collecte de données — des formulaires de contact, des sondages, des demandes, des inscriptions, et bien plus encore. Construisez des formulaires visuellement avec des champs glissés-déposés, configurez des règles de validation, activez des workflows multi-étapes et collectez des réponses avec des analyses détaillées. Les formulaires s'intègrent parfaitement aux éléments du Constructeur de Pages, pouvant être insérés n'importe où sur votre site. Toutes les soumissions sont stockées dans la base de données avec une métadonnée complète (adresse IP, navigateur, temps de complétion) pour l'analyse et l'export.

Utilisez le Constructeur de Formulaires lorsque vous avez besoin de collecter des données structurées auprès des clients, qu'il s'agisse d'informations de contact simples ou d'applications complexes multi-pages.

## Qu'est-ce que le Constructeur de Formulaires ?

Le Constructeur de Formulaires est un outil visuel de glissé-déposé pour créer des formulaires personnalisés sans code :

**Types de formulaires pris en charge**:
- Formulaires de contact (nom, courriel, message)
- Enquêtes clients (notations, retours, NPS)
- Inscriptions de produits (garantie, support)
- Candidatures à un emploi (téléchargement de CV, multi-étapes)
- Inscriptions à un événement (informations des participants, préférences)
- Demandes de service (exigences détaillées)
- Inscriptions à la newsletter (avec des cases à cocher pour les préférences)

**Fonctionnalités clés**:
- **22 types de champs** - Texte, courriel, téléphone, téléchargement de fichiers, notations, sélecteurs de produits, et plus
- **Formulaires multi-étapes** - Divisez les formulaires longs en étapes logiques avec un suivi de progression
- **Logique conditionnelle** - Affichez/masquez des champs en fonction des réponses de l'utilisateur
- **Règles de validation** - Champs obligatoires, longueur minimale/maximale, motifs regex personnalisés
- **Protection contre le spam** - Champs honeypot ou Google reCAPTCHA v3
- **Analyse des réponses** - Suivez le temps de complétion, l'adresse IP, le navigateur, le référent
- **Export CSV** - Téléchargez toutes les réponses pour l'analyse dans Excel/Google Sheets
- **Multilingue** - Traduisez les étiquettes et messages du formulaire dans toutes les langues actives

## Créer votre premier formulaire

Accédez à **Paramètres > Pages > Formulaires** pour accéder au gestionnaire de formulaires :

**Étape 1 : Créer un nouveau formulaire**
- Cliquez sur **+ Créer un nouveau formulaire**
- Entrez le nom du formulaire (identifiant interne, non affiché aux clients)
- Entrez le titre du formulaire (affiché en tant que titre au-dessus du formulaire)
- Optionnel : Ajoutez une description (texte d'aide affiché en dessous du titre)

**Étape 2 : Ajouter des champs**
- Cliquez sur **Éditer la conception du formulaire** pour ouvrir le constructeur visuel
- Glissez les types de champs depuis la barre latérale gauche vers le canevas
- Cliquez sur un champ pour le configurer dans le panneau de droite
- Définissez l'étiquette, le texte d'exemple, le texte d'aide
- Activez/désactivez le statut obligatoire
- Ajoutez des règles de validation

**Étape 3 : Configurer les paramètres du formulaire**
- Définissez le texte du bouton de soumission (par défaut : "Soumettre")
- Personnalisez le message de succès (affiché après la soumission)
- Choisissez la protection contre le spam (champ honeypot recommandé)
- Activez/désactivez "Requiert une connexion" si nécessaire
- Activez "Formulaire multi-étapes" pour les formulaires complexes

**Étape 4 : Activer le formulaire**
- Activez le statut **Actif**
- Seuls les formulaires actifs acceptent les soumissions
- Enregistrez le formulaire

**Étape 5 : Utiliser dans le Constructeur de Pages**
- Ajoutez l'élément **Formulaire** à toute page
- Sélectionnez votre formulaire dans le menu déroulant
- Le formulaire hérite du style de la page
- Les soumissions sont envoyées au backend automatiquement

## Formulaires à page unique vs. formulaires multi-étapes

**Formulaires à page unique** (par défaut) : 
- Tous les champs sont affichés en une seule fois
- Faites défiler pour voir tous les champs
- Bouton de soumission en bas
- Idéal pour : formulaires de contact, sondages courts, collecte de données simples

**Formulaires multi-étapes** : 
- Les champs sont organisés en étapes numérotées
- Une barre de progression indique l'étape actuelle
- Boutons de navigation "Retour"/"Suivant"
- Soumission uniquement sur l'étape finale
- Optionnel : Enregistrer les réponses partielles (mode brouillon)
- Idéal pour : candidatures à un emploi, inscriptions, sondages complexes, flux de paiement

**Activer les formulaires multi-étapes** : 
1. Activez "Formulaire multi-étapes" dans les paramètres du formulaire
2. Cliquez sur l'onglet **Étapes** dans le panneau de droite
3. Ajoutez une étape (ex. : "Informations personnelles", "Détails de contact", "Préférences")
4. Attribuez des champs aux étapes en utilisant le menu déroulant d'étape lors de la modification du champ
5. Réorganisez les étapes en les faisant glisser
6. Définissez les propriétés de l'étape : titre, description, sautable

**Avantages des formulaires multi-étapes** : 
- Réduit l'abandon des formulaires (psychologique : "seulement 3 questions sur cette page")
- Groupe logique améliore l'UX
- Indicateur de progression motive la complétion
- Enregistrement de brouillon optionnel pour les formulaires longs

## Explication des paramètres du formulaire

**Paramètres de base** : 
- **Nom interne** - La manière dont vous identifiez le formulaire dans l'administration (non visible aux clients)
- **Slug** - Identifiant convivial pour l'URL (généré automatiquement, utilisé dans les points de terminaison API)
- **Titre du formulaire** - Titre affiché au-dessus du formulaire
- **Description** - Texte d'aide optionnel affiché en dessous du titre
- **Texte du bouton de soumission** - Personnalisez l'étiquette du bouton (ex. : "Envoyer un message", "Postuler maintenant")

**Messages** : 
- **Message de succès** - Affiché après une soumission réussie (par défaut : "Merci pour votre soumission !")
- **Message d'erreur** - Affiché si la soumission échoue (par défaut : "Une erreur s'est produite. Veuillez réessayer.")

**Sécurité et accès** : 
- **Actif** - Seuls les formulaires actifs acceptent les soumissions (les formulaires inactifs affichent "Formulaire indisponible")
- **Requiert une connexion** - Restreint aux utilisateurs authentifiés uniquement (les utilisateurs anonymes voient un message d'invitation à se connecter)

**Protection contre le spam** : 
- **Aucun** - Aucune protection (non recommandé, les bots enverront des spams)
- **Champ honeypot** - Champ invisible qui attrape les bots (recommandé pour la plupart des commerçants)
- **Google reCAPTCHA v3** - Requiert une clé de site et une clé secrète de Google (meilleure protection)

**Fonctionnalités avancées** : 
- **Formulaire multi-étapes** - Activez le workflow étape par étape
- **Enregistrer les réponses partielles** - Permet aux utilisateurs d'enregistrer leur progression et de reprendre plus tard (uniquement pour les formulaires multi-étapes)

## Options de protection contre le spam

**Champ honeypot (recommandé)** : 
- Champ invisible ajouté au formulaire
- Les bots le remplissent (les humains ne peuvent pas le voir)
- Les soumissions avec un champ honeypot rempli sont rejetées
- Aucune configuration requise
- Aucun désagrément CAPTCHA pour les utilisateurs
- Efficace contre plus de 95 % des bots de spam

**Google reCAPTCHA v3** : 
- Score d'arrière-plan invisible (0,0-1,0)
- Aucun défi "cliquez sur les feux de circulation"
- Configuration requise : 
  1. Créez un compte sur google.com/recaptcha/admin
  2. Générez une clé de site et une clé secrète
  3. Entrez les clés dans les paramètres du constructeur de formulaires
- Plus robuste que le champ honeypot
- Utilisez-le lorsque le champ honeypot est insuffisant

**Aucun** : 
- Aucune protection contre le spam
- Utilisez uniquement pour les formulaires internes ou les tests
- Les formulaires publics seront fortement spammés

## Gestion des réponses des formulaires

Affichez toutes les soumissions à **Paramètres > Pages > Formulaires > [Nom du formulaire] > Réponses** : 

**Vue de la liste des réponses** : 
- Statut : brouillon, soumis, terminé
- Soumission : courriel (si connecté) ou "Anonyme"
- Adresse IP et localisation (si GeoIP activé)
- Date/heure de soumission
- Temps de complétion (en secondes)

**Détail de la réponse** : 
- Toutes les valeurs des champs avec les étiquettes
- Métadonnées : navigateur, référent, langue
- Suivi de progression (multi-étapes) : étape actuelle, étapes terminées
- Résultats des actions (si le formulaire déclenche des actions)

**Filtrage des réponses** : 
- Filtrez par formulaire, statut, plage de dates
- Recherchez par courriel du soumissionnaire ou adresse IP
- Triez par date de soumission, temps de complétion

**Export des réponses** : 
- Cliquez sur le bouton **Exporter en CSV**
- Télécharge {form-slug}_responses_{date}.csv
- Ligne d'en-tête : Soumis le, Utilisateur, IP, Statut, [Étiquettes des champs]
- Une réponse par ligne
- Ouvrez dans Excel, Google Sheets ou des outils d'analyse de données

## Utilisation des formulaires dans les pages

**Intégration des formulaires** : 
1. Ouvrez la page dans le Constructeur de Pages
2. Ajoutez l'élément **Formulaire** depuis le panneau d'éléments
3. Sélectionnez le formulaire dans le menu déroulant
4. Personnalisez le style du conteneur du formulaire (fond, marge, bordure)
5. Enregistrez et publiez la page

**Le formulaire s'affiche avec** : 
- Titre et description du formulaire (du paramétrage du formulaire)
- Tous les champs dans l'ordre (page unique) ou l'étape actuelle (multi-étapes)
- Bouton de soumission avec du texte personnalisé
- Messages de succès/erreur après la soumission

**Héritage de style** : 
- Les formulaires héritent du style du thème de la page
- Les boutons utilisent les styles de boutons du thème
- Les champs d'entrée utilisent les styles d'entrée du thème
- Une classe CSS personnalisée peut être ajoutée aux champs pour un style spécifique

## Interface du Constructeur de Formulaires

**Barre latérale gauche - Bibliothèque de champs** : 
- Organisée par catégorie (Texte, Sélection, Notation, Avancé)
- Glissez le champ vers le canevas ou cliquez pour l'ajouter
- Recherchez pour trouver rapidement les types de champs

**Canevas principal - Éditeur de champs** : 
- Poignée de glissement (≡) pour réorganiser les champs
- Cliquez sur un champ pour le sélectionner et l'éditer
- Bouton de suppression (×) sur chaque champ
- Aperçu visuel du champ tel qu'il est configuré
- État vide avec des instructions sur la zone de dépôt

**Barre latérale droite - Panneau des propriétés** : 
- **Onglet Paramètres du formulaire** - Informations de base, messages, protection contre le spam
- **Onglet Paramètres du champ** - Configurez le champ sélectionné (étiquette, validation, etc.)
- **Onglet Étapes** - Gérez les étapes (uniquement pour les formulaires multi-étapes)
- **Onglet Règles conditionnelles** - Ajoutez des logiques d'affichage/masquage basées sur les réponses

**Fonctionnalités de la barre d'outils** : 
- **Annuler/Rétablir** - Historique complet des modifications
- **Prévisualiser** - Testez la fonctionnalité du formulaire
- **Enregistrer** - Enregistrement automatique toutes les 3 secondes pendant l'édition
- **Traductions** - Traduisez le texte du formulaire en d'autres langues

## Exemples de formulaires courants

**Formulaire de contact** : 
- Champs : Nom complet (obligatoire), Courriel (obligatoire), Téléphone, Message (obligatoire)
- Bouton de soumission : "Envoyer un message"
- Succès : "Merci de nous avoir contactés ! Nous vous répondrons dans les 24 heures." 

**Enquête de retour sur le produit** : 
- Étape 1 : Évaluation par étoiles, échelle de Likert d'accord
- Étape 2 : Score NPS, suggestions d'amélioration
- Conditionnelle : Si la note < 3, demandez des commentaires d'amélioration

**Candidature à un emploi** : 
- Étape 1 : Informations personnelles (nom, courriel, téléphone)
- Étape 2 : Expérience (téléchargement de CV, années d'expérience, références)
- Étape 3 : Disponibilité (date de début, attentes salariales)
- Enregistrement partiel activé (les candidats peuvent reprendre plus tard)

**Inscription à la newsletter avec préférences** : 
- Courriel (obligatoire)
- Groupe de cases à cocher : centres d'intérêt (Produits, Ventes, Mises à jour du blog)
- reCAPTCHA activé (prévenir les inscriptions fausses)

## Conseils

- **Commencez par une page unique** - Ajoutez des étapes multiples uniquement si le formulaire dépasse 10 champs
- **Utilisez d'abord le champ honeypot** - N'upgradez que vers reCAPTCHA si le spam persiste
- **Testez avant de publier** - Utilisez le mode prévisualisation pour vérifier la validation et le flux
- **Exportez régulièrement** - Téléchargez le CSV des réponses hebdomadairement pour sauvegarder
- **Surveillez le temps de complétion** - Si la moyenne >5 minutes, le formulaire peut être trop long
- **Utilisez la logique conditionnelle** - Cacher les champs non pertinents pour réduire la perception de la longueur du formulaire
- **Activez l'enregistrement partiel pour les formulaires longs** - Réduit l'abandon sur les candidatures multi-étapes
- **Traduisez les étiquettes du formulaire** - Utilisez le système de traduction intégré pour les sites multilingues
- **Exigez une connexion pour les données sensibles** - Empêche les spams anonymes, relie les soumissions aux comptes utilisateurs
- **Gardez les messages de succès spécifiques** - "Nous vous répondrons dans les 24 heures" est meilleur que "Merci"