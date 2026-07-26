---
title: Configuration de l'affichage client POS
---

Chaque article ajouté ou retiré, avec la quantité et le prix"
    },
    {
      "type": "list-item",
      "content": "Le sous-total du panier, les remises appliquées et le décompte des taxes"
    },
    {
      "type": "list-item",
      "content": "Le montant dû et, pendant le paiement, le montant versé et le reste"
    }
  ],
  "PARAGRAPH_3": "Lorsque le terminal est inactif (aucune transaction active), l'affichage passe à un diaporama promotionnel. Vous contrôlez le contenu de ce diaporama séparément — consultez [Diapositives promotionnelles de l'affichage client](customer-display-promo-slides).",
  "HEADING_2": "Configurations matérielles courantes",
  "PARAGRAPH_4": "Il existe trois façons pratiques de configurer un écran destiné aux clients :",
  "LIST_2": [
    {
      "type": "list-item",
      "content": "**Tablette ou moniteur séparé sur un support** — la configuration la plus courante pour les ventes au comptoir. Une petite tablette posée sur un support fait face au client pendant que votre terminal principal fait face à vous. Vous mettez en paire les deux appareils à l'aide d'un code à durée limitée (décrit ci-dessous)."
    },
    {
      "type": "list-item",
      "content": "**Deuxième moniteur en mode bureau étendu** — si votre terminal principal est un ordinateur portable ou un ordinateur de bureau, branchez un deuxième moniteur, étendez votre bureau vers celui-ci, puis faites glisser la fenêtre d'affichage sur le deuxième moniteur et maximisez-la. Les deux écrans fonctionnent sur le même appareil ; aucun code de mise en paire n'est nécessaire."
    },
    {
      "type": "list-item",
      "content": "**Écran dédié sur une colonne** — un appareil d'affichage matériel monté sur une colonne, généralement connecté au terminal du comptoir via un port USB ou positionné sur le comptoir. Ouvrez `/pos/display/` dans le navigateur de l'appareil de la colonne et mettez-le en paire à l'aide du code provenant du terminal principal."
    }
  ],
  "HEADING_3": "Activer l'affichage client sur un terminal",
  "PARAGRAPH_5": "La fonction d'affichage client est activée par terminal via la configuration matérielle du terminal.",
  "LIST_3": [
    {
      "type": "list-item",
      "content": "Accédez à **POS > Terminals** et ouvrez le terminal que vous souhaitez configurer (ou cliquez sur **+ Ajouter un terminal POS** pour un nouveau terminal)."
    },
    {
      "type": "list-item",
      "content": "Cliquez sur l'onglet **Device**."
    },
    {
      "type": "list-item",
      "content": "Faites défiler jusqu'à la carte **Configuration matérielle**. Vous verrez un champ JSON."
    },
    {
      "type": "list-item",
      "content": "Ajoutez `"customer_display": true` à l'objet JSON. Par exemple :"
    },
    {
      "type": "code-block",
      "content": "```json
{
  "customer_display": true
}
```"
    },
    {
      "type": "list-item",
      "content": "Si le champ contient déjà d'autres paramètres matériels (comme la configuration d'imprimante ou de scanner), ajoutez `"customer_display": true` à côté d'eux :"
    },
    {
      "type": "code-block",
      "content": "```json
{
  "printer": {"type": "network", "url": "http://192.168.1.100:9100"},
  "scanner": "keyboard_wedge",
  "customer_display": true
}
```"
    },
    {
      "type": "list-item",
      "content": "Cliquez sur **Enregistrer**."
    }
  ],
  "IMAGE": {
    "type": "image",
    "content": "![Configuration matérielle du terminal avec customer_display activé](/static/core/admin/img/help/pos-customer-display-setup/terminal-capabilities-toggle.webp)"
  },
  "PARAGRAPH_6": "Une fois activé, l'application POS sur ce terminal ouvrira la vue d'affichage client dans une deuxième fenêtre ou onglet du navigateur lors du démarrage d'une session.",
  "HEADING_4": "Mettre en paire un appareil séparé en tant qu'affichage",
  "PARAGRAPH_7": "Si vous utilisez un appareil physique séparé pour l'écran client (une tablette, un téléphone ou un deuxième ordinateur), vous le mettez en paire avec le terminal à l'aide d'un code à durée limitée à 6 chiffres.",
  "HEADING_5": "Étape 1 : Générer un code de mise en paire sur le terminal principal

Ouvrez l'application POS sur votre terminal principal et accédez aux paramètres d'affichage ou à la section de liaison du terminal.

Demandez un nouveau code de liaison d'affichage.

Le code est un nombre à 6 chiffres et est valide pendant **5 minutes**.

Lorsque vous générez un nouveau code, tous les codes précédents non utilisés pour ce terminal sont automatiquement annulés.

### Étape 2 : Ouvrez l'URL d'affichage sur le dispositif client

Sur le dispositif destiné aux clients, ouvrez un navigateur web et accédez à :

```
https://your-store-domain.com/pos/display/
```

Aucune connexion n'est requise — la page d'affichage est publiquement accessible. Cela est intentionnel : le dispositif d'affichage n'a pas besoin de crédentiels du personnel, et le code de liaison établit le lien entre l'affichage et le terminal correct.

![Vue d'affichage client inactive](/static/core/admin/img/help/pos-customer-display-setup/customer-display-view.webp)

### Étape 3 : Entrez le code de liaison

Sur le dispositif client, entrez le code à 6 chiffres provenant du terminal principal. L'affichage se liera à ce terminal et commencera à afficher les données du panier en temps réel.

Une fois le code utilisé, il est immédiatement invalidé et ne peut plus être réutilisé.

## Regénérer un code de liaison

Si le code de liaison expire avant que vous ne puissiez l'entrer, ou si vous devez relier à nouveau le dispositif d'affichage (par exemple, si un dispositif d'affichage est remplacé ou réinitialisé), générez un nouveau code depuis l'application POS sur le terminal principal.

La génération d'un nouveau code annule automatiquement tout code existant non utilisé pour ce terminal. Le nouveau code est valide pendant 5 minutes.

Vous n'avez pas besoin de modifier quoi que ce soit dans l'administration pour régénérer un code — cela se fait entièrement à l'intérieur de l'application POS.

## Configuration multi-écran sur un seul dispositif

Si votre terminal principal est un ordinateur portable ou un ordinateur de bureau avec deux écrans :

1. Connectez le deuxième écran et définissez-le en mode **bureau étendu** dans les paramètres d'affichage de votre système d'exploitation (et non en mode miroir).
2. Ouvrez l'application POS sur l'écran principal comme d'habitude.
3. L'application POS ouvrira l'affichage client dans une deuxième fenêtre. Déplacez cette fenêtre vers le deuxième écran.
4. Maximisez ou passez en mode plein écran sur le deuxième écran.

Aucun code de liaison n'est requis car les deux fenêtres s'exécutent sur le même dispositif et communiquent directement.

## Comportement en mode inactif

Lorsqu'il n'y a pas de vente active, l'affichage client affiche un diaporama en rotation d'images promotionnelles. Vous créez et gérez ces diapositives séparément sous **POS > Diapositives promotionnelles**.

Pour plus de détails sur la création de diapositives, leur ciblage vers des magasins spécifiques et la gestion du contenu saisonnier, consultez [Diapositives promotionnelles de l'affichage client](customer-display-promo-slides).

Si aucune diapositive n'est configurée, l'affichage affiche un écran d'accueil simple avec le nom de votre magasin.

## Dépannage

**L'affichage est devenu vide ou a arrêté de mettre à jour**

L'affichage communique en temps réel avec le terminal principal. Si la connexion est interrompue, l'affichage peut devenir vide ou afficher des données obsolètes. Actualisez le navigateur sur le dispositif client. Si cela ne fonctionne pas, générez un nouveau code de liaison et reliez à nouveau l'affichage.

**L'affichage affiche le panier du mauvais terminal**

Chaque affichage est lié à un terminal spécifique. Si vous avez plusieurs terminaux, assurez-vous que vous avez généré le code de liaison sur le terminal correct et que vous l'avez entré sur l'affichage. Pour corriger un désaccord, générez un nouveau code sur le terminal correct et reliez à nouveau le dispositif d'affichage.

**Le code de liaison a expiré avant que je ne puisse l'entrer**

Les codes sont valides pendant 5 minutes. Générez un nouveau code depuis l'application POS et entrez-le rapidement sur le dispositif d'affichage. Gardez les deux dispositifs proches l'un de l'autre pendant le processus de liaison.

**Le code de liaison a été entré mais l'affichage n'a pas établi la connexion**

Vérifiez que le dispositif client peut accéder à votre domaine de magasin (il a besoin d'un accès réseau). Vérifiez également que `"customer_display": true` est défini dans la configuration matérielle du terminal et que le terminal a été enregistré.

**L'URL de l'affichage renvoie une erreur**

Assurez-vous que vous accédez à `/pos/display/` sur votre domaine de magasin et non à l'URL d'administration. La vue d'affichage n'exige pas de connexion — si vous êtes invité à vous connecter, vérifiez à nouveau l'URL.

## Conseils

Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques.

- **Gardez la session de liaison courte** — assurez-vous que l'appareil du client est prêt et que le navigateur est ouvert sur `/pos/display/` avant de générer le code de liaison.

Vous avez 5 minutes, mais terminer cela en moins d'une minute évite le dépassement du délai.
- **Testez avant d'ouvrir** — effectuez un test de vente avec l'écran connecté pour vérifier que les clients verront les articles et les totaux corrects avant votre première transaction réelle.
- **Ajoutez un signet à l'URL de l'écran** — configurez le navigateur de l'appareil client pour ouvrir `/pos/display/` au démarrage afin qu'il soit toujours prêt.
- **Utilisez un bureau étendu pour plus de simplicité** — si votre terminal dispose d'une prise HDMI disponible et d'un moniteur, l'approche du bureau étendu n'exige aucune liaison continue et ne expire jamais.
- **Ajoutez des diapositives promotionnelles avant d'ouvrir** — un écran vide qui affiche uniquement un écran d'accueil vide représente une opportunité manquée.

Configurez au moins quelques diapositives promotionnelles afin que l'écran soit utile même lorsque aucune vente n'est en cours.

Voir [Diapositives promotionnelles de l'écran client](customer-display-promo-slides).
- **Sécurisez l'appareil d'affichage** — l'URL de l'écran est accessible publiquement par conception, mais elle n'affiche les données du panier en temps réel que lorsqu'elle est associée à un terminal actif.

Toutefois, envisagez le mode navigateur kiosque sur l'appareil client pour empêcher les clients de naviguer ailleurs.