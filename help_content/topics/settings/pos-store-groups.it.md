---
title: POS Store Groups
---

I gruppi di negozi organizzano più ubicazioni retail con configurazioni condivise. Invece di configurare ogni terminale singolarmente, raggruppa i terminali per regione, franchising o tipo di ubicazione e applica le impostazioni a livello di gruppo. I gruppi supportano l'ereditarietà delle impostazioni—valuta, lingua, fuso orario, modelli di ricevute e contenuti promozionali si propagano da gruppo a singoli negozi. Questo semplifica la gestione per i commercianti con più ubicazioni, mantenendo flessibilità per le sovrascritture specifiche del negozio quando necessario.

Utilizza i gruppi di negozi quando gestisci più ubicazioni retail, franchising o mercati regionali con requisiti operativi diversi.

![Elenco dei gruppi di negozi](/static/core/admin/img/help/pos-store-groups/storegroup-list.webp)

## Cosa sono i gruppi di negozi?

I gruppi di negozi sono contenitori organizzativi per magazzini e terminali che condividono caratteristiche comuni:

**Strategie di gruppo comuni**:
- **Geografiche**: Nord, Sud, Costa Ovest, Costa Est
- **Franchising**: Negozio Franchising A, Negozio Franchising B, Negozio Corporativo
- **Formato**: Ubicazioni in centro commerciale, Negozio autonomo, Negozio temporaneo
- **Mercato**: Negozio domestico, Negozio europeo, Negozio Asia-Pacifico

I gruppi non modificano l'operazione fisica dei terminali—forniscono uno strato di configurazione che semplifica la gestione su larga scala.

## Quando utilizzare i gruppi di negozi

**Singola ubicazione** - Non necessari. Configura i terminali direttamente.

**2-3 ubicazioni con impostazioni identiche** - I gruppi sono opzionali. Potrebbe essere più facile configurare i terminali direttamente.

**4+ ubicazioni** - I gruppi sono fortemente raccomandati. La configurazione centralizzata risparmia tempo.

**Operazioni a livello internazionale** - I gruppi sono essenziali. Diverse valute, lingue e fusi orari richiedono sovrascritture a livello di gruppo.

**Operazioni di franchising** - I gruppi sono critici. Ogni franchisor ha bisogno di impostazioni indipendenti mantenendo la coerenza del brand.

## Gerarchia dell'ereditarietà delle impostazioni

Spwig POS utilizza una cascata di 4 livelli di impostazioni (priorità più alta a priorità più bassa):

| Livello | Priorità | Esempio | Caso d'uso |
|---------|----------|---------|----------|
| **Terminale** | 1 (Maggiore) | Il terminale 5 sovrascrive la larghezza della carta a 58mm | Un singolo terminale ha hardware della stampante unico |
| **Negozio** | 2 | Il negozio 2 sovrascrive la valuta a GBP | Ubicazione UK tra negozi principalmente statunitensi |
| **Gruppo** | 3 | Il gruppo europeo imposta il fuso orario a CET | Coerenza regionale in più negozi |
| **Sito** | 4 (Minore) | Predefinito globale: USD, inglese, UTC | Impostazioni di fallback per tutte le impostazioni non configurate |

**Come funziona**:
- Il sistema controlla prima le impostazioni del terminale
- Se non sono impostate, controlla le impostazioni del negozio
- Se non sono impostate, controlla le impostazioni del gruppo
- Se non sono impostate, utilizza i predefiniti del sito

**Esempio**:
- Predefinito globale: Valuta = USD, Lingua = Inglese
- Gruppo "Negozio europeo": Valuta = EUR, Lingua = non impostato
- Negozio "Flagship di Parigi": Valuta = non impostato, Lingua = Francese
- Terminale "Cassa 1 di Parigi": Valuta = non impostato, Lingua = non impostato

**Risultato per la Cassa 1 di Parigi**:
- Valuta: EUR (ereditata dal gruppo)
- Lingua: Francese (ereditata dal negozio)

Questa cascata consente di avere impostazioni generali ampie con sovrascritture mirate quando necessario.

## Creare un gruppo di negozi

Naviga a **POS > Gruppi di negozi** e fai clic su **+ Aggiungi gruppo di negozi**:

![Form per l'aggiunta di un gruppo di negozi](/static/core/admin/img/help/pos-store-groups/storegroup-add-form.webp)

### Configurazione di base

**Nome del gruppo** - Etichetta descrittiva (es. "Negozio della costa ovest", "Franchising europeo", "Ubicazioni in centro commerciale")

**Codice** - Identificatore breve e univoco (es. "WEST", "EUR", "MALL"):
- Utilizzato internamente per riferimenti
- Deve essere univoco in tutti i gruppi
- 2-10 caratteri, alfanumerici
- Consigliato l'uso di maiuscole per coerenza

**Ordine di ordinamento** - Controlla l'ordine di visualizzazione nelle liste amministrative (i numeri più bassi appaiono per primi):
- Utilizza multipli di 10: 10, 20, 30 (consente di inserire nuovi gruppi tra quelli esistenti)
- Aiuta a organizzare i gruppi in modo logico (ordine geografico, ordine di dimensione, ecc.)

### Sovrascritture regionali

**Sovrascrittura della valuta** - Imposta la valuta a livello di gruppo diversa dal predefinito del sito:
- Esempio: Il gruppo europeo utilizza EUR, il gruppo Asia-Pacifico utilizza JPY
- I terminali in questo gruppo predefinito utilizzano questa valuta
- Influisce sulla visualizzazione dei prezzi, sulla conciliazione del contante e sui report

**Sovrascrittura della lingua** - Imposta la lingua a livello di gruppo diversa dal predefinito del sito:
- Esempio: I negozi francesi utilizzano francese, i negozi tedeschi utilizzano tedesco
- Influisce sulla lingua dell'interfaccia POS, sulla lingua delle ricevute (se il modello lo supporta)
- Il personale vede l'interfaccia POS in questa lingua quando si connette a terminali del gruppo

**Sovrascrittura del fuso orario** - Imposta il fuso orario a livello di gruppo diverso dal predefinito del sito:
- Esempio: I negozi della costa ovest utilizzano America/Los_Angeles, i negozi europei utilizzano Europe/Paris
- Influisce sui timestamp degli orari di lavoro, sulla programmazione dei report e sulla programmazione delle diapositive promozionali
- Garantisce che i report degli orari di lavoro siano allineati alle ore di lavoro locali

**Quando sovrascrivere**:
- **Valuta**: Sovrascrivi sempre per le ubicazioni internazionali (diverse valute di pagamento)
- **Lingua**: Sovrascrivi per i mercati non parlanti inglese (contenuti rivolti ai clienti)
- **Fuso orario**: Sovrascrivi per le ubicazioni a più di 2 ore di differenza dal predefinito del sito (timestamp locali accurati)

## Associare i magazzini ai gruppi

Dopo aver creato un gruppo, assegna i magazzini a esso:

1. Naviga a **Catalogo > Magazzini**
2. Modifica il magazzino che rappresenta un'ubicazione del negozio
3. Imposta il campo **Gruppo di negozi** sul gruppo creato
4. Salva

Tutti i terminali assegnati a questo magazzino ora ereditano le impostazioni del gruppo.

**Configurazione di esempio**:
- Crea gruppo: "Negozio europeo" (Valuta: EUR, Lingua: non impostato, Fuso orario: CET)
- Crea magazzini: "Negozio di Parigi", "Negozio di Berlino", "Negozio di Roma"
- Assegna tutti e 3 i magazzini al gruppo "Negozio europeo"
- Crea terminali: "Cassa 1 di Parigi", "Cassa 1 di Berlino", "Cassa 1 di Roma"
- Ogni terminale eredita la valuta EUR e il fuso orario CET dal gruppo
- Sovrascrivi la lingua a livello di negozio: Parigi=Francese, Berlino=Tedesco, Roma=Italiano

## Impostazioni controllate dai gruppi

I gruppi possono sovrascrivere queste impostazioni:

**Impostazioni operative**:
- Valuta (influenza la visualizzazione dei prezzi e la conciliazione del contante)
- Lingua (influenza la lingua dell'interfaccia POS)
- Fuso orario (influenza i timestamp e la programmazione)

**Impostazioni del contenuto** (tramite modelli a ambito):
- Modelli di ricevute (crea progettazioni di ricevute specifiche per il gruppo)
- Diapositive promozionali (targetizza le promozioni a gruppi specifici)

**Non controllate dai gruppi**:
- Configurazione hardware del terminale (configurata per terminale)
- Assegnamento del personale (configurato per terminale)
- Livelli di stock del magazzino (configurato per magazzino)
- Conti dei fornitori di pagamento (configurati a livello sito o per fornitore)

## Esempi reali

### Esempio 1: Retail di moda internazionale

**Configurazione**:
- 50 negozi in 5 paesi
- Ogni paese ha valuta, lingua e requisiti fiscali diversi

**Struttura dei gruppi**:
- Gruppo: "Negozio USA" (USD, inglese, America/New_York)
  - 20 magazzini (NY, LA, Chicago, ecc.)
  - 60 terminali
- Gruppo: "Negozio UK" (GBP, inglese, Europe/London)
  - 10 magazzini (Londra, Manchester, ecc.)
  - 30 terminali
- Gruppo: "Negozio UE" (EUR, non impostato, Europe/Paris)
  - 15 magazzini (Parigi, Berlino, Roma, ecc.)
  - 45 terminali
  - Sovrascrittura della lingua a livello di negozio (Parigi=Francese, Berlino=Tedesco, Roma=Italiano)
- Gruppo: "Negozio Giappone" (JPY, giapponese, Asia/Tokyo)
  - 5 magazzini (Tokyo, Osaka, ecc.)
  - 15 terminali

**Vantaggi**:
- Una configurazione del gruppo si applica a tutti i negozi in ogni mercato
- Modelli di ricevute specifici per i gruppi (formato IVA per UE, tasse di vendita per USA)
- Diapositive promozionali mirate per regione (USA: Vendita Memorial Day, UE: Vendita delle vacanze estive)

### Esempio 2: Catena di caffetterie

**Configurazione**:
- 30 ubicazioni, tutti nello stesso paese, ma diversi formati

**Struttura dei gruppi**:
- Gruppo: "Ubicazioni in centro commerciale" (non impostato, non impostato, non impostato)
  - 10 negozi in centro commerciale
  - Diapositive promozionali con orari estesi (aperti fino alle 21:00)
  - Modello di ricevuta con codice QR per la validazione del parcheggio del centro commerciale
- Gruppo: "Negozio autonomo" (non impostato, non impostato, non impostato)
  - 15 negozi in strada
  - Diapositive promozionali con orari standard
  - Modello di ricevuta standard
- Gruppo: "Ubicazioni aeroportuali" (non impostato, non impostato, non impostato)
  - 5 negozi aeroportuali
  - Diapositive promozionali a 24 ore
  - Modello di ricevuta con integrazione del codice QR per le informazioni sui voli

**Vantaggi**:
- Contenuti promozionali diversi per diversi formati
- Personalizzazioni specifiche per l'ubicazione delle ricevute
- Gestione semplificata (aggiorna un gruppo invece di aggiornare 10 singoli negozi)

### Esempio 3: Operazione di franchising

**Configurazione**:
- 100 negozi, 20 diversi franchisor

**Struttura dei gruppi**:
- Gruppo: "Franchisor A" (non impostato, non impostato, non impostato)
  - 10 negozi gestiti da Franchisor A
  - Informazioni di contatto di Franchisor A sulle ricevute (tramite modello di ricevuta del gruppo)
  - Contenuti promozionali di Franchisor A (eventi locali, offerte speciali)
- Gruppo: "Franchisor B" (non impostato, non impostato, non impostato)
  - 8 negozi gestiti da Franchisor B
  - Informazioni di contatto di Franchisor B sulle ricevute
  - Contenuti promozionali di Franchisor B
- (Ripetere per tutti i franchisor)
- Gruppo: "Negozio aziendale" (non impostato, non impostato, non impostato)
  - 5 negozi di proprietà aziendale
  - Branding aziendale e promozioni

**Vantaggi**:
- Ogni franchisor gestisce le proprie impostazioni del gruppo
- Coerenza del brand mantenuta tramite predefiniti del sito
- Indipendenza del franchisor tramite sovrascritture del gruppo

## Gestione delle impostazioni del gruppo

**Modificare le impostazioni del gruppo** influisce su tutti i terminali in quel gruppo:
- Modifica della valuta: Tutti i terminali del gruppo passano alla nuova valuta alla prossima sincronizzazione
- Modifica della lingua: Tutti i terminali del gruppo passano alla nuova lingua alla prossima sincronizzazione
- Modifica del fuso orario: Tutti i terminali del gruppo ricalcolano i timestamp alla prossima sincronizzazione

**Considerazioni sull'impatto**:
- Testa le modifiche su un singolo terminale prima di applicarle a tutto il gruppo
- Notifica il personale delle modifiche imminenti (es. cambio di lingua)
- Programma le modifiche durante gli orari di bassa intensità per minimizzare i disagi

**Rimuovere un gruppo**:
- Riassocia tutti i magazzini a un altro gruppo o rimuovi l'assegnazione del gruppo
- I terminali perdono le impostazioni a livello di gruppo e ricorrono ai predefiniti del sito
- Non è possibile eliminare un gruppo mentre i magazzini sono ancora assegnati

## Consigli

- **Utilizza codici significativi** - "WEST" è più chiaro di "GRP1" quando si esaminano le configurazioni
- **Pianifica la gerarchia prima di creare i gruppi** - Pensa alla struttura organizzativa prima; il ristrutturare in seguito è faticoso
- **Testa le impostazioni del gruppo con un singolo terminale** - Prima di assegnare 50 magazzini a un gruppo, testa le impostazioni del gruppo con un singolo terminale
- **Sovrascrivi raramente a livello di negozio** - Troppi sovrascritture a livello di negozio annullano lo scopo dei gruppi
- **Documenta lo scopo dei gruppi** - Nota nel nome del gruppo ciò che rende questo gruppo distintivo (geografia, formato, franchisor)
- **Utilizza l'ordine di ordinamento in modo strategico** - Ordina i gruppi per importanza (Negozio aziendale in primo luogo) o per geografia (da ovest a est) per una navigazione più facile
- **Mantieni un numero ragionevole di gruppi** - 20+ gruppi suggeriscono un'eccessiva segmentazione; considera di consolidare
- **Le sovrascritture della valuta sono permanenti** - Cambiare la valuta di un gruppo durante l'operazione complica il contabile; pianifica con attenzione

Ricorda: Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.