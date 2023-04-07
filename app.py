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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters



TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1_FPdKuYoSq6iCCLK7f6dDCOrFpa3s5aBcfQIlXKfSyc/edit#gid=549163929")
sheet = planilha.worksheet("cotacao")
app = Flask(__name__)


@app.route("/")
def hello_world():
  return menu + "Olá! Eu sou um robô que compila e automatiza dados do Banco Central"

menu = """
<a href="/">Página inicial</a> |  
<br>
<br>
"""

###Recebendo aviso de nova mensagem
@app.route("/novamensagem")
def novamensagem():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Um novo usuário acessou o Robô de Dados do Banco Central"}
  requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return "Mensagem enviada."


#Configurando as informações de forma segura


#------------------------------------------------------------------------------------------------------------------------------------------------------------------

###Importando as moedas

###Os códigos de cada moeda ou índice

selic = sgs.get({'selic':432}, start = '1994-01-01')
ipca_mensal = sgs.get({'ipca':433}, start = '1994-01-01')
dolar = sgs.get({'dolar':1}, start = '1994-01-01')
euro = sgs.get({'euro':21619}, start = '1994-01-01')
libra = sgs.get({'libra':21623}, start = '1994-01-01')
dolar_canadense = sgs.get({'dolar_canadense':21635}, start = '1994-01-01')
iene = sgs.get({'iene':21621}, start = '1994-01-01')
peso_argentino = sgs.get({'dolar':14001}, start = '1994-01-01')


###Definindo a data de hoje

def hoje():
    return date.today()

def amanha():
    return date.today() + timedelta(days=1)

def ontem():
    return date.today() - timedelta(days=1)


###Consultando diferentes moedas

def dolar_ptax():
    dolar_df = sgs.get(1)
    dolar_df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    dolar_df = dolar_df.sort_index(ascending=False).reset_index()
    dolar_df = dolar_df.rename(columns={"date": "Dólar", df.columns[1]: "Dólar"})
    pd.set_option('float_format', '{:.4}'.format)
    return dolar_df.head(5)

dolar_ptax_df = dolar_ptax()
dolar_ptax_reset = dolar_ptax_df.reset_index()

def euro_ptax():
    euro_df = sgs.get(21619)
    euro_df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    euro_df = euro_df.sort_index(ascending=False).reset_index()
    euro_df = euro_df.rename(columns={"date": "Euro", df.columns[1]: "Euro"})
    pd.set_option('float_format', '{:.4}'.format)
    return euro_df.head(5)

euro_ptax_df = euro_ptax()
euro_ptax_reset = euro_ptax_df.reset_index()

def dolar_canadense_ptax():
    dolar_canadense_df = sgs.get(21635)
    dolar_canadense_df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    dolar_canadense_df = dolar_canadense_df.sort_index(ascending=False).reset_index()
    dolar_canadense_df = dolar_canadense_df.rename(columns={"date": "dólar_canadense", df.columns[1]: "dólar canadense"})
    pd.set_option('float_format', '{:.4}'.format)
    return dolar_canadense_df.head(5)

dolar_canadense_ptax_df = dolar_canadense_ptax()
dolar_canadense_ptax_reset = dolar_canadense_ptax_df.reset_index()


def libra_ptax():
    libra_df = sgs.get(21623)
    libra_df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    libra_df = libra_df.sort_index(ascending=False).reset_index()
    libra_df = libra_df.rename(columns={"date": "libra", df.columns[1]: "libra"})
    pd.set_option('float_format', '{:.4}'.format)
    return libra_df.head(5)

libra_ptax_df = libra_ptax()
libra_ptax_reset = libra_ptax_df.reset_index()
 
 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
  
#Memorizando as cotações das moedas na planilha

###Dólar

pd.set_option('float_format', '{:.2}'.format)

dolar_hoje = dolar_ptax_reset.loc[0,'dolar']
dolar_ontem = dolar_ptax_reset.loc[1,'dolar']
dolar_anteontem = dolar_ptax_reset.loc[2,'dolar']
dolar_ante_anteontem = dolar_ptax_reset.loc[3,'dolar']

###Dólar canadense

pd.set_option('float_format', '{:.2}'.format)

dolar_canadense_hoje = dolar_canadense_ptax_reset.loc[0,'dolar canadense']
dolar_canadense_ontem = dolar_canadense_ptax_reset.loc[1,'dolar canadense']
dolar_canadense_anteontem = dolar_canadense_ptax_reset.loc[2,'dolar canadense']
dolar_canadense_ante_anteontem = dolar_canadense_ptax_reset.loc[3,'dolar canadense']

###Euro
pd.set_option('float_format', '{:.2}'.format)

euro_hoje = euro_ptax_reset.loc[0,'euro']
euro_ontem = euro_ptax_reset.loc[1,'euro']
euro_anteontem = euro_ptax_reset.loc[2,'euro']
euro_ante_anteontem = euro_ptax_reset.loc[3,'euro']


###Libra
pd.set_option('float_format', '{:.2}'.format)

libra_hoje = libra_ptax_reset.loc[0,'libra']
libra_ontem = libra_ptax_reset.loc[1,'libra']
libra_anteontem = libra_ptax_reset.loc[2,'libra']
libra_ante_anteontem = libra_ptax_reset.loc[3,'libra']


#------------------------------------------------------------------------------------------------------------------------------------------------------------------  
  
#ESTABELECENDO OS PERCENTUAIS

###Dólar 

def dolar_percentual():
    pd.set_option('float_format', '{:.0}'.format)
    dolar_percentual = dolar_ptax_reset['dolar'].pct_change(periods=-1)
    dolar_percentual = dolar_percentual.reset_index()
    return dolar_percentual

dolar_percentual_df = dolar_percentual()
dolar_percentual_reset = dolar_percentual_df.reset_index()

dolar_percentual_hoje = dolar_percentual_reset.loc[0, 'dolar']
dolar_percentual_ontem = dolar_percentual_reset.loc[1,'dolar']

#Dólar Canadense


def dolar_canadense_percentual():
    pd.set_option('float_format', '{:.0}'.format)
    dolar_canadense_percentual = dolar_canadense_ptax_reset['dolar canadense'].pct_change(periods=-1)
    dolar_canadense_percentual = dolar_canadense_percentual.reset_index()
    return dolar_canadense_percentual


dolar_canadense_percentual_df = dolar_canadense_percentual()
dolar_percentual_reset = dolar_percentual_df.reset_index()

variacao_hoje_canadense = dolar_percentual_reset.loc[0, 'dolar canadense']
variacao_ontem_canadense = dolar_percentual_reset.loc[1,'dolar canadense']

#Euro 

def euro_percentual():
    pd.set_option('float_format', '{:.0}'.format)
    euro_percentual = euro_ptax_reset['euro'].pct_change(periods=-1)
    euro_percentual = euro_percentual.reset_index()
    return euro_percentual

euro_percentual_df = euro_percentual()
euro_percentual_reset = euro_percentual_df.reset_index()

variacao_hoje_euro = euro_percentual_reset.loc[0, 'euro']
variacao_ontem_euro = euro_percentual_reset.loc[1,'euro']

#Libra

def libra_percentual():
    pd.set_option('float_format', '{:.0}'.format)
    libra_percentual = libra_ptax_reset['libra'].pct_change(periods=-1)
    libra_percentual = libra_percentual.reset_index()
    return libra_percentual

libra_percentual_df = libra_percentual()
libra_percentual_reset = libra_percentual_df.reset_index()
    
variacao_hoje_libra = libra_percentual_reset.loc[0, 'libra']
variacao_ontem_libra = libra_percentual_reset.loc[1,'libra']
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
#PROCESSANDO O DÓLAR AMERICANO


def dolar_processo():
  
  if dolar_hoje > dolar_ontem:
    return (f'O dólar fechou o dia em R${dolar_hoje:.4}, patamar {dolar_percentual_hoje:.0}% acima de ontem. No dia anterior, a moeda americana havia encerrado em R${dolar_ontem:.4}')
  
  else:
      return (f'O dólar fechou o dia em R${dolar_hoje:.4}, percentual {dolar_percentual_hoje:.0}% abaixo de ontem. No dia anterior, a moeda americana havia encerrado em R${dolar_ontem:.4} ')

dolar_processo()    

#------------------------------------------------------------------------------------------------------------------------------------------------------------------ 

#PROCESSANDO O DÓLAR CANADENSE

def dolar_canadense_processo():
  
  if dolar_canadense_hoje > dolar_canadense_ontem:
    return (f'O dólar canadense fechou o dia em R${dolar_canadense_hoje:.4}, patamar {variacao_hoje_canadense:.0}% acima de ontem. No dia anterior, a moeda canadense havia encerrado em R${dolar_canadense_ontem:.4}')
  
  else:
      return (f'O dólar canadense fechou o dia em R${dolar_canadense_hoje:.4}, percentual {variacao_hoje_canadense:.0}% abaixo de ontem. No dia anterior, a moeda canadense havia encerrado em R${dolar_canadense_ontem:.4} ')

dolar_canadense_processo()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------ 

#PROCESSANDO OS DADOS DO EURO

def euro_processo():
  
  if euro_hoje > euro_ontem:
    return (f'O euro fechou o dia em R${euro_hoje:.4}, patamar {variacao_hoje_euro:.0}% acima de ontem. No dia anterior, a moeda europeia havia encerrado em R${euro_ontem:.4}')
  
  else:
      return (f'O euro fechou o dia em R${euro_hoje:.4}, percentual {variacao_hoje_euro:.0}% abaixo de ontem. No dia anterior, a moeda europeia havia encerrado em R${euro_ontem:.4} ')

euro_processo()  


#------------------------------------------------------------------------------------------------------------------------------------------------------------------ 

#Consultando os percentuais da libra

###Processando os dados da libra

def libra_processo():
  
  if libra_hoje > libra_ontem:
    return (f'A libra fechou o dia em R${libra_hoje:.4}, patamar {variacao_hoje_libra:.0}% acima de ontem. No dia anterior, a moeda europeia havia encerrado em R${libra_ontem:.4}')

  else:
      return (f'A libra fechou o dia em R${libra_hoje:.4}, patamar {variacao_hoje_libra:.0}% abaixo de ontem. No dia anterior, a moeda europeia havia encerrado em R${libra_ontem:.4} ')

libra_processo()  

#------------------------------------------------------------------------------------------------------------------------------------------------------------------


                    
###Configuração do bot
app = Flask(Dados_do_Banco_Central)

# Defina a chave de acesso do seu bot aqui
bot_token = os.environ.get('TELEGRAM_API_KEY')
bot = telegram.Bot(token=bot_token)

# Defina a URL pública do seu aplicativo Render
# Certifique-se de que essa URL corresponde ao seu endereço Render
app_url = 'https://site-teste-fernando.onrender.com'

# Rota para o webhook do Telegram
@app.route(f"/{bot_token}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat_id
    message = update.message.text
    telegram_bot(message, chat_id)
    return "ok"

# Função para responder às mensagens do Telegram
def telegram_bot(message, chat_id):
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

if __name__ == "__main__":
    # Defina o webhook para escutar as atualizações de mensagem do Telegram
    bot.setWebhook(url=f"{app_url}{bot_token}")
    app.run()
