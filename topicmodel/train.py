import argparse
import logging
import os

import nltk
from azureml.core import Dataset, Run, Workspace
from gensim.corpora import Dictionary
from gensim.models import LdaModel, Phrases
from gensim.models.coherencemodel import CoherenceModel
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer


def get_data(dataset_id):
    run = Run.get_context()
    ws = run.experiment.workspace
    dataset = Dataset.get_by_id(ws, id=dataset_id)
    df = dataset.to_pandas_dataframe()
    # Keep only text content
    train_docs = df.iloc[:, 2].values
    # Remove empty elements (?)
    train_docs = [d for d in train_docs if d]
    return train_docs


def preprocess_docs(docs):

    # 1. Tokenize the documents.

    # Split the documents into tokens.
    tokenizer = RegexpTokenizer(r'\w+')
    for idx in range(len(docs)):
        docs[idx] = docs[idx].lower()  # Convert to lowercase.
        docs[idx] = tokenizer.tokenize(docs[idx])  # Split into words.

    # Remove numbers, but not words that contain numbers.
    docs = [[token for token in doc if not token.isnumeric()] for doc in docs]

    # Remove words that are only one character.
    docs = [[token for token in doc if len(token) > 1] for doc in docs]

    # Remove stop words
    stop_words = set(stopwords.words('english')) 
    docs = [[token for token in doc if not token in stop_words] for doc in docs]

    # 2. Lemmatize the documents.

    lemmatizer = WordNetLemmatizer()
    docs = [[lemmatizer.lemmatize(token) for token in doc] for doc in docs]

    # 3. Compute bigrams.

    # Add bigrams and trigrams to docs (only ones that appear 20 times or more).
    bigram = Phrases(docs, min_count=20)
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)

    # 4. Remove rare and common tokens.

    # Create a dictionary representation of the documents.
    dictionary = Dictionary(docs)

    # Filter out words that occur less than 20 documents, or more than 50% of the documents.
    dictionary.filter_extremes(no_below=20, no_above=0.5)

    # Remove some "bad words"
    dictionary.filter_tokens(bad_ids=[dictionary.token2id['ax']])

    # Remove most frequent
    dictionary.filter_n_most_frequent(5)
    
    # Bag-of-words representation of the documents.
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    return corpus, docs, dictionary


def train_model(corpus, docs, dictionary, args):
    # Train LDA model.

    model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        chunksize=args.chunksize,
        alpha='auto',
        eta='auto',
        iterations=args.iterations,
        num_topics=args.num_topics,
        passes=args.passes,
        eval_every=10
    )

    return model


def main():

    # Set up logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

    # Download NLTK components
    nltk.download('stopwords')
    nltk.download('wordnet')

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-data', type=str, required=True)
    parser.add_argument('--num-topics', type=int, required=True)
    parser.add_argument('--chunksize', type=int, required=True)
    parser.add_argument('--passes', type=int, required=True)
    parser.add_argument('--iterations', type=int, required=True)
    args = parser.parse_args()

    # Prepare data

    train_docs = get_data(args.input_data)

    corpus, docs, dictionary = preprocess_docs(train_docs)

    print('Number of unique tokens: %d' % len(dictionary))
    print('Number of documents: %d' % len(corpus))

    # Train model
    model = train_model(corpus, docs, dictionary, args)

    # Compute and log Coherence Score
    coherence_model_lda = CoherenceModel(model=model, texts=docs, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('Coherence Score: ', coherence_lda)

    run = Run.get_context()
    run.log(name='c_v', value=coherence_lda)

    # Save model & dictionary
    os.makedirs('outputs', exist_ok=True)
    model.save('./outputs/model.pickle')
    dictionary.save('./outputs/dictionary.pickle')


if __name__ == "__main__":
    main()
