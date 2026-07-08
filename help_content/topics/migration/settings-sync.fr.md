---
title: Synchronisation des paramètres
---

La synchronisation des paramètres vous permet de copier la configuration du magasin entre deux installations Spwig. Cela est idéal pour maintenir des environnements de test et de production, où vous configurez et testez les modifications sur l'environnement de test avant de les déployer sur votre magasin en production.

## Quand utiliser la synchronisation des paramètres

- **Test vers Production** : Configurez les paramètres sur votre magasin de test, puis envoyez-les vers la production
- **Production vers Test** : Téléchargez les paramètres de production vers le test pour commencer avec un environnement correspondant
- **Sauvegarde de la configuration** : Téléchargez les paramètres depuis la production vers une instance de sauvegarde en tant que mesure de sécurité

La synchronisation des paramètres gère uniquement les données de configuration - elle ne transfère pas les produits, les clients, les commandes ou les fichiers multimédias. Pour un transfert complet des données, utilisez plutôt la Migration du système complet.

## Ce qui peut être synchronisé

La synchronisation des paramètres prend en charge les catégories suivantes :

| Groupe | Catégories |
|-------|-----------|
| **Paramètres** | Paramètres du site, Taxes et devises, Taux de taxes, Langues, Paramètres du blog, Partage social, Régions de vente et entrepôts, Configuration de recherche, Champs personnalisés, Rôles du personnel, Analyse des clients |
| **Design** | Design et thème, En-têtes/Pieds de page/Menus |
| **Fournisseurs** | E-mail, SMS/WhatsApp, Fournisseurs de paiement, Envoi, Fournisseurs SEO, Fournitures de produits, Connecteurs sociaux du blog, Configuration du point de vente |
| **Contenu** | Pages et modèles, Articles de blog, Annonces, Formulaires, Collections de produits |
| **Commerce** | Règles de commerce (bons, promotions, fidélité, abonnements), Programme d'affiliation, Webhooks et intégrations |

> **Note** : Les catégories contenant des identifiants (fournisseurs de paiement, comptes d'expédition, etc.) sont marquées par une icône de clé. Les clés API et les secrets sont transférés en toute sécurité, mais peuvent avoir besoin d'être réintroduits pour les intégrations basées sur OAuth.

## Guide étape par étape

### Étape 1 : Configurer une connexion

1. Accédez à **Migration des données > Synchronisation Spwig-to-Spwig** dans le menu latéral d'administration
2. Cliquez sur **Démarrer la synchronisation des paramètres**
3. Sélectionnez une connexion enregistrée ou créez-en une nouvelle :
   - Entrez l'URL du magasin distant (par exemple, `https://staging.yourstore.com`)
   - Collez le jeton de synchronisation généré sur le magasin distant
   - Donnez à la connexion un nom descriptif
   - Définissez le rôle (Test, Production, Sauvegarde ou Autre)
4. Cliquez sur **Tester la connexion** pour vérifier qu'elle fonctionne
5. Cliquez sur **Suivant** pour continuer

### Étape 2 : Choisir les catégories et la direction

**Direction :**
- **Télécharger** -- Copie les paramètres depuis le magasin connecté vers ce magasin
- **Envoyer** -- Copie les paramètres depuis ce magasin vers le magasin connecté

**Mode de synchronisation :**
- **Ajouter et mettre à jour** -- Ajoute de nouveaux éléments et met à jour les existants, mais ne supprime jamais rien. C'est l'option la plus sûre.
- **Copie exacte** -- Fait correspondre la cible à la source de manière exacte, y compris la suppression des éléments présents sur la cible mais pas sur la source. Utilisez avec prudence.

Sélectionnez les catégories que vous souhaitez inclure, puis cliquez sur **Suivant**.

### Étape 3 : Aperçu des modifications

Avant que les modifications ne soient appliquées, vous verrez un aperçu détaillé montrant exactement ce qui sera ajouté, modifié ou supprimé pour chaque catégorie. Vérifiez cela soigneusement.

Si vous envoyez vers une connexion de production, vous devrez confirmer que vous comprenez que les modifications affecteront votre magasin en production.

Cliquez sur **Démarrer la synchronisation** lorsque vous êtes prêt.

### Étape 4 : Suivre la progression

La synchronisation s'exécute en arrière-plan. Vous pouvez naviguer librement loin de la page de progression - la synchronisation continuera à s'exécuter.

La page de progression affiche :
- Le pourcentage de progression global avec le temps restant estimé
- La progression par catégorie avec les comptes de succès/échec
- Un journal d'activité en direct que vous pouvez développer pour obtenir une sortie détaillée

## Retour en arrière

Après la fin d'une synchronisation, vous avez **24 heures** pour revenir en arrière. Un retour en arrière restaure l'état précédent de tous les paramètres affectés.

Pour revenir en arrière :
1. Allez sur le **Tableau de bord de synchronisation**
2. Trouvez le travail terminé
3. Cliquez sur **Retour en arrière** et confirmez

Après 24 heures, l'option de retour en arrière expire et les modifications deviennent permanentes.

## Conseils

Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques.

- **Testez sur l'environnement de staging en premier**:

Synchronisez toujours vers un environnement de staging en premier pour vérifier les résultats avant de pousser vers la production

- **Utilisez le mode Ajouter & Mettre à jour**:

C'est le mode le plus sûr car il ne supprime jamais les données existantes

- **Vérifiez soigneusement l'aperçu**:

L'aperçu de la différence vous montre exactement ce qui changera avant que rien ne soit appliqué

- **Les connexions de production affichent des avertissements**:

Lorsque vous poussez vers une connexion marquée comme Production, des confirmations supplémentaires de sécurité sont requises