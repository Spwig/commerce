---
title: Regole di prezzo attraente
---

Il prezzo attraente (chiamato anche prezzatura psicologica) regola automaticamente i prezzi dei tuoi prodotti in modo che terminino con cifre specifiche che risultano più attraenti per i clienti. Ad esempio, invece di visualizzare un prezzo di $20.00, il prezzo attraente può mostrare $19.99 — una tecnica ampiamente utilizzata che rende i prezzi sembrare più bassi a prima vista.

Spwig applica automaticamente le regole del prezzo attraente nel tuo negozio, per valuta, quindi devi impostare ogni regola solo una volta.

## Funzionamento del prezzo attraente

Quando viene calcolato il prezzo di un prodotto (compresi i prezzi dopo promozioni o sconti), Spwig verifica se esiste una regola attiva del prezzo attraente per quella valuta. Se esiste, il prezzo viene modificato prima di essere visualizzato ai clienti. La modifica si applica ai prezzi superiori al tuo limite minimo scelto.

Puoi configurare regole separate per ciascuna valuta accettata dal tuo negozio. Ad esempio, potresti utilizzare terminazioni `.99` per USD ma arrotondare al valore più vicino `¥10` per JPY.

## Creare una regola del prezzo attraente

1. Vai a **Catalogo > Regole del prezzo attraente**
2. Clicca su **+ Aggiungi regola del prezzo attraente**
3. Seleziona la **Valuta** a cui si applica questa regola (es. `USD`, `EUR`, `NZD`)
4. Scegli un **Tipo di regola** (vedi la tabella di seguito)
5. Opzionalmente, imposta un **Limite minimo di prezzo** per escludere i prezzi molto bassi
6. Seleziona **Applica ai prezzi di vendita** se desideri che il prezzo attraente venga applicato anche quando gli articoli sono in vendita
7. Assicurati che **Attivo** sia selezionato
8. Clicca su **Salva**

Solo una regola può esistere per valuta. Se devi modificare una regola, modifica quella esistente.

## Tipi di regole

| Tipo di regola | Esempio | Migliore per |
|----------------|---------|--------------|
| **Attraente con terminazione .99** | $20.50 → $19.99 | La maggior parte dei prodotti al dettaglio — il classico prezzo psicologico |
| **Attraente con terminazione .95** | $20.50 → $19.95 | Alternativa leggermente più dolce rispetto a .99 |
| **Attraente con terminazione .90** | $20.50 → $19.90 | Arrotondato ma comunque inferiore al dollaro successivo |
| **Arrotonda verso il basso** | $19.50 → $19.00 | Negozio che preferisce numeri interi |
| **Arrotonda verso l'alto** | $19.50 → $20.00 | Arrotondamento leggero per visualizzazioni pulite |
| **Arrotonda al valore più vicino 5** | $23.00 → $25.00 | Retail e mercati ad alto traffico |
| **Arrotonda al valore più vicino 10** | $23.00 → $20.00 | Oggetti con prezzi più elevati come elettrodomestici |
| **Arrotonda al valore più vicino 100** | $1,234 → $1,200 | Oggetti ad alto valore come mobili o elettronica |
| **Terminazione personalizzata** | Qualsiasi — specificare di seguito | Quando il tuo brand utilizza una terminazione specifica come `.88` |

### Terminazioni personalizzate

Se scegli **Terminazione personalizzata**, inserisci il valore della terminazione nel campo **Terminazione personalizzata**. Ad esempio, inserisci `0.88` per far sì che tutti i prezzi terminino in `.88` (comune in alcuni mercati asiatici).

## Limite minimo di prezzo

Utilizza il campo **Limite minimo di prezzo** per saltare il prezzo attraente per gli articoli con prezzi molto bassi in cui l'adattamento sembrerebbe strano. Ad esempio, impostando un limite di `5.00` i prodotti con un prezzo inferiore a $5 vengono visualizzati al loro prezzo calcolato effettivo senza alcun adattamento.

Lascialo a `0` per applicare il prezzo attraente a tutti i prezzi.

## Prezzi di vendita

Di default, il prezzo attraente viene applicato sia ai prezzi regolari che a quelli di vendita. Se desideri che i prezzi di vendita vengano visualizzati con i loro valori calcolati esatti (utile per i prezzi promozionali limitati nel tempo in cui i numeri esatti contano), deseleziona **Applica ai prezzi di vendita**.

## Disattivare una regola

Per fermare temporaneamente il prezzo attraente senza eliminare la regola, deseleziona **Attivo** e salva. La regola viene conservata e può essere riattivata in qualsiasi momento.

## Consigli

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- Inizia con gli ultimi `.99` se non sei sicuro — è la tecnica psicologica di prezzo più riconosciuta e funziona bene per la maggior parte dei tipi di prodotti.
- Imposta un limite minimo se vendi articoli a basso costo (sotto i $5) in modo che un articolo da $3,50 non venga ridotto a $2,99.
- Controlla i prezzi dopo aver abilitato una nuova regola visualizzando un prodotto sul negozio online — i prezzi con il charm vengono visualizzati in tempo reale.
- I yen giaponesi e altre valute a numeri interi funzionano meglio con **Arrotonda al più vicino 10** o **Arrotonda al più vicino 100**, poiché le finiture decimali sembrano insolite.
- Il charm dei prezzi viene applicato dopo tutti gli sconti e le promozioni, quindi anche i prezzi di vendita appariranno con il charm a meno che non deselezioni **Applica ai prezzi di vendita**.
- Puoi avere tipi di regole diversi per diverse valute, che è utile se vendi in diversi mercati con convenzioni di prezzo diverse.