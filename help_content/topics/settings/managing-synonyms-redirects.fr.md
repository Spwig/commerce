---
title: Gestion des synonymes et des redirections
---

Les synonymes et les redirections rendent votre recherche plus intelligente en gérant les termes équivalents et en routant des requêtes spécifiques vers des pages ciblées. Les synonymes étendent les recherches pour inclure des termes liés (« laptop » trouve également « notebook »), tandis que les redirections envoient des requêtes comme « sale » directement vers votre page de vente. Ce guide explique comment créer et gérer ces fonctionnalités pour améliorer la pertinence des recherches et l'expérience client.

Utilisez des synonymes pour l'équivalence des termes et des redirections pour des raccourcis de navigation.

![Liste des synonymes](/static/core/admin/img/help/managing-synonyms-redirects/synonym-list.webp)

## Comprendre les synonymes

Les synonymes indiquent au système de recherche que certains termes doivent être traités comme équivalents. Lorsqu'un client recherche un terme, le système inclut automatiquement les résultats correspondant aux termes synonymes.

**Exemple** : Créez une carte de synonymes « laptop » → « notebook », « ordinateur portable ». Maintenant, lorsqu'une personne recherche « laptop », elle obtient également des résultats pour les produits contenant « notebook » ou « ordinateur portable » dans leurs noms ou descriptions.

Les synonymes sont particulièrement utiles pour :
- L'anglais britannique vs américain (jumper/sweater, trainers/sneakers)
- Les termes de marque vs généraux (tissues/Kleenex)
- Les fautes de frappe courantes (accommodate/accomodate)
- Le jargon du secteur vs le langage courant (CPU/processor)

## Créer des synonymes

Accédez à **Search > Synonyms** et cliquez sur **+ Ajouter un synonyme**.

![Formulaire d'ajout d'un synonyme](/static/core/admin/img/help/managing-synonyms-redirects/synonym-form.webp)

**Term** - Le terme de recherche original qui déclenche l'expansion des synonymes

**Synonyms** - Tableau JSON des termes équivalents, par exemple `['sweater', 'pullover', 'jumper']`

**Bidirectional** - Par défaut : Coché. Lorsqu'il est activé, les relations de synonymes fonctionnent dans les deux sens :
- Recherche « laptop » trouve les produits « notebook »
- Recherche « notebook » trouve les produits « laptop »

Décochez pour des cartes unidirectionnelles (voir ci-dessous).

**Language** - Optionnel. Limitez ce synonyme aux recherches dans une langue spécifique. Laissez vide pour l'appliquer à toutes les langues.

**Engine** - Optionnel. Limitez ce synonyme à un moteur de recherche spécifique. Laissez vide pour l'appliquer globalement.

**Active** - Indique si ce synonyme est actuellement utilisé. Décochez pour le désactiver temporairement sans le supprimer.

## Exemples de synonymes bidirectionnels

La plupart des synonymes devraient être bidirectionnels - des équivalents véritables qui fonctionnent dans les deux sens :

| Term | Synonyms | Use Case |
|------|----------|----------|
| laptop | notebook, portable computer | Anglais américain/britannique + termes généraux |
| sofa | couch, settee | Variations régionales |
| trainers | sneakers, running shoes | Anglais britannique/Américain |
| mobile | cell phone, cellular | Variations internationales |

Avec le bidirectionnel activé, tous ces termes trouvent les mêmes produits indépendamment du terme utilisé par le client.

## Exemples de synonymes unidirectionnels

Décochez « Bidirectional » pour les relations unidirectionnelles :

**Cas d'utilisation courants** :
- **Fautes de frappe** : Terme : « accomodat » → Synonymes : `['accommodate']` (unidirectionnel donc la bonne orthographe ne trouve pas la faute de frappe)
- **Spécifique → Général** : Terme : « MacBook » → Synonymes : `['laptop']` (les MacBooks sont des ordinateurs portables, mais tous les ordinateurs portables ne sont pas des MacBooks)
- **Abréviations** : Terme : « CPU » → Synonymes : `['processor']` (CPU trouve les produits processor, mais les recherches processor ne devraient pas toujours inclure CPU)

## Synonymes spécifiques à une langue

Utilisez le champ Language pour créer des synonymes adaptés à une région : 

**Exemple** : Magasin en anglais britannique
- Terme : « jumper », Synonymes : `['sweater', 'pullover']`, Language : English (UK)
- Terme : « trainers », Synonymes : `['sneakers']`, Language : English (UK)

**Exemple** : Magasin multilingue
- Terme : « ordinateur portable », Synonymes : `['laptop', 'notebook']`, Language : French
- Terme : « zapatos », Synonymes : `['shoes']`, Language : Spanish

Les synonymes spécifiques à une langue ne s'appliquent que lorsque les clients naviguent dans cette langue.

## Synonymes spécifiques à un moteur

La plupart des synonymes devraient s'appliquer globalement (laissez le champ Engine vide). Utilisez des synonymes spécifiques à un moteur uniquement lorsque différents contextes de recherche nécessitent des cartes de termes différentes : 

**Exemple** : Vous avez des moteurs « shop » et « blog » séparés
- Synonyme du blog : Terme : « tutorial » → Synonymes : `['guide', 'how-to']`, Engine : blog
- Ce synonyme s'applique uniquement aux recherches de blog, pas aux recherches de produits

## Comprendre les redirections

Les redirections de recherche envoient directement des requêtes spécifiques vers des pages désignées, contournant les résultats de recherche normaux. Utilisez des redirections lorsque vous savez exactement où un client doit aller.

**Exemple** : Créez une redirection pour « sale » → `/products/sale/`. Maintenant, lorsqu'une personne recherche « sale », elle saute les résultats de recherche et atterrit directement sur votre page de vente.

Les redirections sont idéales pour : 
- Des raccourcis de navigation courants (« returns » → page de politique de retour)
- Des promotions saisonnières (« summer sale » → collection d'été)
- Des catégories populaires (« laptops » → page de catégorie d'ordinateurs portables)
- Des pages de politique (« shipping » → informations sur l'expédition)

![Liste des redirections](/static/core/admin/img/help/managing-synonyms-redirects/redirect-list.webp)

## Types de correspondance

Les redirections prennent en charge quatre types de correspondance qui contrôlent à quel point la requête de recherche doit correspondre strictement : 

**Exact** - Correspondance exacte insensible à la casse. La requête doit correspondre exactement au terme (en ignorant la majusculation).
- Terme : « sale »
- Correspondances : « sale », « SALE », « Sale »
- Ne correspond pas : « summer sale », « on sale »

**Contains** - La requête contient le terme n'importe où.
- Terme : « sizing »
- Correspondances : « sizing guide », « help with sizing », « what sizing »
- Ne correspond pas : « size chart » (mot différent)

**Starts With** - La requête commence par le terme.
- Terme : « return »
- Correspondances : « returns », « return policy », « returning items »
- Ne correspond pas : « how to return » (ne commence pas par le terme)

**Regex** - Correspondance de motif à l'aide d'expressions régulières. **⚠️ Avertissement de performance** - les motifs d'expressions régulières complexes ralentissent les recherches. Utilisez-les avec parcimonie.
- Motif : `^(laptop|notebook)s?$`
- Correspondances : « laptop », « laptops », « notebook », « notebooks »
- Utilisez uniquement si les autres types de correspondance ne fonctionnent pas

## Créer des redirections

Accédez à **Search > Redirects** et cliquez sur **+ Ajouter une redirection**.

![Formulaire d'ajout d'une redirection](/static/core/admin/img/help/managing-synonyms-redirects/redirect-form.webp)

**Term** - La requête de recherche à correspondre

**Match Type** - Exact, Contains, Starts With, ou Regex (voir ci-dessus)

**Redirect URL** - Où envoyer le client. Peut être relatif (`/products/sale/`) ou absolu (`https://example.com/page/`)

**Redirect Type** - Code d'état HTTP : 
- **302 (Temporaire)** : Recommandé. Le navigateur ne met pas en cache, vous pouvez changer l'URL de destination plus tard
- **301 (Permanent)** : Le navigateur et les moteurs de recherche mettent en cache. Utilisez uniquement pour les redirections permanentes

**Engine** - Optionnel. Limitez à un moteur de recherche spécifique

**Hit Count** - Incrémente automatiquement chaque fois que cette redirection est utilisée. Aide à identifier les raccourcis de navigation les plus utilisés.

**Active** - Activer/désactiver cette redirection

## Exemples de redirections

| Term | Match Type | URL | Use Case |
|------|-----------|-----|----------|
| sale | Exact | `/products/sale/` | Redirige les recherches « sale » vers la page de vente |
| clearance | Exact | `/clearance/` | Saute les résultats de recherche pour les articles en solde |
| sizing | Contains | `/pages/size-guide/` | Toute requête concernant la taille va vers le guide |
| return | Starts With | `/pages/returns/` | Les requêtes liées aux retours vont vers la politique |

Toutes utilisent des redirections 302 (temporaires) pour plus de flexibilité.

## Type de redirection : 302 vs 301

**302 (Temporaire)** - Recommandé pour la plupart des redirections
- Le navigateur effectue une nouvelle requête à chaque fois
- Vous pouvez changer l'URL de destination à tout moment
- Choix plus sûr si vous n'êtes pas certain

**301 (Permanent)** - Utilisez avec parcimonie
- Le navigateur met en cache la redirection
- Les moteurs de recherche mettent à jour leurs index
- Plus difficile à modifier plus tard

**Recommandation** : Utilisez 302 sauf si vous êtes absolument certain que la redirection ne changera jamais.

## Analyse des comptes d'impact

Le champ Hit Count s'incrémente automatiquement chaque fois qu'une redirection est déclenchée. Utilisez cela pour : 
- Identifier les raccourcis de navigation les plus utilisés
- Trouver les redirections qui ne sont jamais utilisées (considérez les supprimer)
- Découvrir les schémas de recherche populaires

Revuez les comptes d'impact mensuellement pour optimiser votre stratégie de redirection.

## Identifier les opportunités de synonymes

**Utilisez les requêtes sans résultats** : Accédez à **Search > Search Analytics** et filtrez les requêtes sans résultats. Cela révèle : 
- Des termes utilisés par les clients qui ne correspondent pas à vos descriptions de produits
- Des variations régionales que vous n'avez pas considérées
- Des fautes de frappe courantes

**Workflow** : 
1. Révisez les requêtes sans résultats hebdomadairement
2. Identifiez les motifs (mêmes termes apparaissant répétitivement)
3. Ajoutez des synonymes pour mapper le langage des clients à vos noms de produits
4. Surveillez si les requêtes sans résultats diminuent

## Conseils

- **Surveillez les requêtes sans résultats hebdomadairement pour obtenir des idées de synonymes** - Elles révèlent les écarts entre le langage des clients et vos descriptions de produits
- **Commencez par les synonymes courants, étendez-vous en fonction des données** - Commencez par les variations régionales évidentes, puis ajoutez en fonction du comportement de recherche réel
- **Utilisez le bidirectionnel pour les équivalents véritables** - La plupart des synonymes devraient fonctionner dans les deux sens (laptop ↔ notebook)
- **Évitez les motifs d'expressions régulières complexes** - La correspondance avec des expressions régulières est plus lente que d'autres types de correspondance ; utilisez-les uniquement si nécessaire
- **Utilisez par défaut des redirections 302 (temporaires)** - Cela vous donne de la flexibilité pour changer les destinations plus tard
- **Testez les synonymes avec des requêtes réelles** - Recherchez les termes synonymes pour vérifier s'ils retournent les résultats attendus
- **Synonymes spécifiques à une langue pour les magasins multilingues** - Créez des cartes de termes adaptés à chaque langue que vous supportez