---
title: Démarrage avec le POS
---

<!-- screenshots-needed:
- url: /en/admin/pos/
  filename: getting-started-dashboard.webp
  description: POS dashboard as it appears on a fresh install with no terminals registered
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/pos/terminal-provider/wizard/step1/
  filename: getting-started-provider-wizard-step1.webp
  description: Payment provider wizard first step showing available provider options
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/catalog/warehouse/
  filename: getting-started-store-location.webp
  description: Warehouse list showing a store location with the POS toggle enabled
  save-to: core/static/core/admin/img/help/pos/
-->

Le POS Spwig transforme tout tablette ou navigateur en caisse enregistreuse complète au sein du magasin — connectée à votre catalogue de produits, à votre stock et à l'historique des commandes. Ce guide vous mène d'une installation fraîche à la validation de votre première vente. Chaque étape est liée à un sujet dédié si vous souhaitez les détails complets.

![Tableau de bord POS](/static/core/admin/img/help/pos/getting-started-dashboard.webp)

## Étape 1 : Activer le POS pour un emplacement de magasin

Les terminaux POS sont associés à un emplacement physique de magasin. Dans Spwig, les emplacements de magasin sont des entrepôts marqués comme emplacements de vente au détail.

1. Accédez à **Catalogue > Entrepôts** dans votre barre latérale d'administration.
2. Ouvrez l'entrepôt que vous souhaitez utiliser comme magasin, ou créez-en un nouveau.
3. Activez le curseur **Emplacement de vente au détail** et saisissez un **nom d'affichage du POS** (ex. : "Magasin de la Grande Rue"). Ce nom apparaît sur les reçus et dans le sélecteur de terminal.
4. Enregistrez l'entrepôt.

Si vous avez plusieurs magasins ou souhaitez les regrouper pour des rapports régionaux, créez d'abord un **Groupe de magasins** à **POS > Groupes de magasins**, puis affectez chaque entrepôt à ce groupe. Les groupes de magasins vous permettent de définir une devise, un fuseau horaire et un modèle de reçu partagés que tous les emplacements du groupe héritent.

## Étape 2 : Créer ou vérifier au moins un compte d'employé avec accès au POS

Les employés se connectent au POS en utilisant les mêmes identifiants qu'ils utilisent pour l'administration Spwig. Tout compte d'employé avec le statut **Actif** et au moins la permission `pos_admin` peut accéder au POS.

Pour vérifier ou accorder l'accès, allez à **Paramètres > Gestion des employés**, ouvrez le compte de l'employé et confirmez qu'il a le rôle POS approprié attribué. Aucun compte POS distinct n'est nécessaire.

## Étape 3 : Enregistrer votre premier terminal POS

Un terminal représente une caisse ou un appareil unique. Vous l'enregistrez dans l'administration, puis vous le reliez à un appareil physique à l'aide d'un code de liaison à usage unique.

1. Accédez à **POS > Terminaux POS** et cliquez sur **+ Ajouter un terminal POS**.
2. Donnez un nom au terminal (ex. : "Caisse avant") et attribuez-le à l'emplacement de magasin que vous avez activé à l'étape 1.
3. Enregistrez le terminal. Spwig génère un **code de liaison à 8 caractères** — vous le verrez sur la page des détails du terminal.
4. Sur l'appareil que vous souhaitez utiliser comme caisse, ouvrez un navigateur et allez à `/pos/`.
5. Entrez le code de liaison lorsque cela vous est demandé. L'appareil est désormais lié à ce terminal.

Le code de liaison est à usage unique. Si vous devez relier à nouveau un appareil, ouvrez le terminal dans l'administration et cliquez sur **Générer à nouveau le code de liaison**.

Pour les options de configuration matérielle (imprimante de reçus, lecteur de codes-barres, caisse enregistreuse), consultez [Configuration du terminal POS](pos-terminal-setup).

## Étape 4 : Configurer un fournisseur de paiement

Le fournisseur de paiement connecte vos lecteurs de carte à un réseau de paiement tel que Stripe Terminal ou Square. Utilisez le assistant de configuration en 5 étapes pour entrer vos identifiants.

1. Accédez à **POS > Fournisseurs de paiement** et cliquez sur **Configurer le fournisseur**.
2. L'assistant s'ouvre à `/admin/pos/terminal-provider/wizard/step1/`.

![Assistant de configuration du fournisseur de paiement](/static/core/admin/img/help/pos/getting-started-provider-wizard-step1.webp)

3. Sélectionnez votre fournisseur (ex. : **Stripe Terminal**) et suivez les instructions à l'écran à travers les cinq étapes : sélection du fournisseur → instructions d'installation → entrée des identifiants → test de la connexion → configuration de l'emplacement.
4. Un badge **Connecté** en vert confirme que l'intégration est active.

Si vous n'avez besoin que de paiements en espèces et d'entrée manuelle de carte, sélectionnez **Manuel** en tant que fournisseur — aucunes identifiants requis.

Pour des informations détaillées sur les champs d'identifiants pour chaque fournisseur pris en charge, consultez [Configuration du fournisseur de paiement POS](pos-payment-provider-setup).

## Étape 5 : Associer un lecteur de carte

Avec un fournisseur de paiement connecté, vous pouvez associer un lecteur de carte physique à l'un de vos terminaux en utilisant l'assistant en 3 étapes pour le lecteur.

1. Accédez à **POS > Lecteurs de carte** et cliquez sur **Ajouter un lecteur**.
2. L'assistant commence à l'URL `/admin/pos/reader/wizard/step1/`.
3. Sélectionnez votre fournisseur, puis choisissez **Enregistrer un nouvel appareil** (saisissez le code affiché à l'écran du lecteur) ou **Découvrir un appareil existant** (Spwig récupère les lecteurs déjà enregistrés auprès du fournisseur).
4. À l'étape finale, attribuez le lecteur au terminal que vous avez créé à l'étape 3.

Chaque terminal prend en charge un seul lecteur de carte assigné. Vous pouvez réassigner des lecteurs à tout moment depuis la liste des lecteurs de carte.

## Étape 6 : Concevoir votre reçu (facultatif pour le premier jour)

Spwig crée automatiquement un modèle de reçu par défaut. Vous pouvez commencer à vendre immédiatement sans le modifier — le reçu par défaut affiche le nom de votre magasin, l'adresse, la liste des articles vendus, le mode de paiement et un pied de page « Merci pour votre achat ! ».

Lorsque vous êtes prêt à personnaliser, allez à **POS > Modèles de reçu**. Les options incluent votre logo, votre numéro d'identification fiscale, une promotion via un code QR, une politique de retour et la largeur du papier (58 mm ou 80 mm pour les imprimantes thermiques). Vous pouvez créer des modèles distincts par magasin ou par groupe de magasins.

## Étape 7 : Ouvrir votre première journée de travail

Les journées de travail suivent qui a traité les ventes et combien d'espèces devraient être dans le tiroir. Les caissiers ouvrent et ferment les journées de travail directement au POS.

1. Sur le dispositif associé, allez à `/pos/` et connectez-vous avec vos identifiants d'équipe.
2. Sélectionnez le terminal et le lieu du magasin.
3. Spwig vous demande de **compter le solde initial** — saisissez le montant d'espèces déjà présent dans le tiroir (saisissez `0` si le tiroir est vide).
4. Cliquez sur **Ouvrir la journée**. Le registre est maintenant prêt à vendre.

Pour une explication complète des journées de travail, des mouvements d'espèces et des rapports de conciliation, consultez [Gestion des journées de travail POS](pos-shifts).

## Étape 8 : Passer votre première vente

Une fois une journée de travail ouverte, le processus de vente est simple :

1. Recherchez des produits par nom, scannez un code-barres ou naviguez dans les catégories pour ajouter des articles au panier.
2. Appliquez un rabais ou un code promo si nécessaire.
3. Cliquez sur **Payer** pour commencer le paiement. Choisissez le mode de paiement (espèces, carte via le lecteur ou paiement fractionné).
4. Pour les paiements par carte, le lecteur invite le client à taper ou insérer sa carte.
5. Le reçu s'imprime automatiquement (ou affiche une option de reçu numérique). La commande est enregistrée dans votre historique de commandes en temps réel.

## Étape 9 : Fermer la journée à la fin de la journée

Fermer une journée de travail verrouille le registre et génère un résumé de conciliation.

1. Depuis le menu POS, cliquez sur **Fermer la journée**.
2. Comptez l'argent dans le tiroir et saisissez le total lorsque cela vous est demandé.
3. Spwig calcule le montant d'espèces attendu en fonction du solde initial, des ventes en espèces et de tout mouvement d'espèces pendant la journée, et affiche la différence.
4. Confirmez pour fermer. Le rapport de la journée est enregistré et visible dans **POS > Journées** dans votre administration.

Notez tout argent retiré ou ajouté au tiroir pendant la journée comme **mouvements d'espèces** (via le menu de la journée) plutôt que d'ajuster le solde de fermeture — cela maintient votre conciliation précise.

## Conseils

- Terminez les étapes 1 à 5 avant votre première journée de commerce.

Les étapes 6 à 9 peuvent être effectuées le jour même.
- Utilisez un mot de passe fort mais mémorable pour le personnel — les employés du POS tapent leurs identifiants au registre, donc des mots de passe trop complexes ralentissent les employés.
- Si le lecteur de carte ne s'affiche pas en ligne, cliquez sur **Synchroniser les lecteurs** sur la page des lecteurs de carte pour récupérer l'état le plus récent auprès de votre fournisseur.
- Testez le flux complet (ouvrir la journée → vente → reçu → fermer la journée) avec une transaction de test de 0,01 $ avant votre période de commerce chargée.
- Le POS fonctionne hors ligne pour les ventes en espèces basiques.

Les paiements via le terminal de carte nécessitent une connexion internet pour être approuvés.
- Vous pouvez avoir plusieurs terminaux dans un même emplacement de magasin — ajoutez un nouveau terminal dans l'admin et associez-le à un appareil différent.