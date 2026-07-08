---
title: Configuration de plusieurs devises
---

La prise en charge de plusieurs devises permet à vos clients d'explorer les produits et de finaliser leur commande dans leur devise préférée. Les prix sont automatiquement convertis à partir de votre devise de base en utilisant les taux de change d'un fournisseur connecté ou des taux définis manuellement.

## Avant de commencer

Avant d'activer la prise en charge de plusieurs devises, vous avez besoin de :

1. **Un fournisseur de taux de change actif** - Allez dans **Paramètres > Onglet Multi-Devise > Tableau de bord des taux de change** et connectez au moins un fournisseur (tel que Open Exchange Rates, Fixer.io ou ExchangeRate-API). Le fournisseur doit être actif et synchroniser les taux.
2. **Au moins deux devises** - Votre devise de base plus une ou plusieurs devises supplémentaires que vous souhaitez prendre en charge.

## Activation de la prise en charge de plusieurs devises

Accédez à **Paramètres > Multi-Devise** et cochez **Activer la Multi-Devise**. Une fois activée, configurez les options suivantes :

| Paramètre | Description |
|---------|-------------|
| **Mode de sélection de la devise** | La manière dont les clients choisissent leur devise. *Auto* détecte à partir de leur localisation, *Manuel* leur permet de choisir via un commutateur, *Both* combine les deux approches. |
| **Afficher le commutateur de devise** | Affichez un sélecteur de devise sur votre boutique en ligne afin que les clients puissent changer de devise manuellement. |
| **Position du commutateur** | L'endroit où le commutateur de devise apparaît (en-tête, pied de page ou bande latérale). |
| **Afficher les informations sur le taux de change** | Affichez une notification aux clients indiquant que les prix sont des conversions approximatives à partir de votre devise de base. |
| **Activer le formatage local** | Formatez les nombres et les symboles de devise selon le fuseau local de chaque client (par exemple, 1.234,56 pour les formats européens). |

## Mode de paiement

Choisissez comment la prise en charge de plusieurs devises fonctionne lors du paiement :

| Mode | Description |
|------|-------------|
| **Multi-Devise complet** | Les clients naviguent, ajoutent des articles au panier et paient dans leur devise sélectionnée. Le taux de change est verrouillé lors du paiement et enregistré avec la commande. C'est le mode par défaut. |
| **Affichage uniquement** | Les prix sont affichés dans la devise du client pour commodité, mais le panier et le paiement sont toujours traités dans votre devise de base. Lors du paiement, les clients voient une notification indiquant le montant approximatif converti ainsi que le montant réel facturé dans votre devise de base. |

**Affichage uniquement** est utile lorsque votre fournisseur de paiement ne prend en charge que votre devise de base, ou lorsque vous souhaitez éviter complètement les risques liés aux taux de change. Les clients voient toujours des prix localisés lors de la navigation, leur donnant une idée du coût dans leur propre devise.

## Intervalle de synchronisation des taux de change

Contrôlez la fréquence à laquelle votre boutique récupère les taux de change frais auprès de votre fournisseur connecté :

| Intervalle | Description |
|----------|-------------|
| **En temps réel** | Toutes les 15 minutes. Idéal pour les boutiques ayant un volume important de ventes internationales. |
| **Hebdomadaire** | Une fois par heure. Bon équilibre entre fraîcheur et utilisation de l'API. |
| **Quotidien** | Une fois par jour. Adapté pour la plupart des boutiques. C'est le mode par défaut. |
| **Mensuel / Trimestriel** | Mises à jour moins fréquentes pour les boutiques qui changent rarement les taux. |
| **Uniquement manuel** | Les taux ne sont jamais récupérés automatiquement. Vous gérez tous les taux manuellement. |

L'intervalle de synchronisation affecte la fréquence à laquelle la tâche en arrière-plan récupère les taux auprès de votre fournisseur. Entre les synchronisations, les taux mis en cache sont utilisés. Si vous souhaitez forcer une synchronisation immédiate, utilisez le bouton **Synchroniser maintenant** sur le Tableau de bord des taux de change ou **Synchroniser depuis le fournisseur** sur la page des taux de change manuels.

## Taux de change manuels

Les taux de change manuels vous permettent de définir des taux de conversion exacts pour des paires de devises spécifiques. Ils prennent le pas sur les taux récupérés par le fournisseur, vous donnant un contrôle complet sur les prix.

Accédez à **Taux de change > Taux de change manuels** pour les gérer.

### Définition des taux manuellement

Cliquez sur **Ajouter un taux** pour créer un taux pour une paire de devises. Spécifiez la devise de base, la devise cible et le taux. Par exemple, définir USD/EUR à 0,92 signifie que 1 USD = 0,92 EUR.

### Synchronisation depuis un fournisseur

Cliquez sur **Synchroniser depuis le fournisseur** pour remplir automatiquement les taux manuels à partir des derniers taux de votre fournisseur connecté.

Cela crée des taux manuels pour toutes les devises prises en charge, vous donnant un point de départ pour affiner davantage.

Les taux verrouillés sont ignorés lors de la synchronisation, donc aucun des taux que vous avez ajustés manuellement ne sera écrasé.

### Verrouiller les taux

Cliquez sur l'icône de verrou sur tout taux pour l'empêcher d'être écrasé lors de la synchronisation avec le fournisseur. Cela est utile lorsque vous avez négocié un taux spécifique ou que vous souhaitez maintenir un taux fixe indépendamment des mouvements du marché.

- Les **taux verrouillés** affichent un badge de verrou et sont exclus de la synchronisation automatique.
- Les **taux non verrouillés** peuvent être mis à jour lorsque vous cliquez sur *Synchroniser depuis le fournisseur*.

### Comparaison des fournisseurs

Chaque taux manuel affiche le taux actuel du fournisseur à côté de lui, avec une différence en pourcentage. Cela vous aide à voir à un coup d'œil comment vos taux manuels se comparent aux taux du marché :

- Un pourcentage **vert** signifie que votre taux est plus élevé que le taux du fournisseur.
- Un pourcentage **rouge** signifie que votre taux est plus bas que le taux du fournisseur.

## Marge sur le taux de change

Vous pouvez ajouter une marge en pourcentage aux taux de change pour couvrir les frais de conversion de devise et protéger contre les fluctuations de taux entre le moment où un client passe une commande et celui où vous recevez le paiement.

Par exemple, une marge de 2 % sur un taux de change de 1,18 USD/EUR l'ajusterait à environ 1,20 USD/EUR. Ce petit buffer aide à garantir que vous ne perdez pas d'argent sur les conversions de devise.

## Stratégie de sélection des taux

Lorsque vous avez plusieurs fournisseurs de taux de change connectés, vous pouvez choisir la manière dont les taux sont sélectionnés :

- **Fournisseur principal** - Utilise toujours les taux de votre fournisseur principal désigné. Cela garantit un prix cohérent à travers votre magasin. Si le fournisseur principal n'a pas de données pour un couple de devises, il revient au taux le plus récent disponible auprès de tout fournisseur.
- **Plus récent disponible** - Utilise le taux le plus récemment synchronisé provenant de tout fournisseur actif. Cela vous donne les données les plus récentes, mais les taux peuvent varier légèrement entre les fournisseurs.

Pour la plupart des magasins, **Fournisseur principal** est le choix recommandé car il fournit le prix le plus prévisible.

## Devise prise en charge

Utilisez le gestionnaire de devise glisser-déposer pour choisir les devises prises en charge par votre magasin :

1. **Devises disponibles** (colonne de gauche) affiche toutes les devises que vous pouvez activer.
2. **Devises actives** (colonne de droite) affiche les devises actuellement activées sur votre magasin.
3. Glissez les devises entre les colonnes pour les activer ou les désactiver.
4. Glissez à l'intérieur de la colonne Active pour réorganiser l'ordre dans lequel les devises apparaissent dans le commutateur.
5. Cliquez sur **Enregistrer la configuration des devises** pour appliquer vos modifications.

Votre devise de base est toujours active et ne peut pas être supprimée.

## Comment les taux de change sont résolus

Lorsqu'un prix doit être converti, le système vérifie les taux dans cet ordre :

1. **Taux de change manuel** - Si un taux manuel actif existe pour le couple de devises, il est toujours utilisé en premier.
2. **Taux du fournisseur** - Si aucun taux manuel n'existe, le taux le plus récent de votre fournisseur connecté est utilisé.

Cela signifie que vous pouvez utiliser des fournisseurs pour la plupart des devises et remplacer des paires spécifiques avec des taux manuels là où vous avez besoin d'un contrôle précis.

## Important : Ce paramètre est permanent

Une fois que le multi-devise est activé et que les clients passent des commandes en devises étrangères, ce paramètre **ne peut pas être désactivé**. Cela est dû au fait que :

- Les commandes stockent définitivement la devise choisie par le client et le taux de change utilisé au moment de l'achat.
- Les rapports financiers et les calculs de remboursement dépendent de ces données historiques en devise.
- Désactiver le multi-devise laisserait les commandes existantes en devise multiple dans un état incohérent.

Si aucune commande n'a été passée en devises étrangères, vous pouvez toujours désactiver le multi-devise.

## Conseils

Conservez tout le formatage markdown, les chemins d'image, les blocs de code et les termes techniques.

- **Testez avec une commande petite première** - Placez une commande de test en devise étrangère pour vérifier le flux de paiement et vous assurer que les taux de change sont appliqués correctement.
- **Surveillez régulièrement les taux de change** - Vérifiez régulièrement le tableau de bord des taux de change pour vous assurer que votre fournisseur synchronise les taux et qu'ils semblent raisonnables.
- **Pensez à un markup pour les devises volatiles** - Si vous supportez des devises à forte volatilité, un markup légèrement plus élevé (2-3 %) peut protéger vos marges.
- **Commencez par les principales devises** - Commencez par les devises largement utilisées (EUR, GBP, JPY, CAD, AUD) et étendez-vous en fonction de la demande des clients.
- **Vérifiez la compatibilité avec le fournisseur de paiement** - Tous les fournisseurs de paiement ne supportent pas toutes les devises.

Vérifiez la documentation de votre fournisseur de paiement pour confirmer les devises qu'ils traitent.
- **Utilisez le mode Affichage uniquement si vous n'êtes pas sûr** - Si vous n'êtes pas sûr que votre fournisseur de paiement gère le paiement en plusieurs devises, commencez par le mode Affichage uniquement.

Vous pouvez passer en mode Multi-devise complète plus tard.
- **Verrouillez les taux avant les périodes promotionnelles** - Si vous faites une promotion, verrouillez vos taux de change à l'avance pour garantir des prix cohérents pendant toute la promotion.