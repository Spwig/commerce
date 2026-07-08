---
title: Modèles SMS
---

Les modèles SMS contrôlent le texte de chaque notification que votre magasin envoie aux clients via les messages texte. Chaque modèle correspond à un événement spécifique — comme la confirmation d'une commande ou une mise à jour d'expédition — et utilise des variables de remplacement que Spwig remplace par les détails réels de la commande lors de l'envoi du message.

Accédez à **Système SMS > Modèles SMS** pour consulter et modifier vos modèles.

![Liste des modèles SMS](/static/core/admin/img/help/sms-templates/templates-list.webp)

## Types de modèles disponibles

Spwig inclut les types de modèles suivants :

| Type de modèle | Quand il est envoyé |
|---------------|---------------------|
| Confirmation de commande | Lorsqu'un client passe une commande |
| Mise à jour d'expédition | Lorsque le statut de suivi d'une commande change |
| Notification de livraison | Lorsqu'une commande est marquée comme livrée |
| Réinitialisation du mot de passe | Lorsqu'un client demande une réinitialisation du mot de passe |
| Code de vérification | Lorsqu'un code à usage unique est nécessaire pour la vérification du compte |
| Reçu POS | Lorsqu'un achat est traité à un terminal de point de vente |
| Marketing | Pour des campagnes promotionnelles (nécessite un consentement séparé) |
| Personnalisé | Pour toute autre notification que vous créez |

## Modifier un modèle

1. Accédez à **Système SMS > Modèles SMS**
2. Cliquez sur le modèle que vous souhaitez modifier
3. Mettez à jour le champ **Message** avec votre texte souhaité
4. Utilisez des placeholders `{variable}` pour inclure des informations spécifiques à la commande (voir les variables ci-dessous)
5. Cochez **Actif** pour activer le modèle — les modèles non actifs ne sont pas envoyés
6. Cliquez sur **Enregistrer**

![Modification d'un modèle SMS](/static/core/admin/img/help/sms-templates/template-edit.webp)

## Utilisation des variables

Les variables sont des placeholders écrits entre accolades — par exemple, `{name}` ou `{order_number}`. Lorsque Spwig envoie le message, il remplace chaque placeholder par la valeur réelle pour ce client ou cette commande.

### Variables courantes

| Variable | Remplacé par |
|----------|---------------|
| `{name}` | Le prénom du client |
| `{order_number}` | Le numéro de référence de la commande |
| `{total}` | Le montant total de la commande |
| `{tracking_number}` | Le numéro de suivi du colis |
| `{store_name}` | Le nom de votre magasin |
| `{code}` | Un code de vérification ou de réinitialisation |

**Exemple de message :**

```
Bonjour {name}, votre commande #{order_number} a été confirmée. Total : {total}. Nous vous tiendrons informé lors de l'expédition. - {store_name}
```

Lors de l'envoi, cela devient :

```
Bonjour Sarah, votre commande #10045 a été confirmée. Total : $89,00. Nous vous tiendrons informé lors de l'expédition. - The Garden Shop
```

> N'incluez que les variables disponibles pour un type de modèle donné. Par exemple, `{tracking_number}` est disponible dans un modèle de mise à jour d'expédition mais pas dans un modèle de réinitialisation du mot de passe. Si vous utilisez une variable non disponible, elle apparaîtra telle quelle (non remplacée) dans le message.

## Limites de caractères et longueur du message

Les messages SMS standards sont limités à **160 caractères** pour un seul segment. Les messages plus longs sont divisés en plusieurs segments et envoyés comme un seul message (SMS concaténé), mais les opérateurs comptent chaque segment séparément pour les facturations.

**Conseils pour rester dans la limite :**
- Gardez les messages concis — un seul objectif par message
- Abbréviez les phrases courantes là où c'est naturel (par exemple, « Ord » au lieu de « Order »)
- Évitez les mots inutiles

Spwig ne force pas de limite de caractères stricte dans l'éditeur, donc comptez vos caractères (y compris les valeurs des variables) avant d'enregistrer.

## Activer et désactiver les modèles

Le commutateur **Actif** sur chaque modèle contrôle si ce type de notification est envoyé. Si un modèle n'est pas actif, Spwig ignore complètement l'envoi de cette notification — le message apparaîtra comme **Ignoré** dans la boîte de sortie SMS avec la raison `template_inactive`.

Pour activer un modèle :
1. Ouvrez le modèle
2. Cochez la case **Actif**
3. Enregistrez

Pour désactiver (arrêter l'envoi d'un type de notification sans supprimer le modèle) :
1. Ouvrez le modèle
2. Décochez **Actif**
3. Enregistrez

## Conseils

Conservez tous les formats markdown, les chemins d'image, les blocs de code et les termes techniques.

- Utilisez un ton correspondant à celui de votre marque — le SMS est un canal direct et personnel, donc un ton amical convient bien
- Incluez toujours le nom de votre magasin dans le message pour que les clients sachent qui les contacte
- Gardez les messages de confirmation des commandes courts : le numéro de commande, le total et une note sur les étapes suivantes suffisent
- Testez les messages en passant une commande test sur votre propre magasin (en utilisant un numéro de téléphone que vous contrôlez) pour voir exactement ce que reçoivent les clients
- Si une notification génère de la confusion ou des réclamations, désactivez le modèle et révisez-le plutôt que de le supprimer — ainsi, vous pourrez le réactiver une fois les modifications apportées
- Les modèles de marketing ne doivent être envoyés qu'aux clients qui ont explicitement souscrit au marketing par SMS, conformément aux réglementations des télécommunications dans la plupart des pays