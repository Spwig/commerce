---
title: Configuration du domaine & SSL
---

Ce guide explique comment connecter un domaine personnalisé à votre boutique Spwig et configurer des certificats SSL pour un accès sécurisé via HTTPS. Vous pouvez configurer un domaine lors de l'installation ou l'ajouter plus tard.

## Ajout d'un domaine après l'installation

Si vous avez installé Spwig sans domaine (en utilisant l'adresse IP du serveur), vous pouvez en ajouter à tout moment.

### Étape 1 : Configurer le DNS

Avec votre registrar de domaine ou votre fournisseur DNS :

1. Créer un **enregistrement A** pointant votre domaine (ou sous-domaine) vers l'adresse IP de votre serveur
2. Si vous utilisez un sous-domaine comme `shop.example.com`, créer l'enregistrement A pour `shop`
3. Attendre la propagation du DNS — cela prend généralement 5 à 60 minutes

Vérifier que l'enregistrement DNS fonctionne :

```bash
 dig +short shop.example.com
```

Cela devrait retourner l'adresse IP de votre serveur.

### Étape 2 : Exécuter le script de configuration du domaine

Connectez-vous en SSH à votre serveur et accédez au répertoire d'installation de Spwig :

```bash
 ./configure-domain.sh
```

Le script effectuera les actions suivantes :

1. Demander votre nom de domaine
2. Vérifier que le DNS pointe vers votre serveur
3. Mettre à jour la configuration de la boutique
4. Obtenir un certificat SSL gratuit de Let's Encrypt
5. Configurer le serveur web pour utiliser HTTPS
6. Redémarrer les services concernés

Votre boutique est désormais accessible à `https://yourdomain.com`.

### Étape 3 : Mettre à jour les paramètres de la boutique

Après avoir ajouté un domaine, connectez-vous à votre panneau d'administration et allez dans **Store Settings**. Vérifiez que l'**URL de la boutique** correspond à votre nouveau domaine. Cela garantit que les e-mails, les factures et les liens utilisent l'adresse correcte.

## Certificats SSL

### SSL automatique (Let's Encrypt)

En mode **standalone**, l'installeur obtient automatiquement un certificat SSL gratuit de Let's Encrypt. Ces certificats :

- Sont reconnus par tous les principaux navigateurs
- Sont valides pendant 90 jours
- Se renouvellent automatiquement — un contrôle de renouvellement s'exécute quotidiennement, et les certificats sont renouvelés lorsque moins de 30 jours restent
- Couvrent votre domaine exact (par exemple, `shop.example.com`)

Vous n'avez pas besoin de gérer manuellement le renouvellement.

### Certificats auto-signés

Dans certaines situations, Spwig utilise un certificat auto-signé à la place :

- **Mode local** (développement/test)
- Lorsque Let's Encrypt ne peut pas atteindre votre serveur (port 80 bloqué par un pare-feu, DNS non propagé)
- Lorsqu'aucun domaine n'est configuré (accès uniquement via l'IP)

Les certificats auto-signés chiffreront le trafic mais ne seront pas reconnus par les navigateurs — les visiteurs verront un avertissement de sécurité. Cela est acceptable pour le test mais ne doit pas être utilisé en production.

### SSL en mode Sidecar

En **mode Sidecar**, votre serveur web existant (Apache, Nginx, Caddy, etc.) gère la terminaison SSL. Spwig fonctionne sur un port HTTP derrière votre proxy. Configurez SSL sur votre serveur web principal comme vous le feriez normalement.

L'installeur génère un bloc de configuration de proxy que vous pouvez ajouter à votre serveur web. Pour Nginx, cela ressemble à :

```nginx
 location / {
     proxy_pass http://127.0.0.1:8080;
     proxy_set_header Host $host;
     proxy_set_header X-Real-IP $remote_addr;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
 }
```

## Changer de domaine

Pour passer à un autre domaine :

1. Configurer le DNS pour le nouveau domaine (enregistrement A pointant vers votre serveur)
2. Exécuter à nouveau `./configure-domain.sh` avec le nouveau domaine
3. Le script mettra à jour toutes les configurations, obtiendra un nouveau certificat et redémarrera les services
4. Mettre à jour les **Store Settings** dans le panneau d'administration avec l'URL nouvelle

Votre ancien domaine ne fonctionnera plus une fois que la configuration aura été mise à jour.

## Dépannage

### "Validation DNS échouée"

Le script configure-domain vérifie que votre domaine pointe vers votre serveur avant de demander un certificat. Si ce test échoue :

- Vérifiez que l'enregistrement A est correct avec `dig +short yourdomain.com`
- Attendez quelques minutes supplémentaires pour la propagation du DNS
- Vérifiez que vous configurez exactement le domaine ou le sous-domaine (et non un wildcard)

### "Limite de taux de Let's Encrypt atteinte"

Let's Encrypt limite les demandes de certificats à 5 par domaine par semaine. Si vous atteignez cette limite :


- Attendez 7 jours avant de réessayer
- Utilisez un sous-domaine différent en attendant
- Le magasin reste accessible via HTTP ou avec un certificat auto-signé pendant que vous attendez

### "Le port 80 n'est pas accessible"

Let's Encrypt doit se connecter à votre serveur sur le port 80 pour vérifier la propriété du domaine. Assurez-vous de :

- Ce que votre pare-feu permet l'entrée TCP sur le port 80
- Aucune autre application ne bloque le port 80
- Votre fournisseur de cloud autorise le port 80 via son groupe de sécurité ou son pare-feu réseau

### Échecs de renouvellement de certificat

Si le renouvellement automatique échoue, le certificat expirera après 90 jours. Pour renouveler manuellement :

```bash
docker exec spwig_nginx certbot renew
docker exec spwig_nginx nginx -s reload
```

Vérifiez le journal de renouvellement pour plus de détails si cela échoue. La cause la plus courante est le port 80 étant bloqué par un changement de pare-feu après l'installation initiale.