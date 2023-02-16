from fastapi import FastAPI
from pydantic import BaseModel
from nlp import saudacao, respostas, sent_tokens
from typing import List, Optional

app = FastAPI()

class Pergunta(BaseModel): 
    mensagem: str

banco: List[Pergunta] = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/pergunta")
def fazer_perguntas(pergunta: Pergunta):
    respostas.user_respostas = pergunta.mensagem
    user_respostas = pergunta.mensagem
    user_respostas=user_respostas.lower() 
    if(user_respostas!='sair'): 
        if(user_respostas=='obrigado' or user_respostas=='obrigada'): 
            return {'Chatbot: Você é bem-vindo.'}
        else:
            if(saudacao(user_respostas)!=None):
                return {'Chatbot: '+saudacao(user_respostas)}
            else:
                return {'Chatbot: '+respostas(user_respostas)} 
                sent_tokens.remove(user_respostas)
    else:
        return {'Chatbot: Tchau, até mais.'}