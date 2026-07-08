---
title: Configurazione delle tasse
---

Configura le regole fiscali per il tuo negozio in modo che le tasse corrette vengano applicate automaticamente agli ordini in base alla posizione del cliente. Puoi caricare preset regionali con un clic o creare regole personalizzate per qualsiasi paese, stato, città o codice postale.

![Tax Dashboard](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## Tax Dashboard

Accedi a **Orders > Shipments > Tax Rates** per aprire il pannello delle tasse. La pagina mostra:

- **Statistics panel** — quattro schede che mostrano Total Rules, Active Rules, Countries Covered, e Tax Types in uso
- **Filters** — cerca per nome, paese o stato, e filtra per paese, tipo di tassa (Sales Tax, VAT, GST, Custom), o stato (Active/Inactive)
- **Tax rule cards** — ogni scheda mostra la bandiera del paese, il nome della regola, la posizione, la percentuale di tassa, il badge del tipo di tassa, il badge dello stato, la priorità e il numero di esenzioni

## Loading Tax Presets

Fai clic su **Load Presets** per aprire il modal dei preset. I preset sono raccolte di tasse standard per una regione, pronte per essere caricate nel tuo negozio con un clic.

![Load Presets](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

I preset sono organizzati per regione del mondo:

| Region | Preset Groups |
|--------|--------------|
| **Africa** | Africa VAT (25 rates) |
| **Asia Pacific** | Asia-Pacific VAT/GST (24 rates), Central Asia VAT (6 rates) |
| **Europe** | EU VAT Rates, UK VAT, Other European VAT |
| **Latin America** | Latin America VAT |
| **Middle East** | Middle East VAT |
| **North America** | US State Sales Tax, Canadian GST/HST |
| **Oceania** | Oceania GST/VAT |

### How Presets Work

1. Fai clic su **Load** sul gruppo di preset che desideri
2. Il sistema crea regole fiscali per ogni paese o stato in quel gruppo
3. Le regole esistenti con lo stesso paese, stato e tipo di tassa vengono automaticamente ignorate per evitare duplicati
4. Dopo il caricamento, ogni regola è completamente modificabile — aggiungi tassi, aggiungi esenzioni o disattiva le regole che non necessiti

Puoi caricare più gruppi di preset. Ad esempio, carica sia le tasse dell'UE che quelle del Regno Unito se vendi a clienti in tutta Europa.

## Creating Tax Rules Manually

Fai clic su **Add Tax Rate** per creare una regola personalizzata. Il modulo ha quattro sezioni:

![Tax Rate Form](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### Basic Information

| Field | Description |
|-------|-------------|
| **Name** | Nome visualizzato per la regola (es. "California Sales Tax") |
| **Is Active** | Interruttore per abilitare o disabilitare la regola |
| **Tax Type** | Sales Tax, VAT, GST, o Custom Tax |
| **Rate (%)** | La percentuale di tassa (es. inserisci 8.25 per 8.25%) |
| **Priority** | I numeri più alti hanno la precedenza quando più regole corrispondono alla stessa posizione |

### Geographic Scope

| Field | Description |
|-------|-------------|
| **Country** | Codice ISO 3166-1 alpha-2 (es. US, GB, DE) |
| **State** | Stato o provincia (lascia vuoto per applicare a tutto il paese) |
| **City** | Nome della città (opzionale, per le regole fiscali a livello di città) |
| **Postal Codes** | Elenco di codici postali specifici (opzionale, per le regole fiscali a livello di codice postale) |

Le regole vengono corrisposte da più specifiche a meno specifiche. Una regola per un codice postale specifico ha la precedenza rispetto a una regola per lo stesso stato, che ha la precedenza rispetto a una regola a livello nazionale.

### Application Rules

| Field | Description |
|-------|-------------|
| **Applies to Shipping** | Quando selezionato, questa tassa si applica anche ai costi di spedizione |
| **Compound Tax** | Quando selezionato, questa tassa viene calcolata sopra ad altre tasse (l'importo base più le tasse già applicate) |

### Product Exemptions

| Field | Description |
|-------|-------------|
| **Exempt Product Types** | Tipi di prodotti esenti da questa tassa (es. digitale, servizio) |
| **Exempt Categories** | Categorie specifiche di prodotti esenti da questa tassa |

## Tax Types

| Type | Used For | Examples |
|------|----------|---------|
| **Sales Tax** | US, Canada | Tasse sulle vendite a livello di stato e provincia |
| **VAT** | Europa, UK, gran parte dell'Asia e dell'Africa | Tassa sul valore aggiunto |
| **GST** | Australia, Nuova Zelanda, India, Singapore | Tassa sulle merci e servizi |
| **Custom Tax** | Casi particolari | Surchi locali, tasse ambientali, tasse sui lussi |

## How Tax Calculation Works

Quando un cliente raggiunge la cassa, il sistema calcola automaticamente le tasse in base all'indirizzo di spedizione:

1. **Geographic matching** — trova tutte le regole attive che corrispondono al paese del cliente, quindi restringe per stato, città e codice postale
2. **Specificity scoring** — le regole più specifiche (codice postale > città > stato > paese) sono classificate più in alto
3. **Priority ordering** — all'interno dello stesso livello di specificità, le regole con priorità più alta hanno la precedenza
4. **Product exemptions** — i prodotti esenti vengono esclusi da ogni regola applicabile
5. **Non-compound taxes** — calcolate prima sul prezzo base di ogni articolo
6. **Compound taxes** — calcolate sul prezzo base più tutte le tasse non composte già applicate
7. **Shipping tax** — se una regola ha "Applies to Shipping" abilitato, il costo di spedizione è incluso nell'importo soggetto a tassa

La suddivisione delle tasse viene memorizzata con l'ordine in modo da poter vedere esattamente quali regole sono state applicate e quanto hanno contribuito ciascuna.

## Common Setups

### EU Store

1. Fai clic su **Load Presets** e carica il gruppo **EU VAT Rates**
2. Questo crea regole IVA per tutti gli Stati membri dell'UE con le loro attuali aliquote standard
3. Carica opzionalmente **UK VAT** se vendi anche nel Regno Unito

### US Store

1. Fai clic su **Load Presets** e carica il gruppo **US State Sales Tax**
2. Questo crea regole sulle tasse sulle vendite per tutti gli Stati degli Stati Uniti che riscuotono le tasse sulle vendite
3. Per le tasse a livello di città, aggiungi manualmente le regole con il campo città compilato e una priorità più alta

### Multi-Region Store

1. Carica diversi gruppi di preset per ogni mercato in cui vendi
2. Il sistema applica la tassa corretta in base alla posizione di ciascun cliente
3. Modifica le regole individuali come necessario per i requisiti specifici del tuo business

## Tips

- **Inizia con i preset** — carica i gruppi di preset per i tuoi mercati di destinazione, quindi personalizza le aliquote individuali invece di creare ogni regola da zero.
- **Usa la priorità con attenzione** — assegna valori di priorità più elevati alle regole locali più specifiche in modo che correttamente sovrascrivano le regole regionali più ampie.
- **Verifica attentamente le tasse composte** — le tasse composte sono rare. La maggior parte delle giurisdizioni utilizza tasse semplici (non composte). Abilita le tasse composte solo quando le tue normative locali richiedono specificamente il calcolo delle tasse sulle tasse.
- **Mantieni le regole attive/disattive** — invece di eliminare le regole fiscali per modifiche stagionali o temporanee, disattivali e riassegnale quando necessario.
- **Testa prima di andare online** — dopo aver configurato le tue regole fiscali, piazza un ordine di test da diversi indirizzi per verificare che le tasse corrette vengano applicate.