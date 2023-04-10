import os

import gspread
import pandas as pd
import requests
import telegram

from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper
from bcb import sgs
from datetime import datetime, date
from datetime import date, timedelta


TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1_FPdKuYoSq6iCCLK7f6dDCOrFpa3s5aBcfQIlXKfSyc")
sheet = planilha.worksheet("cotacao")
app = Flask(__name__)


@app.route("/")
def hello_world():
  return menu + "Olá! Eu sou um robô que compila e automatiza dados do Banco Central"

###Recebendo aviso de nova mensagem
@app.route("/novamensagem")
def novamensagem():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Um novo usuário acessou o Robô de Dados do Banco Central"}
  requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return "Mensagem enviada."

menu = """
<a href="/">Página inicial</a> | <a href="/promocoes">PROMOÇÕES</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a> | <a href="/dedoduro2">dedoduro2</a>
<br>
"""

@app.route("/")
def index():
  return menu + "Olá, mundo! Esse é meu site. (Álvaro Justen)"

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato"

@app.route("/dedoduro2")
def dedoduro2():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acesso o bot do Banco Central!"}
  resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"

###Definindo a data de hoje

def hoje():
    return date.today()

def amanha():
    return date.today() + timedelta(days=1)

def ontem():
    return date.today() - timedelta(days=1)


###Os códigos de cada moeda ou índice

selic = sgs.get({'selic':432}, start = '1994-01-01')
ipca_mensal = sgs.get({'ipca':433}, start = '1994-01-01')
dolar = sgs.get({'dolar':1}, start = '1994-01-01')
euro = sgs.get({'euro':21619}, start = '1994-01-01')
libra = sgs.get({'libra':21623}, start = '1994-01-01')
dolar_canadense = sgs.get({'dolar_canadense':21635}, start = '1994-01-01')
iene = sgs.get({'iene':21621}, start = '1994-01-01')
peso_argentino = sgs.get({'peso_argentino':14001}, start = '1994-01-01')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------

###Consultando diferentes moedas

def dolar_ptax():
    df = sgs.get(1)
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    df = df.sort_index(ascending=False).reset_index()
    df = df.rename(columns={"date": "Dólar", df.columns[1]: "Dólar"})
    pd.set_option('float_format', '{:.4}'.format)
    return df.head(10)

dolar_ptax_df = dolar_ptax()
dolar_ptax_reset = dolar_ptax_df.reset_index()

def euro_ptax():
    df = sgs.get(21619)
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    df = df.sort_index(ascending=False).reset_index()
    df = df.rename(columns={"date": "Euro", df.columns[1]: "Euro"})
    pd.set_option('float_format', '{:.4}'.format)
    return df.head(10)

euro_ptax_df = euro_ptax()
euro_ptax_reset = euro_ptax_df.reset_index()

def dolar_canadense_ptax():
    df = sgs.get(21635)
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    df = df.sort_index(ascending=False).reset_index()
    df = df.rename(columns={"date": "dólar_canadense", df.columns[1]: "dólar canadense"})
    pd.set_option('float_format', '{:.4}'.format)
    return df.head(10)

dolar_canadense_ptax_df = dolar_canadense_ptax()
dolar_canadense_ptax_reset = dolar_canadense_ptax_df.reset_index()


def libra_ptax():
    df = sgs.get(21623)
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    df = df.sort_index(ascending=False).reset_index()
    df = df.rename(columns={"date": "Libra", df.columns[1]: "Libra"})
    pd.set_option('float_format', '{:.4}'.format)
    return df.head(10)

libra_ptax_df = libra_ptax()
libra_ptax_reset = libra_ptax_df.reset_index()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------

#MEMORIZANDO AS COTAÇÕES DAS MOEDAS NA PLANILHA

###Dólar

pd.set_option('float_format', '{:.3}'.format)

dolar_hoje = dolar_ptax_reset.loc[0,'Dólar']
dolar_ontem = dolar_ptax_reset.loc[1,'Dólar']
dolar_anteontem = dolar_ptax_reset.loc[2,'Dólar']
dolar_ante_anteontem = dolar_ptax_reset.loc[3,'Dólar']

###Dólar canadense

pd.set_option('float_format', '{:.2}'.format)

dolar_canadense_hoje = dolar_canadense_ptax_reset.loc[0,'dólar canadense']
dolar_canadense_ontem = dolar_canadense_ptax_reset.loc[1,'dólar canadense']
dolar_canadense_anteontem = dolar_canadense_ptax_reset.loc[2,'dólar canadense']
dolar_canadense_ante_anteontem = dolar_canadense_ptax_reset.loc[3,'dólar canadense']

###Euro
pd.set_option('float_format', '{:.3}'.format)

euro_hoje = euro_ptax_reset.loc[0,'Euro']
euro_ontem = euro_ptax_reset.loc[1,'Euro']
euro_anteontem = euro_ptax_reset.loc[2,'Euro']
euro_ante_anteontem = euro_ptax_reset.loc[3,'Euro']

###Libra
pd.set_option('float_format', '{:.2}'.format)

libra_hoje = libra_ptax_reset.loc[0,'Libra']
libra_ontem = libra_ptax_reset.loc[1,'Libra']
libra_anteontem = libra_ptax_reset.loc[2,'Libra']
libra_ante_anteontem = libra_ptax_reset.loc[3,'Libra']


#------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Estabelecendo os percentuais

###Dólar 

def dolar_percentual():
    pd.set_option('float_format', '{:.0}'.format)
    dolar_percentual = dolar_ptax_reset['Dólar'].pct_change(periods=-1)
    dolar_percentual = dolar_percentual.reset_index()
    return dolar_percentual

dolar_percentual_df = dolar_percentual()
dolar_percentual_reset = dolar_percentual_df.reset_index()

dolar_percentual_hoje = dolar_percentual_reset.loc[0, 'Dólar']
dolar_percentual_ontem = dolar_percentual_reset.loc[1,'Dólar']

#Dólar Canadense

def dolar_canadense_percentual():
    pd.set_option('float_format', '{:.0}'.format)
    dolar_canadense_percentual = dolar_canadense_ptax_reset['dólar canadense'].pct_change(periods=-1)
    dolar_canadense_percentual = dolar_canadense_percentual.reset_index()
    return dolar_canadense_percentual

dolar_canadense_percentual_df = dolar_canadense_percentual()
dolar_canadense_percentual_reset = dolar_canadense_percentual_df.reset_index()

variacao_hoje_canadense = dolar_canadense_percentual_reset.loc[0, 'dólar canadense']
variacao_ontem_canadense = dolar_canadense_percentual_reset.loc[1,'dólar canadense']

#Euro 

def euro_percentual():
    pd.set_option('float_format', '{:.0}'.format)
    euro_percentual = euro_ptax_reset['Euro'].pct_change(periods=-1)
    euro_percentual = euro_percentual.reset_index()
    return euro_percentual

euro_percentual_df = euro_percentual()
euro_percentual_reset = euro_percentual_df.reset_index()

variacao_hoje_euro = euro_percentual_reset.loc[0, 'Euro']
variacao_ontem_euro = euro_percentual_reset.loc[1,'Euro']

#Libra

def libra_percentual():
    pd.set_option('float_format', '{:.0}'.format)
    libra_percentual = libra_ptax_reset['Libra'].pct_change(periods=-1)
    libra_percentual = libra_percentual.reset_index()
    return libra_percentual

libra_percentual_df = libra_percentual()
libra_percentual_reset = libra_percentual_df.reset_index()
    
variacao_hoje_libra = libra_percentual_reset.loc[0, 'Libra']
variacao_ontem_libra = libra_percentual_reset.loc[1,'Libra']

#------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Processamento dos dados
# 
###Dólar

def dolar_processo():
  
  if dolar_hoje > dolar_ontem:
    return (f'O dólar fechou o dia em R${dolar_hoje:.4}, patamar {dolar_percentual_hoje:.0}% acima de ontem. No dia anterior, a moeda americana havia encerrado em R${dolar_ontem:.4}')
  
  else:
      return (f'O dólar fechou o dia em R${dolar_hoje:.4}, percentual {dolar_percentual_hoje:.0}% abaixo de ontem. No dia anterior, a moeda americana havia encerrado em R${dolar_ontem:.4} ')

dolar_processo()

  
###Dólar Canadense

def dolar_canadense_processo():
  
  if dolar_canadense_hoje > dolar_canadense_ontem:
    return (f'O dólar canadense fechou o dia em R${dolar_canadense_hoje:.4}, patamar {variacao_hoje_canadense:.0}% acima de ontem. No dia anterior, a moeda canadense havia encerrado em R${dolar_canadense_ontem:.4}')
  
  else:
      return (f'O dólar canadense fechou o dia em R${dolar_canadense_hoje:.4}, percentual {variacao_hoje_canadense:.0}% abaixo de ontem. No dia anterior, a moeda canadense havia encerrado em R${dolar_canadense_ontem:.4} ')

dolar_canadense_processo()

###Euro

def euro_processo():
  
  if euro_hoje > euro_ontem:
    return (f'O euro fechou o dia em R${euro_hoje:.4}, patamar {variacao_hoje_euro:.0}% acima de ontem. No dia anterior, a moeda europeia havia encerrado em R${euro_ontem:.4}')
  
  else:
      return (f'O euro fechou o dia em R${euro_hoje:.4}, percentual {variacao_hoje_euro:.0}% abaixo de ontem. No dia anterior, a moeda europeia havia encerrado em R${euro_ontem:.4} ')

euro_processo()  

###Libra

def libra_processo():
  
  if libra_hoje > libra_ontem:
    return (f'A libra fechou o dia em R${libra_hoje:.4}, patamar {variacao_hoje_libra:.0}% acima de ontem. No dia anterior, a moeda europeia havia encerrado em R${libra_ontem:.4}')

  else:
      return (f'A libra fechou o dia em R${libra_hoje:.4}, patamar {variacao_hoje_libra:.0}% abaixo de ontem. No dia anterior, a moeda europeia havia encerrado em R${libra_ontem:.4} ')

libra_processo()  



#------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
###Configuração do bot


# Rota para o webhook do Telegram
@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat_id
    message = update.message.text
    nova_mensagem = {
        "chat_id": chat_id,
        "text": f"Você enviou a mensagem: <b>{message}</b>",
        "parse_mode": "HTML",
    }
    if message == "/start":
        texto_resposta = "Olá! Seja bem-vindo(a).\nSou um robô criado no curso de Jornalismo de Dados do Insper para mostrar informações econômicas.\n\nVocê gostaria de saber sobre dólar, euro ou libra?\nPressione 1 para dólar, 2 para euro, 3 para a libra e 4 para dólar canadense"
        
    elif message == "1":
        texto_resposta = dolar_processo()
    elif message == "2":
        texto_resposta = euro_processo()  
    elif message == "3":
        texto_resposta = libra_processo()  
    elif message == "4":
        texto_resposta = dolar_canadense_processo()       
    else:
        bot.send_message(chat_id=chat_id, text="Desculpe, não entendi.")
        return nova_mensagem
    
    # envie a mensagem de resposta para o Telegram
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": texto_resposta,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    print(response.json())
    

    return "ok"

if __name__ == "__main__":
    app.run()




