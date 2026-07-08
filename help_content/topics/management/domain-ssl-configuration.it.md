---
title: Configurazione del dominio & SSL
---

Questo documento spiega come collegare un dominio personalizzato al tuo negozio Spwig e configurare certificati SSL per un accesso sicuro tramite HTTPS. Puoi configurare un dominio durante l'installazione o aggiungerne uno in un secondo momento.

## Aggiunta di un dominio dopo l'installazione

Se hai installato Spwig senza un dominio (utilizzando l'indirizzo IP del server), puoi aggiungerne uno in qualsiasi momento.

### Passaggio 1: Configurazione DNS

Con il tuo registrar di dominio o fornitore DNS:

1. Crea un **record A** che punti il tuo dominio (o sottodominio) all'indirizzo IP del tuo server
2. Se utilizzi un sottodominio come `shop.example.com`, crea il record A per `shop`
3. Attendere la propagazione DNS — questo richiede in genere da 5 a 60 minuti

Verifica che il record DNS funzioni:

```bash
 dig +short shop.example.com
```

Questo dovrebbe restituire l'indirizzo IP del tuo server.

### Passaggio 2: Esecuzione dello script di configurazione del dominio

Accedi via SSH al tuo server e naviga nella directory di installazione di Spwig:

```bash
 ./configure-domain.sh
```

Lo script eseguirà le seguenti operazioni:

1. Chiedere il nome del dominio
2. Verificare che il DNS punti al tuo server
3. Aggiornare la configurazione del negozio
4. Ottenere un certificato SSL gratuito da Let's Encrypt
5. Configurare il server web per utilizzare HTTPS
6. Riavviare i servizi pertinenti

Il tuo negozio è ora accessibile all'indirizzo `https://yourdomain.com`.

### Passaggio 3: Aggiornamento delle impostazioni del negozio

Dopo aver aggiunto un dominio, accedi al pannello di amministrazione e vai a **Impostazioni del negozio**. Verifica che l'**URL del negozio** corrisponda al tuo nuovo dominio. Questo assicura che le e-mail, le fatture e i collegamenti utilizzino l'indirizzo corretto.

## Certificati SSL

### SSL automatico (Let's Encrypt)

In **modalità standalone**, l'installer ottiene automaticamente un certificato SSL gratuito da Let's Encrypt. Questi certificati:

- Sono riconosciuti da tutti i principali browser
- Hanno una validità di 90 giorni
- Vengono rinnovati automaticamente — un controllo di rinnovo viene eseguito quotidianamente e i certificati vengono rinnovati quando hanno meno di 30 giorni rimanenti
- Coprono esattamente il tuo dominio (es. `shop.example.com`)

Non è necessario gestire il rinnovo manualmente.

### Certificati self-signed

In alcune situazioni, Spwig utilizza un certificato self-signed:

- **Installazioni in modalità locale** (sviluppo/test)
- Quando Let's Encrypt non può raggiungere il tuo server (il firewall blocca la porta 80, il DNS non è ancora propagato)
- Quando non è configurato alcun dominio (accesso solo tramite IP)

I certificati self-signed crittografano il traffico ma non sono riconosciuti dai browser — i visitatori vedranno un avviso di sicurezza. Questo è accettabile per il test ma non dovrebbe essere utilizzato in produzione.

### SSL in modalità sidecar

In **modalità sidecar**, il tuo server web esistente (Apache, Nginx, Caddy, ecc.) gestisce la terminazione SSL. Spwig funziona su una porta HTTP dietro al tuo proxy. Configura SSL sul tuo server web principale come faresti di solito.

L'installer genera un blocco di configurazione del proxy che puoi aggiungere al tuo server web. Per Nginx, sembra simile a:

```nginx
 location / {
     proxy_pass http://127.0.0.1:8080;
     proxy_set_header Host $host;
     proxy_set_header X-Real-IP $remote_addr;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
 }
```

## Modifica del tuo dominio

Per passare a un dominio diverso:

1. Configura il DNS per il nuovo dominio (record A che punta al tuo server)
2. Esegui nuovamente `./configure-domain.sh` con il nuovo dominio
3. Lo script aggiorna tutta la configurazione, ottiene un nuovo certificato e riavvia i servizi
4. Aggiorna le **Impostazioni del negozio** nel pannello di amministrazione con l'URL nuovo

Il tuo vecchio dominio smetterà di funzionare una volta aggiornata la configurazione.

## Risoluzione dei problemi

### "Validazione DNS fallita"

Lo script configure-domain verifica che il tuo dominio punti al tuo server prima di richiedere un certificato. Se questo controllo fallisce:

- Verifica che il record A sia corretto con `dig +short yourdomain.com`
- Aspetta alcuni minuti aggiuntivi per la propagazione DNS
- Controlla che stai configurando esattamente il dominio o il sottodominio (non un wildcard)

### "Limite di richieste Let's Encrypt raggiunto"

Let's Encrypt limita le richieste di certificati a 5 per dominio a settimana. Se raggiungi questo limite:



- Attendere 7 giorni prima di riprovare
- Usare un sottodominio diverso nel frattempo
- Il negozio rimane accessibile tramite HTTP o con un certificato autofirmato mentre si attende

### "La porta 80 non è raggiungibile"

Let's Encrypt deve connettersi al tuo server sulla porta 80 per verificare la proprietà del dominio. Assicurati che:

- Il tuo firewall consenta l'ingresso TCP sulla porta 80
- Nessun'altra applicazione blocchi la porta 80
- Il gruppo di sicurezza o il firewall di rete del tuo provider cloud consenta la porta 80

### Fallimenti del rinnovo del certificato

Se il rinnovo automatico fallisce, il certificato scadrà dopo 90 giorni. Per rinnovare manualmente:

```bash
docker exec spwig_nginx certbot renew
docker exec spwig_nginx nginx -s reload
```

Controlla il registro del rinnovo per ulteriori dettagli se questo fallisce. La causa più comune è la porta 80 bloccata da un cambiamento nel firewall dopo l'installazione iniziale.