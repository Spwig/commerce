---
title: Configuration du CDN
---

Un réseau de distribution de contenu (CDN) stocke des copies des images, des feuilles de style et des scripts de votre magasin sur des serveurs à travers le monde. Lorsqu'un client visite votre magasin, ces fichiers sont fournis à partir du serveur le plus proche de lui plutôt qu'à partir de votre serveur d'hébergement principal. Cela réduit les temps de chargement des pages, surtout pour les clients situés loin de l'endroit où votre magasin est hébergé.

Spwig optimise déjà la livraison des actifs statiques par défaut avec la compression préalable Brotli et gzip, le stockage en cache des actifs avec des en-têtes immuables de 1 an, et une négociation de contenu appropriée. L'ajout d'un CDN est facultatif, mais il peut améliorer davantage la vitesse pour les magasins ayant une clientèle internationale.

## Votre magasin a-t-il besoin d'un CDN ?

Pas tous les magasins bénéficient également d'un CDN. Utilisez ces lignes directrices pour décider :

**Un CDN est recommandé si**:
- Vos clients sont répartis dans plusieurs pays ou continents
- Votre magasin présente de nombreuses images de produits ou des pages lourdes en médias
- Vous souhaitez les temps de chargement de page les plus rapides possible à l'échelle mondiale
- Vous vendez dans des régions éloignées de votre serveur d'hébergement (par exemple, serveur en Europe, clients en Asie)

**Un CDN est probablement inutile si**:
- Vos clients sont principalement locaux ou situés dans le même pays que votre serveur
- Votre magasin a un catalogue petit avec peu d'images
- Votre fournisseur d'hébergement inclut déjà un CDN intégré

Lorsque vous avez des doutes, un CDN n'altère pas les performances. Des services comme Cloudflare offrent des niveaux gratuits, donc il n'y a aucun coût pour essayer.

## Fonctionnement de Spwig avec les CDNs

Spwig est prêt à l'emploi avec les CDNs par défaut. Vous n'avez pas besoin de modifier tout code ou paramètres à l'intérieur du panneau d'administration Spwig. Voici ce que Spwig fait déjà pour vous :

- **Fichiers statiques avec empreinte digitale** -- Chaque fichier CSS, JavaScript et image inclut un hachage de version unique dans son nom de fichier. Cela signifie que les CDNs peuvent stocker en cache ces fichiers pendant une longue période sans fournir du contenu obsolète.
- **En-têtes de cache à long terme** -- Les actifs statiques sont fournis avec des en-têtes de cache immuables de 1 an, informant les CDNs et les navigateurs de les stocker de manière agressive.
- **Fichiers pré-compressés** -- Spwig compresse préalablement les actifs à l'aide de Brotli et gzip, donc votre CDN peut livrer des fichiers plus petits sans traitement supplémentaire.
- **Négociation de contenu appropriée** -- Spwig envoie les en-têtes de type de contenu et d'encodage corrects sur lesquels les CDNs s'appuient pour un stockage en cache correct.

Tout ce que vous avez à faire, c'est de pointer les DNS de votre domaine vers le fournisseur de CDN, et tout fonctionne automatiquement.

## Configuration de Cloudflare

Cloudflare est le CDN le plus populaire et propose un niveau gratuit qui convient bien à la plupart des magasins. Suivez ces étapes :

**Étape 1 : Créer un compte Cloudflare**
- Visitez cloudflare.com et inscrivez-vous à un compte gratuit

**Étape 2 : Ajouter votre domaine**
- Cliquez sur **Ajouter un site** et entrez le nom de domaine de votre magasin
- Sélectionnez le **plan gratuit** (suffisant pour la plupart des magasins)

**Étape 3 : Mettre à jour les serveurs de noms DNS**
- Cloudflare vous montrera deux serveurs de noms (par exemple, `anna.ns.cloudflare.com`)
- Connectez-vous à votre registrar de domaine (où vous avez acheté votre domaine)
- Remplacez vos serveurs de noms actuels par les serveurs de noms de Cloudflare
- Les changements DNS peuvent prendre jusqu'à 24 heures pour prendre effet

**Étape 4 : Configurer SSL/TLS**
- Dans le tableau de bord Cloudflare, allez à **SSL/TLS**
- Définissez le mode d'encodage sur **Full (strict)**
- Cela garantit que tout le trafic entre Cloudflare et votre serveur reste chiffré

**Étape 5 : Vérifier qu'il fonctionne**
- Une fois que les DNS se propagent, visitez votre magasin et vérifiez l'en-tête `cf-cache-status` dans votre navigateur (voir Vérifier votre CDN ci-dessous)

## Configuration d'AWS CloudFront

Si vous utilisez déjà Amazon Web Services, CloudFront s'intègre naturellement à votre infrastructure :

1. Ouvrez le **console CloudFront** dans votre compte AWS
2. Créez un nouveau **Distribution** avec le domaine de votre magasin comme origine
3. Définissez la **politique de protocole d'origine** sur "HTTPS Only"
4. Sous **Comportement de mise en cache**, définissez la **politique de mise en cache** sur "CachingOptimized" pour les actifs statiques
5. Ajoutez le domaine de votre magasin comme **Nom de domaine alternatif (CNAME)**
6. Attachez un certificat SSL depuis AWS Certificate Manager
7. Mettez à jour les DNS de votre domaine pour pointer vers l'URL de la distribution CloudFront

Le tarif de CloudFront est basé sur l'utilisation.

Pour la plupart des magasins, les coûts sont minimes puisque les actifs de Spwig sont mis en cache pendant de longues périodes.

## Paramètres CDN recommandés

Pour obtenir les meilleurs résultats, configurez votre CDN afin de mettre en cache le contenu approprié et de passer à côté du reste.

**Ce qui doit être mis en cache** (actifs statiques) :
- `/static/` -- Tous les styles, scripts, polices et actifs de thème
- `/media/` -- Images de produits et fichiers multimédias téléchargés
- Fichiers d'images (`.jpg`, `.png`, `.webp`, `.svg`, `.gif`)
- Fichiers de polices (`.woff`, `.woff2`)

**Ce qui ne doit pas être mis en cache** (pages dynamiques) :
- `/admin/` -- Le panneau d'administration doit toujours fournir du contenu frais
- `/cart/` -- Les pages de panier contiennent des données spécifiques à la session
- `/checkout/` -- Les pages de paiement ne doivent jamais être mises en cache pour des raisons de sécurité
- `/accounts/` -- Les pages de compte client contiennent des données privées
- Toute page nécessitant une connexion ou affichant du contenu personnalisé

**Règles de mise en cache générales** :
- **Respecter les en-têtes de cache d'origine** -- Spwig envoie les bons en-têtes de contrôle de cache pour chaque type de contenu. Configurez votre CDN pour respecter ces en-têtes plutôt que de les remplacer.
- **Activer la compression Brotli** -- À la fois Cloudflare et CloudFront prennent en charge Brotli. Activez-le pour tirer parti des actifs pré-compressés de Spwig.
- **Définir le TTL de mise en cache du navigateur sur "Respecter les en-têtes existants"** -- Cela permet à la politique de mise en cache intégrée de Spwig de déterminer le comportement.

## Vérification de votre CDN

Après la configuration, confirmez que le CDN fournit correctement votre contenu :

**Étape 1 : Ouvrir les outils de développement du navigateur**
- Dans Chrome ou Firefox, appuyez sur **F12** pour ouvrir les outils de développement
- Cliquez sur l'onglet **Réseau**

**Étape 2 : Charger votre magasin**
- Visitez la page d'accueil de votre magasin avec les outils de développement ouverts
- Cliquez sur toute demande de fichier statique (par exemple, un fichier `.css` ou `.js`)

**Étape 3 : Vérifier les en-têtes de réponse**
- **Cloudflare** : Cherchez l'en-tête `cf-cache-status`. Une valeur de `HIT` signifie que le fichier a été fourni à partir du cache du CDN. `MISS` signifie qu'il a été récupéré depuis votre serveur (seule la première demande).
- **CloudFront** : Cherchez l'en-tête `x-cache`. Une valeur de `Hit from cloudfront` confirme la livraison via le CDN.

**Étape 4 : Tester depuis un autre emplacement**
- Utilisez un outil gratuit comme gtmetrix.com ou webpagetest.org pour tester votre magasin depuis différentes localisations géographiques
- Comparez les temps de chargement avant et après la mise en place du CDN

## Problèmes courants

### Contenu obsolète après des modifications de thème

**Problème** : Après avoir mis à jour votre thème ou effectué des modifications de design, les clients voient toujours l'ancienne version.

**Solution** : Nettoyez le cache de votre CDN. Dans Cloudflare, allez dans **Caching > Configuration > Purge Everything**. Dans CloudFront, créez une **Invalidation** pour `/*`. Notez que les actifs de Spwig avec empreinte digitale empêchent généralement ce problème, car les fichiers mis à jour reçoivent automatiquement de nouveaux noms de fichiers. Ce problème affecte le plus souvent les actifs non empreintés comme les uploads personnalisés.

---

### Avertissements de contenu mixte

**Problème** : Votre navigateur affiche un avertissement de sécurité concernant le "contenu mixte" après l'activation du CDN.

**Solution** : Assurez-vous que le mode SSL de votre CDN est défini sur **Full (strict)**, et non sur "Flexible". Le mode Flexible peut entraîner le fait que votre serveur reçoive des requêtes HTTP au lieu de HTTPS, ce qui provoque des avertissements de contenu mixte. Dans Cloudflare, vérifiez **SSL/TLS > Overview** et vérifiez le mode.

---

### Panneau d'administration lent

**Problème** : Le panneau d'administration semble plus lent après l'ajout d'un CDN.

**Solution** : Les CDNs ne doivent pas mettre en cache les pages d'administration. Créez une **Règle de page** (Cloudflare) ou un **Comportement de mise en cache** (CloudFront) qui définit la mise en cache sur "Bypass" pour toute URL correspondant à `/admin/*`. Cela garantit que les demandes d'administration passent directement à votre serveur sans surcharge du CDN.

---

### Les images ne s'affichent pas

**Problème** : Les images de produits ou les fichiers multimédias renvoient des erreurs après la configuration du CDN.

**Solution** : Vérifiez que l'origine de votre CDN est configurée avec le protocole correct (HTTPS) et le port. Vérifiez également que le pare-feu de votre serveur autorise les connexions provenant des plages d'adresses IP du CDN.

## Conseils

Conservez tous les formats de markdown, les chemins d'image, les blocs de code et les termes techniques.

- **Commencez avec le niveau gratuit de Cloudflare** -- Il couvre les besoins de la plupart des magasins et ne prend que quelques minutes pour être configuré
- **Utilisez toujours le mode SSL complet (strict)** -- Le mode flexible crée des vulnérabilités de sécurité et peut perturber les flux de paiement
- **Nettoyez votre cache CDN après des mises à jour importantes du thème** -- Bien que les fichiers avec empreinte de Spwig gèrent la plupart des cas, un nettoyage complet du cache garantit qu'aucun contenu obsolète ne reste
- **N'archivez pas les pages de panier ou de checkout** -- L'archivage de ces pages peut exposer les données d'un client à un autre
- **Testez depuis les emplacements de vos clients** -- Utilisez des outils gratuits comme webpagetest.org pour mesurer les performances réelles depuis les régions où vos clients achètent
- **Surveillez les statistiques de votre CDN** -- À la fois Cloudflare et CloudFront proposent des tableaux de bord affichant les taux de cache, le bande passant économisé et le trafic par pays
- **Gardez votre TTL DNS bas pendant la configuration** -- Fixez le TTL DNS à 300 secondes (5 minutes) pendant le passage à un CDN, puis augmentez-le une fois que tout fonctionne correctement
- **Un CDN ne remplace pas un bon hébergement** -- Votre serveur d'origine reste important pour les pages dynamiques comme le checkout, le panier et l'administration

Choisissez un hébergement de qualité en association avec un CDN