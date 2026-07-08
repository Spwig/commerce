---
title: Configurazione SSL
---

SSL (Secure Sockets Layer) crittografa la connessione tra i browser dei tuoi clienti e il tuo negozio. Quando l'SSL è attivo, l'URL del tuo negozio inizia con `https://` e i browser mostrano un'icona a forma di lucchetto. L'SSL è essenziale per accettare pagamenti, proteggere i dati dei clienti e ottenere un buon posizionamento nei motori di ricerca.

Spwig supporta diversi modi di utilizzo dell'SSL per adattarsi a diverse configurazioni di hosting. Questa guida spiega ogni modalità e ti aiuta a scegliere quella giusta.

## Scegliere una Modalità SSL

| Modalità | Migliore per | Costo del certificato | Rinnovo |
|----------|----------------|------------------------|---------|
| **Let's Encrypt** | La maggior parte dei negozi | Gratuito | Automatico |
| **Cloudflare Origin CA** | Negozi che utilizzano il proxy di Cloudflare | Gratuito | Manuale (fino a 15 anni) |
| **Certificato Personalizzato** | Negozi con certificati acquistati | Varia | Manuale |
| **Gestito Esternamente** | Load balancer, Cloudflare Flexible | N/A | N/A |
| **Autosignato** | Sviluppo e test | Gratuito | Manuale |
| **Nessuno (HTTP)** | Solo sviluppo locale | N/A | N/A |

Se non sei sicuro di quale modalità utilizzare, **Let's Encrypt** è la scelta migliore per la maggior parte dei negozi. È gratuito, automatico e riconosciuto da tutti i browser.

## Let's Encrypt

Let's Encrypt fornisce certificati SSL gratuiti e attendibili che si rinnovano automaticamente ogni 60-90 giorni. Questa è l'opzione consigliata per la maggior parte dei commercianti.

**Requisiti:**
- Il tuo dominio deve puntare al tuo server (record A nel DNS)
- La porta 80 deve essere accessibile da Internet (per la verifica del certificato)
- Un indirizzo email per le notifiche di scadenza del certificato

**Passaggi per la configurazione:**
1. Vai a **Impostazioni > Impostazioni del sito** e apri l'**scheda Dominio & SSL**
2. Inserisci il nome del tuo dominio
3. Seleziona **Let's Encrypt**
4. Inserisci l'indirizzo email dell'amministratore
5. Clicca su **Applica Configurazione**

Spwig gestisce tutto il resto automaticamente: verifica del dominio, ottenimento del certificato, configurazione di NGINX e impostazione del rinnovo automatico.

## Cloudflare Origin CA

I certificati Cloudflare Origin CA crittografa la connessione tra i server edge di Cloudflare e il tuo negozio. Questi certificati sono gratuiti e possono durare fino a 15 anni, ma sono **riconosciuti solo da Cloudflare** -- i browser che si connettono direttamente al tuo server vedranno un avviso sul certificato.

Questa modalità è ideale se utilizzi Cloudflare come proxy (nuvola gialla attiva) per il tuo dominio. Cloudflare presenta il proprio certificato attendibile ai visitatori, e il certificato Origin CA protegge la connessione tra Cloudflare e il tuo server.

**Requisiti:**
- Un account Cloudflare con il tuo dominio aggiunto
- Un certificato Origin CA e una chiave privata generate dal pannello di Cloudflare
- La modalità SSL/TLS di Cloudflare impostata su **Full (Strict)**

**Generazione del certificato Origin CA:**
1. Accedi al pannello di amministrazione di Cloudflare
2. Seleziona il tuo dominio
3. Vai a **SSL/TLS > Origin Server**
4. Clicca su **Crea Certificato**
5. Scegli RSA o ECC (RSA è la scelta più compatibile)
6. Aggiungi il tuo dominio (es. `example.com` e `*.example.com`)
7. Scegli un periodo di validità (si consiglia 15 anni)
8. Clicca su **Crea** e copia sia il certificato che la chiave privata

**Configurazione in Spwig:**
1. Vai a **Impostazioni > Impostazioni del sito** e apri l'**scheda Dominio & SSL**
2. Inserisci il nome del tuo dominio
3. Seleziona **Cloudflare Origin CA**
4. Incolla il certificato nel campo **Certificato (PEM)**
5. Incolla la chiave privata nel campo **Chiave privata (PEM)**
6. Clicca su **Applica Configurazione**

**Dopo la configurazione:**
- In Cloudflare, imposta la modalità SSL/TLS su **Full (Strict)**
- Abilita il proxy di Cloudflare (nuvola gialla) per il record DNS del tuo dominio
- Il tuo negozio sarà accessibile tramite HTTPS con il certificato attendibile di Cloudflare

## Certificato Personalizzato

Utilizza questa modalità se hai acquistato un certificato SSL da un'autorità di certificazione (CA) come DigiCert, Sectigo o GoDaddy, o se il tuo fornitore di hosting ne ha emesso uno per te.

**Passaggi per la configurazione:**
1.

Vai a **Impostazioni > Impostazioni del sito** e apri l'**scheda Dominio & SSL**
2.

Inserisci il nome del tuo dominio
3.

Seleziona **Certificato Personalizzato**
4.

Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

Incolla la catena del certificato (inclusi i certificati intermedi) nel campo **Certificate (PEM)**
5.

Incolla la tua chiave privata nel campo **Private Key (PEM)**
6.

Fai clic su **Apply Configuration**

Il tuo certificato deve includere l'intera catena: il certificato del tuo dominio seguito da eventuali certificati intermedi. La chiave privata deve essere in formato PEM (che inizia con `-----BEGIN PRIVATE KEY-----` o `-----BEGIN RSA PRIVATE KEY-----`).

## Managed Externally

Seleziona questa modalità quando l'SSL viene terminato da un servizio esterno prima che il traffico raggiunga il tuo server. In questa configurazione, il tuo server riceve solo traffico HTTP puro - nessun certificato è installato sul server stesso.

**Scenari comuni:**
- **Cloudflare Flexible SSL** -- Cloudflare crittografa il traffico dal browser a Cloudflare, ma invia HTTP al tuo server
- **Load balancer cloud** -- AWS ALB, Google Cloud Load Balancer o DigitalOcean Load Balancer terminano l'SSL e inoltrano HTTP
- **Reverse proxy** -- Un altro server davanti a Spwig gestisce l'SSL

**Passaggi per la configurazione:**
1. Vai a **Settings > Site Settings** e apri l'**Domain & SSL**
2. Inserisci il nome del tuo dominio
3. Seleziona **Managed Externally**
4. Fai clic su **Apply Configuration**

Spwig configurerà NGINX per servire solo HTTP e si affiderà all'intestazione `X-Forwarded-Proto` dal tuo proxy per rilevare correttamente i visitatori HTTPS.

## Self-Signed Certificate

I certificati self-signed crittografano la connessione ma non sono riconosciuti dai browser. I visitatori vedranno un avviso di sicurezza che devono bypassare manualmente. Questa modalità è adatta solo per server di sviluppo e test interni.

**Passaggi per la configurazione:**
1. Vai a **Settings > Site Settings** e apri l'**Domain & SSL**
2. Inserisci il nome del tuo dominio
3. Seleziona **Self-Signed**
4. Fai clic su **Apply Configuration**

Spwig genera automaticamente un certificato self-signed. Non utilizzare questa modalità per un negozio in produzione.

## Troubleshooting

**Certificato non funzionante dopo la configurazione:**
- Verifica che il record A del tuo dominio punti all'indirizzo IP del tuo server
- Assicurati che i porte 80 e 443 siano aperte nel tuo firewall
- Aspetta alcuni minuti affinché i cambiamenti DNS si propaghino

**Let's Encrypt non riesce a emettere un certificato:**
- Controlla che il tuo dominio risolva a questo indirizzo IP del server
- Assicurati che la porta 80 non sia bloccata da un firewall
- Se sei dietro Cloudflare, imposta temporaneamente il DNS su "DNS only" (nuvola grigia) durante l'emissione del certificato

**Cloudflare mostra "Error 526" (Certificato SSL non valido):**
- Assicurati di aver selezionato la modalità **Cloudflare Origin CA** (non Managed Externally)
- Controlla che la modalità SSL/TLS di Cloudflare sia impostata su **Full (Strict)**
- Verifica che il certificato Origin CA non sia scaduto

**Il browser mostra "Not Secure" nonostante abbia SSL:**
- Alcune pagine potrebbero caricare immagini o script tramite HTTP (contenuto misto). Controlla la console dello sviluppatore del browser per avvisi sul contenuto misto.
- Assicurati che l'URL del tuo sito nelle Impostazioni utilizzi `https://`