# Tsv file paths
NAME_BASICS = './data/imdb/name.basics.tsv'
TITLE_AKAS = './data/imdb/title.akas.tsv'
TITLE_BASICS = './data/imdb/title.basics.tsv'
TITLE_EPISODE = './data/imdb/title.episode.tsv'
TITLE_PRINCIPALS = './data/imdb/title.principals.tsv'

# Quiz decision  structure

QUIZ = { 'quiz': {
    'tvSeries': [
        { 0: '_number_episodes' },
        { 1: '_crew' },
    ],
    'movie': [ 
        { 0: '_duration' },
        { 1: '_crew' },
    ],
}}
QUIZ_TITLE_TYPE = ['tvSeries', 'movie']