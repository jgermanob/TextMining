from nltk.tokenize import RegexpTokenizer
import chardet

"""
Función para obtener la codificación de un archivo
de texto
"""
def get_encoding(path):
    f = open(path, 'rb').read()
    result = chardet.detect(f)
    encoding = result['encoding']
    return encoding

"""
Función para obtener una lista con los documentos del corpus
"""
def get_corpus(path, corpus_length):
    tokenizer = RegexpTokenizer(r'[a-záéíóú]+')
    corpus = []
    for index in range(1,corpus_length+1):
        file_path = path+'{}.txt'.format(index)
        encoding = get_encoding(file_path)
        text = open(file_path, 'r', encoding=encoding).read()
        text = text.lower()
        tokens = tokenizer.tokenize(text)
        clean_text = ' '.join(tokens)
        corpus.append(clean_text.strip())
    return corpus

"""
Métricas de evaluación para recuperación de información
"""
def precision(relevant_docs, retrieved_docs):
    relevant_retrieved_docs = set(retrieved_docs).intersection(set(relevant_docs))
    prec = len(relevant_retrieved_docs) / len(retrieved_docs)
    return prec

def recall(relevant_docs, retrieved_docs):
    relevant_retrieved_docs = set(retrieved_docs).intersection(set(relevant_docs))
    rec = len(relevant_retrieved_docs) / len(relevant_docs)
    return rec

def f1_score(relevant_docs, retrieved_docs):
    prec = precision(relevant_docs,retrieved_docs)
    rec = recall(relevant_docs,retrieved_docs)
    f1 = (2 * (prec * rec))/(prec + rec)
    return f1