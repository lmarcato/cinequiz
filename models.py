import pandas as pd
import numpy as np
import constant

class Player:
    """
    Classe utilizzata per rappresentare il giocatore
    
    Attributi
    ---------
    name : str
        la stringa che rappresenta il nome del giocatore
    _games : dict
        la collezzione delle partite giocate, tiene traccia delle risposte esatte e 
        del punteggio di ogni partita
        
    Metodi
    ------
    add_game(game, result, score)
        Aggiunge al dizionario '_games' una partita giocata
    get_games()
        Restituisce le informazioni riguardo le partite giocate
    total_score()
        Restituisce la somma dei punteggi di tutte le partite giocate
    """
    
    def __init__(self, name: str):
        """
        Parametri
        ---------
        name : str
            Il nome del giocatore
        """
        self.name = name
        self._games = {}
        
    def add_game(self, game: int, result: tuple, score: int) -> None:
        """Aggiunge a '_games' le ifnormazioni riguardo la partita giocata
        
        Parametri
        ---------
        game : int
            Il numero di partite giocate
        result : tuple
            Il numero di risposte corrette e di quelle totali 
        score:
            Il punteggio della partita giocata
        """
        self._games[game] = result, score
    
    def get_games(self) -> list:
        """Restituisce le informazioni riguardo le partite giocate
        """
        games = []
        for game, ((correct_ans, total_ans), score) in self._games.items():
            games.append(
                "Game {} correct answers: [{}/{}], final score: {}"
                .format(game, correct_ans, total_ans, score)
            )
        return games
    
    def total_score(self) -> int:
        """Restituisce la somma dei punteggi di tutte le partite giocate
        """
        total_score = 0
        for _, score in self._games.values():
            total_score += score
        return total_score
    
class Quiz:
    """
    Classe utilizzata per rappresentare un Quiz
    
    Attributi
    ---------
    question : str
        la domanda del quiz
    answers : dict
        le possibili risposte del quiz
    score : int
        il punteggio assegnato al quiz in base alla difficoltà
    
    Metodi
    ------
    check_answer(answer)
        Verifica che la risposta selezionata sia quella corretta
    get_solution()
        Restituisce la risposta corretta
    """
    
    def __init__(self, question: str, answers: dict, score: int):
        """
        Parametri
        ---------
        question : str
            La domanda del quiz
        answers : dict
            Le possibili risposte del quiz
        score: int
            Il punteggio assegnato al quiz in base alla difficoltà
        """
        self.question = question
        self.answers = answers
        self.score = score
        
    def check_answer(self, answer: str) -> bool:
        """Verifica che la risposta selezionata sia quella corretta
        
        Parametri
        ---------
        answer : str
            La chiave della risposta da verificare
        """
        _, is_correct = self.answers[answer]
        return is_correct
    
    def get_solution(self) -> tuple:
        """Restituisce la risposta corretta
        """
        for key, (answer, is_correct) in self.answers.items():
            if is_correct:
                return key, answer

class ImdbTsvReader:
    """
    Classe utilizzata per leggere il contenuto dei file .tsv del database Imdb
    e caricarli nei DataFrame Pandas
    
    Attributi
    ---------
    name_basics : DataFrame
        contiene le informazioni riguardo il cast dei 'movie' 
        (id, nome, data_nascita, professione, ..)
    title_akas : DataFrame
        contiene la conversione del titolo originale di un 'movie' in lingua inglese 
        (id_movie, titolo_inglese)
    title_basics : DataFrame
        contiene le informazioni generali dei 'movie' presenti nel database
        (id, tipologia, titolo, data_uscita, durata, genere, ..)
    title_episode : DataFrame
        contiene il numero di episodi del 'movie' di tipologia serie tv
        (id_movie, numero_episodi)
    title__principals : DataFrame
    
    Metodi
    ------
    get_movie_by_id(id)
        Ricerca uno specifico movie in base al suo id e restituisce le informazioni associate
    get_number_episodes()
        Restituisce le informazioni e in particolare il numero di episodi di un movie (serie tv) casuale
    get_number_episodes_by_difficulty(difficulty, different_from, size, genre, year)
        Restituisce le informazioni e il numero di episodi di un insieme 'size' di movie (serie tv)
        in base alla difficoltà selezionata
    get_duration()
        Restituisce le informazioni e in particolare la durata di un movie (film) casuale
    get_duration_by_difficulty(difficulty, different_from, size, genre, year)
        Restituisce le informazioni e in particolare la durata di un un insieme 'size'
        di movie (film) in base alla difficoltà selezionata
    get_crew(title_type)
        Restituisce le informazioni riguardo un membro del cast di un movie casuale
    get_crew_by_difficulty(difficulty, title_type, different_from, size, category, birth_year, death_year)
        Restituisce le informazioni riguardo un insieme 'size' dei cast di movie 
        in base alla difficoltà selezionata
    get_english_title(id)
        Restituisce il titolo di un movie tradotto in inglese
    """
    
    def __init__(self):
        """"""
        self.name_basics = pd.read_csv(constant.NAME_BASICS, sep='\t')
        self.title_akas = pd.read_csv(constant.TITLE_AKAS, sep='\t')
        self.title_basics = pd.read_csv(constant.TITLE_BASICS, sep='\t')
        self.title_episode = pd.read_csv(constant.TITLE_EPISODE, sep='\t')
        self.title_principals = pd.read_csv(constant.TITLE_PRINCIPALS, sep='\t')
    
    def get_movie_by_id(self, id:str) -> pd.DataFrame:
        """Ricerca uno specifico movie in base al suo id e restituisce le informazioni associate
           
        Parametri
        ---------
        id : str
            L'identificativo del movie
        """
        return self.title_basics[self.title_basics['tconst'] == id]
    
    def get_number_episodes(self) -> pd.DataFrame:
        """Restituisce le informazioni e in particolare il numero di episodi di un movie (serie tv) casuale
        """
        join_table = pd.merge(self.title_basics, self.title_episode, left_on='tconst', right_on='parentTconst')
        
        filter_table =  join_table[(join_table['titleType'] == 'tvSeries') &
                           (join_table['genres'] != '\\N') &
                           (join_table['startYear'] != '\\N')]
        
        return filter_table.sample(frac=1).head(1)
    
    def get_number_episodes_by_difficulty(self, difficulty:str, different_from:str, size:int=3, genre:str=None, year:str=None) -> pd.DataFrame:
        """Restituisce le informazioni e il numero di episodi di un insieme 'size' di movie (serie tv)
        in base alla difficoltà selezionata
        
        Parametri
        ---------
        difficulty : str
            Indica il livello di difficoltà delle risposte del quiz ('EASY', 'MEDIUM', 'HARD')
        different_from : str
            Il valore corretto del quiz da non ripetere nelle risposte sbagliate
        genre : str
            Il genere del movie su cui filtrare la ricerca (default: None)
        year : str
            L'anno di uscita del movie su cui filtrare la ricerca (default: None)
        size : int
            Il numero massimo di risposte sbagliate del quiz (default: 3)
        """
        if difficulty == 'EASY':
            filter_table = self.title_episode[self.title_episode['episodeNumber'] != different_from]
        else:
            join_table = pd.merge(self.title_basics, self.title_episode, left_on='tconst', right_on='parentTconst')
            filter_table =  join_table[(join_table['titleType'] == 'tvSeries') &
                           (join_table['genres'].str.contains(genre)) &
                           (join_table['episodeNumber'] != different_from)]
            if difficulty == 'HARD':
                filter_table = filter_table[filter_table['startYear'] == year]
        
        return filter_table.sample(frac=1).head(size)
    
    def get_duration(self) -> pd.DataFrame:
        """Restituisce le informazioni e in particolare la durata di un movie (film) casuale
        """
        filter_table = self.title_basics[(self.title_basics['titleType'] == 'movie') &
                                         (self.title_basics['runtimeMinutes'] != '\\N') &
                                         (self.title_basics['genres'] != '\\N') &
                                         (self.title_basics['startYear'] != '\\N')]
        
        return filter_table.sample(frac=1).head(1)
    
    def get_duration_by_difficulty(self, difficulty: str, different_from:str, size:int=3, genre:str=None, year:str=None) -> pd.DataFrame:
        """Restituisce le informazioni e in particolare la durata di un un insieme 'size'
        di movie (film) in base alla difficoltà selezionata
        
        Parametri
        ---------
        difficulty : str
            Indica il livello di difficoltà delle risposte del quiz ('EASY', 'MEDIUM', 'HARD')
        different_from : str
            Il valore corretto del quiz da non ripetere nelle risposte sbagliate
        genre : str
            Il genere del movie su cui filtrare la ricerca (default: None)
        year : str
            L'anno di uscita del movie su cui filtrare la ricerca (default: None)
        size : int
            Il numero massimo di risposte sbagliate del quiz (default: 3)
        """
        filter_table = self.title_basics[(self.title_basics['titleType'] == 'movie') &
                                         (self.title_basics['runtimeMinutes'] != '\\N') &
                                         (self.title_basics['runtimeMinutes'] != different_from)]            
        if difficulty != 'EASY':
            filter_table =  filter_table[filter_table['genres'].str.contains(genre)]
            if difficulty == 'HARD':
                filter_table =  filter_table[filter_table['startYear'] == year]
        
        return filter_table.sample(frac=1).head(size)
    
    def get_crew(self, title_type:str) -> pd.DataFrame:
        """Restituisce le informazioni riguardo un membro del cast di un movie casuale
        
        Parametri
        ---------
        title_type : str
            Indica se il movie è un film o una serie tv
        """
        join_table = pd.merge(self.title_principals, self.name_basics, left_on='nconst', right_on='nconst')
        
        filter_table = join_table[(join_table['primaryName'] != '\\N') &
                                  (join_table['birthYear'] != '\\N') &
                                  (join_table['deathYear'] != '\\N') &
                                  (join_table['category'] != '\\N')]
        
        filter_table = filter_table[filter_table['tconst'].isin(
            self.title_basics[self.title_basics['titleType'] == title_type]['tconst'].tolist())]
        
        return filter_table.sample(frac=1).head(1)
    
    def get_crew_by_difficulty(self, difficulty: str, title_type:str, different_from:list, size:int=3, category:str=None, birth_year:str=None, death_year:str=None) -> pd.DataFrame:
        """Restituisce le informazioni riguardo un insieme 'size' dei cast di movie 
        in base alla difficoltà selezionata
        
        Parametri
        ---------
        difficulty : str
            Indica il livello di difficoltà delle risposte del quiz ('EASY', 'MEDIUM', 'HARD')
        title_type : str
            Indica se il movie è un film o una serie tv
        different_from : list
            I valori corretti del quiz da non ripetere nelle risposte sbagliate
        category : str
            Il ruolo del cast su cui filtrare la ricerca
        birth_year: str
            La data iniziale del range degli anni su cui filtrare la ricerca
        death_year : str
            La data fianale del range degli anni su cui filtrare la ricerca
        size : int
            Il numero massimo di risposte sbagliate del quiz (default: 3)
        """
        join_table = pd.merge(self.title_principals, self.name_basics, left_on='nconst', right_on='nconst')
        
        filter_table = join_table[(join_table['primaryName'] != '\\N') &
                                  (join_table['primaryName'] != different_from[0])]
        
        filter_table = filter_table[filter_table['tconst'].isin(
            self.title_basics[(self.title_basics['titleType'] == title_type) &
                              (self.title_basics['tconst'] != different_from[1])]['tconst'].tolist())]
        
        if difficulty != 'EASY':
            filter_table = filter_table[filter_table['category'] == category]
            if difficulty == 'HARD':
                filter_table = filter_table[(filter_table['birthYear'] >= birth_year) &
                                            (filter_table['birthYear'] < death_year)]
        
        return filter_table.sample(frac=1).head(size)
    
    def get_english_title(self, id:str) -> pd.DataFrame:
        """Restituisce il titolo di un movie tradotto in inglese
        
        Parametri
        ---------
        id : str
            L'identificativo del movie
        """
        filter_table = self.title_akas[(self.title_akas['titleId'] == id) &
                                       (self.title_akas['region'] == 'US')]
        
        return filter_table.head(1)
        
class QuizGenerator:
    """
    Classe utilizzata per la creazione di un Quiz
    
    Attributi
    ---------
    _imdb : ImdbTsvReader()
        permette di ottenere le informazioni dal dataset imdb
        
    Metodi
    ------
    generate(difficulty)
        Sceglie la tipologia di quiz (numero di episodi, durata, cast)
    _combine_answers(correct, wrong)
        Unisce le riposte del quiz in un unico dizionario
    _set_score(difficulty)
        Restituisce lo score associato al quiz in base alla difficoltà selezionata
    _number_episode(difficulty, _)
        Restituisce un quiz la cui domanda riguarda il numero di episodi di un movie (serie tv)
    _duration(difficulty, _)
        Restituisce un quiz la cui domanda riguarda la durata di un movie (film)
    _crew(difficulty, title_type)
        Restituisce un quiz la cui domanda riguarda il cast di un movie (serie tv o film)
    """
    
    def __init__(self):
        """"""
        self._imdb = ImdbTsvReader()

    def generate(self, difficulty: str) -> Quiz:
        """Sceglie la tipologia di quiz (numero di episodi, durata, cast)
        
        Parametri
        ---------
        difficulty : str
            Indica il livello di difficoltà con cui generare il quiz
        """
        quiz = constant.QUIZ['quiz']
        title_type = np.random.choice(constant.QUIZ_TITLE_TYPE)
        movie = quiz[title_type]
        quiz_question = movie[np.random.choice(range(len(movie)))]
        callable = [v for v in quiz_question.values()][0]
        call = getattr(self, callable)
        return call(difficulty, title_type)
        
    def _combine_answers(self, correct: str, wrong: list) -> dict:
        """Unisce le riposte del quiz in un unico dizionario
        
        Parametri
        ---------
        correct : str
            Rappresenta la risposta corretta del quiz
        wrong : list
            Rappresenta le possibili domande sbagliate del quiz
        """
        keys = [str(key + 1) for key in range(len(wrong) + 1)]
        np.random.shuffle(keys)
        answers = {keys.pop(): (correct, True)}
        for i in range(len(wrong)):
            answers[keys.pop()] = (wrong[i], False)
        return answers
        
    def _set_score(self, difficulty:str) -> int:
        """Restituisce lo score associato al quiz in base alla difficoltà selezionata
        
        Parametri
        ---------
        difficulty : str
            Indica il livello di difficoltà per poter restituire lo score associato
        """
        if difficulty == 'EASY':
            return 100
        elif difficulty == 'MEDIUM':
            return 200
        elif difficulty == 'HARD':
            return 300
    
    def _number_episodes(self, difficulty: str, _=None) -> Quiz:
        """Restituisce un quiz la cui domanda riguarda il numero di episodi di un movie (serie tv)
        
        Parametri
        ---------
        difficulty : str
            Indica il livello di difficoltà con cui generare le risposte del quiz
        """
        movie = self._imdb.get_number_episodes()
        
        correct_answer = movie.iloc[0]['episodeNumber']
        genre = (movie.iloc[0]['genres']).split(',')[0]
        year = movie.iloc[0]['startYear']
        wrong_answers = self._imdb.get_number_episodes_by_difficulty(difficulty=difficulty,
                                                                     genre=genre, 
                                                                     year=year, 
                                                                     different_from=correct_answer)

        
        title_eng = self._imdb.get_english_title(id=movie.iloc[0]['tconst'])
        title = title_eng.iloc[0]['title'] if not title_eng.empty else movie.iloc[0]['primaryTitle']
        wrong_answers = [str(answer) for answer in wrong_answers.iloc[:3]['episodeNumber']]
        return Quiz(
            question=f"Da quanti episodi è composta la serie tv '{title}'?", 
            answers=self._combine_answers(str(correct_answer), wrong_answers), 
            score=self._set_score(difficulty))
    
    def _duration(self, difficulty: str, _: str=None) -> Quiz:
        """Restituisce un quiz la cui domanda riguarda la durata di un movie (film)
        
        Parametri
        ---------
        difficulty : str
            Indica il livello di difficoltà con cui generare le risposte del quiz
        """
        movie = self._imdb.get_duration()
        
        correct_answer = movie.iloc[0]['runtimeMinutes']
        genre = (movie.iloc[0]['genres']).split(',')[0]
        year = movie.iloc[0]['startYear']
        wrong_answers = self._imdb.get_duration_by_difficulty(difficulty=difficulty,
                                                              different_from=correct_answer,
                                                              genre=genre, 
                                                              year=year)

        title_eng = self._imdb.get_english_title(id=movie.iloc[0]['tconst'])
        title = title_eng.iloc[0]['title'] if not title_eng.empty else movie.iloc[0]['primaryTitle']
        correct_answer = f"{int(correct_answer) // 60}:{int(correct_answer) % 60}"
        wrong_answers = [f"{int(answer) // 60}:{int(answer) % 60}" for answer in wrong_answers.iloc[:3]['runtimeMinutes']]
        return Quiz(
            question=f"Qual è la durata del film '{title}'?", 
            answers=self._combine_answers(correct_answer, wrong_answers), 
            score=self._set_score(difficulty))
        
    def _crew(self, difficulty: str, title_type: str) -> Quiz:
        """Restituisce un quiz la cui domanda riguarda il cast di un movie (serie tv o film)
        
        Parametri
        ---------
        difficulty : str
            Indica il livello di difficoltà con cui generare le risposte del quiz
        title_type : str
            Indica il tipo di movie (serie tv o film) su cui fare a domanda
        """
        movie = self._imdb.get_crew(title_type=title_type)
        
        correct_answer = movie.iloc[0]['primaryName']
        category = movie.iloc[0]['category']
        tconst = movie.iloc[0]['tconst']
        birth_year = movie.iloc[0]['birthYear']
        death_year = movie.iloc[0]['deathYear']
        wrong_answers = self._imdb.get_crew_by_difficulty(difficulty=difficulty,
                                                          title_type=title_type,
                                                          different_from=[correct_answer, tconst],
                                                          category=category,
                                                          birth_year = birth_year,
                                                          death_year = death_year)
            
        title_eng = self._imdb.get_english_title(id=tconst)
        title = title_eng.iloc[0]['title'] if not title_eng.empty else self._imdb.get_movie_by_id(id=tconst).iloc[0]['primaryTitle']
        wrong_answers = [str(answer) for answer in wrong_answers.iloc[:3]['primaryName']]
        return Quiz(
            question=f"Quale {category} ha fatto parte del cast di '{title}'?", 
            answers=self._combine_answers(str(correct_answer), wrong_answers), 
            score=self._set_score(difficulty))

class Game:
    """
    Classe regola il funzionamento del gioco
    
    Attributi
    ---------
    quiz_generator : QuizGenerator
        permette di generare i quiz
    player : Player
        rappresenta il giocatore
    quiz_number: int
        il numero di quiz per partita
    game_score : int
        il punteggio totale della partita
    current_game : int
        indica il numero di partite giocate
        
    Metodi
    ------
    _iteration()
        Rappresenta gli step di un'azione completa di gioco
    run()
        Permette di effettuare il corretto numero di iterazioni di gioco e di giocare più partite
    """
    def __init__(self, player: Player, quiz_number:int):
        """
        Pamaretri
        ---------
            player : Player
            quiz_number : int
        """
        self.quiz_generator = QuizGenerator()
        self.player = player
        self.quiz_number = quiz_number
        self.correct_answer = 0
        self.game_score = 0
        self.current_game = 0
        
    def _iteration(self) -> None:
        """Rappresenta gli step di un'azione completa di gioco.
        Questa prevede:
        1. selezione della difficoltà
        2. lettura e risposta al quiz
        3. valutazione della risposta e assegnazione del punteggio
        """
        difficulty = ''
        while difficulty not in ['EASY', 'MEDIUM', 'HARD']:
            difficulty = input('Inserisci il livello di difficoltà [EASY, MEDIUM, HARD]:')

        quiz = self.quiz_generator.generate(difficulty)
        
        print(quiz.question)
        quiz_answers_len = np.arange(start=1, stop=len(quiz.answers) + 1)
        for i in quiz_answers_len:
            print(f"{i}:",quiz.answers[str(i)][0])

        user_answer = 0
        while user_answer not in quiz_answers_len: 
            try:
                user_answer = int(input(f'Qual è la riposta giusta? Inserisci {str(quiz_answers_len).replace(" ",", ")}'))
            except ValueError:
                user_answer = 0
                print("Seleziona un opzione valida!")
        
        key, solution = quiz.get_solution()
        if(quiz.check_answer(str(user_answer))):
            self.game_score += quiz.score
            self.correct_answer += 1
            print(f'Risposta corretta! Esattamente {solution}')
        else:
            print(f'Peccato la riposta giusta era la {key}: {solution}')
        
        
    def run(self) -> None:
        """Permette di effettuare il corretto numero di iterazioni di gioco e di giocare più partite
        """
        print(f'Ciao {self.player.name}.')
        print('Iniziamo!')
        play_again = 'SI'
        while play_again == 'SI':
            for i in range(self.quiz_number):
                print(f"""
                -------------------------
                    Quiz numero {i + 1}
                -------------------------
                    """)
                self._iteration()

            self.current_game += 1
            self.player.add_game(game=self.current_game,
                                result=(self.correct_answer, self.quiz_number),
                                score=self.game_score)
            
            play_again = ''
            while play_again not in ['SI', 'NO']:
                play_again = input('Vuoi giocare un\'altra partita? [Si, No]').upper()
        
        print(f'Risultati: {self.player.get_games()}')        
        print(f'Il tuo punteggio totale è di {self.player.total_score()}!')