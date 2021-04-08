from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import pandas as pd
from Tools import get_corpus
from sklearn.metrics.pairwise import cosine_similarity

class TFIDF_Information_Retrieval:
    def __init__(self, corpus):
        self.vectorizer = TfidfVectorizer(stop_words=list(stopwords.words('spanish')))
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        self.df_tfidf = pd.DataFrame(tfidf_matrix.todense(), columns=self.vectorizer.get_feature_names())
        self.invertIndex_dict = self.get_invert_index()
    
    """
    Función para oderdenar de forma decreciente los 
    elementos del posting con base en los valores TF-IDF
    """
    def sort_tfidf(self, posting):
        posting.sort(key = lambda x: x[1], reverse=True)
        return posting
    
    """
    Función para obtener diccionario de indice invertido.
    El diccionario de indice invertido tiene la forma:
    'palabra':[(indice de documento, valor tf-idf)]
    """
    def get_invert_index(self):
        invert_index_dict = dict()
        for word in self.vectorizer.get_feature_names():
            query = '{} > 0.0'.format(str(word))
            df_filtered = self.df_tfidf.query(query)
            tf_idf_values = df_filtered[word].values
            index = df_filtered.index + 1
            index = index.tolist()
            invert_index_dict[word] = self.sort_tfidf(list(zip(index,tf_idf_values)))
        return invert_index_dict
    
    """
    Función para obtener el vector de una consulta
    con base en el modelo tf-idf que se obtuvo de la
    colección de documentos, devuelve una lista de tuplas
    de la forma (palabra, valor tf-idf)
    """
    def get_query_vector(self, query):
        tokens = query.split(' ')
        query_matrix = self.vectorizer.transform([query])
        df_query = pd.DataFrame(query_matrix.todense(), columns=self.vectorizer.get_feature_names())
        values = []
        for token in tokens:
            value = df_query[token].values
            values.append(value[0])
        vectors = list(zip(tokens,values))
        return vectors
    
    def tfidf_query(self, query):
        query_vector = self.get_query_vector(query)
        for element in query_vector:
            word, tfidf_value = element
            posting = self.invertIndex_dict.get(word)
            for doc in posting:
                index, tfidf = doc
                similarity = cosine_similarity(tfidf_value,tfidf)
                print(similarity)

        


corpus = get_corpus('./corpus/',15)
info_ret = TFIDF_Information_Retrieval(corpus)
info_ret.tfidf_query('zoofilia bestialismo sexualidad')