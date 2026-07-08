---
title: Campi personalizzati
---

I campi personalizzati ti permettono di aggiungere dati aggiuntivi ai Prodotti, alle Categorie, agli Ordini e ai Profili dei Clienti senza modificare alcun codice. Utilizzali per archiviare informazioni specifiche del tuo business, come ID di API esterne, ubicazioni dei magazzini, dati di conformità o qualsiasi attributo necessario al tuo negozio.

## Accesso ai Campi Personalizzati

Naviga verso **Impostazioni > Campi Personalizzati** nel menu laterale di amministrazione.

![Pagina Campi Personalizzati](/static/core/admin/img/help/custom-fields/custom-fields-page.webp)

## Concetti Principali

### Gruppi di Campi

I campi sono organizzati in **gruppi** — raccolte logiche che vengono visualizzate insieme come una sezione. Ad esempio, un gruppo "Informazioni di Spedizione" potrebbe contenere campi per l'ubicazione del magazzino, le dimensioni del pacco e la classificazione Hazmat.

### Definizioni dei Campi

Ogni definizione di campo controlla:
- **Nome**: L'etichetta visualizzata nei moduli
- **Slug**: La chiave leggibile da macchina utilizzata per lo storage JSON e le risposte API
- **Tipo di Campo**: Che tipo di input viene visualizzato (testo, numero, menu a discesa, ecc.)
- **Validazione**: Regole come min/max, lunghezza massima, regex o scelte consentite
- **Visibilità**: Se il campo viene visualizzato nel negozio online

### Tipi di Campo Supportati

| Tipo | Descrizione | Utilizzo Esempio |
|------|-------------|-------------|
| **Testo** | Input di testo a una riga | ID API esterno, codice marchio |
| **Testo lungo** | Testo a più righe | Note per gestione speciale |
| **Numero** | Valori interi | Quantità minima di ordine |
| **Decimale** | Valori decimali | Sovrascrittura del peso, dimensione personalizzata |
| **Sì/No** | Interruttore a spillo | È fragile, richiede firma |
| **Data** | Selettore di data | Data di rilascio, data di scadenza |
| **Data e Ora** | Selettore di data e ora | Disponibilità programmata |
| **URL** | Indirizzo web | Link al fornitore, URL del foglio specifiche |
| **Email** | Indirizzo email | Contatto produttore |
| **Menu a discesa** | Elenco a singola selezione | Tipo di materiale, paese d'origine |
| **Selezione multipla** | Elenco a selezione multipla | Certificazioni, tag |
| **Colore** | Selettore di colore | Colore del marchio, colore dell'etichetta |

## Gestione dei Campi Personalizzati

### Creare un Gruppo di Campi

1. Apri **Impostazioni > Campi Personalizzati**
2. Seleziona la scheda del modello (Prodotti, Categorie, Ordini o Profili dei Clienti)
3. Clicca su **Aggiungi Gruppo**
4. Inserisci un **Nome del Gruppo** (es. "Integrazioni Esterne")
5. Abilita opzionalmente **Mostra nel negozio online** se i clienti devono vedere questi campi
6. Clicca su **Salva Gruppo**

### Aggiungere un Campo a un Gruppo

1. Sul cartellino del gruppo, clicca su **Aggiungi Campo**
2. Inserisci un **Nome del Campo** — lo slug viene generato automaticamente
3. Scegli il **Tipo di Campo**
4. Imposta opzionalmente un **Testo di Aiuto** e un **Valore Predefinito**
5. Configura le opzioni di validazione (varia in base al tipo di campo):
   - Testo: lunghezza massima, pattern regex
   - Numero/Decimale: valori min e max
   - Menu a discesa: definisci l'elenco delle scelte
6. Imposta le opzioni del campo:
   - **Obbligatorio**: I commercianti devono compilare questo campo al salvataggio
   - **Mostra nel negozio online**: Mostra il valore sulla pagina rivolta ai clienti
   - **Traducibile**: Consente al valore di essere tradotto (solo testo/testo lungo)
7. Clicca su **Salva Campo**

### Modifica e Riordino

- Clicca sull'icona **matita** per modificare qualsiasi gruppo o campo
- Trascina la **maniglia di presa** per riordinare i gruppi o i campi all'interno di un gruppo
- Le modifiche hanno effetto immediato su tutti i moduli pertinenti

### Eliminazione di Gruppi e Campi

- Clicca sull'icona **cestino** su un gruppo o campo per eliminarlo
- Le eliminazioni sono **eliminazioni soft** — i dati vengono conservati nel database ma nascosti dai moduli
- Questo protegge i dati esistenti da una perdita accidentale

## Utilizzo dei Campi Personalizzati nei Moduli

Una volta definiti i campi personalizzati per un modello, un **tab Campi Personalizzati** appare automaticamente sulla relativa pagina di modifica.

### Prodotti e Categorie

1. Apri qualsiasi prodotto o categoria per la modifica
2. Clicca sul **tab Campi Personalizzati**
3. Compila i campi necessari
4. Clicca su **Salva** — i valori vengono salvati insieme al record

### Ordini

I valori dei campi personalizzati per gli ordini vengono visualizzati come una **sezione in sola lettura** sulla pagina dei dettagli dell'ordine. I campi personalizzati degli ordini vengono in genere impostati tramite l'API o al momento del checkout.

### Profili dei Clienti

1. Apri un profilo cliente
2. Clicca sul **tab Campi Personalizzati**
3. Compila i campi e salva

## Accesso API

### Elenco delle Definizioni dei Campi

Recupera tutte le definizioni dei campi personalizzati per un modello:

```
GET /api/custom-fields/definitions/?model=product&app=catalog
```

**Risposta:"
```
[
  {
    "id": 1,
    "name": "External API ID",
    "slug": "external_api_id",
    "field_type": "text",
    "is_required": false,
    "group": { "name": "External Integrations" }
  }
]
```

### Lettura dei Valori dei Campi Personalizzati

I valori dei campi personalizzati vengono inclusi nell'oggetto JSON `custom_fields` nelle risposte API del modello:

```
{
  "id": 42,
  "name": "Blue Widget",
  "custom_fields": {
    "external_api_id": "API-12345",
    "is_fragile": true
  }
}
```

### Scrittura dei Valori dei Campi Personalizzati

Includi `custom_fields` quando crei o aggiorni un record tramite l'API:

```
{
  "custom_fields": {
    "external_api_id": "API-67890",
    "warehouse_location": "WH-A3"
  }
}
```

I valori vengono validati rispetto alle definizioni dei campi. I valori non validi restituiscono un errore `400` con dettagli.

### Query tramite Campi Personalizzati

I campi personalizzati sono indicizzati per query rapide del database. Filtra i record utilizzando i filtri di query del database:

```
GET /api/products/?custom_fields__warehouse_location=WH-A3
```

## Visualizzazione nel Negozio Online

### Per gli Sviluppatori di Temi

Utilizza il tag di modello `render_custom_fields` per visualizzare i campi personalizzati nel negozio online:

```
{% load custom_fields_tags %}

{# Rendi tutti i campi visibili nel negozio online #}
{% render_custom_fields product %}

{# Ottieni un valore di campo specifico #}
{% get_custom_field product "warehouse_location" as location %}
<p>Spedito da: {{ location }}</p>
```

Vengono visualizzati solo i campi con **Mostra nel negozio online** abilitato sia a livello di gruppo che di campo.

## Linee Guida per l'Utilizzo

- **Utilizza nomi descrittivi** — i nomi dei campi appaiono nei moduli e nel negozio online
- **Imposta il testo di aiuto** — guida i commercianti su cosa inserire in ogni campo
- **Raggruppa i campi correlati** — mantieni i moduli organizzati e intuitivi
- **Utilizza valori predefiniti** — imposta valori sensati per ridurre l'inserimento di dati
- **Sii selettivo con la visibilità nel negozio online** — mostra solo i campi che sono significativi per i clienti
- **Utilizza gli slug nelle integrazioni** — gli slug sono identificatori stabili; i nomi dei campi possono cambiare

## Risoluzione dei Problemi

**Il tab Campi Personalizzati non appare:"
- Verifica che esista almeno un gruppo di campi attivo per quel modello
- Controlla che la classe amministrativa includa il `CustomFieldsAdminMixin`
- Pulisci la cache e ricarica la pagina

**I valori dei campi non vengono salvati:"
- Assicurati che i campi obbligatori siano compilati
- Controlla le regole di validazione (min/max, pattern regex, scelte consentite)
- Verifica che il campo sia attivo e non eliminato in modo soft

**L'API restituisce custom_fields vuoti:"
- Conferma che il modello abbia il `CustomFieldsMixin`
- Controlla che esistano definizioni dei campi per il tipo di contenuto corretto
- Assicurati che il serializzatore includa `CustomFieldsSerializerMixin`

## Argomenti Correlati

- [Aggiunta di Prodotti](#)
- [Impostazioni del Negozio](#)