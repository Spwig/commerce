---
title: Mises à jour de la plateforme
---

Votre installation Spwig est construite à partir d'une collection de composants — thèmes, widgets, intégrations, éléments du constructeur de pages et connexions de fournisseurs — chacun avec sa propre version pouvant être mise à jour indépendamment. Le Registre des composants vous donne une vue centrale de tout ce qui est installé, affiche les composants ayant des mises à jour en attente et vous permet d'installer ou de revenir en arrière des mises à jour à tout moment.

![Aperçu du Registre des composants](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Comprendre le registre des composants

Accédez à **Extensions > Registre des composants** pour voir chaque composant installé sur votre boutique. Chaque ligne affiche :

- **Nom** — le nom d'affichage du composant
- **Type** — le type de composant (thème, widget, intégration, etc.)
- **Version actuelle** — la version actuellement en cours d'exécution sur votre boutique
- **Statut de mise à jour** — si une mise à jour est disponible
- **Canal** — quel canal de mise à jour le composant suit
- **Mise à jour automatique** — si les mises à jour s'installent automatiquement
- **Verrouillé** — si le composant est figé à sa version actuelle

Le tableau de bord en haut de la page affiche des compteurs récapitulatifs : nombre total de composants installés, combien ont des mises à jour disponibles et combien sont à jour.

### Types de composants

| Type | Ce que c'est |
|------|------------|
| Thème | Le design visuel de votre boutique |
| Widget | Blocs réutilisables du constructeur de pages |
| Élément du constructeur de pages | Éléments personnalisés pour le constructeur de pages |
| Outil du constructeur de pages | Outils et utilitaires de l'éditeur |
| Modèle d'en-tête/pied de page | Mise en page de l'en-tête et du pied de page |
| Fournisseur d'expédition | Intégrations de transporteurs (FedEx, UPS, etc.) |
| Fournisseur d'e-mail | Services de livraison d'e-mails |
| Fournisseur de paiement | Intégrations des passerelles de paiement |
| Fournisseur de taux de change | Sources de données des taux de change |
| Fournisseur de traduction | Services de traduction par IA |
| Pack de langues | Fichiers de traduction de l'interface |

## Canaux de mise à jour

Chaque composant suit un canal de mise à jour qui contrôle les versions de mise à jour qu'il reçoit. Vous pouvez affecter chaque composant à un canal différent en fonction du niveau de risque que vous êtes prêt à accepter.

| Canal | Description | Meilleur pour |
|---------|-------------|----------|
| **Stable** | Versions prêtes pour la production, soigneusement testées | Tous les composants sur des boutiques en production |
| **Bêta** | Versions pré-rélease pour tester de nouvelles fonctionnalités avant qu'elles ne deviennent stables | Composants non critiques que vous souhaitez prévisualiser |
| **Développement** | Fonctionnalités les plus récentes, peuvent être instables | Environnements de test uniquement |
| **Sécurité** | Correctifs de sécurité critiques uniquement, livrés avec la plus haute priorité | Composants pour lesquels la stabilité est primordiale |

Pour changer le canal d'un composant, cliquez sur son nom pour ouvrir la vue détaillée, puis sélectionnez une nouvelle valeur dans le champ **Canal de mise à jour** et enregistrez.

## Vérifier les mises à jour

Spwig vérifie automatiquement les mises à jour à l'intervalle configuré dans vos paramètres du serveur de mise à jour (par défaut : toutes les 24 heures). Pour vérifier immédiatement :

1. Accédez à **Extensions > Registre des composants**
2. Cliquez sur le bouton **Vérifier les mises à jour** en haut de la page
3. Le système contacte le serveur de mise à jour Spwig et met à jour le statut de mise à jour pour tous les composants
4. Les composants avec des mises à jour disponibles sont mis en évidence, et le compte **Mises à jour disponibles** est mis à jour

Vous pouvez également déclencher une vérification de mise à jour pour des composants individuels en utilisant l'action **Vérifier les mises à jour** depuis le menu d'action de la liste.

## Installer des mises à jour

### Mettre à jour un seul composant

1. Accédez à **Extensions > Registre des composants**
2. Trouvez le composant que vous souhaitez mettre à jour — les composants avec des mises à jour disponibles affichent un indicateur de mise à jour à côté de leur version
3. Cliquez sur le bouton **Installer la mise à jour** sur la ligne de ce composant
4. Confirmez la mise à jour lorsqu'elle vous est demandée
5. La mise à jour est téléchargée, vérifiée et installée — un indicateur de progression affiche chaque étape
6. Une fois terminé, la version actuelle du composant est mise à jour au nouveau numéro de version

### Mettre à jour plusieurs composants

1.

Sélectionnez les cases à cocher à côté des composants que vous souhaitez mettre à jour
2.

Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques.

Choisissez **Installer les mises à jour** dans le menu déroulant **Action**
3.

Cliquez sur **Go** pour continuer
4.

Les mises à jour sont installées dans l'ordre des dépendances — les composants sur lesquels d'autres dépendent sont mis à jour en premier

### Ce qui se produit lors d'une mise à jour

Le processus de mise à jour passe par les étapes suivantes :

1. **Vérification** — confirme que la mise à jour est disponible et que votre licence est valide
2. **Téléchargement** — récupère le package depuis le serveur de mise à jour Spwig
3. **Vérification** — vérifie l'intégrité du package à l'aide d'un hachage SHA-256
4. **Extraction** — décompresse les nouveaux fichiers
5. **Déploiement** — active la nouvelle version
6. **Vérification de l'état** — vérifie que le composant fonctionne après la mise à jour

Si une étape échoue, le système tente automatiquement de restaurer la version précédente.

## Mises à jour au niveau de la plateforme

En plus des composants individuels, Spwig peut recevoir des mises à jour au niveau de la plateforme qui mettent à jour le moteur de magasin principal. Ces mises à jour passent par un processus plus rigoureux comprenant des migrations de base de données et une courte période de maintenance.

L'historique des mises à jour de la plateforme est visible dans la section **Mises à jour de la plateforme** du registre. Chaque entrée affiche la transition de version (par exemple, `v1.3.2 → v1.3.3`), le statut et la durée du processus de mise à jour.

Les mises à jour de sécurité sont signalées séparément et, si **Auto Install Security Updates** est activé dans la configuration de votre serveur de mise à jour, elles s'installent automatiquement sans nécessiter d'action manuelle.

## Afficher l'historique des versions

Pour voir toutes les versions précédemment installées d'un composant :

1. Cliquez sur le nom du composant pour ouvrir sa vue détaillée
2. Faites défiler jusqu'à la section **Versions du composant** en bas de la page
3. Chaque entrée de version affiche le numéro de version, la date d'installation, la méthode d'installation et son statut d'état

Le système conserve les trois dernières versions installées disponibles pour le retour en arrière. Les versions au-delà de cela sont automatiquement supprimées.

## Retourner à une version d'un composant

Si une mise à jour provoque des problèmes, vous pouvez revenir à une version précédente :

1. Ouvrez la vue détaillée du composant
2. Faites défiler jusqu'à la section **Retour en arrière**
3. Sélectionnez la version que vous souhaitez restaurer
4. Cliquez sur **Retourner à cette version**

Seules les versions marquées **Retour en arrière disponible** peuvent être restaurées. L'entrée du journal de retour en arrière enregistre qui a initié le retour en arrière et à quelle date.

## Verrouiller les composants

Le verrouillage d'un composant empêche l'installation de toute mise à jour, y compris les mises à jour automatiques. Cela est utile lorsque vous avez des personnalisations ou des intégrations qui dépendent d'une version spécifique.

1. Ouvrez la vue détaillée du composant
2. Cochez la case **Verrouillé** dans la section **Verrouillage et gel**
3. Entrez une raison dans **Raison du verrouillage** afin que votre équipe comprenne pourquoi il est gelé
4. Enregistrez l'enregistrement

Les composants verrouillés sont affichés avec un indicateur de verrou dans la liste du registre. Pour les déverrouiller, décochez **Verrouillé** et enregistrez.

## Lire les journaux de mise à jour

Le journal de mise à jour enregistre chaque opération d'installation, de mise à jour, de retour en arrière et de vérification de l'état :

1. Ouvrez la vue détaillée d'un composant
2. Les **Journaux de mise à jour** sont visibles en ligne en bas de la page
3. Chaque entrée affiche : l'action effectuée, les heures de début et de fin, les anciennes et nouvelles versions, si elle a été automatique ou manuelle, et tout message d'erreur si l'opération a échoué

Les entrées de journal avec un statut **Échoué** incluent le message d'erreur complet pour aider à la résolution des problèmes.

## Activer les mises à jour automatiques

Vous pouvez autoriser Spwig à installer automatiquement les mises à jour dès qu'elles sont disponibles :

1. Ouvrez la vue détaillée du composant
2. Cochez **Mise à jour automatique** dans la section **Version et statut de mise à jour**
3. Enregistrez l'enregistrement

Avec la mise à jour automatique activée, le système installe les mises à jour pendant le prochain cycle de vérification planifié. Les mises à jour de sécurité suivent le paramètre global **Auto Install Security Updates**, indépendamment des paramètres individuels des composants.

## Conseils

Conservez tous les formats de mise en forme Markdown, les chemins d'image, les blocs de code et les termes techniques.

- Mettez toujours à jour le canal **Stable** pour les thèmes et les fournisseurs de paiement — ce sont les composants les plus orientés client et la stabilité est la plus importante
- Verrouillez un composant avant d'y apporter des modifications personnalisées, et notez clairement la raison afin que les membres de l'équipe futurs sachent ne pas le mettre à jour
- Vérifiez les **Notes de publication** sur l'entrée de version du composant avant d'installer une mise à niveau majeure — les changements cassants y sont signalés
- Après une mise à jour, accédez à la partie concernée de votre magasin pour confirmer que tout semble fonctionner comme prévu avant de déclarer la mise à jour terminée
- Si la mise à jour automatique est activée sur un composant, surveillez périodiquement les **Journaux de mise à jour** pour vous assurer que les mises à jour automatiques se terminent avec succès