from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import pandas as pd
from Tools import get_corpus, precision, recall, f1_score
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
    Función para obtener el vector de una consulta con base en el modelo tf-idf 
    que se obtuvo de la colección de documentos
    """
    def get_query_vector(self, query):
        vector = self.vectorizer.transform([query])
        return vector.todense()
    
    """
    Función para obtener los documentos relevantes dada la consulta
    ingresada con base en la disstancia coseno y un umbral definido 
    por el usuario
    """
    def tfidf_query(self, query, threshold=0.2):
        query_vector = self.get_query_vector(query)
        tokens = query.split(' ')
        retrieved_documents = []
        for token in tokens:
            posting = self.invertIndex_dict.get(token)
            for element in posting:
                document_index = element[0] - 1
                if (document_index + 1) not in retrieved_documents:
                    document_vector = self.df_tfidf.iloc[document_index].values.reshape(1,230)
                    similarity = cosine_similarity(query_vector,document_vector)[0][0]
                    if similarity > threshold:
                        retrieved_documents.append(document_index + 1)
        return retrieved_documents

relevant_docs = [1, 2, 3, 4, 7, 12, 13, 15]

corpus = get_corpus('./corpus/',15)
info_ret = TFIDF_Information_Retrieval(corpus)
query = 'sexo animales orgasmo sexualidad humana planificación familiar'
retrieved_docs = info_ret.tfidf_query(query)

print(retrieved_docs)

prec = precision(relevant_docs, retrieved_docs)
rec = recall(relevant_docs, retrieved_docs)
f1 = f1_score(relevant_docs,retrieved_docs)

print("Precision= {}".format(prec))
print('Recall = {}'.format(rec))
print('F1-score = {}'.format(f1))
