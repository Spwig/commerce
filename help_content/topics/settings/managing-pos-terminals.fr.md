---
title: Gestion des terminaux POS
---

La gestion des terminaux POS constitue la base de vos opérations de vente au détail. Chaque terminal représente un appareil physique (tablette, ordinateur ou matériel POS dédié) sur lequel le personnel traite les ventes. Configurez les terminaux avec des affectations de magasin, des autorisations du personnel, des intégrations matérielles et des paramètres de synchronisation hors ligne. Surveillez l'état des terminaux grâce à la puce de suivi en temps réel et déverrouillez à distance les terminaux en cas de problème. Une gestion correcte des terminaux garantit une opération en magasin fluide et empêche les conflits de configuration entre les emplacements.

Accédez à **POS > Terminaux** pour enregistrer de nouveaux terminaux, consulter l'état en ligne/hors ligne et gérer toutes les configurations de terminaux.

![Liste des terminaux](/static/core/admin/img/help/managing-pos-terminals/terminal-list.webp)

## Vue de la liste des terminaux

La liste des terminaux affiche tous les terminaux enregistrés avec des informations d'état clés:

**Nom du terminal** - Étiquette descriptive du terminal (ex. : "Caisse 1", "Caisse principale", "Terminal mobile")

**UUID** - Identifiant unique généré automatiquement à la création (utilisé internement pour l'identification des appareils)

**Magasin** - Emplacement physique assigné à ce terminal (détermine la disponibilité des stocks et l'attribution des commandes)

**Statut en ligne** - Indicateur en direct montrant si le terminal est actuellement connecté:
- **Point vert** - En ligne (puce reçue au cours des 5 dernières minutes)
- **Point rouge** - Hors ligne (aucune puce depuis plus de 5 minutes)
- **Point gris** - Jamais appairé (terminal créé mais appareil jamais connecté)

**Dernière puce** - Horodatage de la dernière demande ping du terminal (mis à jour toutes les 5 minutes lorsqu'en ligne)

**Code d'appairage** - Code alphanumérique de 8 caractères utilisé pour l'appairage initial de l'appareil (caché après la première utilisation)

**Utilisateurs assignés** - Nombre de membres du personnel autorisés à utiliser ce terminal

## Création d'un nouveau terminal

Cliquez sur **+ Ajouter un terminal** pour enregistrer un nouveau dispositif POS:

![Formulaire d'ajout de terminal](/static/core/admin/img/help/managing-pos-terminals/terminal-add-form.webp)

### Configuration de base

**Nom du terminal** - Choisissez un nom descriptif qui indique:
- Emplacement physique : "Caisse d'entrée nord"
- Fonction : "Terminal de remboursements"
- Séquence : "Caisses 1", "Caisses 2", "Caisses 3"

Les noms aident le personnel à identifier les terminaux lors de l'affectation des shifts et de la résolution des problèmes. Utilisez des conventions de nommage cohérentes dans toutes les locations.

**Magasin** - **REQUIS** - Sélectionnez le magasin à partir duquel ce terminal opère:
- Détermine les stocks disponibles pour la vente
- Les commandes passées sur ce terminal sont attribuées à ce magasin
- Les réservations de stock vérifient la disponibilité dans le magasin assigné
- **Impossible de traiter des ventes sans affectation de magasin**

Si vous avez plusieurs emplacements de vente, créez un magasin distinct pour chaque emplacement et affectez les terminaux en conséquence.

**Actif** - Basculer pour activer/désactiver le terminal sans supprimer la configuration:
- Les terminaux inactifs ne peuvent pas être appairés
- Les sessions existantes sur les terminaux inactifs expirent immédiatement
- Utilisez pour désactiver temporairement les terminaux volés ou endommagés

### Affectation du personnel

**Utilisateurs assignés** - Sélectionnez les membres du personnel qui peuvent accéder à ce terminal:
- Seuls les utilisateurs assignés peuvent se connecter au terminal
- Les utilisateurs doivent également avoir des autorisations POS dans leur rôle de personnel
- Affecter zéro utilisateur verrouille effectivement le terminal
- Schéma courant : Affecter tous les employés du magasin à tous les terminaux du magasin

**Exemples d'utilisation**:
- **Magasin général** : Affecter tous les employés à tous les terminaux (n'importe quel caissier peut travailler n'importe quelle caisse)
- **Magasin par département** : Affecter les employés spécifiques aux terminaux par département
- **Multi-emplacements** : Affecter les employés spécifiques aux terminaux par emplacement
- **Gestionnaires** : Affecter la gestion à tous les terminaux pour un accès de supervision

Les utilisateurs sans affectation de terminal voient l'erreur "Non autorisé pour ce terminal" lorsqu'ils tentent de se connecter.

### Configuration matérielle

Le champ **Configuration matérielle** est une structure JSON définissant les périphériques externes:

**Imprimante thermique**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  }
}
```

**Lecteur de codes-barres USB**:
```json
{
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  }
}
```

**Caisse enregistreuse** (connectée à l'imprimante):
```json
{
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

**Exemple complet**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  },
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  },
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

Laissez vide si le terminal n'a aucun périphérique (adapté aux terminaux mobiles ou tablettes sans imprimante/scanneur).

### Paramètres de cache hors ligne

Configurez la quantité de données que le terminal cache pour le fonctionnement hors ligne:

**Jours de synchronisation des commandes** (7-30 jours, par défaut : 14):
- Nombre de jours de commandes récentes à stocker localement
- Plus de valeur = plus de données historiques disponibles hors ligne
- Moins de valeur = synchronisation plus rapide, moins d'espace de stockage utilisé
- **Recommandation** : 7 jours pour les terminaux à fort volume, 14 jours pour une utilisation normale, 30 jours pour les opérations d'audit intensives

**Limite de synchronisation des commandes** (200-1000 commandes, par défaut : 500):
- Nombre maximum de commandes à stocker indépendamment de la plage de dates
- Empêche l'utilisation excessive de l'espace de stockage sur les terminaux à fort volume
- **Recommandation** : 200 pour les tablettes à faible espace de stockage, 500 pour les terminaux standards, 1000 pour les dispositifs POS dédiés

**Compromis**:
- **Paramètres plus élevés** : Meilleur accès hors ligne aux données historiques, synchronisation initiale plus lente, plus d'espace de stockage utilisé
- **Paramètres plus bas** : Synchronisation plus rapide, moins d'espace de stockage, historique hors ligne limité

Le terminal télécharge les X commandes les plus récentes (dans les Y jours) lors de chaque cycle de synchronisation. Si le terminal traite 50 commandes par jour et que sync_days est de 14, prévoyez environ 700 commandes stockées (peut atteindre la limite de synchronisation).

## Workflow d'appairage des terminaux

Après avoir créé un terminal, appairez l'appareil physique:

1. **Générer le code d'appairage** - Créé automatiquement lors de l'enregistrement du terminal (8 caractères alphanumériques)

2. **Noter le code** - Affiché dans la liste des terminaux et dans la vue détaillée (expiré après la première appairage réussie)

3. **Accédez au terminal physique** - Sur l'appareil physique (tablette/ordinateur), ouvrez le navigateur et allez à : `https://yourstore.com/pos/`

4. **Entrez le code d'appairage** - Tapez le code à 8 caractères lorsque demandé

5. **Le terminal télécharge la configuration** - L'appareil reçoit:
   - Affectation du magasin
   - Configuration matérielle (imprimante, scanneur, caisse)
   - Paramètres de cache hors ligne
   - Liste des utilisateurs assignés
   - Synchronisation initiale du catalogue de produits

6. **Écran de connexion apparaît** - Le terminal affiche l'écran de connexion pour les utilisateurs assignés

7. **Le personnel se connecte** - Entrez les identifiants de l'utilisateur assigné à ce terminal

8. **La synchronisation initiale est terminée** - Le terminal télécharge:
   - Commandes récentes (selon sync_days et sync_limit)
   - Catalogue complet de produits pour le magasin assigné
   - Base de données clients
   - Configurations de promotions

9. **Le terminal est prêt** - L'écran "Prêt pour la vente" apparaît avec la barre de recherche

10. **Code d'appairage utilisé** - Le code est supprimé de l'admin ; générez un nouveau code si un nouvel appairage est nécessaire

**Régénération du code d'appairage** : Si vous avez besoin de réappairer un terminal (réinitialisation de l'appareil, suppression du cache du navigateur, nouveau matériel), utilisez l'action **Régénération du code d'appairage** dans l'admin. Cela invalide l'ancien code et en crée un nouveau.

## Surveillance de l'état du terminal

### Système de puce

Les terminaux envoient un signal de puce au serveur toutes les **5 minutes** contenant:
- UUID du terminal
- Horodatage actuel
- Nombre d'utilisateurs en ligne
- Horodatage de la dernière synchronisation
- État du service worker

**Indicateur de statut en ligne**:
- **Vert** - Puce reçue au cours des 5 dernières minutes (terminal en ligne et opérationnel)
- **Rouge** - Aucune puce depuis plus de 5 minutes (terminal hors ligne ou déconnecté)
- **Gris** - Terminal jamais appairé (aucune puce jamais reçue)

**Cas d'utilisation**:
- **Ouverture quotidienne** : Vérifiez que tous les terminaux sont en ligne avant l'ouverture du magasin
- **Dépannage** : Identifiez les terminaux qui rencontrent des problèmes de connectivité
- **Audit** : Vérifiez que les terminaux sont actifs pendant les heures d'ouverture

### Horodatage de la dernière puce

Affiche la date et l'heure exactes de la dernière puce. Utilisez cela pour:
- Déterminer depuis combien de temps un terminal est hors ligne
- Identifier les modèles (ex. : le terminal est hors ligne chaque nuit à la fermeture)
- Vérifier la fréquence de synchronisation (devrait être mis à jour toutes les ~5 minutes lorsqu'en ligne)

## Fonctionnalité de déverrouillage à distance

Lorsqu'un terminal devient non réactif ou coincé à l'écran (plantage logiciel, problème de timeout de session, blocage du navigateur), utilisez l'action **Déverrouillage à distance** dans l'admin:

**Fonctionnement**:
1. Sélectionnez le terminal problématique dans la liste admin
2. Choisissez **Déverrouillage à distance** dans le menu d'actions admin
3. Confirmez l'action
4. Le serveur envoie un signal de déverrouillage via la réponse de la puce
5. Le terminal reçoit le signal lors du prochain cycle de puce (<5 min)
6. Le terminal force la déconnexion de l'utilisateur actuel et retourne à l'écran de connexion

**Quand l'utiliser**:
- Terminal bloqué à l'écran de transaction
- Personnel incapable de se déconnecter (bouton de déconnexion non réactif)
- Session semble active mais le terminal est non réactif
- Navigateur planté mais le cookie de session persiste

**Important** : Le déverrouillage à distance ne redémarre pas l'appareil ou le navigateur - il force uniquement la déconnexion et la suppression de la session. Si le terminal est complètement bloqué, le personnel peut avoir besoin de redémarrer manuellement le navigateur ou l'appareil.

## Modification de la configuration du terminal

Cliquez sur un terminal dans la liste pour modifier sa configuration:

![Formulaire de modification du terminal](/static/core/admin/img/help/managing-pos-terminals/terminal-edit-form.webp)

**En toute sécurité à modifier même si le terminal est en ligne**:
- Nom du terminal
- Utilisateurs assignés
- Configuration matérielle (prend effet après le redémarrage de l'application du terminal)
- Paramètres de cache hors ligne (prend effet lors de la prochaine synchronisation)

**Nécessite un réappairage**:
- Affectation du magasin (le changement de magasin nécessite un réappairage pour synchroniser le nouveau stock)

**Ne peut pas être modifié**:
- UUID (identifiant immuable)

Les modifications de la plupart des paramètres s'appliquent lors du prochain cycle de puce/synchronisation. Les modifications de configuration matérielle nécessitent que le personnel ferme et rouvre l'application POS (ou actualise le navigateur).

## Résolution des problèmes courants

**Le terminal affiche "Non autorisé" lors de la connexion**:
- Vérifiez que l'utilisateur est dans la liste **Utilisateurs assignés** pour ce terminal
- Vérifiez que l'utilisateur a des autorisations POS dans **Personnel et autorisations > Rôles**
- Vérifiez que le terminal est marqué **Actif**

**Le terminal ne peut pas s'appairer (code invalide)**:
- Les codes d'appairage expirent après la première utilisation - régénérez si nécessaire
- Les codes sont sensibles à la casse - vérifiez la capitalisation
- Vérifiez que le terminal est marqué **Actif**

**Le terminal affiche hors ligne (point rouge)**:
- Vérifiez que l'appareil a une connexion internet
- Vérifiez que le terminal est effectivement en cours d'exécution (navigateur ouvert sur l'URL /pos/)
- Assurez-vous que le pare-feu ne bloque pas les demandes de puce
- Attendez 5 minutes pour le prochain cycle de puce

**Le terminal est lent à synchroniser**:
- Réduisez **Jours de synchronisation des commandes** de 30 à 7
- Réduisez **Limite de synchronisation des commandes** de 1000 à 200
- Vérifiez la vitesse du réseau au terminal
- Vérifiez que le serveur n'est pas sous charge

**Imprimante non fonctionnelle**:
- Vérifiez l'IP et le port de l'imprimante dans **Configuration matérielle**
- Testez la connectivité de l'imprimante depuis le terminal (ping de l'IP)
- Vérifiez que l'imprimante est compatible ESC/POS
- Vérifiez que l'imprimante est allumée et en ligne

## Conseils

- **La convention de nommage compte** - Utilisez un nommage cohérent (emplacement + numéro) pour simplifier la gestion à grande échelle
- **Affectez toujours le magasin avant l'appairage** - Les terminaux ne peuvent pas traiter des ventes sans affectation de magasin
- **Testez la configuration matérielle avant le déploiement** - Imprimez un reçu de test pour vérifier l'intégration de l'imprimante/caisse
- **Surveillez la puce quotidiennement** - Mettez en place une routine pour vérifier que tous les terminaux sont en ligne à l'ouverture du magasin
- **Réduisez les limites de synchronisation pour les terminaux mobiles** - Les tablettes et les téléphones bénéficient de sync_days : 7, sync_limit : 200
- **Utilisez le déverrouillage à distance avec modération** - La déconnexion forcée interrompt les transactions en cours ; confirmez que le terminal est effectivement bloqué avant d'utiliser cette fonction
- **Documentez les codes d'appairage** - Notez le code avant de déployer le terminal sur le terrain de vente (au cas où l'installation prendrait plus longtemps que prévu)
- **Affectez un gestionnaire à tous les terminaux** - Assurez-vous que les superviseurs peuvent accéder à toute caisse pour les annulations, les remboursements et le dépannage

