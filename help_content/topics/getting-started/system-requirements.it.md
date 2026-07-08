---
title: Requisiti del sistema
---

Spwig funziona su la maggior parte dei server Linux moderni. Questa pagina copre le specifiche minime e raccomandate, cosa accade su server più piccoli e quali provider di cloud funzionano bene.

## Requisiti minimi

| Risorsa | Minimo | Raccomandato |
|----------|---------|-------------|
| **Sistema operativo** | Ubuntu 22.04 LTS, Ubuntu 24.04 LTS o Debian 12 | Ubuntu 24.04 LTS |
| **RAM** | 4 GB | 8 GB o più |
| **Spazio su disco** | 20 GB | 40 GB o più |
| **CPU** | 1 vCPU | 2+ vCPUs |
| **Architettura** | x86_64 (AMD64) | x86_64 |
| **Rete** | Indirizzo IP pubblico (per la modalità standalone) | Indirizzo IP pubblico statico |
| **Porte** | 80 e 443 (standalone) o qualsiasi porta alternativa (sidecar) | 80 e 443 |

> **Nota:** I server basati su ARM (es. AWS Graviton, Oracle Ampere) non sono attualmente supportati.

## Livelli di risorse

L'installer rileva automaticamente la RAM disponibile sul server e seleziona il livello di risorse appropriato.

### Livello standard (6 GB+ RAM)

Tutti i servizi funzionano con le capacità complete:

- Servizio di **traduzione alimentato dall'AI** abilitato — traduci descrizioni dei prodotti, contenuti delle pagine e testi SEO in diversi linguaggi direttamente dal pannello di amministrazione
- Assegnazione completa della memoria per l'applicazione, il database e i lavoratori in background
- Concorrenza ottimizzata per i lavoratori in background in base al numero di CPU

### Livello piccolo (4–6 GB RAM)

L'installer si adatta per risparmiare memoria:

- Il servizio di traduzione AI è **disabilitato** per risparmiare circa 2 GB di RAM. Puoi comunque gestire le traduzioni manualmente o utilizzare strumenti esterni per la traduzione — solo il traduttore AI integrato è influenzato.
- I limiti di memoria per l'applicazione e i lavoratori sono ridotti
- Tutte le altre funzionalità funzionano esattamente come nel livello standard

> **Consiglio:** Se inizi con un server piccolo e successivamente aggiorni a 6 GB+ RAM, riavvia l'installer per abilitare il servizio di traduzione.

## Provider di cloud raccomandati

Spwig funziona su qualsiasi server Linux che soddisfa i requisiti. Questi provider sono testati e offrono un buon valore:

| Provider | Piano raccomandato | RAM | Disco | Costo approssimativo |
|----------|-----------------|-----|------|-----------------|
| **DigitalOcean** | Droplet di base | 4 GB | 80 GB | $24/mese |
| **Linode (Akamai)** | Condiviso 4 GB | 4 GB | 80 GB | $24/mese |
| **Vultr** | Calcolo cloud | 4 GB | 100 GB | $24/mese |
| **Hetzner** | CX31 | 8 GB | 80 GB | €8/mese |
| **OVH** | VPS iniziale | 4 GB | 80 GB | €7/mese |

Per negozi che prevedono un traffico significativo o cataloghi di prodotti molto grandi (10.000+ prodotti), inizia con 8 GB di RAM e 2+ vCPUs.

## Utilizzo dello spazio su disco

Un'installazione di Spwig fresca utilizza circa 8 GB di spazio su disco:

| Componente | Dimensione |
|-----------|------|
| Immagini Docker | ~4 GB |
| Database (negozio vuoto) | ~200 MB |
| Modelli di traduzione AI (se abilitati) | ~2 GB |
| File dell'applicazione e configurazione | ~500 MB |
| Sistema operativo e motore Docker | ~3 GB |

Pianifica spazio aggiuntivo per:

- **Immagini e media dei prodotti** — dipende dalla dimensione del tuo catalogo. Riserva 1–5 GB per un negozio tipico con centinaia di prodotti.
- **Crescita del database** — cresce con gli ordini, i clienti e i dati analitici. Un negozio che gestisce 100 ordini al giorno cresce di circa 1 GB all'anno.
- **Backup** — se si archiviano i backup localmente, ogni backup completo è di dimensioni pari a quelle del database più i media. Con una politica di conservazione di 30 giorni, riserva 2–3× la dimensione dei dati correnti.

## Dominio e DNS

Un nome di dominio è opzionale durante l'installazione ma necessario per l'uso in produzione. Hai bisogno di:

- Un dominio o sottodominio (es. `shop.example.com`)
- Un **record A** che punta all'indirizzo IP pubblico del tuo server
- Propagazione DNS completata (tipicamente 5–60 minuti dopo l'aggiunta del record)

L'installer ottiene automaticamente un certificato SSL gratuito da Let's Encrypt quando viene rilevato un dominio valido. Puoi anche aggiungere un dominio dopo l'installazione utilizzando lo script `./configure-domain.sh`.

## Firewall

Se il tuo server ha un firewall (la maggior parte dei provider di cloud ne abilita uno di default), assicurati che queste porte siano aperte:

| Porta | Protocollo | Scopo |
|------|----------|---------|
| **22** | TCP | Accesso SSH (per gestire il server) |
| **80** | TCP | HTTP (necessario per la validazione del certificato Let's Encrypt) |
| **443** | TCP | HTTPS (traffico sicuro del tuo negozio) |

In modalità sidecar, apri la porta alternativa assegnata dall'installer invece di 80/443.

## Requisiti software

L'installer gestisce automaticamente l'installazione di tutti i software. Per riferimento, questi sono i componenti che installa o verifica:

- **Docker Engine** — runtime per container (installato automaticamente se mancante)
- **Docker Compose** — orchestrazione dei servizi (incluso con Docker Engine)
- **curl** — utilizzato dall'installer stesso (presente in quasi tutti i sistemi Linux)

Non è necessario installare alcun altro software. Spwig non richiede di installare manualmente Python, Node.js, PostgreSQL, Redis o Nginx — tutto funziona all'interno dei contenitori Docker.