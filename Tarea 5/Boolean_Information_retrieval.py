from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import chardet
import pandas as pd


"""
Clase que implementa un sistema de recuperación booleana
"""
class Boolean_Information_Retrieval:
    def __init__(self, corpus):
        self.vectorizer = CountVectorizer(stop_words=list(stopwords.words('spanish')))
        boolean_matrix = self.vectorizer.fit_transform(corpus)
        self.df_boolean = pd.DataFrame(boolean_matrix.todense(), columns=self.vectorizer.get_feature_names())
        self.boolean_operators = ['and', 'or', 'not']
        self.group_symbols = ['(',')']
    
    """
    Clase que permite ajustar el query solicitado, por ejemplo
    si el query es (zoofilia and bestialismo), el query ajustado será
    (zoofilia==1 and bestialismo==1) para buscar en el dataframe que 
    contiene la matriz de incidencias
    """
    def adjust_query(self, query):
        words = query.split(' ')
        for word in words:
            if word not in self.boolean_operators and word not in self.group_symbols:
                print(word)
                query = query.replace(word, '{}==1'.format(word))
        return query
    
    """
    Obtiene los documentos que cumplen con el query solicitado
    y devuelve una lista con los indices de los documentos
    que cumplen dicho criterio
    """
    def boolean_query(self, query):
        query = self.adjust_query(query)
        df_filtered = self.df_boolean.query(query)
        index = df_filtered.index + 1
        return index.tolist()

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
tokenizer = RegexpTokenizer(r'\w+')
def get_corpus(path, corpus_length, tokenizer):
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


corpus = get_corpus('./corpus/',15,tokenizer)
info_ret = Boolean_Information_Retrieval(corpus)
relevant_docs = info_ret.boolean_query('zoofilia and bestialismo')






