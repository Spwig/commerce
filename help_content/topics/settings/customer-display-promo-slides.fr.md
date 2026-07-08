---
title: Affichage des diapositives de promotion client
---

Les diapositives de promotion s'affichent à l'écran destiné aux clients lorsque le terminal de caisse est inactif (aucune transaction active). Créez un carrousel d'images mettant en valeur les promotions saisonnières, les lancements de nouveaux produits, les politiques du magasin, les événements à venir et les avantages du programme de fidélité. Les diapositives peuvent être ciblées vers des magasins ou des groupes spécifiques via l'affectation de portée - faites des promotions de fin de semaine uniquement dans les magasins des États-Unis, ou affichez des informations sur les événements locaux uniquement aux emplacements pertinents. Les diapositives actives passent automatiquement toutes les 5 à 10 secondes, créant un écran numérique engageant qui informe les clients pendant qu'ils attendent.

Utilisez les diapositives de promotion pour augmenter la visibilité des promotions en cours, informer les clients des politiques et stimuler l'engagement avec les programmes de fidélité et les événements.

![Liste des diapositives de promotion](/static/core/admin/img/help/customer-display-promo-slides/promoslide-list.webp)

## Comportement de l'affichage client

Lorsqu'un terminal de caisse est inactif (aucun client au comptoir, aucune transaction en cours), l'écran destiné aux clients affiche :

**Mode Carrousel** :
- Parcourt toutes les diapositives actives
- Chaque diapositive s'affiche pendant 5 à 10 secondes (configurable par terminal)
- Transitions fluides entre les diapositives
- Boucle continuellement jusqu'à ce qu'une transaction commence

**Pendant une transaction** :
- Le carrousel s'arrête immédiatement
- L'écran passe à la vue de la transaction (articles, total en cours, prompts de paiement)
- Le carrousel reprend lorsqu'une transaction est terminée et que le terminal retourne à l'état inactif

**Aucune diapositive configurée** :
- L'écran affiche un message "Bienvenue" avec la marque du magasin
- Écran statique (aucun carrousel)

**Exigences techniques** :
- L'écran client peut être un moniteur séparé ou le même écran que le caissier (l'application de caisse prend en charge le mode image dans image)
- L'écran se synchronise via l'API BroadcastChannel (communication sur le même appareil) ou WebSocket (affichages sur des appareils séparés)

## Ciblage par portée

Comme les modèles de reçus, les diapositives de promotion prennent en charge le ciblage basé sur la portée (priorité la plus élevée à la plus basse) :

| Priorité | Portée | Exemple | Cas d'utilisation |
|----------|-------|---------|----------|
| **1** | Spécifique au magasin | Diapositives du magasin de Paris | Diapositive d'événement de festival estival parisien |
| **2** | Spécifique au groupe | Diapositives des magasins européens | Diapositive de politique de confidentialité RGPD uniquement pour l'UE |
| **3** | Tous les magasins | Diapositives globales | "Livraison gratuite sur les commandes >$50" (promotion d'entreprise) |

**Fonctionnement de la portée** : 
- Le terminal affiche les diapositives correspondant à la portée de son magasin (diapositives spécifiques au magasin)
- Plus les diapositives correspondant à la portée de son groupe (si le magasin appartient à un groupe)
- Plus les diapositives sans affectation de portée (diapositives globales)
- Résultat : Un magasin peut afficher 3 à 5 diapositives (mélange de diapositives ciblées et globales)

**Exemple** : 
- Diapositive globale : "Nouveau programme de fidélité - Rejoignez-nous aujourd'hui !" (aucune portée)
- Diapositive de groupe : "Vente du Memorial Day - 30 % de réduction" (groupe uniquement des magasins des États-Unis)
- Diapositive de magasin : "Grand ouverture - Flagship de NYC" (magasin NYC uniquement)

**Le terminal du magasin de NYC** affiche toutes les 3 diapositives (magasin + groupe + globale)
**Le terminal du magasin de Londres** affiche uniquement la diapositive globale (pas dans le groupe des magasins des États-Unis, pas le magasin NYC)

## Exigences d'image

Les diapositives de promotion sont des images à écran complet optimisées pour les moniteurs d'affichage client :

**Ratio d'aspect** : 16:9 (écran large)

**Résolution recommandée** : 1920×1080 pixels (Full HD)
- S'adapte proprement à la plupart des écrans modernes
- Équilibre de la taille de fichier (qualité vs vitesse de chargement)

**Résolutions acceptées** : 
- Minimum : 1280×720 (HD)
- Optimal : 1920×1080 (Full HD)
- Maximum : 3840×2160 (4K) - non recommandé (grande taille de fichier, chargement plus lent)

**Format de fichier** : JPG, PNG ou WebP
- JPG pour les photographies
- PNG pour les graphismes avec transparence (bien que les arrière-plans soient recommandés)
- WebP pour la taille de fichier la plus petite

**Taille de fichier** : <500KB par diapositive
- Les fichiers plus volumineux ralentissent le chargement du carrousel
- Compressez les images avant de les télécharger (utilisez l'optimisation de la bibliothèque multimédia)

**Recommandations de conception** : 
- Contraste élevé pour la lisibilité à distance (clients à 2-6 pieds de l'écran)
- Texte grand (minimum 48pt pour le texte principal, 72pt+ pour les titres)
- Polices épaisses (les polices fines s'estompent sur certains écrans)
- Évitez les détails petits (ne seront pas visibles depuis la position du client)
- Incluez un appel à l'action (ce que le client doit faire : "Demandez au caissier les détails", "Inscrivez-vous aujourd'hui")

## Création d'une diapositive de promotion

Accédez à **POS > Diapositives de promotion** et cliquez sur **+ Ajouter une diapositive de promotion** :

![Formulaire d'ajout de diapositive de promotion](/static/core/admin/img/help/customer-display-promo-slides/promoslide-add-form.webp)

**Image** - Télécharger ou sélectionner depuis la bibliothèque multimédia : 
- Cliquez sur **Parcourir la bibliothèque multimédia** pour sélectionner une image existante
- Ou téléchargez une nouvelle image correspondant aux exigences ci-dessus
- Aperçu montre comment l'image s'affichera sur l'écran

**Titre** (facultatif) - Texte superposé en haut de la diapositive : 
- Maximum 60 caractères (le texte plus long est tronqué)
- Apparaît dans une barre sombre semi-transparente en haut de l'image
- Utilisez pour le titre de la diapositive ("Vente d'été", "Nouveautés")
- Laissez vide si l'image inclut déjà un titre

**Sous-titre** (facultatif) - Texte superposé sous le titre : 
- Maximum 120 caractères
- Apparaît sous le titre dans la même barre semi-transparente
- Utilisez pour les détails complémentaires ("Jusqu'à 50 % de réduction", "Cadeau gratuit avec achat")
- Laissez vide si l'image est autonome

**Actif** - Basculer pour activer/désactiver la diapositive : 
- Seules les diapositives actives apparaissent dans le carrousel
- Utilisez pour l'activation saisonnière (désactivez après la fin de la promotion)
- Désactiver préserve la diapositive pour une réactivation ultérieure

**Ordre de tri** - Contrôle la position de la diapositive dans le carrousel : 
- Les numéros plus bas apparaissent plus tôt dans la rotation
- Utilisez des multiples de 10 : 10, 20, 30 (permet d'insérer des diapositives entre les existantes)
- Exemple : Vente de fin de semaine (ordre de tri 10) s'affiche avant le programme de fidélité général (ordre de tri 20)

**Affectation de portée** (facultatif) : 
- **Entrepôt** - Sélectionnez pour afficher uniquement à un magasin spécifique
- **Groupe de magasins** - Sélectionnez pour afficher uniquement aux magasins du groupe
- **Laissez les deux vides** - Affiche à tous les magasins (diapositive globale)

## Ordre de tri et flux du carrousel

**Exemple de carrousel** (terminal du magasin de NYC) : 
- Diapositive 1 (ordre de tri 10) : "Grand Opening - NYC Flagship" (spécifique au magasin)
- Diapositive 2 (ordre de tri 15) : "Memorial Day Sale - 30% Off" (groupe des magasins des États-Unis)
- Diapositive 3 (ordre de tri 20) : "New Loyalty Program - Join Today!" (globale)
- Diapositive 4 (ordre de tri 30) : "Follow us @yourstore" (globale)

Le carrousel boucle : 1 → 2 → 3 → 4 → 1 → 2 → ...

**Terminal du magasin de Londres** (pas dans le groupe des magasins des États-Unis, magasin différent) : 
- Diapositive 1 (ordre de tri 20) : "New Loyalty Program - Join Today!" (globale)
- Diapositive 2 (ordre de tri 30) : "Follow us @yourstore" (globale)

Le carrousel boucle : 1 → 2 → 1 → 2 → ...

Utilisez l'ordre de tri pour prioriser le contenu le plus important en premier dans la rotation.

## Stratégie d'activation saisonnière

**Problème** : Créer/supprimer des diapositives pour chaque promotion saisonnière est fastidieux.

**Solution** : Créez des diapositives une seule fois, activez/désactivez-les selon les saisons : 

1. **Créez des diapositives pour les grands événements** : 
   - "Vente d'été" (Actif : Non, créée à l'avance)
   - "Retour à l'école" (Actif : Non, créée à l'avance)
   - "Black Friday" (Actif : Non, créée à l'avance)
   - "Vente de fin de semaine" (Actif : Non, créée à l'avance)

2. **Activez lorsqu'elles sont pertinentes** : 
   - 1er juin : Mettez "Vente d'été" → Actif : Oui
   - 15 août : Mettez "Vente d'été" → Actif : Non, mettez "Retour à l'école" → Actif : Oui
   - 20 novembre : Mettez "Black Friday" → Actif : Oui
   - 1er décembre : Mettez "Black Friday" → Actif : Non, mettez "Vente de fin de semaine" → Actif : Oui

3. **Désactivez après l'événement** : 
   - Garde la bibliothèque de diapositives organisée
   - Réutilisez les diapositives année après année (mettez à jour l'image si nécessaire, gardez la configuration)

## Exemples de cas d'utilisation

**Cas d'utilisation 1 : Promotion saisonnière**
- Image : arrière-plan rouge avec texte blanc "VENTE D'ÉTÉ - JUSQU'À 60 % DE RÉDUCTION"
- Titre : "Vente d'été"
- Sous-titre : "50-60 % de réduction sur certains articles. Demandez au caissier les détails."
- Portée : Tous les magasins (globale)
- Ordre de tri : 10 (priorité la plus élevée pendant l'été)
- Actif : uniquement en juin-août

**Cas d'utilisation 2 : Politique du magasin**
- Image : Infographie montrant les étapes de la politique de retour
- Titre : "Retours faciles"
- Sous-titre : "30 jours avec le reçu. Aucune question posée."
- Portée : Tous les magasins (globale)
- Ordre de tri : 40 (priorité plus basse que les promotions)
- Actif : toute l'année

**Cas d'utilisation 3 : Lancement de nouveau produit**
- Image : photo principale du nouveau produit
- Titre : "NOUVEAU : Earbuds sans fil Pro"
- Sous-titre : "Disponible maintenant en magasin et en ligne. 199,99 $"
- Portée : Tous les magasins (globale)
- Ordre de tri : 5 (priorité la plus élevée pendant la semaine de lancement)
- Actif : uniquement pendant la semaine de lancement, puis désactiver

**Cas d'utilisation 4 : Événement local**
- Image : affiche d'une course caritative locale
- Titre : "Soutenez le local"
- Sous-titre : "Rejoignez-nous à la course de 5 km de la communauté le 15 juin !"
- Portée : magasin spécifique (uniquement le magasin de NYC)
- Ordre de tri : 8 (priorité pour ce magasin)
- Actif : 2 semaines avant l'événement

**Cas d'utilisation 5 : Programme de fidélité**
- Image : visuel de la carte de fidélité avec des exemples de points
- Titre : "Gagnez des récompenses"
- Sous-titre : "Rejoignez notre programme de fidélité et gagnez 1 point par $1 dépensé"
- Portée : Tous les magasins (globale)
- Ordre de tri : 30 (contenu éternel)
- Actif : toute l'année

## Gestion des diapositives

**Vue de la liste des diapositives** : 
- Affiche toutes les diapositives avec aperçu d'image, titre, portée, statut
- Filtre par actif/inactif
- Filtre par portée (affiche toutes les diapositives globales, toutes les diapositives de groupe, etc.)

**Activation/désactivation en masse** : 
- Sélectionnez plusieurs diapositives dans la liste
- Utilisez l'action d'administration pour activer ou désactiver toutes en une fois
- Utile pour les transitions saisonnières (désactiver toutes les diapositives d'été, activer toutes les diapositives d'automne)

**Test des diapositives** : 
- Après avoir créé/mis à jour une diapositive, accédez au terminal de caisse
- Laissez le terminal devenir inactif (aucune transaction)
- Vérifiez que la diapositive s'affiche dans le carrousel
- Vérifiez la qualité de l'image, la lisibilité du texte superposé, le timing

**Mise à jour des diapositives actives** : 
- Les modifications prennent effet lors de la prochaine mise à jour du carrousel (généralement <30 secondes)
- Aucun besoin de redémarrer les terminaux

## Conseils

- **Concevoir pour la distance** - Les clients regardent l'écran à 2-6 pieds ; utilisez un grand texte et un contraste élevé
- **Garder le message simple** - La diapositive s'affiche pendant <10 secondes ; un message clair par diapositive
- **Utiliser la désactivation saisonnière** - Créez une seule fois, basculez sur/off chaque année plutôt que de recréer
- **Prioriser avec l'ordre de tri** - Les promotions les plus importantes devraient avoir le plus bas ordre de tri (apparaître en premier)
- **Tester sur du matériel réel** - La calibration des couleurs de l'écran varie ; vérifiez que les diapositives ont l'air bonnes sur vos moniteurs spécifiques
- **Limiter le nombre de diapositives actives** - 3-5 diapositives actives par magasin sont optimales ; 10+ diapositives signifie que chacune apparaît rarement
- **Inclure des appels à l'action** - Dites aux clients ce qu'ils doivent faire ("Demandez au caissier", "Visitez le site web", "Scannez le code QR sur le reçu")
- **Mettre à jour régulièrement** - Les promotions périmées (ventes expirées, événements passés) réduisent la confiance des clients
- **Utiliser la portée de manière stratégique** - Les promotions régionales (portée de groupe) et les événements locaux (portée de magasin) semblent plus pertinents que le contenu global constant

