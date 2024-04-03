import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker

# Download NLTK resources
# nltk.download('punkt')
# nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
spell = SpellChecker()

def tokenize(sentence):
    """
    Split sentence into array of words/tokens.
    A token can be a word or punctuation character, or number.
    """
    tokens = nltk.word_tokenize(sentence)
    # Filter out tokens consisting only of punctuation characters
    tokens = [token for token in tokens if token.isalnum()]
    print("Tokenized sentence:", tokens)
    return tokens

def lemmatize(word):
    """
    Lemmatize word to find its root form.
    """
    lemma = lemmatizer.lemmatize(word.lower())
    print("Lemmatized word:", lemma)
    return lemma

def remove_stopwords(tokens):
    """
    Remove stop words from the list of tokens.
    """
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    print("Tokens after removing stop words:", filtered_tokens)
    return filtered_tokens

def correct_spelling(tokens):
    """
    Correct spelling mistakes in the list of tokens.
    """
    corrected_tokens = [spell.correction(word) for word in tokens]
    print("Tokens after spelling correction:", corrected_tokens)
    return corrected_tokens

def preprocess_text(sentence):
    """
    Preprocess the input sentence:
    - Tokenize
    - Lemmatize
    - Remove stop words
    - Correct spelling
    """
    tokens = tokenize(sentence)
    tokens = [lemmatize(word) for word in tokens]
    tokens = remove_stopwords(tokens)
    tokens = correct_spelling(tokens)
    return tokens

def bag_of_words(tokenized_sentence, words):
    """
    Return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise.
    """
    # Initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in tokenized_sentence:
            bag[idx] = 1
    return bag
