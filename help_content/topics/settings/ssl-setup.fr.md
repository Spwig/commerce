---
title: Configuration SSL
---

SSL (Secure Sockets Layer) chiffre la connexion entre les navigateurs de vos clients et votre magasin. Lorsque l'SSL est activé, l'URL de votre magasin commence par `https://` et les navigateurs affichent un icône de verrou. L'SSL est essentiel pour accepter les paiements, protéger les données des clients et obtenir un bon classement dans les moteurs de recherche.

Spwig prend en charge plusieurs modes SSL pour s'adapter à différentes configurations d'hébergement. Ce guide explique chaque mode et vous aide à choisir le bon.

## Choix d'un mode SSL

| Mode | Meilleur pour | Coût du certificat | Renouvellement |
|------|----------|-----------------|---------|
| **Let's Encrypt** | La plupart des magasins | Gratuit | Automatique |
| **Cloudflare Origin CA** | Magasins utilisant le proxy Cloudflare | Gratuit | Manuel (jusqu'à 15 ans) |
| **Certificat personnalisé** | Magasins avec des certificats achetés | Variable | Manuel |
| **Gestion externe** | Balanceurs de charge, Cloudflare Flexible | N/A | N/A |
| **Auto-signé** | Développement et tests | Gratuit | Manuel |
| **Aucun (HTTP)** | Développement local uniquement | N/A | N/A |

Si vous n'êtes pas sûr du mode à utiliser, **Let's Encrypt** est le meilleur choix pour la plupart des magasins. Il est gratuit, automatique et pris en charge par tous les navigateurs.

## Let's Encrypt

Let's Encrypt fournit des certificats SSL gratuits et fiables qui se renouvellent automatiquement toutes les 60 à 90 jours. C'est l'option recommandée pour la plupart des commerçants.

**Exigences :**
- Votre domaine doit pointer vers votre serveur (enregistrement A dans le DNS)
- Le port 80 doit être accessible depuis Internet (pour la vérification du certificat)
- Une adresse e-mail pour les notifications de fin de validité du certificat

**Étapes de configuration :**
1. Allez dans **Paramètres > Paramètres du site** et ouvrez l'onglet **Domaine & SSL**
2. Entrez le nom de votre domaine
3. Sélectionnez **Let's Encrypt**
4. Entrez l'adresse e-mail de votre administrateur
5. Cliquez sur **Appliquer la configuration**

Spwig gère le reste automatiquement : vérification de votre domaine, obtention du certificat, configuration de NGINX et mise en place du renouvellement automatique.

## Cloudflare Origin CA

Les certificats Cloudflare Origin CA chiffrent la connexion entre les serveurs de bordure de Cloudflare et votre magasin. Ces certificats sont gratuits et peuvent durer jusqu'à 15 ans, mais ils sont **seulement pris en charge par Cloudflare** — les navigateurs se connectant directement à votre serveur afficheront une alerte de certificat.

Ce mode est idéal si vous utilisez Cloudflare comme proxy (nuage orange activé) pour votre domaine. Cloudflare affiche son propre certificat fiable aux visiteurs, et le certificat Origin CA sécurise la connexion entre Cloudflare et votre serveur.

**Exigences :**
- Un compte Cloudflare avec votre domaine ajouté
- Un certificat Origin CA et une clé privée générés depuis le tableau de bord Cloudflare
- Le mode SSL/TLS de Cloudflare défini sur **Full (Strict)**

**Génération du certificat Origin CA :**
1. Connectez-vous à votre tableau de bord Cloudflare
2. Sélectionnez votre domaine
3. Allez dans **SSL/TLS > Serveur d'origine**
4. Cliquez sur **Créer un certificat**
5. Choisissez RSA ou ECC (RSA est le plus compatible)
6. Ajoutez votre domaine (par exemple, `example.com` et `*.example.com`)
7. Choisissez une période de validité (15 ans est recommandé)
8. Cliquez sur **Créer** et copiez à la fois le certificat et la clé privée

**Configuration dans Spwig :**
1. Allez dans **Paramètres > Paramètres du site** et ouvrez l'onglet **Domaine & SSL**
2. Entrez le nom de votre domaine
3. Sélectionnez **Cloudflare Origin CA**
4. Collez le certificat dans le champ **Certificat (PEM)**
5. Collez la clé privée dans le champ **Clé privée (PEM)**
6. Cliquez sur **Appliquer la configuration**

**Après la configuration :**
- Dans Cloudflare, définissez le mode SSL/TLS sur **Full (Strict)**
- Activez le proxy Cloudflare (nuage orange) pour l'enregistrement DNS de votre domaine
- Votre magasin sera accessible via HTTPS avec le certificat fiable de Cloudflare

## Certificat personnalisé

Utilisez ce mode si vous avez acheté un certificat SSL auprès d'une autorité de certification (CA) telle que DigiCert, Sectigo ou GoDaddy, ou si votre fournisseur d'hébergement en a fourni un.

**Étapes de configuration :**
1.

Allez dans **Paramètres > Paramètres du site** et ouvrez l'onglet **Domaine & SSL**
2.

Entrez le nom de votre domaine
3.

Sélectionnez **Certificat personnalisé**
4.

Conservez tous les formats de mise en forme Markdown, les chemins d'image, les blocs de code et les termes techniques.

Collez votre chaîne de certificats (y compris les certificats intermédiaires) dans le champ **Certificate (PEM)**
5.

Collez votre clé privée dans le champ **Private Key (PEM)**
6.

Cliquez sur **Apply Configuration**

Votre certificat doit inclure la chaîne complète : votre certificat de domaine suivi de tout certificat intermédiaire. La clé privée doit être au format PEM (commençant par `-----BEGIN PRIVATE KEY-----` ou `-----BEGIN RSA PRIVATE KEY-----`).

## Managed Externally

Choisissez ce mode lorsque le SSL est terminé par un service externe avant que le trafic n'atteigne votre serveur. Dans ce cas, votre serveur ne reçoit que du trafic HTTP brut - aucun certificat n'est installé sur le serveur lui-même.

**Scénarios courants :**
- **Cloudflare Flexible SSL** -- Cloudflare chiffre le trafic navigateur-Cloudflare, mais envoie du HTTP à votre serveur
- **Balanceurs de charge en nuage** -- AWS ALB, Google Cloud Load Balancer ou DigitalOcean Load Balancer terminent le SSL et transmettent du HTTP
- **Proxy inverse** -- Un autre serveur devant Spwig gère le SSL

**Étapes de configuration :**
1. Allez dans **Settings > Site Settings** et ouvrez l'onglet **Domain & SSL**
2. Entrez votre nom de domaine
3. Sélectionnez **Managed Externally**
4. Cliquez sur **Apply Configuration**

Spwig configurera NGINX pour ne servir que du HTTP et fera confiance à l'en-tête `X-Forwarded-Proto` de votre proxy afin de détecter correctement les visiteurs HTTPS.

## Self-Signed Certificate

Les certificats auto-signés chiffreront la connexion mais ne seront pas approuvés par les navigateurs. Les visiteurs verront un avertissement de sécurité qu'ils doivent contourner manuellement. Ce mode est adapté uniquement aux serveurs de développement et aux tests internes.

**Étapes de configuration :**
1. Allez dans **Settings > Site Settings** et ouvrez l'onglet **Domain & SSL**
2. Entrez votre nom de domaine
3. Sélectionnez **Self-Signed**
4. Cliquez sur **Apply Configuration**

Spwig génère automatiquement un certificat auto-signé. Ne utilisez pas ce mode pour un magasin en production.

## Troubleshooting

**Certificat non fonctionnel après la configuration :**
- Vérifiez que l'enregistrement A de votre domaine pointe vers l'adresse IP de votre serveur
- Assurez-vous que les ports 80 et 443 sont ouverts dans votre pare-feu
- Attendez quelques minutes pour que les modifications DNS prennent effet

**Let's Encrypt échoue à l'émission d'un certificat :**
- Vérifiez que votre domaine pointe vers l'adresse IP de ce serveur
- Assurez-vous que le port 80 n'est pas bloqué par un pare-feu
- Si vous êtes derrière Cloudflare, définissez temporairement le DNS sur "DNS only" (nuage gris) pendant l'émission du certificat

**Cloudflare affiche "Error 526" (Certificat SSL invalide) :**
- Assurez-vous d'avoir sélectionné le mode **Cloudflare Origin CA** (et non Managed Externally)
- Vérifiez que le mode SSL/TLS de Cloudflare est défini sur **Full (Strict)**
- Vérifiez que le certificat Origin CA n'a pas expiré

**Le navigateur affiche "Not Secure" malgré la présence de SSL :**
- Certaines pages peuvent charger des images ou des scripts via HTTP (contenu mixte). Vérifiez la console du développeur de votre navigateur pour des avertissements de contenu mixte.
- Assurez-vous que l'URL de votre site dans les paramètres utilise `https://`