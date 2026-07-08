---
title: Impostazioni Predefinite dei Trasportatori
---

# Impostazioni Predefinite dei Trasportatori

Le impostazioni predefinite dei trasportatori definiscono trasportatori manuali (DHL, FedEx, UPS, trasportatori personalizzati) per spedizioni create senza integrazione API—ogni impostazione predefinita fornisce un logo del trasportatore, un modello URL di tracciamento e le impostazioni di visualizzazione. Le impostazioni predefinite del sistema (DHL, FedEx, UPS, USPS) sono preconfigurate e non possono essere eliminate, mentre le impostazioni personalizzate consentono ai commercianti di aggiungere trasportatori regionali o specializzati. Le impostazioni predefinite si collegano alle spedizioni manuali dove i commercianti inseriscono i numeri di tracciamento manualmente invece di acquistare etichette tramite API dei fornitori.

Utilizza le impostazioni predefinite dei trasportatori quando si creano spedizioni manuali o quando si desiderano collegamenti di tracciamento senza un'integrazione API completa.

## Impostazioni Predefinite del Sistema vs Personalizzate

**Impostazioni Predefinite del Sistema** (Preinstallate):
- DHL, FedEx, UPS, USPS, Royal Mail, Canada Post, Australia Post
- Non possono essere eliminate (is_system=True)
- È possibile sovrascrivere l'URL di tracciamento o il logo
- Modelli di URL di tracciamento predefiniti forniti

**Impostazioni Predefinite Personalizzate** (Create dai commercianti):
- Trasportatori regionali (OnTrac, LaserShip, postali regionali)
- Trasportatori specializzati (trasporti di merci, consegne specializzate)
- Possono essere modificate o eliminate
- Richiede un modello URL di tracciamento manuale

---

## Configurazione delle Impostazioni Predefinite dei Trasportatori

Ogni impostazione predefinita definisce:

**Impostazioni di Base**:
- **Nome**: Nome visualizzato del trasportatore (es. "DHL Express", "Corriere Locale")
- **Codice**: Identificatore interno (es. "dhl", "local_courier")
- **Logo**: Immagine del logo del trasportatore (opzionale, utilizza l'icona se non fornito)
- **Icona**: Icona FontAwesome come alternativa (es. "fa-truck")
- **Attivo**: Commutatore di visibilità

**Configurazione di Tracciamento**:
- **Modello URL di Tracciamento**: Modello di URL con il segnaposto {tracking_id}
- **Sovrascrittura URL di Tracciamento**: URL personalizzato (sovrascrive il modello predefinito)

**Impostazioni del Sistema** (solo impostazioni predefinite del sistema):
- **È un sistema**: Non può essere eliminato
- **È predefinito**: Un predefinito per tipo di trasportatore

---

## Modelli di URL di Tracciamento

Le URL di tracciamento utilizzano il segnaposto {tracking_id}:

**Esempi**:

DHL: `https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}`

FedEx: `https://www.fedex.com/fedextrack/?tracknumbers={tracking_id}`

UPS: `https://www.ups.com/track?tracknum={tracking_id}`

USPS: `https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_id}`

Personalizzato: `https://track.localcourier.com/tracking/{tracking_id}`

**Come Funziona**:
1. Il commerciante crea una spedizione con il numero di tracciamento "1234567890"
2. Il sistema sostituisce {tracking_id} con il numero effettivo
3. Il cliente clicca sul collegamento di tracciamento → reindirizzamento al sito del trasportatore
4. Risultato: `https://www.dhl.com/en/express/tracking.html?AWB=1234567890`

---

## Creare un'Impostazione Predefinita di Trasportatore Personalizzato

**Passo dopo passo**:

1. Vai a **Impostazioni > Spedizioni > Impostazioni Predefinite dei Trasportatori**
2. Clicca su "Aggiungi Impostazione Predefinita del Trasportatore"
3. Inserisci il nome (es. "OnTrac")
4. Inserisci il codice (slug: "ontrac")
5. Opzionale: Carica l'immagine del logo
6. Seleziona l'icona (fa-truck, fa-shipping-fast, ecc.)
7. Inserisci il modello URL di tracciamento con {tracking_id}
8. Abilita l'opzione Attivo = Sì
9. Salva

**Esempio - OnTrac**:
```
Nome: OnTrac
Codice: ontrac
URL di Tracciamento: https://www.ontrac.com/tracking.asp?tracking_number={tracking_id}
Icona: fa-truck
Attivo: Sì
```

---

## Sovrascrittura degli URL di Tracciamento delle Impostazioni Predefinite del Sistema

Le impostazioni predefinite del sistema possono avere sovrascritture degli URL di tracciamento:

**Caso d'uso**: Il tuo account del trasportatore ha un portale di tracciamento speciale

**Come Sovrascrivere**:
1. Modifica l'impostazione predefinita del sistema (es. DHL)
2. Inserisci l'URL di sovrascrittura nel campo "Sovrascrittura URL di Tracciamento"
3. La sovrascrittura ha la precedenza sul modello predefinito
4. Salva

**Esempio**:
```
Sistema: DHL
URL predefinito: https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}
URL di sovrascrittura: https://track.dhl.com/special-account/{tracking_id}
Risultato: URL di sovrascrittura utilizzato per tutte le spedizioni DHL
```

---

## Loghi dei Trasportatori

**Linee Guida per i Loghi**:
- Formato: PNG o SVG (SVG preferito per scalabilità)
- Dimensioni: Consigliate 200×60px
- Fondo: Trasparente o bianco
- Colore: Branding a colori pieni del trasportatore

**Icona di Riserva**:
Se non caricato alcun logo, il sistema visualizza l'icona FontAwesome:
- fa-truck (predefinito)
- fa-shipping-fast (espresso)
- fa-plane (trasporto aereo)
- fa-box (pacco)

---

## Utilizzo delle Impostazioni Predefinite dei Trasportatori nelle Spedizioni

Quando si crea una spedizione manuale:

1. Ordini > Dettaglio Ordine > Crea Spedizione
2. Seleziona la modalità "Spedizione Manuale"
3. Scegli il trasportatore dal menu a discesa delle impostazioni predefinite
4. Inserisci il numero di tracciamento
5. Opzionale: Sovrascrivi l'URL di tracciamento per questa spedizione
6. Salva

**Visualizzazione della Spedizione**:
- Mostrato il logo del trasportatore (o icona)
- Visualizzato il numero di tracciamento
- Collegamento di tracciamento cliccabile (utilizza il modello URL predefinito)

---

## Trasportatore Predefinito

Un'impostazione predefinita può essere impostata come predefinita per sistema:

**Caso d'uso**: Trasportatore più utilizzato automaticamente selezionato durante la creazione della spedizione

**Come Impostare**:
1. Modifica l'impostazione predefinita del trasportatore
2. Seleziona "È Predefinita"
3. Salva
4. L'impostazione predefinita precedente (se esisteva) viene automaticamente disattivata

**È consentita una sola impostazione predefinita** - impostare una nuova predefinita rimuove il flag di predefinita precedente.

---

## Consigli

- **Utilizzate nomi descrittivi** - "DHL Express" è meglio di "DHL"
- **Testate gli URL di tracciamento** - Verificate che il modello funzioni con numeri di tracciamento reali
- **Caricate i loghi dei trasportatori** - Aspetto professionale negli e-mail dei clienti
- **Non eliminate le impostazioni predefinite del sistema** - Sono preconfigurate correttamente
- **Utilizzate le sovrascritture con parsimonia** - Solo quando il trasportatore modifica il sistema di tracciamento
- **Impostate la predefinita per il trasportatore principale** - Risparmia tempo durante la creazione della spedizione
- **Mantenetete le impostazioni predefinite attive** - Disattivale solo se il trasportatore è dismesso
- **Documentate i trasportatori personalizzati** - Aggiungete note sui trasportatori regionali