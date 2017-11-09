from string import punctuation

import nltk
import pandas as pd
from unidecode import unidecode

nltk.data.path.append("/var/task/nltk_data")
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

POST_NORMALIZATION_STOP_WORDS_FOR_VENDOR_NAME = {
    'hotel',
    'inn',
    'suit',
    'resort',
    'travel'
}

POST_NORMALIZATION_STOP_WORDS_FOR_CAR_VENDOR_NAME = {
    'car',
    'avi',
    'nation',
    'corp',
    'budget',
    'enterpris',
    'credit',
    'ez',
    'hertz',
    'rentacar',
    'rac',  # short for rent a car
    'payless',
    'advantag',
    'rent',
}

POST_NORMALIZATION_STOP_WORDS_FOR_CAR_EXPENSE_TYPE_NAME = {
    'rental',
    'car',
    'auto',
    'mileag',
    'toll',
    'gas',
}

STOP_WORDS_FOR_FLIGHTS_EXPENSE_TYPE_NAME = {
    'airfar',
    'airlin',
    'baggag',
    'air',
    'book'
}

STOP_WORDS_FOR_FLIGHTS_VENDOR_NAME_EXPENSE = {
    'airlin',
    'air',
    'american',
    'delta',
    'unit',
    'southwest',
    'virgin',
    'jetblu',
    'alaska',
    'southw',
    'airway',
    'british'
}

STOP_WORDS_FOR_RAIL_VENDOR_NAME_EXPENSE = {
    'amtrak'
    'eurostar'
    'greyhound'
    'train'
}

STOP_WORDS_FOR_RAIL_EXPENSE_TYPE_NAME = {
    'train',
    'transport',
    'bus',
    'subway',
    'metro',
    'rail',
}

ABREVIATIONS_DICT = {
    "'m": ' am',
    "'ve": ' have',
    "'ll": " will",
    "'d": " would",
    "'s": " is",
    "'re": " are",
    "  ": " ",
    "' s": " is",

    # debatable between and/or
    "/": " and "
}

STOPWORDS_SET = set(stopwords.words('english'))
SNOWBALL = SnowballStemmer('english')
WORDNET = WordNetLemmatizer()


def find_stop_words(corpus):
    '''
    takes in a normalized corpus and returns stop words in pandas Series
    '''
    unpacked_list = [word for document in corpus for word in document.split()]

    return pd.Series(unpacked_list).value_counts()


# I question the need for this but lets just do it for now
def _multiple_replace(text, adict=ABREVIATIONS_DICT):
    import re
    '''
    Does a multiple find/replace
    '''
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]

    return rx.sub(one_xlat, text.lower())


def _special_char_translation(doc):
    return ' '.join([unidecode(word) for word in doc.split()])


def _remove_stop_words(doc):
    return ' '.join([word for word in doc.split() if word.lower() not in STOPWORDS_SET])


def normalize(document, post_normalization_stop_words={}):
    WHITE_SPACE = ' '

    decoded_doc = _special_char_translation(document)
    abbreviations_removed_doc = _multiple_replace(decoded_doc)
    stops_removed_doc = _remove_stop_words(abbreviations_removed_doc)
    punc_removed = ''.join([char for char in stops_removed_doc if char not in set(punctuation)])

    stripped_lemmatized = map(WORDNET.lemmatize, punc_removed.split())
    stripped_lemmatized_stemmed = map(SNOWBALL.stem, stripped_lemmatized)

    return WHITE_SPACE.join([word for word in stripped_lemmatized_stemmed if word not in post_normalization_stop_words])
