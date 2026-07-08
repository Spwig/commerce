---
title: Editor della tipografia
---

L'Editor della tipografia è un'utilità di stile condivisa che ti dà il pieno controllo sull'aspetto del testo. Si apre come un pannello galleggiante ogni volta che modifichi le proprietà della tipografia su qualsiasi elemento all'interno del Page Builder, Header/Footer Builder o Menu Builder.

![Editor della tipografia](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## Anteprima in tempo reale

L'editor mostra un confronto a lato a lato in alto nel pannello:

| Scatola | Scopo |
|--------|-------|
| **Corrente** | Mostra "The quick brown fox..." nello stile di tipografia esistente |
| **Nuovo** | Aggiorna in tempo reale mentre modifichi le impostazioni, mostrando il risultato prima di applicare |

Questo ti permette di confrontare lo stato prima e dopo senza applicare alcun cambiamento.

## Scheda Font

La scheda Font è la vista predefinita quando l'editor si apre.

**Famiglia del font** — Un menu a discesa cercabile con oltre 70 font organizzati per categoria. Ogni font viene visualizzato nel proprio stile per poter vedere come appare prima di selezionarlo. I font vengono caricati su richiesta da Google Fonts quando necessario.

**Dimensione del font** — Campo numerico con un selettore di unità che supporta px, em, rem e %. Il valore predefinito è 16px.

**Peso del font** — Un cursore da 100 (Sottile) a 900 (Nero):

| Valore | Nome |
|-------|------|
| 100 | Sottile |
| 200 | Extra Light |
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Nero |

Non tutti i font supportano tutti e nove i pesi. L'editor mostra quali pesi sono disponibili per la famiglia di font selezionata.

**Stile del font** — Pulsanti di commutazione per Normale, Corsivo e Obliquo.

## Scheda Spaziatura

Regola con precisione lo spazio intorno e tra i caratteri:

| Controllo | Cosa Fa | Predefinito |
|----------|--------|-----------|
| **Altezza della riga** | Spazio verticale tra le righe di testo | normale |
| **Spaziatura tra lettere** | Spazio orizzontale tra i singoli caratteri | normale |
| **Spaziatura tra parole** | Spazio orizzontale tra le parole | normale |
| **Ritorno del testo** | Rientro della prima riga in un paragrafo | 0 |

Ogni controllo di spaziatura include un selettore di unità (px, em, rem, %).

## Scheda Stile

Controlla le decorazioni del testo ed effetti visivi:

- **Decorazione del testo** — Nessuna, Sottolineato, Sovrapposto o Linea attraverso
- **Stile della decorazione** — Solido, Puntinato, Puntini, Doppio o Ondulato (si applica quando è attiva una decorazione)
- **Colore della decorazione** — Selettore di colori per la linea di decorazione, predefinito al colore del testo
- **Ombra del testo** — Effetto ombra opzionale con controlli di offset, sfocatura e colore

## Scheda Trasformazione

Modifica la capitalizzazione del testo senza modificare il contenuto:

| Opzione | Risultato |
|--------|----------|
| **Nessuna** | Il testo appare come scritto |
| **Maiuscolo** | TUTTE LE LETTERE SONO MAIUSCOLE |
| **Minuscolo** | tutte le lettere sono minuscole |
| **Iniziale maiuscola** | La prima lettera di ogni parola è maiuscola |

Ulteriori controlli in questa scheda includono **Allineamento del testo** (sinistra, centro, destra, giustificato), **Allineamento verticale** e **Direzione del testo** (LTR o RTL).

## Famiglie di font disponibili

L'editor include una libreria curata di font del sistema e Google Fonts, raggruppati per categoria:

| Categoria | Font
|----------|-------
| **Sistema** | Predefinito del sistema, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS
| **Sans-Serif (Modern)** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans
| **Sans-Serif (Classico)** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend
| **Serif** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya
| **Serif (Sistema)** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria
| **Monospace** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono
| **Display** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black

I font di Google sono caricati automaticamente quando vengono selezionati. I font del sistema utilizzano le corrette catene di fallback CSS per un rendering affidabile su diversi piattaforme.

## Dove appare

L'Editor di Tipografia è disponibile ovunque sia necessario lo stile del testo:

- **Page Builder** — Seleziona qualsiasi elemento, apri l' scheda Stile e fai clic sulla sezione Tipografia
- **Header/Footer Builder** — Stila il testo in collegamenti di navigazione, testo del logo, elementi del menu e contenuti del piè di pagina
- **Menu Builder** — Controlla la tipografia per le etichette del menu e gli elementi del sottomenu
- **Catalog Admin** — Utilizzato nella descrizione del prodotto e negli editori di contenuti dove sono disponibili le opzioni di tipografia

L'editor è sempre accessibile tramite lo stesso interfaccia coerente, indipendentemente dal contesto.

## Consigli

- **Abbinare i font in modo intenzionale** — utilizza un font display o serif per gli headings e un sans-serif pulito per il testo principale. Combinazioni classiche come Playfair Display + Inter o Montserrat + Merriweather funzionano bene.
- **Limitare il numero di famiglie di font per pagina** — due o tre famiglie di font per pagina sono di solito sufficienti. Più di questo può rallentare i tempi di caricamento e creare un caos visivo.
- **Utilizzare unità relative per il testo risponsivo** — em e rem si scalano con la dimensione base del font, permettendo alla tua tipografia di adattarsi automaticamente a diverse dimensioni dello schermo.
- **Verificare la disponibilità del peso** — se il testo sembra lo stesso a 400 e 500, il font selezionato potrebbe non supportare quel peso. L'editor indica quali pesi fornisce ogni font.
- **Previsualizza su tutti i dispositivi** — il testo che sembra buono alle dimensioni desktop potrebbe essere troppo piccolo o troppo grande su mobile. Utilizza la previsualizzazione del dispositivo nel Page Builder per verificare.
- **Utilizza la previsualizzazione in tempo reale** — confronta sempre Current vs New nelle caselle di previsualizzazione prima di applicare per evitare modifiche inaspettate.