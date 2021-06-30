from nltk import stem
from nltk.stem import PorterStemmer

#create an object of class PorterStemmer
porter = PorterStemmer()


def stemming(sentences):
    stemmed_sentences=[]
    for sentence in sentences:
        new_sentence = []
        for word in sentence.split():
            new_sentence.append(porter.stem(word))
        new_sentence = ' '.join(new_sentence)
        stemmed_sentences.append(new_sentence)
    return stemmed_sentences

    

            
             

