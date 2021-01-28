import argparse
import json
import logging
import os
import re
import sys
import traceback

import nltk
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer


def preprocess_doc(doc):

    # Remove some stuff before tokenization.

    # Remove email addresses.
    d = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '', doc)

    # Tokenize the document.

    # Split the document into tokens.
    tokenizer = RegexpTokenizer(r'\w+')
    d = d.lower()  # Convert to lowercase.
    d = tokenizer.tokenize(d) # Split into words.

    # Remove numbers, but not words that contain numbers.
    d = [token for token in d if token.isalpha()]

    # Remove words that are only one character.
    d = [token for token in d if len(token) > 1]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    stop_words = stop_words.union(['one', 'ax', 'max'])
    d = [token for token in d if not token in stop_words]

    # Lemmatize the documents.
    lemmatizer = WordNetLemmatizer()
    d = [lemmatizer.lemmatize(token) for token in d]
    
    return d


def init():
    global model
    global dictionary

    # Download NLTK components
    nltk.download('stopwords')
    nltk.download('wordnet')

    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'outputs/model.pickle')
    dict_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'outputs/dictionary.pickle')

    model = LdaModel.load(model_path)
    dictionary = Dictionary.load(dict_path)


def run(data):
    print('# input data:', data)
    try:
        print('# parse json')
        data = json.loads(data)['data']

        print('# preprocess')
        data = preprocess_doc(data)

        print('# submit')
        result = model.get_document_topics(dictionary.doc2bow(data))

        # Convert NumPy float32
        result = [(t[0], t[1].item()) for t in result]

        # Also return topics for reference
        topics = model.print_topics(-1)

        return {
            'distribution': result,
            'topics': topics
        }

    except Exception as e:
        error = str(e)
        traceback.print_exc()
        return error
