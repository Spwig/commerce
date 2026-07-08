---
title: Préférences de transporteur
---

Les préférences de transporteur définissent les transporteurs manuels (DHL, FedEx, UPS, transporteurs personnalisés) pour les envois créés sans intégration API - chaque préférence fournit un logo de transporteur, un modèle d'URL de suivi et des paramètres d'affichage. Les préférences système (DHL, FedEx, UPS, USPS) sont préconfigurées et ne peuvent pas être supprimées, tandis que les préférences personnalisées permettent aux commerçants d'ajouter des transporteurs régionaux ou spécialisés. Les préférences sont liées aux envois manuels où les commerçants entrent manuellement les numéros de suivi au lieu d'acheter des étiquettes via les API des fournisseurs.

Utilisez les préférences de transporteur lors de la création d'envois manuels ou lorsque vous souhaitez des liens de suivi sans une intégration API complète.

## Préférences Système vs Préférences Personnalisées

**Préférences Système** (Préinstallées):
- DHL, FedEx, UPS, USPS, Royal Mail, Canada Post, Australia Post
- Ne peuvent pas être supprimées (is_system=True)
- Peuvent remplacer l'URL de suivi ou le logo
- Modèles d'URL de suivi par défaut fournis

**Préférences Personnalisées** (Créées par le commerçant):
- Transporteurs régionaux (OnTrac, LaserShip, transporteurs régionaux)
- Transporteurs spécialisés (transport en colis, livraison white-glove)
- Peuvent être modifiés ou supprimés
- Nécessite un modèle d'URL de suivi personnalisé

---

## Configuration des Préférences de Transporteur

Chaque préférence définit:

**Paramètres de Base**:
- **Nom**: Nom d'affichage du transporteur (ex. "DHL Express", "Courrier Local")
- **Code**: Identifiant interne (ex. "dhl", "local_courier")
- **Logo**: Image du logo du transporteur (optionnel, utilise l'icône si non fourni)
- **Icône**: Icône FontAwesome en tant qu'alternative (ex. "fa-truck")
- **Actif**: Basculer la visibilité

**Configuration de Suivi**:
- **Modèle d'URL de Suivi**: Modèle d'URL avec le marque-placer {tracking_id}
- **Remplacement d'URL de Suivi**: URL personnalisée (remplace le modèle par défaut)

**Paramètres Système** (uniquement pour les préférences système):
- **Est un Système**: Ne peut pas être supprimé
- **Est par Défaut**: Un par type de transporteur

---

## Modèles d'URL de Suivi

Les URLs de suivi utilisent le marque-placer {tracking_id}:

**Exemples**:

DHL: `https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}`

FedEx: `https://www.fedex.com/fedextrack/?tracknumbers={tracking_id}`

UPS: `https://www.ups.com/track?tracknum={tracking_id}`

USPS: `https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_id}`

Personnalisé: `https://track.localcourier.com/tracking/{tracking_id}`

**Fonctionnement**:
1. Le commerçant crée un envoi avec le numéro de suivi "1234567890"
2. Le système remplace {tracking_id} par le numéro réel
3. Le client clique sur le lien de suivi → redirection vers le site du transporteur
4. Résultat: `https://www.dhl.com/en/express/tracking.html?AWB=1234567890`

---

## Créer une Préférence de Transporteur Personnalisée

**Étapes à suivre**:

1. Accédez à Paramètres > Expédition > Préférences de transporteur
2. Cliquez sur "Ajouter une préférence de transporteur"
3. Entrez le nom (ex. "OnTrac")
4. Entrez le code (slug: "ontrac")
5. Optionnel : Téléchargez un logo
6. Sélectionnez une icône (fa-truck, fa-shipping-fast, etc.)
7. Entrez le modèle d'URL de suivi avec {tracking_id}
8. Activez l'option Actif = Oui
9. Enregistrez

**Exemple - OnTrac**:
```
Nom: OnTrac
Code: ontrac
URL de suivi: https://www.ontrac.com/tracking.asp?tracking_number={tracking_id}
Icône: fa-truck
Actif: Oui
```

---

## Remplacer les URLs de Suivi des Préférences Système

Les préférences système peuvent avoir des remplacements d'URL de suivi:

**Cas d'utilisation**: Votre compte de transporteur a un portail de suivi spécial

**Comment remplacer**:
1. Éditez la préférence système (ex. DHL)
2. Entrez l'URL de remplacement dans le champ "Remplacement d'URL de suivi"
3. Le remplacement a la priorité sur le modèle par défaut
4. Enregistrez

**Exemple**:
```
Système: DHL
URL par défaut: https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}
URL de remplacement: https://track.dhl.com/special-account/{tracking_id}
Résultat: URL de remplacement utilisée pour tous les envois DHL
```

---

## Logos des Transporteurs

**Lignes directrices pour les logos**:
- Format: PNG ou SVG (SVG recommandé pour l'échelle)
- Taille: 200×60px recommandée
- Arrière-plan: Transparent ou blanc
- Couleur: Marquage complet du transporteur

**Icône par défaut**:
Si aucun logo n'est téléchargé, le système affiche l'icône FontAwesome:
- fa-truck (défaut)
- fa-shipping-fast (express)
- fa-plane (transport aérien)
- fa-box (colis)

---

## Utilisation des Préférences de Transporteur dans les Envois

Lors de la création d'un envoi manuel:

1. Commandes > Détail de la commande > Créer un envoi
2. Sélectionnez le mode "Envoi manuel"
3. Choisissez le transporteur dans le menu déroulant des préférences
4. Entrez le numéro de suivi
5. Optionnel : Remplacer l'URL de suivi pour cet envoi
6. Enregistrez

**Affichage de l'envoi**:
- Logo du transporteur affiché (ou icône)
- Numéro de suivi affiché
- Lien de suivi cliquable (utilise le modèle d'URL de la préférence)

---

## Transporteur par Défaut

Un seul préférence peut être défini comme par défaut par système:

**Cas d'utilisation**: Transporteur le plus utilisé automatiquement sélectionné lors de la création d'envoi

**Comment définir**:
1. Éditez la préférence de transporteur
2. Cochez "Est par Défaut"
3. Enregistrez
4. La préférence par défaut précédente (si elle existe) est automatiquement désactivée

**Un seul préférence par défaut autorisé** - définir un nouveau préférence par défaut supprime le drapeau du préférence par défaut précédent.

---

## Conseils

- **Utilisez des noms descriptifs** - "DHL Express" est préférable à "DHL"
- **Testez les URLs de suivi** - Vérifiez que le modèle fonctionne avec des numéros de suivi réels
- **Téléchargez les logos des transporteurs** - Apparence professionnelle dans les emails clients
- **Ne supprimez pas les préférences système** - Elles sont correctement préconfigurées
- **Utilisez les remplacements avec parcimonie** - Seulement lorsque le transporteur change le système de suivi
- **Définissez le transporteur principal comme par défaut** - Économisez du temps lors de la création d'envois
- **Maintenez les préférences actives** - Désactivez uniquement si le transporteur est discontinué
- **Documentez les transporteurs personnalisés** - Ajoutez des notes sur les transporteurs régionaux


