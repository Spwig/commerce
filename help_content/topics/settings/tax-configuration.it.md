---
title: Configurazione delle tasse
---

Le aliquote fiscali definiscono le tasse sui consumi, l'IVA e altre tasse applicate al momento del checkout in base alla posizione del cliente e al tipo di prodotto - configura le aliquote a livello di paese/regione/città con esenzioni opzionali per le categorie di prodotti. Spwig supporta le tasse composte (tassa su tassa), la selezione delle aliquote basata sulla priorità e gruppi di imposte predefinite per un rapido setup dei sistemi fiscali regionali (IVA UE, IVA USA). Le aliquote possono esentare tipi specifici di prodotti (cibo, libri, beni digitali) o categorie per il rispetto delle leggi fiscali locali.

Utilizza la configurazione fiscale per garantire la conformità legale ai requisiti di raccolta delle tasse nelle tue giurisdizioni di vendita.

## Configurazione delle aliquote fiscali

Ogni aliquota fiscale definisce:

**Ambito geografico**:
- Paese (obbligatorio)
- Stato/Provincia (opzionale)
- Città (opzionale)
- Modello del codice postale (opzionale, regex)

**Dettagli dell'aliquota**:
- **Aliquota fiscale**: Percentuale (es. 8,5%)
- **Nome**: Nome visualizzato (es. "IVA del California")
- **Priorità**: Maggiore priorità vince quando più aliquote corrispondono
- **Attivo**: Interruttore senza eliminazione

**Esenzioni**:
- **Tipi di prodotti esenti**: Beni digitali, beni fisici, servizi
- **Categorie esenti**: Categorie specifiche di prodotti (Cibo, Libri, Medici)

**Tassa composta**:
- **È composta**: Applica questa aliquota sopra le tasse precedenti (tassa su tassa)
- Esempio: L'IVA del Quebec si applica sull'IVA federale

---

## Scenario fiscali comuni

### IVA USA (a livello di stato)

```
Nome: IVA del California
Paese: USA
Stato: CA
Aliquota: 7,25%
Priorità: 50
```

### IVA UE (a livello di paese)

```
Nome: IVA del Regno Unito
Paese: GB
Aliquota: 20%
Priorità: 50

Nome: IVA della Germania
Paese: DE
Aliquota: 19%
Priorità: 50
```

### IVA canadese GST/PST (composto)

```
Aliquota 1: IVA federale
Paese: CA
Aliquota: 5%
Priorità: 100
È composta: No

Aliquota 2: IVA del Quebec
Paese: CA
Stato: QC
Aliquota: 9,975%
Priorità: 50
È composta: Sì  (si applica sul sottototale + IVA federale)
```

### Tassa a livello di città

```
Nome: IVA di Seattle
Paese: USA
Stato: WA
Città: Seattle
Aliquota: 10,1%
Priorità: 100
```

---

## Esenzioni fiscali

### Esenzioni per tipo di prodotto

Esenzione per interi tipi di prodotti:

- **Beni digitali**: Software, e-book, musica
- **Beni fisici**: Prodotti tangibili
- **Servizi**: Consulenza, installazione

Esempio: L'IVA non si applica ai beni digitali per i consumatori (in alcuni casi)

### Esenzioni per categoria

Esenzione per categorie specifiche di prodotti:

- Cibo e prodotti alimentari (spesso esenti o con aliquota ridotta)
- Libri e materiali didattici
- Materiali medici e farmaci
- Abbigliamento (alcune giurisdizioni)

Configurazione:
```
Nome: IVA del California
Aliquota: 7,25%
Categorie esenti: ["Cibo e bevande", "Farmaci da prescrizione"]
```

---

## Gruppi di imposte predefinite

Carica rapidamente configurazioni fiscali comuni:

**Preset di IVA USA**:
- Tutti e 50 gli stati + DC
- Aliquote a livello di stato
- Aggiornamenti automatici quando le aliquote cambiano

**Preset di IVA UE**:
- Tutti e 27 stati membri dell'UE
- Aliquote standard di IVA
- Logica di reverse charge per B2B

**Per utilizzare i preset**:
1. Impostazioni > Carrello > Imposte predefinite
2. Seleziona il gruppo di preset (es. "IVA USA 2026")
3. Clicca su "Carica preset"
4. Le aliquote vengono importate automaticamente
5. Personalizza come necessario

---

## Risoluzione delle priorità

Quando più aliquote corrispondono, vince la priorità più alta:

Esempio:
```
Cliente a Seattle, WA:

Aliquota A: Federale USA (Priorità 1) - 0%
Aliquota B: Stato di Washington (Priorità 50) - 6,5%
Aliquota C: Città di Seattle (Priorità 100) - 3,6%

Risultato: aliquota di Seattle (10,1% totale) si applica
```

---

## Opzioni di visualizzazione delle tasse

Configura in Impostazioni > Carrello > Impostazioni tasse:

- **Prezzi che includono le tasse**: Visualizza i prezzi con le tasse incluse (stile UE)
- **Mostra le tasse separatamente**: Mostra le tasse come elemento separato (stile USA)
- **Arrotonda le tasse**: Per articolo o per ordine
- **Etichetta delle tasse**: Personalizza l'etichetta ("IVA", "Tassa sulle vendite", "IVA")

---

## Test della configurazione fiscale

Prima di andare online:

1. Crea ordini di test da diverse giurisdizioni
2. Verifica che l'aliquota fiscale corretta venga applicata
3. Controlla che le esenzioni funzionino per le categorie escluse
4. Testa il calcolo delle tasse composte
5. Rivedi le voci delle tasse negli estratti conto

---

## Note sulla conformità

- **USA**: Le regole del Nexus richiedono la raccolta delle tasse negli stati in cui hai una presenza fisica o un nexus economico
- **UE**: Le aziende registrate all'IVA devono raccogliere l'IVA dai clienti dell'UE
- **Canada**: L'IVA/HST/PST varia per provincia
- **Consulta un professionista fiscale**: Le leggi fiscali cambiano frequentemente, verifica i requisiti correnti

---

## Consigli

- **Utilizza i preset fiscali** - Più veloce dell'inserimento manuale, aggiornamenti automatici
- **Monitora i limiti del Nexus** - Traccia le vendite per stato per il nexus economico USA
- **Imposta correttamente la priorità** - Città > Stato > Paese
- **Testa le tasse composte** - Verifica che i calcoli corrispondano alle somme previste
- **Aggiorna annualmente** - Le aliquote fiscali cambiano, rivedi ogni gennaio
- **Documenta le esenzioni** - Mantieni registri del motivo per cui le categorie sono esenti
- **Utilizza nomi descrittivi** - "IVA del California 2026" è meglio di "Tassa 1"
- **Abilita le tasse di default** - Più sicuro che dimenticare di applicare le tasse

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.