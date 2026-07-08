---
title: Modèles d'e-mail
---

Les modèles d'e-mail contrôlent la conception et le contenu de chaque e-mail automatisé que votre magasin envoie aux clients et à vous-même — confirmations de commande, mises à jour de livraison, réinitialisation de mot de passe, notifications de remboursement, et bien plus encore. La modification d'un modèle modifie tous les e-mails futurs de ce type ; les e-mails précédents déjà dans la boîte d'envoi ne sont pas affectés.

Accédez à **Email System > Email Templates** pour consulter et gérer vos modèles.

![Liste des modèles d'e-mail](/static/core/admin/img/help/email-templates/templates-list.webp)

## Types de modèles

Votre magasin inclut des modèles pour une large gamme d'événements. Ils sont regroupés par catégorie :

### E-mails liés aux commandes du client
| Modèle | Envoyé lors de |
|----------|-----------|
| Confirmation de commande | Un client achète un produit |
| Confirmation de paiement | Un paiement est traité avec succès |
| Commande expédiée | Une commande est marquée comme expédiée |
| Confirmation d'expédition | Un numéro de suivi est ajouté |
| Confirmation de livraison | Une commande est marquée comme livrée |
| Commande annulée | Une commande est annulée |
| Notification de retard | Un retard est enregistré sur une commande |
| Notification de remboursement | Un remboursement est émis |

### E-mails liés au compte
| Modèle | Envoyé lors de |
|----------|-----------|
| Bienvenue sur le compte | Un client crée un compte |
| Invitation au compte | Vous invitez un client à créer un compte |
| Vérification de l'e-mail | Un client vérifie son adresse e-mail |
| Réinitialisation du mot de passe | Un client demande une réinitialisation du mot de passe |

### Retours
| Modèle | Envoyé lors de |
|----------|-----------|
| Retours : Demande reçue | Un client soumet une demande de retour |
| Retours : Approuvée | Une demande de retour est approuvée |
| Retours : Refusée | Une demande de retour est refusée |
| Retours : Colis reçu | L'article retourné arrive à votre emplacement |
| Retours : Remboursement traité | Le remboursement d'un retour est émis |

### Notifications administrateur (envoyées à vous)
| Modèle | Envoyé lors de |
|----------|-----------|
| Admin : Nouvelle commande | Une nouvelle commande est passée |
| Admin : Paiement échoué | Un tentative de paiement échoue |
| Admin : Rapport de ventes quotidien | Le résumé des ventes quotidiennes est généré |
| Admin : Avertissement de stock bas | Un produit tombe en dessous de seuil de stock |
| Admin : Résumé hebdomadaire | Le résumé du magasin hebdomadaire est généré |

D'autres modèles couvrent les jalons de suivi des livraisons, l'activité du programme d'affiliation, les confirmations de réservation (si la fonctionnalité de réservation est activée), et les événements du programme de fidélité.

## Édition d'un modèle

1. Accédez à **Email System > Email Templates**
2. Trouvez le modèle que vous souhaitez modifier. Vous pouvez filtrer par **Type de modèle**, **Langue**, ou **Statut** en utilisant les filtres à droite
3. Cliquez sur le modèle pour l'ouvrir
4. Modifiez la **Ligne d'objet** (l'objet de l'e-mail affiché dans la boîte de réception du client)
5. Modifiez le **Contenu HTML** pour la version complète du design de l'e-mail
6. Modifiez éventuellement le **Contenu texte** — une version texte simple pour les clients de messagerie qui ne prennent pas en charge le HTML
7. Cliquez sur **Enregistrer**

> **E-mails HTML :** Le champ de contenu HTML accepte le HTML standard, y compris le CSS en ligne. Spwig rend ce dernier en un e-mail correctement formaté. Si vous utilisez des balises MJML, elles sont compilées automatiquement à l'enregistrement.

## Aperçu d'un modèle

Avant d'enregistrer, vous pouvez apercevoir l'apparence du modèle dans un client de messagerie :

1. Ouvrez le modèle que vous souhaitez apercevoir
2. Cliquez sur le bouton **Aperçu** (visible dans la liste des modèles ou sur la page de détail du modèle)
3. Un aperçu s'ouvre dans un nouvel onglet du navigateur, affichant l'e-mail rendu

Cela vous permet de vérifier le mise en page, le formatage et l'apparence des variables de placeholder avant que le modèle ne soit mis en ligne.

## Variables de modèle

Les variables sont des placeholders dans votre modèle que Spwig remplace par des données réelles lors de l'envoi de l'e-mail. Elles sont écrites comme `{{ variable_name }}`.

Variables courantes disponibles dans la plupart des modèles :

| Variable | Remplacé par |
|----------|---------------|
| `{{ customer_name }}` | Le nom complet du client |
| `{{ order_number }}` | Le numéro de référence de la commande |
| `{{ order_total }}` | Le montant total de la commande |
| `{{ store_name }}` | Le nom de votre boutique |
| `{{ store_url }}` | L'adresse web de votre boutique |
| `{{ tracking_number }}` | Le numéro de suivi du colis |
| `{{ tracking_url }}` | Un lien cliquable pour suivre le colis |

Les variables exactes disponibles dépendent du type de modèle. Les variables pertinentes pour un modèle lié à une commande (comme `{{ order_number }}`) ne sont pas disponibles dans un modèle de compte (comme Réinitialisation du mot de passe). Si vous incluez une variable qui ne s'applique pas, elle apparaîtra vide ou non remplacée.

## Prise en charge des langues

Chaque type de modèle peut avoir une version pour chaque langue que votre boutique prend en charge. Le champ **Langue** sur chaque modèle contrôle quelle version de langue est active.

Spwig sélectionne automatiquement la bonne version de langue en fonction des préférences linguistiques du client lors de l'envoi. Si aucun modèle n'existe pour la langue d'un client, Spwig revient à la version anglaise.

Pour ajouter un modèle pour une nouvelle langue :
1. Ouvrez un modèle existant
2. Cliquez sur **Cloner le modèle** dans le menu **Actions**
3. Définissez le **Code de langue** sur le clone pour la nouvelle langue
4. Traduisez le contenu
5. Activez le modèle cloné

## Clonage, activation et désactivation des modèles

### Clonage d'un modèle

Le clonage crée une copie exacte d'un modèle — utile pour créer des variantes linguistiques ou tester différentes versions sans affecter le modèle en production.

1. Sélectionnez un ou plusieurs modèles dans la liste
2. Choisissez **Cloner les modèles sélectionnés** dans le menu déroulant **Actions**
3. Le clone est créé comme inactif — éditez-le et activez-le lorsque vous serez prêt

### Activation et désactivation des modèles

Un modèle doit être **Actif** pour être utilisé pour l'envoi. Un seul modèle actif par type et combinaison de langue est utilisé à la fois.

Pour activer ou désactiver en masse :
1. Sélectionnez les modèles
2. Choisissez **Activer les modèles sélectionnés** ou **Désactiver les modèles sélectionnés** dans le menu déroulant **Actions**

Ou ouvrez un modèle individuel et basculez le bouton **Actif**.

## Modèles système

Les modèles marqués d'un badge **Système** sont les modèles par défaut fournis par Spwig. Ils ne peuvent pas être supprimés. Vous pouvez les modifier directement ou les cloner pour créer une version personnalisée.

## Conseils

- Ayez toujours un aperçu d'un modèle après l'édition pour détecter les problèmes de mise en forme avant que les clients ne les voient
- Gardez les lignes d'objet courtes et spécifiques — `Votre commande #10045 a été expédiée` fonctionne mieux que des sujets génériques comme `Mise à jour de notre boutique`
- Modifiez également le contenu en texte brut — certains clients de courriel ne montrent que la version en texte brut, et certains clients préfèrent celle-ci
- Clonnez la version anglaise d'un modèle comme point de départ avant de créer une version traduite
- Si vous souhaitez tester un changement sans affecter les courriels en production, clonez le modèle, modifiez la copie, et laissez les deux actifs brièvement pendant que vous vérifiez l'aperçu — puis désactivez l'original
- Les modèles de notification d'administrateur (comme **Administrateur : Nouvelle commande**) sont envoyés à l'adresse e-mail d'administrateur de votre boutique — assurez-vous que cette adresse e-mail est correcte dans les paramètres de votre boutique