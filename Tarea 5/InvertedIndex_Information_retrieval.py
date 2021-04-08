from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import pandas as pd
from Tools import get_corpus, precision, recall, f1_score

class InvertedIndex_Information_Retrieval:
    def __init__(self, corpus):
        self.vectorizer = CountVectorizer(stop_words=list(stopwords.words('spanish')))
        boolean_matrix = self.vectorizer.fit_transform(corpus)
        self.df_boolean = pd.DataFrame(boolean_matrix.todense(), columns=self.vectorizer.get_feature_names())
        self.invertIndex_dict = self.get_invert_index()
        self.boolean_operators = ['and', 'or', 'not']
        self.group_symbols = ['(',')']
    
    """
    Función para obtener diccionario de indice invertido
    """
    def get_invert_index(self):
        invert_index_dict = dict()
        for word in self.vectorizer.get_feature_names():
            query = '{} > 0'.format(str(word))
            df_filtered = self.df_boolean.query(query)
            index = df_filtered.index + 1
            invert_index_dict[word] = index.tolist()
        return invert_index_dict
    
    """
    Operaciones boolenas entre postings
    """
    def AND(self, posting1, posting2):
        return list(set(posting1).intersection(set(posting2)))
    
    def OR(self, posting1, posting2):
        return list(set(posting1).union(set(posting2)))
    
    def NOT(self, posting1):
        all_docs = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        for doc in posting1:
            all_docs.remove(doc)
        return all_docs
    
    """
    Función para pasar una consulta de notación infija a
    notación posfija
    """
    def postfix(self, query):
        # Precendcia de operadores #
        precedence = {'not':3, 'and':2, 'or':1, '(':0, ')':0}
        output = []
        operator_stack = []
        infix_tokens = query.split(' ')
        #creación de expresion posfija
        for token in infix_tokens:
            if (token == '('):
                operator_stack.append(token)
            elif (token == ')'):
                operator = operator_stack.pop()
                while operator != '(':
                    output.append(operator)
                    operator = operator_stack.pop()
            elif (token in precedence):
                if (operator_stack):
                    current_operator = operator_stack[-1]
                while (operator_stack and precedence[current_operator] > precedence[token]):
                    output.append(operator_stack.pop())
                    if (operator_stack):
                        current_operator = operator_stack[-1]
                operator_stack.append(token)
            else:
                output.append(token.lower())
        
        while (operator_stack):
            output.append(operator_stack.pop())
        return output
    
    """
    Función para obtener lista de indices de documentos
    que cumplen con la consulta realizada
    """
    def boolean_query(self, query):
        results_stack = []
        postfix_query = self.postfix(query)
        for i in postfix_query:
            if( i!= 'and' and i!= 'or' and i!= 'not'):
                i = i.replace('(', ' ')
                i = i.replace(')', ' ')
                i = self.invertIndex_dict.get(i)
                results_stack.append(i)
            elif (i=='and'):
                a = results_stack.pop()
                b = results_stack.pop()
                results_stack.append(self.AND(a,b))
            elif (i=='or'):
                a = results_stack.pop()
                b = results_stack.pop()
                results_stack.append(self.OR(a,b))
            elif (i == 'not'):
                a = results_stack.pop()
                results_stack.append(self.NOT(a))
        return results_stack.pop()


relevant_docs = [1, 2, 3, 4, 7, 12, 13, 15]

corpus = get_corpus('./corpus/',15)
info_ret = InvertedIndex_Information_Retrieval(corpus)
query = 'preservativo or ( sexualidad and humana ) or orgasmo or sexo or fecundidad or pelo'
retrieved_docs = info_ret.boolean_query(query)

prec = precision(relevant_docs, retrieved_docs)
rec = recall(relevant_docs, retrieved_docs)
f1 = f1_score(relevant_docs,retrieved_docs)

print("Precision= {}".format(prec))
print('Recall = {}'.format(rec))
print('F1-score = {}'.format(f1))