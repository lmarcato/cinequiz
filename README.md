# Cinequiz

![cinequiz logo](./data/img/cinequiz.png)

## 1. La risposta giusta

Lo scopo del progetto è creare automaticamente quiz a scelta multipla relativi a film, sfruttando i dati di IMDb. Ogni quiz deve essere composto da una domanda e quattro possibili risposte, di cui solo
una corretta. Il programma che genera quiz deve inoltre implementare un criterio per generare le
possibili risposte proporzionale alla difficoltà del quiz desiderato. Il programma deve inoltre
consentire ad un giocatore umano di rispondere al quiz e deve misurare la sua prestazione con un
punteggio che tenga conto della difficoltà di ogni singola domanda. \
I dati IMDb possono essere acquisiti tramite API specifiche (come Cinemagoer) o set di dati esistenti,
come IMDb Dataset.

### Dataset utilizzato

Il [dataset](https://developer.imdb.com/non-commercial-datasets/) utilizzato è un subset dei dati IMDb messi a disposizione per uso personale e non ad uso commerciale.
Il dataset è stato modificato e ridotto per renderlo utilizzabile, i file sono presenti al percorso 'cinequiz/data/imdb/':

- name.basics.tsv
- title.akas.tsv
- title.basics.tsv
- title.episode.tsv
- title.principals.tsv

### Classi

- Player
- Quiz
- QuizGenerator
- ImdbTsvReader
- Game

### Strutture dati utilizzate

Classe Player attributo *_games*

```python
    _games = { 0: ((7,15), 700) }
```

Dove:

- la chiave rappresenta il numero della partita giocata
- il valore contiene una tupla con il numero di riposte esatte su quelle totali e il punteggio della partita

Classe Quiz attributo *answers*

```python
    answers = { 
            0: ('answer', False),
            1: ('answer', True),
            2: ('answer', False),
            3: ('answer', False)
        }
```

Dove:

- la chiave rappresenta il numero della domanda
- il valore contiene una tupla con il testo della risposta e la soluzione

### Logica dei quiz

