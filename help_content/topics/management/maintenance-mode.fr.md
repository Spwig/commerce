---
title: Mode maintenance
---

Le mode maintenance met temporairement votre boutique en ligne hors ligne et affiche aux clients un message indiquant « nous reviendrons bientôt ». Votre arrière-plan administrateur reste pleinement accessible pendant le mode maintenance — vous pouvez continuer à travailler pendant que les clients sont redirigés vers la page de maintenance.

Utilisez le mode maintenance avant de faire des changements qui pourraient provoquer un état temporairement instable, comme l'exécution d'une importation de produits importante, l'application d'une refonte majeure du thème ou l'attente que l'opération de restauration se termine.

![Commutateur de mode maintenance sur le tableau de bord du système](/static/core/admin/img/help/maintenance-mode/system-dashboard-maintenance.webp)

## Activer le mode maintenance

1. Accédez à **Management > Métriques du système**
2. Cliquez sur **Tableau de bord du système** depuis la barre d'outils
3. Dans le panneau **Statut de la boutique**, cliquez sur **Activer le mode maintenance**
4. Entrez éventuellement une **raison** — ceci est à des fins de référence personnelle et n'est pas affiché aux clients (ex. : `Mise à jour du catalogue de produits en cours`)
5. Confirmez en cliquant sur **Activer**

Votre boutique en ligne commence immédiatement à afficher la page de maintenance à tous les visiteurs. L'arrière-plan administrateur n'en est pas affecté et vous pouvez continuer à travailler normalement.

## Ce que les clients voient

Lorsque le mode maintenance est actif, chaque page de votre boutique en ligne (le magasin, les pages produits, le processus de paiement et les pages du compte) affiche un message de maintenance personnalisé. Le message indique aux clients que la boutique est temporairement indisponible et les encourage à revenir bientôt.

Les clients qui sont en cours de session ou en cours de paiement au moment où le mode maintenance est activé verront également la page de maintenance lors de leur prochaine demande. Aucun ordre en cours n'est perdu — les données restent disponibles lorsque vous désactivez le mode maintenance.

## Désactiver le mode maintenance

1. Accédez à **Management > Métriques du système**
2. Cliquez sur **Tableau de bord du système**
3. Dans le panneau **Statut de la boutique**, vous verrez un bandeau confirmant que le mode maintenance est actif
4. Cliquez sur **Désactiver le mode maintenance**
5. Confirmez lorsque vous y êtes invité

La boutique revient en ligne immédiatement. Les clients peuvent naviguer et acheter comme d'habitude.

## Quand Spwig active automatiquement le mode maintenance

Certaines opérations du système activent automatiquement le mode maintenance et réactivent la boutique en ligne lorsqu'elles sont terminées :

- **Mises à jour du système** — le processus de mise à jour active le mode maintenance avant d'appliquer les changements et le désactive une fois la mise à jour terminée
- **Opérations de restauration** — la restauration à partir d'une sauvegarde met la boutique en mode maintenance pendant la durée de la restauration

Si une opération automatisée se termine de manière inattendue, le mode maintenance peut rester actif. Dans ce cas, suivez les étapes ci-dessus pour le désactiver manuellement.

## Conseils

- Informez toujours votre équipe avant d'activer le mode maintenance — cela affecte tous les visiteurs de votre boutique en ligne
- Gardez les périodes de maintenance aussi courtes que possible ; même quelques minutes hors ligne peuvent affecter la confiance des clients
- Utilisez le champ raison comme rappel pour vous-même sur la raison pour laquelle le mode maintenance a été activé — il apparaît dans le journal du système
- Si vous remarquez que le mode maintenance est actif mais que vous ne l'avez pas activé vous-même, vérifiez le journal du système pour voir si une opération automatisée l'a déclenché
- Planifiez les périodes de maintenance pendant les heures creuses (soirs ou matins tôt) pour minimiser l'impact sur les ventes