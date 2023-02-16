import nltk
import io
import numpy as np
import random
import string
import warnings
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')

f = open('respostas.txt', 'r', errors = 'ignore', encoding="utf-8") 
raw = f.read()
raw = raw.lower() 
nltk.download('punkt') 
nltk.download('wordnet')
nltk.download('popular', quiet=True)
sent_tokens = nltk.sent_tokenize(raw) 
word_tokens = nltk.word_tokenize(raw) 

sent_tokens[:2] # mostra as duas primeiras frases
word_tokens[:2] # mostra as duas primeiras palavras

lemmer = nltk.stem.WordNetLemmatizer() # seleciona o lemmatizer
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens] # lemmatiza as palavras
remove_pontuacao = dict((ord(punct), None) for punct in string.punctuation) # remove pontuação
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_pontuacao))) # lemmatiza e remove pontuação

Saudacao_input = ("e aí", "oi", "saudações", "eai", "como vai", "olá", "tchau") # entradas de saudação
Respostas_input = ["Oi", "Olá", "Oi, como vai?", "Oi, tudo bem?", "Oi, como você está?", "Até a próxima"] # respostas de saudação

def saudacao(sentence): # função de saudação
    for palavra in sentence.split(): # para cada palavra na frase
        if palavra.lower() in Saudacao_input: # se a palavra for uma saudação
            return random.choice(Respostas_input) # retorna uma resposta aleatória
        
        
def respostas(user_respostas): # função de resposta
    chatbot_respostas = '' # resposta do chatbot
    sent_tokens.append(user_respostas) # adiciona a resposta do usuário na lista de frases
    Vetorizar_palavras = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english') # vetoriza as palavras
    Vetor_palavars = Vetorizar_palavras.fit_transform(sent_tokens) # transforma as palavras em vetores
    similar = cosine_similarity(Vetor_palavars[-1], Vetor_palavars) # calcula a similaridade entre as frases
    indice_matriz = similar.argsort()[0][-2] # pega o índice da frase mais similar
    flat = similar.flatten() # transforma em uma lista
    flat.sort() # ordena a lista
    aprox_similar = flat[-2] # pega o valor da frase mais similar
    if(aprox_similar == 0):
        chatbot_respostas = chatbot_respostas + "Desculpe, não entendi!" # se não entendeu, retorna essa frase
        return chatbot_respostas
    else:
        chatbot_respostas = chatbot_respostas + sent_tokens[indice_matriz] # se entendeu, retorna a frase mais similar
        return chatbot_respostas
 