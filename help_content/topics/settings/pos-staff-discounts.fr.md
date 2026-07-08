---
title: Remises pour le personnel et sécurité du terminal POS
---

Les paramètres des remises pour le personnel POS vous permettent de contrôler le montant des remises que chaque membre du personnel peut appliquer au moment du paiement. Les événements de verrouillage du terminal fournissent un historique d'audit de chaque fois qu'un terminal a été verrouillé ou déverrouillé — vous aidant à suivre qui a accédé au terminal et si des tentatives de connexion échouées se sont produites.

## Limites des remises du personnel

Chaque membre du personnel utilisant le POS peut avoir des permissions de remise individuelles. Par défaut, le personnel peut appliquer jusqu'à 10 % de remise sur des articles ou sur l'ensemble du panier. Vous pouvez augmenter ou diminuer cette limite par personne, ou désigner du personnel comme gestionnaires capables d'approuver des remises dépassant les limites standard.

### Configuration de la limite de remise d'un membre du personnel

1. Accédez à **POS > Remises du personnel**
2. Cliquez sur **+ Ajouter une remise du personnel POS** ou cliquez sur un membre du personnel existant pour l'éditer
3. Sélectionnez le **Membre du personnel** dans la liste
4. Définissez les limites de remise :

| Champ | Description |
|-------|-------------|
| **Max Discount %** | Pourcentage maximal de remise que cette personne peut appliquer (ex. `10` pour 10 %) |
| **Max Discount Amount** | Montant fixe maximal par transaction (laissez vide pour aucun plafond fixe) |
| **Can Apply Item Discounts** | Permettre l'application de remises sur des éléments individuels |
| **Can Apply Cart Discounts** | Permettre l'application de remises sur le total du panier |
| **Requires Reason** | Lorsqu'il est coché, le membre du personnel doit saisir une raison avant d'appliquer toute remise |

5. Cliquez sur **Enregistrer**

### Fonctionnement des limites de remise au POS

Lorsqu'un caissier tente d'appliquer une remise :
- Si la remise est dans sa limite, elle est appliquée immédiatement
- Si la remise dépasse sa limite, le terminal demande une **approbation du gestionnaire**
- Un gestionnaire entre son code PIN pour autoriser la remise, puis la remise est appliquée

Ce workflow empêche les remises non autorisées de grande valeur tout en permettant de flexibilité lorsque des remises authentiques sont justifiées.

## Rôles de gestionnaire

Les membres du personnel avec le drapeau **Is Manager** peuvent approuver des remises dépassant les limites d'autres membres du personnel. Les gestionnaires sont identifiés au terminal par un code PIN qu'ils entrent lorsqu'une approbation est demandée.

### Configuration d'un gestionnaire

1. Ouvrez le dossier de remise d'un membre du personnel
2. Cochez **Is Manager**
3. Entrez un **Manager PIN** (4 à 6 chiffres) — ce code est haché de manière sécurisée lors de l'enregistrement
4. Cliquez sur **Enregistrer**

Le code PIN du gestionnaire est distinct du code PIN du caissier utilisé pour le verrouillage/déverrouillage du terminal. Un gestionnaire peut avoir à la fois un code PIN de gestionnaire (pour l'approbation des remises) et un code PIN de caissier (pour l'accès au terminal).

### Sécurité du code PIN du gestionnaire

Lorsque vous entrez un code PIN dans le formulaire d'administration et que vous l'enregistrez, Spwig le hache automatiquement — le code PIN brut n'est jamais stocké. Le champ de code PIN brut se vide après l'enregistrement, ce qui est un comportement attendu.

## Codes PIN des caissiers et accès par carte

Chaque membre du personnel peut également avoir un **Code PIN du caissier** pour verrouiller et déverrouiller le terminal :

- **Code PIN du caissier** — code PIN de 4 à 6 chiffres utilisé pour déverrouiller le terminal après qu'il s'est verrouillé automatiquement ou manuellement
- **Identifiant de carte** — Une carte enregistrée (carte à puce ou NFC) peut également être utilisée pour déverrouiller le terminal

Pour configurer un code PIN du caissier, saisissez-le dans le champ **Code PIN du caissier** et enregistrez-le. Comme le code PIN du gestionnaire, il est automatiquement haché lors de l'enregistrement.

## Événements de verrouillage du terminal

Chaque fois qu'un terminal est verrouillé ou déverrouillé, Spwig enregistre un événement de verrouillage du terminal. Cela crée un historique complet d'audit de la sécurité.

### Visionner les événements de verrouillage

Accédez à **POS > Événements de verrouillage du terminal** pour voir l'historique complet. Vous pouvez filtrer les événements par :
- Terminal
- Type d'événement
- Plage de dates

### Types d'événements

| Événement | Signification |
|-------|---------|
| **Verrouillage manuel** | Un membre du personnel a verrouillé délibérément le terminal |
| **Verrouillage automatique (délai d'inactivité)** | Le terminal a été verrouillé automatiquement en raison de l'inactivité |
| **Désverrouillage par caissier** | Le caissier s'est authentifié et a désverrouillé le terminal |
| **Désverrouillage par gestionnaire** | Un gestionnaire a utilisé ses identifiants pour désverrouiller le terminal |
| **Désverrouillage par carte** | Le terminal a été désverrouillé à l'aide d'une carte de swiping enregistrée |
| **Désverrouillage par biométrie** | Le terminal a été désverrouillé à l'aide d'une empreinte digitale ou de la reconnaissance faciale |
| **Essai de désverrouillage échoué** | Un essai de désverrouillage a été effectué avec des identifiants incorrects |
| **Verrouillage (3+ échecs)** | Le terminal a été verrouillé après plusieurs échecs répétés |

### Quels enregistrements d'événements de verrou contiennent

Chaque événement enregistre :
- Le **Terminal** concerné
- Le **Type d'événement**
- Qui a effectué l'action (**Effectué par**) et qui était connecté lors du verrou (**Verrouillé par**)
- Si un **Désactivation par gestionnaire** a été utilisée
- La **Méthode de désverrouillage** (code PIN, carte ou biométrie)
- **Essais échoués** avant cet événement (utiles pour détecter les motifs de force brute)
- Le **Total du panier** et le nombre d'articles au moment de l'événement
- L'**adresse IP** de la demande

### Enquêter sur une préoccupation de sécurité

Si vous soupçonnez un accès non autorisé à un terminal :

1. Accédez à **POS > Événements de verrou des terminaux**
2. Filtrez par le terminal en question
3. Cherchez des événements du type **Essai de désverrouillage échoué** ou **Verrouillage** — cela indique des accès répétés échoués
4. Vérifiez le champ **Effectué par** sur les désverrouillages réussis pour voir qui a obtenu l'accès
5. Vérifiez avec les enregistrements de poste de travail (**POS > Postes de travail**) pour confirmer le caissier qui devait être de garde

## Conseils

- Fixez des limites de remise en fonction du niveau d'expérience du personnel — le personnel nouveau peut commencer à 5 %, le personnel expérimenté à 10-15 %, et les gestionnaires peuvent approuver tout montant plus élevé.
- Activez **Exige une raison** pour tout personnel ayant des limites de remise plus élevées. Avoir une raison enregistrée vous aide à analyser les motifs de remise et à identifier tout abus.
- Vérifiez les événements de verrou des terminaux hebdomadairement si votre magasin a plusieurs employés ou un taux de rotation élevé — les motifs d'accès irréguliers sont plus faciles à détecter avant qu'ils ne deviennent un problème.
- Si un membre du personnel quitte, supprimez immédiatement son code PIN de caissier et son identifiant de carte pour empêcher l'accès au terminal.
- Utilisez l'événement de verrouillage pour identifier les terminaux qui pourraient avoir besoin d'un délai de verrouillage automatique ajusté — si les clients déclenchent fréquemment des verrouillages accidentels, le délai d'inactivité peut être trop court.
- Les codes PIN des gestionnaires doivent être changés périodiquement. Mettez-les à jour dans l'enregistrement des remises du personnel — le nouveau code PIN est haché à l'enregistrement.