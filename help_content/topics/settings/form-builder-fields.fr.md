---
title: Champs et validation du constructeur de formulaires
---

Les champs de formulaire sont les blocs de base de vos formulaires — chaque champ collecte un morceau de données des utilisateurs. Le constructeur de formulaires propose 22 types de champs allant des entrées de texte simples à des échelles de notation avancées et des sélecteurs de produits. Configurez chaque champ avec des étiquettes, des règles de validation, du texte d'aide et de la logique conditionnelle pour créer des formulaires dynamiques qui s'adaptent en fonction des réponses des utilisateurs. Les champs peuvent être obligatoires ou optionnels, validés avec des motifs regex et stylisés avec des classes CSS personnalisées.

Utilisez ce guide pour comprendre tous les types de champs disponibles, quand utiliser chacun et comment configurer la validation et la logique conditionnelle.

## Configuration de base des champs

Chaque champ partage ces paramètres communs :

**Identité**:
- **Nom du champ** - Nom machine pour le stockage des données (aucun espace, utilisez des tirets bas : `email_address`)
- **Type de champ** - Détermine le comportement d'entrée et le rendu
- **Affectation à une étape** - À quelle étape appartient ce champ (uniquement pour les formulaires multi-étapes)

**Affichage**:
- **Étiquette** - Question ou invite affichée aux utilisateurs (ex. : "Quelle est votre adresse e-mail ?")
- **Aide** - Texte d'indice à l'intérieur de l'entrée (ex. : "you@example.com")
- **Texte d'aide** - Guide supplémentaire en dessous du champ (ex. : "Nous ne partagerons jamais votre e-mail")
- **Valeur par défaut** - Valeur préremplie (les utilisateurs peuvent la modifier)

**Disposition**:
- **Largeur** - Pleine (100 %), Moitié (50 %) ou Un tiers (33 %) de la largeur du formulaire
- **Classe CSS** - Classes supplémentaires de style pour un design personnalisé
- **Ordre** - Position dans l'étape (glissez pour réorganiser)

**Validation**:
- **Obligatoire** - Activez/désactivez l'état obligatoire (un astérisque rouge apparaît sur l'étiquette)
- **Longueur minimale/maximale** - Limites de caractères (champs de texte)
- **Valeur minimale/maximale** - Limites numériques (champs de nombres)
- **Motif de validation** - Motif regex personnalisé pour une validation complexe
- **Message d'erreur** - Texte personnalisé affiché lorsqu'une validation échoue

## Champs de saisie de texte

**Texte à une seule ligne** (`text`):
- Saisie de texte de base pour des réponses courtes
- Validation : longueur minimale/maximale, motif regex
- Cas d'utilisation : Noms, adresses, codes de produits, réponses courtes
- Exemple : "Prénom et nom", "Adresse", "Nom de l'entreprise"

**Texte à plusieurs lignes** (`textarea`):
- Zone de texte étendable pour un contenu plus long (3 à 10 lignes)
- Validation : longueur minimale/maximale
- Cas d'utilisation : Commentaires, retours, descriptions détaillées, messages
- Exemple : "Dites-nous de votre expérience", "Notes supplémentaires"

**Adresse e-mail** (`email`):
- Validation spécifique aux e-mails (doit comporter @ et un domaine)
- Les claviers mobiles affichent le bouton @ de manière prominente
- Cas d'utilisation : E-mail de contact, inscriptions aux newsletters, création de compte
- Exemple : "Adresse e-mail", "E-mail professionnel"

**Numéro de téléphone** (`phone`):
- Formate automatiquement les numéros de téléphone
- Les claviers mobiles affichent un agencement numérique
- Validation : motif configurable (formats internationaux pris en charge)
- Cas d'utilisation : Numéro de contact, contact d'urgence, planification de rendez-vous
- Exemple : "Numéro de téléphone", "Téléphone mobile", "Numéro de contact"

**Nombre** (`number`):
- Saisie numérique avec des contrôles d'incrémentation/décrémentation
- Validation : valeur minimale/maximale, incrément de pas
- Retourne un nombre (et non une chaîne) dans les réponses
- Cas d'utilisation : Quantités, âges, années d'expérience, montants budgétaires
- Exemple : "Combien d'employés ?", "Votre âge", "Années d'expérience"

**URL** (`url`):
- Validation de l'URL (doit comporter http:// ou https://)
- Les claviers mobiles affichent le bouton .com
- Cas d'utilisation : Site web, profil LinkedIn, lien vers portfolio
- Exemple : "Site de l'entreprise", "URL du portfolio"

## Champs de sélection

**Sélection déroulante** (`select`):
- Sélection d'une seule option à partir d'un menu déroulant
- Configuration : tableau de {value, label} options
- Prend en charge la sélection par défaut
- Cas d'utilisation : Catégories, états/pays, sélection d'état
- Exemple : "Sélectionnez votre pays", "Département", "Comment avez-vous entendu parler de nous ?"
- Meilleur pour : 5+ options (moins d'options utilisent des cases à cocher au lieu de cela)

**Boutons radio** (`radio`):
- Choix unique parmi des options visibles (toutes les options affichées)
- Configuration : tableau de {value, label} options
- Meilleure UX que select pour 2-4 options
- Cas d'utilisation : Questions oui/non, genre, préférences avec peu de choix
- Exemple : "Recommanderiez-vous ?", "Méthode de contact préférée"

**Case à cocher** (`checkbox`):
- Case à cocher unique (activé/désactivé)
- Retourne true/false dans les réponses
- Cas d'utilisation : Acceptation des conditions, accords, préférence unique
- Exemple : "J'accepte les conditions et les mentions légales", "Abonnez-vous à la newsletter"

**Groupe de cases à cocher** (`checkbox_group`):
- Sélection multiple parmi des options (les utilisateurs peuvent sélectionner 0, 1 ou plusieurs)
- Configuration : tableau de {value, label} options
- Retourne un tableau des valeurs sélectionnées
- Cas d'utilisation : Préférences à choix multiples, centres d'intérêt, fonctionnalités nécessaires
- Exemple : "Quels sont vos centres d'intérêt ?", "Sélectionnez toutes les options applicables"

## Champs de notation

**Notation par étoiles** (`rating_stars`):
- Échelle de notation visuelle (généralement 1 à 5 étoiles)
- Configuration : 
  - `max_stars`: 3 à 10 étoiles (par défaut : 5)
  - `allow_half`: true/false pour les demi-étoiles
  - `icon`: fa-star (par défaut) ou fa-heart
  - `color`: code de couleur hexadécimal (par défaut : #FFD700 or) 
- Cas d'utilisation : Notations de produits, qualité du service, scores de satisfaction
- Exemple : "Notez votre expérience", "Comment était notre service ?"

**Échelle de Likert** (`rating_likert`):
- Échelle de notation basée sur une déclaration : fortement désapprobation → fortement approbation
- Configuration : 
  - `scale_type`: 5_point (1-5) ou 7_point (1-7)
  - `labels`: personnalisez le texte des extrémités (gauche : "Forte désapprobation", droite : "Forte approbation")
- Retourne une valeur numérique (1-5 ou 1-7)
- Cas d'utilisation : Déclarations de sondage, échelles d'accord, mesure de sentiment
- Exemple : "Le produit répond à mes besoins", "Le service client a été utile"

**Score de Promoteur Net (NPS)** (`rating_nps`):
- Échelle de 0 à 10 : "Pas du tout probable" à "Très probable"
- Configuration : 
  - `low_label`: texte de l'extrémité gauche (par défaut : "Pas du tout probable")
  - `high_label`: texte de l'extrémité droite (par défaut : "Très probable")
- Retourne une valeur de 0 à 10 (0-6 = détracteurs, 7-8 = passifs, 9-10 = promoteurs)
- Cas d'utilisation : Enquêtes NPS, probabilité de recommandation, mesure de fidélité
- Exemple : "Quelle est la probabilité que vous recommandiez à un ami ?"

## Champs avancés

**Téléchargement de fichier** (`file`):
- Téléchargement d'un ou plusieurs fichiers
- Configuration : 
  - `max_size_mb`: limite de taille de fichier par fichier (par défaut : 5 Mo)
  - `allowed_types`: tableau d'extensions (ex. : ["pdf", "doc", "docx", "jpg", "png"])
  - `max_files`: nombre maximal de fichiers (1 pour un seul, 2+ pour plusieurs)
- Retourne le chemin du fichier(s) dans les réponses
- Les fichiers sont stockés dans `/media/form_uploads/{form-slug}/`
- Cas d'utilisation : Téléchargement de CV, soumission de documents, pièces jointes de photos
- Exemple : "Téléchargez votre CV", "Joignez des documents complémentaires"

**Sélecteur de produit** (`product_select`):
- Sélection multiple à partir de votre catalogue de produits
- Configuration : 
  - `category_filters`: limitez à des catégories spécifiques (tableau d'IDs de catégories)
  - `max_selections`: 1 pour un seul produit, 2+ pour plusieurs
  - `display_mode`: "list" (par défaut) ou "grid" (avec miniatures)
- Retourne les IDs/numéros de référence des produits dans les réponses
- Cas d'utilisation : Recommandations de produits, listes de souhaits, enquêtes de feedback, paquets
- Exemple : "Quels produits vous intéressent ?", "Sélectionnez vos articles préférés"

**Date** (`date`):
- Interface de sélection de date (popup calendrier)
- Retourne le format ISO (YYYY-MM-DD)
- Validation : date minimale/maximale
- Cas d'utilisation : Dates de naissance, dates d'événements, planification de rendez-vous, délais
- Exemple : "Date de naissance", "Date de rendez-vous souhaitée"

**Heure** (`time`):
- Sélecteur d'heure (heures et minutes)
- Retourne le format d'heure ISO (HH:MM)
- Cas d'utilisation : Heure de rendez-vous, fenêtres d'horaires disponibles
- Exemple : "Heure souhaitée", "Disponible après"

**Date et heure** (`datetime`):
- Sélecteur combiné de date et d'heure
- Retourne la date et l'heure ISO complète
- Cas d'utilisation : Planification d'événements, réservation de rendez-vous
- Exemple : "Heure de début de l'événement", "Fenêtre de livraison"

## Champs de mise en page (non-saisie)

**En-tête de section** (`heading`):
- Texte d'en-tête pour organiser les sections du formulaire
- Configuration : niveau d'en-tête (h2, h3, h4)
- Aucune collecte de données
- Cas d'utilisation : Séparer les formulaires longs en sections logiques
- Exemple : "Informations personnelles", "Détails de contact", "Préférences"

**Paragraphe descriptif** (`paragraph`):
- Bloc de texte enrichi pour les instructions ou l'information
- Aucune collecte de données
- Prend en charge le formatage de base (gras, italique, liens)
- Cas d'utilisation : Instructions par étape, avertissements juridiques, explications
- Exemple : Avertissement de politique de confidentialité, explication de consentement RGPD

**Ligne de séparation** (`divider`):
- Séparateur horizontal visuel
- Aucune collecte de données
- Cas d'utilisation : Organisation visuelle entre les sections

**Champ caché** (`hidden`):
- Champ invisible avec une valeur programmée
- Configuration : `default_value` (obligatoire)
- Aucune étiquette ou texte d'aide affiché aux utilisateurs
- Cas d'utilisation : Paramètres UTM, données de suivi, identifiants de session, codes de référence
- Exemple : Champ caché avec valeur provenant d'un paramètre d'URL

## Règles de validation des champs

**Champs obligatoires**:
- Cochez la case "Obligatoire" dans les paramètres du champ
- Un astérisque rouge (*) apparaît à côté de l'étiquette
- Le formulaire ne peut pas être soumis si les champs obligatoires sont vides
- Message d'erreur personnalisé : "Ce champ est obligatoire" (ou message personnalisé)

**Longueur minimale/maximale** (champs de texte) : 
- Définissez le nombre minimal de caractères : empêche les réponses trop courtes
- Définissez le nombre maximal de caractères : empêche l'entrée excessive
- Exemple : Champ de message nécessite au moins 10 caractères (empêche les réponses "ok")

**Valeur minimale/maximale** (champs numériques) : 
- Définissez la valeur numérique minimale : empêche les âges négatifs, les quantités
- Définissez la valeur numérique maximale : limite l'entrée à une plage raisonnable
- Exemple : Champ d'âge nécessite un minimum de 18, un maximum de 120

**Motif de validation** (regex) : 
- Expression régulière personnalisée pour une validation complexe
- Modèles courants : 
  - Code postal : `^{5}(-{4})?$` (format US)
  - Téléphone : `^{3}{3}-{4}$` (format US)
  - Code de produit : `^[A-Z]{2}{4}$` (2 lettres, 4 chiffres)
- Message d'erreur personnalisé requis lors de l'utilisation de motifs

**Validation des fichiers** : 
- Taille maximale du fichier : empêche les téléchargements volumineux (par défaut 5 Mo)
- Types autorisés : liste blanche d'extensions spécifiques (sécurité)
- Exemple : Champ de CV autorise ["pdf", "doc", "docx"], max 2 Mo

## Logique conditionnelle

Créez des formulaires dynamiques où les champs apparaissent ou disparaissent en fonction des réponses des utilisateurs : 

**Fonctionnement des règles conditionnelles** : 
1. L'utilisateur répond au "champ source" (le déclencheur)
2. Le système évalue la règle : opérateur + valeur de comparaison
3. Si la condition est vraie, l'action s'exécute (afficher/masquer/rendre obligatoire un champ ou une étape)
4. Plusieurs règles peuvent s'enchaîner (la règle A déclenche la règle B)

**Opérateurs disponibles** : 
- **Égal à** (`equals`) : correspondance exacte (ex. : pays égal à "US")
- **Pas égal à** (`not_equals`) : tout sauf la valeur
- **Contient** (`contains`) : texte inclut un sous-chaîne (insensible à la casse)
- **Plus grand que** (`greater_than`) : comparaison numérique (ex. : âge > 18)
- **Plus petit que** (`less_than`) : comparaison numérique (ex. : notation < 3)
- **Est vide** (`is_empty`) : le champ n'a pas de valeur
- **N'est pas vide** (`is_not_empty`) : le champ a toute valeur
- **Dans la liste** (`in_list`) : la valeur est l'une des ["Option1", "Option2"]

**Actions disponibles** : 
- **Afficher le champ** - Afficher un champ caché
- **Masquer le champ** - Cacher le champ (la valeur est effacée si le champ est masqué)
- **Rendre le champ obligatoire** - Rendre le champ obligatoire
- **Rendre le champ non obligatoire** - Rendre le champ optionnel
- **Définir la valeur** - Remplir le champ avec une valeur
- **Afficher l'étape** - Afficher une étape cachée (uniquement pour les formulaires multi-étapes)
- **Masquer l'étape** - Cacher l'étape (uniquement pour les formulaires multi-étapes)
- **Passer à l'étape** - Passer à une étape spécifique (uniquement pour les formulaires multi-étapes)

**Exemples de règles** : 
- SI `contact_method` ÉGAL À "phone" ALORS afficher_champ `phone_number`
- SI `rating` MOINS QUE "3" ALORS rendre_obligatoire `improvement_feedback`
- SI `country` DANS_LA_LISTE ["US", "CA"] ALORS afficher_etape `shipping_details`
- SI `budget` PLUS GRAND QUE "10000" ALORS afficher_champ `enterprise_features`

**Création de règles conditionnelles** : 
1. Cliquez sur l'onglet "Règles conditionnelles" dans le panneau de droite
2. Cliquez sur "Ajouter une règle"
3. Sélectionnez le champ source (déclencheur)
4. Sélectionnez l'opérateur (comment comparer)
5. Entrez la valeur de comparaison (ce à quoi comparer)
6. Sélectionnez l'action (ce que faire)
7. Sélectionnez la cible (champ ou étape affectée)
8. Optionnel : Définir la priorité (les règles avec une priorité plus élevée sont évaluées en premier)
9. Enregistrer la règle

**Priorité des règles** : 
- Les numéros plus élevés sont évalués en premier (priorité 100 avant priorité 10)
- Utilisez la priorité lorsque les règles entrent en conflit ou s'enchaînent
- Exemple : La règle A (priorité 100) affiche le champ, la règle B (priorité 50) le rend obligatoire (A s'exécute en premier, puis B)

## Schémas de champs courants

**Formulaire de contact** : 
- Nom complet (texte, obligatoire)
- E-mail (e-mail, obligatoire)
- Téléphone (téléphone)
- Sujet (sélection avec options : "Ventes", "Support", "Partenariat")
- Message (textarea, obligatoire, min 10 caractères)

**Feedback sur le produit** : 
- Produit (product_select, sélection unique)
- Note globale (rating_stars, 5 étoiles)
- Conditionnel : SI note < 3 ALORS rendre_obligatoire "Qu'est-ce que nous pouvons améliorer ?" (textarea)
- Recommandation (rating_nps)

**Candidature à un emploi** : 
- Étape 1 : Personnel (nom, e-mail, téléphone)
- Étape 2 : CV (téléchargement de fichier, autorise ["pdf", "doc"], max 2 Mo)
- Étape 3 : Disponibilité (date de début, groupe de cases à cocher pour les jours de travail)
- Conditionnel : SI "years_experience" > 5 ALORS afficher_champ "leadership_experience"

## Conseils

- **Utilisez les types de champs appropriés** - Champ e-mail pour les e-mails (et non texte), fournit une validation et un clavier mobile amélioré
- **Gardez les étiquettes courtes** - Utilisez le texte d'aide pour les détails, pas les étiquettes
- **Groupez les champs liés** - Utilisez des en-têtes et des séparateurs pour une organisation visuelle
- **Testez la validation** - Aperçu du formulaire et essayez de soumettre avec des données invalides
- **Limitez la taille des téléchargements de fichiers** - 5 Mo max empêche la surcharge du serveur à partir de grands fichiers
- **Utilisez la logique conditionnelle avec modération** - Trop de règles désorientent les utilisateurs ; gardez les formulaires simples
- **Définissez des valeurs maximales réalistes** - Max d'âge de 120, max de quantité de 100 (empêche les fautes de frappe comme 1000)
- **Fournissez des exemples de motifs** - Si vous utilisez une validation regex, montrez un exemple dans le texte d'aide
- **Rendez les champs évidents obligatoires** - Nom et e-mail pour les formulaires de contact, toujours obligatoires
- **Utilisez les boutons radio pour 2-4 options** - Sélection déroulante pour 5+ options (améliore l'UX)
- **Utilisez des champs à largeur moitié pour les entrées courtes** - Numéro de téléphone et code postal peuvent être à largeur moitié, économise l'espace vertical
- **Utilisez les sélecteurs de produits pour les listes de souhaits** - Permettez aux clients de sélectionner plusieurs produits pour les recommandations

