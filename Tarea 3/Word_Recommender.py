from nltk.corpus import words
from nltk.metrics import edit_distance

class Word_Recommender:
    """
    Se carga la lista de palabras correctas al inicializar el objeto
    """
    def __init__(self):
        self.correct_words = words.words()
    
    """
    Función que devuele los n-gramas de caracteres de una palabra
    """
    def get_char_ngrams(self, word, n):
        word_len = len(word)
        return [word[i:i+n] for i in range(word_len - n + 1)]
    
    """
    Función que devuelve las opciones de palabras correctas que comienzan
    con la letra de la palabra mal escrita
    """
    def get_word_options(self, char):
        return list(filter(lambda word: char == word[0], self.correct_words))
    
    """
    Función para obtener el coeficiente Jaccard
    """
    def jaccard_index(self, list1, list2):
        list1 = set(list1)
        list2 = set(list2)
        intersection = list1.intersection(list2)
        union = list1.union(list2)
        return len(intersection)/len(union)
    
    """
    Función que devuelve una recomendación con base en el coeficiente Jaccard
    """
    def get_jaccard_option(self, word, options, ngram):
        char_ngrams = self.get_char_ngrams(word, ngram)
        best_score = 0
        best_option = None
        for option in options:    
            ngrams_option = self.get_char_ngrams(option,ngram)
            score = self.jaccard_index(char_ngrams,ngrams_option)
            if score > best_score:
                best_score = score
                best_option = option
        return best_option

    """
    Función que devuelve una recomendación con base en la distancia de 
    edición de Levenshtein
    """
    def get_editDistance_option(self, word, options):
        best_score = 1000000
        best_option = None
        for option in options:
            score = edit_distance(word, option,transpositions=True)
            if score < best_score:
                best_score = score
                best_option = option
        return best_option
    
    """
    Función que devuelve la recomendación para la palabra o
    lista de palabras con base en la métrica de distancia ingresada y 
    los n-gramas a considerar
    """
    def get_recommendation(self, word, metric, ngram=1):
        metric = metric.lower()
        if isinstance(word, list) == False:
            options = self.get_word_options(word[0])
            best_option = None
            if metric == 'jaccard':
                best_option = self.get_jaccard_option(word,options,ngram)
            elif metric == 'levenshtein':
                best_option = self.get_editDistance_option(word, options)
        else:
            best_options =[] 
            if metric == 'jaccard':
                for w in word:
                    options = self.get_word_options(w[0])
                    best_options.append(self.get_jaccard_option(w,options,ngram))
            elif metric == 'levenshtein':
                for w in word:
                    options = self.get_word_options(w[0])
                    best_options.append(self.get_editDistance_option(w,options))
            return best_options

        return best_option
                    



recommender = Word_Recommender()
word = ['cormulent', 'incendenece', 'validrate']
option = recommender.get_recommendation(word,'jaccard',3)
print(option)

