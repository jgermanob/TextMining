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
    tokenizer = RegexpTokenizer(r'\w+')
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