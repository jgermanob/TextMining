from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import pandas as pd
from Tools import get_corpus, precision, recall, f1_score
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
    (zoofilia>0 and bestialismo>0) para buscar en el dataframe que 
    contiene la matriz de incidencias
    """
    def adjust_query(self, query):
        words = query.split(' ')
        for word in words:
            if word not in self.boolean_operators and word not in self.group_symbols:
                query = query.replace(word, '{}>0'.format(word))
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


relevant_docs = [1, 2, 3, 4, 7, 12, 13, 15]

corpus = get_corpus('./corpus/',15)
info_ret = Boolean_Information_Retrieval(corpus)
query = 'preservativo or ( sexualidad and humana ) or orgasmo or sexo or fecundidad or pelo'
retrieved_docs = info_ret.boolean_query(query)

prec = precision(relevant_docs, retrieved_docs)
rec = recall(relevant_docs, retrieved_docs)
f1 = f1_score(relevant_docs,retrieved_docs)

print("Precision= {}".format(prec))
print('Recall = {}'.format(rec))
print('F1-score = {}'.format(f1))

my_retrieved_docs = [1, 2, 4, 7, 12, 13, 15]
prec = precision(relevant_docs, my_retrieved_docs)
rec = recall(relevant_docs, my_retrieved_docs)
f1 = f1_score(relevant_docs,my_retrieved_docs)

print("Precision= {}".format(prec))
print('Recall = {}'.format(rec))
print('F1-score = {}'.format(f1))






