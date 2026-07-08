---
title: Configurazione delle Impostazioni del Negozio
---

Impostazioni del Negozio è il posto centrale per configurare l'identità del tuo negozio, la localizzazione, il branding e le preferenze operative. Naviga verso **Impostazioni > Impostazioni del Negozio** per iniziare.

![Impostazioni del negozio scheda generale](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Scheda Generale

La scheda **Generale** contiene le impostazioni di identità principale del tuo negozio.

### Identità del Negozio

- **Nome del Negozio** — Il nome visualizzato nei titoli delle pagine, negli email e nell'intestazione dell'amministrazione.
- **Slogan** — Una breve descrizione del tuo negozio, utilizzata per l'ottimizzazione dei motori di ricerca e il condivisione su social media.
- **URL del Sito** — L'indirizzo web pubblico del tuo negozio. Viene utilizzato negli email, nella generazione del sitemap e nella costruzione di link.

### Informazioni di Contatto

- **Email di Contatto** — Riceve le notifiche degli ordini e viene mostrata nelle comunicazioni con i clienti.
- **Numero di Telefono** — Numero di supporto opzionale visualizzato nel piè di pagina e negli email.

### Indirizzo Aziendale

Inserisci il tuo indirizzo completo (via, città, stato, codice postale, paese). Viene utilizzato per:
- Calcolo dell'origine del spedizione
- Calcolo delle tasse
- Requisiti legali e fatture

## Branding

### Logo

Carica il logo del tuo negozio (si consiglia PNG o SVG, ~200x50px con sfondo trasparente). Il logo appare in:
- L'intestazione del negozio
- Modelli di email
- Il pannello di amministrazione

### Favicon

Carica una favicon quadrata (ICO o PNG, 32x32px). Appare come:
- Icona della scheda del browser
- Icona del segnalibro
- Icona della home screen mobile

## Localizzazione

### Lingua Predefinita

Scegli la lingua principale del tuo negozio tra 10 opzioni supportate:

| Lingua | Codice |
|----------|------|
| Inglese | en |
| Spagnolo | es |
| Francese | fr |
| Tedesco | de |
| Portoghese | pt |
| Giapponese | ja |
| Cinese Semplificato | zh-hans |
| Cinese Tradizionale | zh-hant |
| Russo | ru |
| Arabo | ar |

La lingua predefinita controlla la lingua dell'interfaccia di amministrazione e il fallback per il contenuto del negozio.

### Fuso Orario

Seleziona il fuso orario del tuo negozio per ottenere timestamp degli ordini accurati, promozioni pianificate e report.

### Valuta

- **Valuta Predefinita** — La valuta principale per i prezzi e l'accounting.
- **Multi-Valuta** — Abilita per permettere ai clienti di visualizzare i prezzi nella loro valuta preferita con conversione automatica utilizzando tassi di cambio in tempo reale.

Configura valute aggiuntive in **Impostazioni > Impostazioni del Negozio > Valuta**.

## Impostazioni di E-Commerce

### Checkout per Visitatori

Consenti acquisti senza creare un account:
- Flusso di checkout più rapido
- Minore attrito per i primi acquirenti
- Raccoglie meno dati dei clienti

### Formato del Numero Ordine

Personalizza l'aspetto dei numeri degli ordini:
- **Prefisso** — ad esempio, "ORD-"
- **Numero di Inizio** — Il primo numero d'ordine
- **Riempimento** — ad esempio, 00001

### Impostazioni Predefinite dell'Inventario

- **Traccia l'Inventario** — Abilita il tracciamento dello stock a livello globale
- **Limite di Scorta Bassa** — Livello di allerta (predefinito: 5 unità)
- **Permetti Ordini di Riserva** — Accetta ordini quando non è disponibile lo stock

## Impostazioni Email

### Informazioni Mittente

- **Nome Mittente** — Appare come il mittente dell'email (di solito il nome del tuo negozio)
- **Email Mittente** — Deve provenire da un dominio verificato
- **Email Risposta** — Dove vengono indirizzate le risposte dei clienti

### Fornitore Email

Configura il tuo servizio di consegna email in **Impostazioni > Configurazione Email**. I fornitori supportati includono SMTP, SendGrid, Mailgun e Amazon SES.

## Legale e Conformità

Aggiungi le tue politiche del negozio per soddisfare i requisiti legali:

- **Termini e Condizioni** — Obbligatori per il checkout; i clienti devono accettare prima di acquistare
- **Informativa sulla Privacy** — Conformità GDPR/CCPA; collegata nel piè di pagina
- **Politica di Reso** — Definisci il periodo di reso, le condizioni e il processo di rimborso

## Modalità Manutenzione

Abilita la modalità manutenzione per mettere temporaneamente offline il tuo negozio:
- Mostra un messaggio personalizzato di manutenzione ai visitatori
- Limita l'accesso solo agli utenti amministrativi
- Utile durante aggiornamenti o migrazioni importanti

## Impostazioni Fiscali

Configura la raccolta delle tasse in **Impostazioni > Impostazioni Fiscali**:

1. **Metodo di Calcolo** — Per indirizzo di spedizione, indirizzo di fatturazione o posizione del negozio
2. **Aliquote Fiscali** — Definisci le aliquote per regione e classe di tasse dei prodotti
3. **Visualizzazione delle Tasse** — Mostra i prezzi con tasse, senza tasse o entrambi

## Suggerimenti

- Imposta correttamente il tuo fuso orario prima di elaborare qualsiasi ordine — influisce su tutti i timestamp e i report.
- Abilita il checkout per visitatori per migliorare i tassi di conversione.
- Compila il tuo indirizzo aziendale per ottenere calcoli di spedizione e tasse accurati.
- Carica sia un logo che una favicon per un'esperienza professionale e marchiata.
- Rivedi regolarmente le tue pagine legali per rimanere conformi alle normative locali.

## Risoluzione dei Problemi

**Le modifiche non appaiono nel negozio:**
- Pulisci la cache del browser
- Esegui un'operazione di pulizia della cache dal pannello di amministrazione
- Controlla se la modalità manutenzione è accidentalmente abilitata

**Email non inviate:**
- Verifica le impostazioni del tuo fornitore email nella Configurazione Email
- Controlla che il dominio dell'email "From" sia verificato
- Testa la connessione dalla pagina di configurazione del fornitore

**Conversione della valuta non funzionante:**
- Verifica che il fornitore dei tassi di cambio sia connesso
- Controlla le credenziali API nelle impostazioni dei tassi di cambio
- Prova ad aggiornare i tassi manualmente

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.