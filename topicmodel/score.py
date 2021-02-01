''' Score the model.'''

import json
import os
import re
import traceback

import nltk
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

MODEL = None
DICTIONARY = None


def preprocess_doc(doc):
    '''Preprocess a document for scoring.'''

    # Remove some stuff before tokenization.

    # Remove email addresses.
    doc = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '', doc)

    # Tokenize the document.

    # Split the document into tokens.
    tokenizer = RegexpTokenizer(r'\w+')
    doc = doc.lower()  # Convert to lowercase.
    doc = tokenizer.tokenize(doc) # Split into words.

    # Remove numbers, but not words that contain numbers.
    doc = [token for token in doc if token.isalpha()]

    # Remove words that are only one character.
    doc = [token for token in doc if len(token) > 1]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    stop_words = stop_words.union(['one', 'ax', 'max'])
    doc = [token for token in doc if not token in stop_words]

    # Lemmatize the documents.
    lemmatizer = WordNetLemmatizer()
    doc = [lemmatizer.lemmatize(token) for token in doc]

    return doc


def init():
    '''Initialize the environment.'''
    global MODEL # pylint: disable=global-statement
    global DICTIONARY # pylint: disable=global-statement

    # Download NLTK components
    nltk.download('stopwords')
    nltk.download('wordnet')

    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'outputs/model.pickle')
    dict_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'outputs/dictionary.pickle')

    MODEL = LdaModel.load(model_path)
    DICTIONARY = Dictionary.load(dict_path)


def run(data):
    '''Invoke the model on input data.'''
    print('# input data:', data)
    try:
        print('# parse json')
        data = json.loads(data)['data']

        print('# preprocess')
        data = preprocess_doc(data)

        print('# submit')
        result = MODEL.get_document_topics(DICTIONARY.doc2bow(data))

        # Convert NumPy float32
        result = [(t[0], t[1].item()) for t in result]

        # Also return topics for reference
        topics = MODEL.print_topics(-1)

        return {
            'distribution': result,
            'topics': topics
        }

    except Exception as ex: # pylint: disable=broad-except
        error = str(ex)
        traceback.print_exc()
        return error
