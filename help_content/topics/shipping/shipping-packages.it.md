---
title: Confezioni di spedizione
---

# Confezioni di spedizione

Le confezioni di spedizione definiscono dimensioni predefinite di scatole e buste per il calcolo delle tariffe e l'imballaggio automatico—specificare le dimensioni interne (spazio utilizzabile), lo spessore delle pareti (dimensioni esterne per le API dei carrier), i limiti di peso e il costo di imballaggio. I carrier utilizzano le dimensioni esterne per calcolare il peso dimensionale per quotazioni di tariffe accurate. Le confezioni hanno un ordinamento di priorità per gli algoritmi di imballaggio automatico che selezionano automaticamente le combinazioni ottimali di confezioni per adattarsi agli articoli del carrello.

Configurare le confezioni quando si utilizzano le API dei carrier per quotazioni in tempo reale o quando si necessita di calcoli accurati del peso dimensionale.

## Configurazione delle confezioni

Ogni confezione definisce:

**Dimensioni**:
- **Lunghezza interna**: Spazio utilizzabile all'interno (cm)
- **Larghezza interna**: Spazio utilizzabile all'interno (cm)
- **Altezza interna**: Spazio utilizzabile all'interno (cm)
- **Spessore delle pareti**: Spessore del materiale di imballaggio (cm)

**Dimensioni esterne** (calcolate automaticamente):
```
Lunghezza esterna = Lunghezza interna + (2 × Spessore delle pareti)
Larghezza esterna = Larghezza interna + (2 × Spessore delle pareti)
Altezza esterna = Altezza interna + (2 × Spessore delle pareti)
```

**Peso e costo**:
- **Peso a vuoto**: Peso della confezione vuota (grammi)
- **Peso massimo**: Capacità di carico massima (grammi)
- **Costo**: Costo del materiale di imballaggio (per l'ottimizzazione dei costi)

**Proprietà**:
- **Nome**: Identificatore della confezione (es. "Small Box", "Large Envelope")
- **Tipo**: Scatola o Busta
- **Priorità**: Ordine di selezione per l'imballaggio automatico (minore = maggiore priorità)
- **Attiva**: Toggle disponibilità

---

## Perché le dimensioni esterne contano

I carrier calcolano **peso dimensionale** a partire dalle dimensioni esterne:

**Formula del peso dimensionale**:
```
Dim Weight = (Lunghezza × Larghezza × Altezza) / Divisore

Divisori comuni:
- DHL: 5000
- FedEx/UPS: 5000 (nazionale), 6000 (internazionale)
```

**Esempio**:
```
Scatola piccola:
Interna: 20cm × 15cm × 10cm
Spessore delle pareti: 0,5cm
Esterna: 21cm × 16cm × 11cm

Peso dimensionale = (21 × 16 × 11) / 5000 = 0,74kg

Se peso reale = 0,5kg → Il carrier addebita 0,74kg (peso dimensionale più alto)
```

**Perché l'accuratezza è importante**: Dimensioni inesatte → quotazioni di tariffe errate → cliente sovrapprezzato o sottoprezzato.

---

## Dimensioni di confezione comuni

### Busta imbottita piccola

```
Interna: 25cm × 18cm × 2cm
Spessore delle pareti: 0,3cm
Peso massimo: 500g
Tipo: Busta
Utilizzo: Documenti, libri, gioielli
```

### Scatola piccola

```
Interna: 20cm × 15cm × 10cm
Spessore delle pareti: 0,5cm
Peso massimo: 5kg
Tipo: Scatola
Utilizzo: Piccoli elettronici, cosmetici, accessori
```

### Scatola media

```
Interna: 30cm × 25cm × 20cm
Spessore delle pareti: 0,5cm
Peso massimo: 15kg
Tipo: Scatola
Utilizzo: Abbigliamento, scarpe, articoli per la cucina
```

### Scatola grande

```
Interna: 45cm × 35cm × 30cm
Spessore delle pareti: 0,6cm
Peso massimo: 30kg
Tipo: Scatola
Utilizzo: Articoli in grandi quantità, prodotti multipli, elettronica di grandi dimensioni
```

---

## Algoritmo di imballaggio automatico

Il sistema seleziona automaticamente le confezioni per gli articoli del carrello:

**Come funziona**:
1. Calcolare il volume totale degli articoli del carrello
2. Ordinare le confezioni per priorità (numeri più bassi per primi)
3. Provare a inserire gli articoli in una singola confezione
4. Se non si adatta, provare la dimensione successiva della confezione
5. Se nessuna singola confezione si adatta, combinare più confezioni
6. Ottimizzare in base all'impostazione `optimize_for`

**Modalità di ottimizzazione**:
- **Costo**: Minimizzare il costo di imballaggio
- **Volume**: Minimizzare lo spazio sprecato
- **Conteggio**: Minimizzare il numero di confezioni

**Esempio**:
```
Articoli del carrello:
- Articolo A: 10cm × 8cm × 5cm, 200g
- Articolo B: 15cm × 12cm × 8cm, 400g

Confezioni (per priorità):
1. Scatola piccola (20×15×10, priorità=1)
2. Scatola media (30×25×20, priorità=2)

Algoritmo:
Prova Scatola piccola: Entrambi gli articoli si adattano
Risultato: 1× Scatola piccola (ottimizzato per il conteggio)
```

---

## Priorità delle confezioni

**La priorità determina l'ordine di imballaggio**:

Priorità 1 (più alta): Le confezioni piccole vengono provate per prime
Priorità 10: Le confezioni grandi sono l'ultima risorsa

**Strategia**:
- Confezioni piccole = numeri di priorità bassi (1-3)
- Confezioni medie = priorità media (4-6)
- Confezioni grandi = numeri di priorità alti (7-10)

**Perché**: Iniziare con la confezione più piccola, scalare se necessario → minimizza i costi di spedizione.

---

## Accuratezza dello spessore delle pareti

Misurare l'imballaggio effettivo:

**Come misurare**:
1. Ottenere una scatola vuota
2. Misurare le dimensioni interne (interno)
3. Misurare le dimensioni esterne (esterno)
4. Calcolare: `(Esterno - Interno) / 2 = Spessore delle pareti`

**Esempio**:
```
Larghezza interna: 20cm
Larghezza esterna: 21cm
Spessore delle pareti: (21 - 20) / 2 = 0,5cm
```

**Spessori comuni**:
- Busta imbottita: 0,2-0,4cm
- Cartone a parete singola: 0,4-0,6cm
- Cartone a parete doppia: 0,8-1,0cm

---

## Creare un preset di confezione

**Passo dopo passo**:

1. Impostazioni > Spedizione > Confezioni di spedizione
2. Fare clic su "Aggiungi confezione di spedizione"
3. Inserire il nome (es. "Scatola media")
4. Selezionare il tipo (Scatola o Busta)
5. Inserire le dimensioni interne (L × W × H in cm)
6. Inserire lo spessore delle pareti (cm)
7. Il sistema calcola automaticamente le dimensioni esterne
8. Inserire il peso a vuoto (peso della confezione vuota in grammi)
9. Inserire il peso massimo (capacità di carico in grammi)
10. Opzionale: Inserire il costo (per l'ottimizzazione dei costi)
11. Impostare la priorità (1-10)
12. Toggle attiva = Sì
13. Salvare

---

## Test della selezione delle confezioni

**Test manuale**:
1. Aggiungere prodotti al carrello di test
2. Procedere al checkout
3. Selezionare il metodo di spedizione in tempo reale (usa le confezioni)
4. Verificare che venga restituita una tariffa ragionevole
5. Controllare la risposta del carrier (i log delle API mostrano le confezioni selezionate)

**Anteprima dell'imballaggio automatico**:
- Alcuni account di provider di spedizione mostrano la suddivisione delle confezioni
- Visualizzare quali confezioni sono state selezionate per il carrello
- Verificare l'imballaggio ottimale

---

## Siti utili

- **Misura accuratamente** - Dimensioni inesatte → tariffe dei carrier errate
- **Includi lo spessore delle pareti** - Critico per il peso dimensionale
- **Inizia con 3-4 dimensioni** - Scatole piccole, medie, grandi coprono la maggior parte dei casi
- **Imposta pesi massimi realistici** - Capacità della scatola, non limite teorico
- **Usa la priorità con saggezza** - Scatole piccole priorità 1, scatole grandi priorità 10
- **Testa con prodotti reali** - Verifica che l'imballaggio automatico selezioni le dimensioni corrette
- **Aggiorna quando cambia l'imballaggio** - Nuovo fornitore = rimesura le dimensioni
- **Considera articoli speciali** - Articoli fragili potrebbero richiedere dimensioni di scatole specifiche
- **Mantieni le confezioni attive al minimo** - Troppi opzioni rallentano l'algoritmo di imballaggio automatico
- **Documenta l'imballaggio** - Nota quali prodotti si adattano a quali confezioni
