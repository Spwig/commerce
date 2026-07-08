---
title: Configuration des impôts
---

Configurez les règles d'impôt pour votre magasin afin que les impôts corrects soient automatiquement appliqués aux commandes en fonction de l'emplacement du client. Vous pouvez charger des paramètres régionaux avec un seul clic ou créer des règles personnalisées pour tout pays, état, ville ou code postal.

![Tableau de bord des impôts](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## Tableau de bord des impôts

Accédez à **Commandes > Envois > Taux d'impôt** pour ouvrir le tableau de bord des impôts. La page affiche :

- **Panneau des statistiques** — quatre cartes affichant Total Rules, Active Rules, Countries Covered, et Tax Types en cours d'utilisation
- **Filtres** — recherchez par nom, pays ou état, et filtrez par pays, type d'impôt (Sales Tax, VAT, GST, Custom), ou statut (Actif/Inactif)
- **Cartes des règles d'impôt** — chaque carte affiche le drapeau du pays, le nom de la règle, l'emplacement, le pourcentage du taux, le badge du type d'impôt, le badge du statut, la priorité, et le nombre d'exemptions

## Chargement des paramètres d'impôt

Cliquez sur **Charger les paramètres** pour ouvrir le modal des paramètres. Les paramètres sont des collections de taux d'impôt standard pour une région, prêts à être chargés dans votre magasin avec un seul clic.

![Charger les paramètres](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

Les paramètres sont organisés par région du monde :

| Région | Groupes de paramètres |
|--------|---------------------|
| **Afrique** | TVA Afrique (25 taux) |
| **Asie-Pacifique** | TVA/TVA de l'Asie-Pacifique (24 taux), TVA de l'Asie centrale (6 taux) |
| **Europe** | Taux de TVA de l'UE, TVA du Royaume-Uni, Autres TVA européennes |
| **Amérique latine** | TVA de l'Amérique latine |
| **Moyen-Orient** | TVA du Moyen-Orient |
| **Amérique du Nord** | TVA étatique des États-Unis, TVA/HST canadien |
| **Océanie** | TVA/GST de l'Océanie |

### Fonctionnement des paramètres

1. Cliquez sur **Charger** sur le groupe de paramètres souhaité
2. Le système crée des règles d'impôt pour chaque pays ou état de ce groupe
3. Les règles existantes avec le même pays, état et type d'impôt sont automatiquement ignorées pour éviter les doublons
4. Après le chargement, chaque règle est entièrement modifiable — ajustez les taux, ajoutez des exemptions ou désactivez les règles que vous n'avez pas besoin

Vous pouvez charger plusieurs groupes de paramètres. Par exemple, chargez à la fois les TVA de l'UE et les TVA du Royaume-Uni si vous vendez à des clients à travers l'Europe.

## Création manuelle des règles d'impôt

Cliquez sur **Ajouter un taux d'impôt** pour créer une règle personnalisée. Le formulaire comporte quatre sections :

![Formulaire de taux d'impôt](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### Informations de base

| Champ | Description |
|-------|-------------|
| **Nom** | Nom d'affichage de la règle (par exemple, « TVA de Californie ») |
| **Actif** | Interrupteur pour activer ou désactiver la règle |
| **Type d'impôt** | TVA, TVA, GST ou Impôt personnalisé |
| **Taux (%)** | Le taux d'impôt en pourcentage (par exemple, entrez 8,25 pour 8,25 %) |
| **Priorité** | Les numéros plus élevés prennent le dessus lorsqu'il y a plusieurs règles correspondant au même emplacement |

### Portée géographique

| Champ | Description |
|-------|-------------|
| **Pays** | Code ISO 3166-1 alpha-2 (par exemple, US, GB, DE) |
| **État** | État ou province (laissez vide pour appliquer à l'ensemble du pays) |
| **Ville** | Nom de la ville (optionnel, pour les règles d'impôt au niveau de la ville) |
| **Codes postaux** | Liste de codes postaux spécifiques (optionnel, pour les règles d'impôt au niveau des codes postaux) |

Les règles sont correspondantes de la plus spécifique à la moins spécifique. Une règle pour un code postal spécifique a la priorité sur une règle pour le même état, qui a la priorité sur une règle nationale.

### Règles d'application

| Champ | Description |
|-------|-------------|
| **S'applique aux frais d'expédition** | Lorsqu'elle est cochée, cette taxe s'applique également aux frais d'expédition |
| **Taxe composée** | Lorsqu'elle est cochée, cette taxe est calculée sur les autres taxes (le montant de base plus les taxes déjà appliquées) |

### Exemptions de produits

| Champ | Description |
|-------|-------------|
| **Types de produits exonérés** | Types de produits exonérés de cette taxe (par exemple, numériques, services) |
| **Catégories de produits exonérés** | Catégories de produits spécifiques exonérées de cette taxe |

## Types d'impôts

| Type | Utilisé pour | Exemples |
|------|--------------|--------|
| **TVA** | États-Unis, Canada | Taxes sur la vente à l'état et provincial |
| **TVA** | Europe, Royaume-Uni, beaucoup d'Asie et d'Afrique | Taxe sur la valeur ajoutée |
| **GST** | Australie, Nouvelle-Zélande, Inde, Singapour | Taxe sur les biens et services |
| **Impôt personnalisé** | Cas spéciaux | Surcharges locales, taxes environnementales, taxes sur les biens de luxe |

## Fonctionnement du calcul des impôts

Lorsqu'un client arrive à la caisse, le système calcule automatiquement les impôts en fonction de son adresse d'expédition :

1. **Correspondance géographique** — trouve toutes les règles actives qui correspondent au pays du client, puis réduit par état, ville et code postal
2. **Évaluation de la spécificité** — les règles plus spécifiques (code postal > ville > état > pays) sont classées plus haut
3. **Ordre de priorité** — au sein du même niveau de spécificité, les règles à plus haute priorité prennent le dessus
4. **Exemptions de produits** — les produits exonérés sont exclus de chaque règle applicable
5. **Taxes non composées** — calculées en premier sur le prix de base de chaque article
6. **Taxes composées** — calculées sur le prix de base plus toutes les taxes non composées déjà appliquées
7. **Taxe sur l'expédition** — si une règle a « S'applique aux frais d'expédition » activé, le coût d'expédition est inclus dans le montant taxable

Le décompte des impôts est stocké avec la commande afin que vous puissiez voir exactement quelles règles ont été appliquées et combien chacune a contribué.

## Configurations courantes

### Magasin de l'UE

1. Cliquez sur **Charger les paramètres** et chargez le groupe **Taux de TVA de l'UE**
2. Cela crée des règles de TVA pour tous les États membres de l'UE avec leurs taux standards actuels
3. Chargez éventuellement **TVA du Royaume-Uni** si vous vendez également au Royaume-Uni

### Magasin des États-Unis

1. Cliquez sur **Charger les paramètres** et chargez le groupe **TVA étatique des États-Unis**
2. Cela crée des règles de TVA pour tous les États des États-Unis qui collectent la TVA
3. Pour les taxes au niveau des villes, ajoutez manuellement des règles avec le champ ville rempli et une priorité plus élevée

### Magasin multi-régions

1. Chargez plusieurs groupes de paramètres pour chaque marché sur lequel vous vendez
2. Le système applique l'impôt correct en fonction de l'emplacement de chaque client
3. Ajustez les règles individuelles selon vos besoins spécifiques d'entreprise

## Conseils

- **Commencez par les paramètres** — chargez les groupes de paramètres pour vos marchés cibles, puis personnalisez les taux individuels plutôt que de créer chaque règle à partir de zéro.
- **Utilisez la priorité avec soin** — définissez des valeurs de priorité plus élevées pour les règles locales plus spécifiques afin qu'elles remplacent correctement les règles régionales plus larges.
- **Vérifiez soigneusement la taxe composée** — la taxe composée est rare. La plupart des juridictions utilisent une taxe simple (non composée). Activez uniquement la taxe composée lorsque vos réglementations locales exigent spécifiquement le calcul de la taxe sur la taxe.
- **Maintenez les règles actives/inactives** — plutôt que de supprimer des règles d'impôt pour des changements saisonniers ou temporaires, basculez-les en inactives et réactivez-les lorsqu'elles sont nécessaires.
- **Testez avant de lancer** — après avoir configuré vos règles d'impôt, placez un ordre de test depuis différentes adresses pour vérifier que les impôts corrects sont appliqués.