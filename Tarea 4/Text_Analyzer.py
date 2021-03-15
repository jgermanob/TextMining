from nltk.tokenize import RegexpTokenizer
from nltk import FreqDist
from nltk import pos_tag
from nltk.tag import StanfordPOSTagger
import spacy


nlp = spacy.load('es_core_news_sm')
INPUT_FILE_PATH = 'elramoazul.txt'
input_file = open(INPUT_FILE_PATH, encoding='utf8').read()
JAR = '/Users/jgerman/Desktop/Models/stanford-postagger-full-2020-11-17/stanford-postagger.jar'
TAGGER= '/Users/jgerman/Desktop/Models/stanford-postagger-full-2020-11-17/models/spanish-ud.tagger'

# Tokenización
input_file = input_file.lower()
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(input_file)

# 1.Cuantas palabras hay en el texto? (descartando símbolos de puntuación). 
words_number = len(tokens)
print("Número de palabras en el texto:",words_number)

# 2.Cuantas palabras diferentes hay?.
unique_words = list(set(tokens))
unique_words_number = len(unique_words)
print("Número de palabras diferentes en el texto:", unique_words_number)

# 3.Después de lematizar las palabras, cuántas palabras diferentes hay?.
lemmas = []
for token in tokens:
    d = nlp(token)
    for token in d:
        lemmas.append(token.lemma_)

unique_lemmas = list(set(lemmas))
unique_lemmas_number = len(unique_lemmas)
print("Número de lemmas diferentes en el texto:",unique_lemmas_number)

# ¿Cuál es la diversidad léxica del texto dado? (relación de palabras únicas con respecto al número total de palabras)
def lexical_diversity(tokens):
    return len(set(tokens)) / len(tokens)

print("Diversidad léxica del texto:",lexical_diversity(tokens))

# 5.¿Cuáles son las 20 palabras (únicas) más frecuentes en el texto? ¿Cuál es su frecuencia?.
frequency = FreqDist(tokens)
print("20 palabras mas frecuentes:")
for word, freq in frequency.most_common(20):
    print('{}: {}'.format(word,freq))

# 6.¿Cuál es el número promedio de palabras por oración?
sentences = input_file.split('\n')
words_per_sentence = []
for sentence in sentences:
    tokens = tokenizer.tokenize(sentence)
    words_per_sentence.append(len(tokens))

print("Promedio de palabras por oración:",sum(words_per_sentence)/len(sentences))

# 7.¿Cuál es la frecuencia de de sustantivos, adjetivos y verbos en el texto?
pos_tagger = StanfordPOSTagger(TAGGER, JAR)
for sentence in sentences:
    tokens = tokenizer.tokenize(sentence)
    pos = pos_tagger.tag(tokens)
    print(pos)
    

