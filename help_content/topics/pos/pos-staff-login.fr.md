---
title: Connexion du personnel POS & Identification biométrique
---

Chaque personne qui sert les clients à un terminal POS doit avoir un compte personnel avec les autorisations appropriées. Ce sujet explique comment créer ce compte, attribuer le membre du personnel à un terminal, puis configurer l'identification biométrique afin qu'ils puissent déverrouiller le terminal avec une empreinte digitale, un scan facial ou une clé matérielle au lieu de taper un mot de passe à chaque fois.

Pour les codes PIN, les limites de remise et les paramètres de verrouillage des terminaux, consultez [Remises du personnel POS & Sécurité du terminal](pos-staff-discounts).

## Ce dont un membre du personnel a besoin pour utiliser un terminal POS

Pour se connecter à un terminal POS, une personne a besoin de :

1. Un **compte personnel** — un utilisateur Spwig avec le drapeau **Statut personnel** activé.
2. Un **rôle incluant l'accès POS** — les rôles déterminent ce que le membre du personnel peut faire dans l'administration. Un rôle avec des autorisations POS est nécessaire pour accéder au terminal.
3. **Affectation à un terminal** — le terminal doit le lister comme membre du personnel affecté, ou il doit être affecté au niveau de l'emplacement du magasin.

## Créer un compte personnel éligible POS

Accédez à **Personnel & Comptes > Membres du personnel** (ou allez à `/admin/accounts/staffmember/`).

1. Cliquez sur **+ Ajouter un membre du personnel**.
2. Remplissez le **prénom**, le **nom de famille** et l'**adresse e-mail** du membre du personnel.
3. Définissez un mot de passe temporaire et demandez au membre du personnel de le changer lors de la première connexion.
4. Assurez-vous que **Statut personnel** est coché — c'est ce qui leur permet de se connecter à l'administration et à l'application POS.
5. Cliquez sur **Enregistrer**.

> **Remarque :** Ne cochez pas **Statut superutilisateur** pour les caissiers ou superviseurs normaux. Le statut superutilisateur contourne toutes les vérifications d'autorisation et doit être réservé au propriétaire du magasin.

### Affecter un rôle avec accès POS

Les comptes personnels n'ont pas de permissions par défaut — les rôles octorent les capacités spécifiques. Après avoir créé le compte, ouvrez le dossier du membre du personnel et allez dans l'onglet **Rôles**. Affectez un rôle incluant l'accès POS.

Pour une explication complète de la manière dont fonctionnent les rôles et des autorisations à inclure, consultez [Rôles du personnel](staff-roles).

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: staff-user-list.webp
  description: Liste des membres du personnel montrant un utilisateur éligible POS avec leur badge de rôle
-->

![Liste des membres du personnel](/static/core/admin/img/help/pos-staff-login/staff-user-list.webp)

## Affecter du personnel à un terminal

Les paramètres suivent une cascade : **Défaut du site → Groupe de magasin → Emplacement du magasin → Terminal individuel**. Pour la plupart des magasins, le bon endroit pour affecter du personnel est au niveau du terminal.

1. Accédez à **POS > Terminaux** (ou allez à `/admin/pos_app/posterminal/`).
2. Ouvrez le terminal que vous souhaitez configurer.
3. Allez à l'onglet **Affectation du personnel**.
4. Dans le champ **Personnel affecté**, recherchez et ajoutez le membre du personnel.
5. Cliquez sur **Enregistrer**.

Les membres du personnel qui apparaissent dans la liste **Personnel affecté** d'un terminal peuvent sélectionner leur nom sur l'écran de connexion de ce terminal. Les membres du personnel non affectés à aucun terminal peuvent tout de même se connecter en tapant directement leur e-mail.

> **Conseil :** Si votre magasin a beaucoup de personnel qui circulent entre les terminaux, affectez-les au niveau de l'emplacement du magasin (entrepôt) plutôt qu'un terminal par terminal. Tout membre du personnel affecté à l'emplacement a automatiquement accès à tous les terminaux de cet emplacement.

## Se connecter au terminal POS

Lorsqu'un caissier ouvre l'application POS (`/pos/`) sur un terminal, il voit un écran de sélection du personnel. Le processus de connexion fonctionne comme suit :

1. Le caissier touche ou clique sur son nom dans la liste (ou tape son e-mail s'il n'est pas listé).
2. Il entre son mot de passe.
3. Il est connecté et le terminal s'ouvre pour son shift.

Pour le déverrouillage basé sur un code PIN (après que le terminal se verrouille pendant un shift), consultez [Remises du personnel POS & Sécurité du terminal](pos-staff-discounts).

## Connexion biométrique

La connexion biométrique permet à un caissier de toucher un capteur d'empreinte digitale, de regarder une caméra faciale ou de taper une clé matérielle au lieu de taper un mot de passe. Sur un terminal occupé, cela économise plusieurs secondes par shift et évite les erreurs pendant les heures de pointe.

Spwig utilise la norme **WebAuthn** du navigateur pour la connexion biométrique.

Un "credential WebAuthn" est une paire de clés liée à un appareil : la clé privée est stockée dans le matériel sécurisé de l'appareil et ne quitte jamais cet appareil.

L'application POS communique avec ce matériel via le navigateur.

### Appareils et navigateurs qui prennent en charge la connexion biométrique

WebAuthn est pris en charge par tous les navigateurs modernes — Chrome, Edge, Firefox et Safari — sur les appareils dotés d'un matériel compatible. Configurations courantes qui fonctionnent bien :

| Appareil | Authentificateur |
|--------|---------------|
| iPad (Touch ID) | Empreinte digitale via Safari ou Chrome |
| Tablette Android | Empreinte digitale ou visage via Chrome |
| Tablette ou PC Windows | Windows Hello (empreinte digitale, visage ou code PIN) |
| Tout appareil + clé de sécurité | Clé FIDO2 USB, NFC ou Bluetooth (ex. YubiKey) |
| iPhone (Face ID) | Visage via Safari |

L'application POS affichera uniquement l'option de connexion biométrique lorsque le navigateur aura confirmé qu'un credential est enregistré pour l'utilisateur actuel sur cet appareil.

### Fonctionnement de l'enregistrement

L'enregistrement se fait au terminal POS, et non dans l'administration. Le membre du personnel doit d'abord effectuer une connexion normale avec un mot de passe, puis choisir d'activer la connexion biométrique depuis l'application POS. Le navigateur lui demande ensuite de vérifier son identité à l'aide du capteur biométrique de l'appareil (ou d'un passkey stocké dans son compte sur iOS/macOS/Windows). Une fois confirmé, le credential est stocké et la connexion biométrique est disponible pour les prochaines sessions sur cet appareil.

Un seul membre du personnel peut s'enregistrer sur plusieurs appareils — par exemple, une tablette personnelle et un caisson partagé — et chaque appareil conserve son propre credential.

> **Note :** Le texte exact de l'invite d'enregistrement ("Enregistrer la biométrie", "Configurer la connexion par empreinte digitale", etc.) provient de l'application POS et peut varier selon le navigateur et l'appareil.

### Connexion avec une biométrie

Une fois enregistré, le nom du caissier sur l'écran de connexion affichera un bouton de connexion biométrique (icône d'empreinte digitale ou similaire). Le caissier :

1. Appuie sur son nom sur l'écran de connexion du terminal.
2. Appuie sur **Se connecter avec l'empreinte digitale** (ou équivalent).
3. Appuie sur le capteur ou regarde la caméra.
4. Le terminal se déverrouille immédiatement.

Si la vérification biométrique échoue (doigt non reconnu, visage masqué), le caissier passe à l'entrée de son mot de passe.

### Révocation d'un credential

Si un appareil est perdu, volé ou si un membre du personnel quitte, vous devez supprimer immédiatement ses credentials biométriques.

1. Accédez à **Personnel & Comptes > Membres du personnel**.
2. Ouvrez le profil du membre du personnel.
3. Faites défiler jusqu'à la section **Paramètres POS**.
4. Dans la ligne **Déverrouillage biométrique**, cliquez sur **Supprimer tout**.
5. Confirmez l'action.

Cela supprime tous les credentials WebAuthn enregistrés pour ce membre du personnel sur tous les appareils. La prochaine fois qu'ils essaieront d'utiliser la connexion biométrique sur tout terminal, ils devront se connecter avec leur mot de passe à la place.

> **Important :** Supprimer les credentials ici n'empêche pas le membre du personnel de se connecter avec son mot de passe. Pour révoquer complètement l'accès, désactivez également leur compte de personnel ou supprimez-les de la liste des membres du personnel assignés au terminal.

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: webauthn-credential-list.webp
  description: Formulaire de modification du membre du personnel montrant la section Paramètres POS avec le nombre de credentials biométriques et le bouton Supprimer tout
-->

## Notes de sécurité

- **Les credentials sont liés au matériel.** La clé privée ne quitte jamais l'élément sécurisé de l'appareil.

Si un tablet est volé, un attaquant ne peut pas extraire la clé biométrique — ils devraient toujours devoir contourner l'écran de verrouillage du dispositif avant que le navigateur ne libère la clé.
- **Perdre un appareil ne fuit pas un mot de passe.** WebAuthn remplace le mot de passe pour cet appareil ; le mot de passe du membre du personnel est séparé et inchangé.
- **Révoquer immédiatement lors du départ du personnel.** Supprimez les informations biométriques et désactivez le compte du membre du personnel dans la même session lors de la sortie du personnel.
- **La biométrie elle-même n'est jamais transmise.** L'empreinte digitale ou le scan facial est entièrement traité par le matériel du dispositif.

Spwig ne reçoit qu'une réponse de défi signée, et non les données biométriques.

## Dépannage

### Le bouton "Se connecter avec l'empreinte digitale" ne s'affiche pas

L'option biométrique n'apparaît que si :
- Le membre du personnel a un credentiel inscrit sur cet appareil spécifique.
- Le navigateur prend en charge WebAuthn (tous les navigateurs modernes le font — mettez à jour si vous utilisez une version plus ancienne).

Si le bouton est absent, le membre du personnel n'a pas encore inscrit d'informations biométriques sur cet appareil. Ils devraient se connecter avec leur mot de passe et configurer l'authentification biométrique via l'application POS.

### Échec de l'inscription

Raisons courantes :
- **Permission du navigateur refusée.** Le navigateur a demandé la permission d'accéder à l'authentificateur et le membre du personnel a refusé. Ils doivent réessayer et appuyer sur **Autoriser** lors de la demande.
- **Aucun authentificateur compatible trouvé.** L'appareil n'a pas de capteur d'empreinte digitale, de caméra pour le visage ou de clé de sécurité attachée. Vérifiez le matériel de l'appareil.
- **Crédentiel en double.** Le membre du personnel a peut-être déjà inscrit des informations sur cet appareil. Les crédentiels existants sont exclus lors de la réinscription pour éviter les doublons.

### La biométrie a fonctionné sur un appareil mais pas sur un autre

Chaque appareil stocke ses propres crédentiels. L'inscription sur un iPad ne fonctionne pas automatiquement sur un deuxième iPad. Le membre du personnel doit terminer l'inscription séparément sur chaque appareil qu'ils utiliseront.

### Passkeys multi-appareils

Certains systèmes d'exploitation (iOS 16+, macOS Ventura+, Windows 11 avec un compte Microsoft) peuvent synchroniser les passkeys entre les appareils via iCloud Keychain ou Windows Hello. Si le membre du personnel s'est inscrit en utilisant un passkey synchronisé, il peut fonctionner automatiquement sur plusieurs appareils. Le comportement dépend du système d'exploitation et du navigateur, et non de Spwig.

## Conseils

- Configurez l'authentification biométrique sur les terminaux partagés avant l'arrivée des membres du personnel pour leur shift — le processus d'inscription de deux minutes est beaucoup plus fluide lorsqu'il est effectué sans clients en attente.
- Attribuez un rôle avec des permissions POS limitées aux caissiers et un rôle distinct de gestionnaire aux superviseurs. Gardez leurs comptes distincts du compte du propriétaire du magasin.
- Lorsqu'un membre du personnel change d'appareil (nouveau tablette, nouveau téléphone), faites-leur inscrire sur le nouveau dispositif en premier, puis révoquez l'ancien credentiel depuis l'admin si l'appareil n'est plus utilisé.
- Pour les magasins avec un taux de rotation élevé du personnel, examinez régulièrement la liste **Personnel affecté** sur chaque terminal et supprimez les membres du personnel qui ne travaillent plus à l'emplacement.
- Si vous utilisez des clés de sécurité matérielles (YubiKey ou similaire), une clé peut être inscrite sur plusieurs terminaux sans aucune modification de l'admin — il suffit de brancher la clé et de terminer l'inscription sur chaque terminal.