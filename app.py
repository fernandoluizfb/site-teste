import os

import gspread
import pandas as pd
import requests

from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper
from bcb import sgs
from datetime import datetime, date
from datetime import timedelta
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


app = Flask(__name__)

------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/")
def hello_world():
  return menu + "Olá! Eu sou um robô que compila e automatiza dados do Banco Central"

menu = """
<a href="/">Página inicial</a> |  
<br>
<br>
"""

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  nova_mensagem = {"chat_id": chat_id, "text": message}
  requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  return "ok"


###Recebendo aviso de nova mensagem
@app.route("/novamensagem")
def novamensagem:
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Um novo usuário acessou o Robô de Dados do Banco Central"}
  requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return "Mensagem enviada."

#Configurando as informações de forma segura

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta) # sheets.new
planilha = api.open_by_key("GOOGLE_SHEETS_CREDENTIALS")
sheet = planilha.worksheet("Sheet1")

------------------------------------------------------------------------------------------------------------------------------------------------------------------

###Importando as moedas

selic = sgs.get({'selic':432}, start = '1994-01-01')
ipca_mensal = sgs.get({'ipca':433}, start = '1994-01-01')
dolar_ptax = sgs.get({'dolar':1}, start = '1994-01-01')
euro_ptax = sgs.get({'euro':21619}, start = '1994-01-01')
libra_ptax = sgs.get({'libra':21623}, start = '1994-01-01')
dolar_canadense_ptax = sgs.get({'dolar canadense':21635}, start = '1994-01-01')
iene_ptax = sgs.get({'iene':21621}, start = '1994-01-01')
peso_argentino_ptax = sgs.get({'dolar':14001}, start = '1994-01-01')


###Definindo a data de hoje

from datetime import date, timedelta

def hoje():
    return date.today()

def amanha():
    return date.today() + timedelta(days=1)

def ontem():
    return date.today() - timedelta(days=1)


###Consultando diferentes moedas

def dolar_ptax():
    df = sgs.get(1)
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    df = df.sort_index(ascending=False).reset_index()
    df = df.rename(columns={"date": "Dólar", df.columns[1]: "Dólar"})
    pd.set_option('float_format', '{:.4}'.format)
    return df.head(5)

def euro_ptax():
    df = sgs.get(21619)
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    df = df.sort_index(ascending=False).reset_index()
    df = df.rename(columns={"date": "Euro", df.columns[1]: "Euro"})
    pd.set_option('float_format', '{:.4}'.format)
    return df.head(5)

def dolar_canadense_ptax():
    df = sgs.get(21635)
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    df = df.sort_index(ascending=False).reset_index()
    df = df.rename(columns={"date": "dólar_canadense", df.columns[1]: "dólar canadense"})
    pd.set_option('float_format', '{:.4}'.format)
    return df.head(5)

def libra_ptax():
    df = sgs.get(21623)
    df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    df = df.sort_index(ascending=False).reset_index()
    df = df.rename(columns={"date": "libra", df.columns[1]: "libra"})
    pd.set_option('float_format', '{:.4}'.format)
    return df.head(5)

 
------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
  
#Memorizando as cotações das moedas na planilha

###Dólar

pd.set_option('float_format', '{:.2}'.format)

dolar_hoje = dolar_ptax.reset_index().loc[0,'dolar']
dolar_ontem = dolar_ptax.reset_index().loc[1,'dolar']
dolar_anteontem = dolar_ptax.reset_index().loc[2,'dolar']
dolar_ante_anteontem = dolar_ptax.reset_index().loc[3,'dolar']

variacao_hoje = dolar_percentual.reset_index().loc[0, 'dolar']
variacao_ontem = dolar_percentual.reset_index().loc[1,'dolar']

###Dólar canadense

pd.set_option('float_format', '{:.2}'.format)

dolar_canadense_hoje = dolar_canadense_ptax.reset_index().loc[0,'dolar canadense']
dolar_canadense_ontem = dolar_canadense_ptax.reset_index().loc[1,'dolar canadense']
dolar_canadense_anteontem = dolar_canadense_ptax.reset_index().loc[2,'dolar canadense']
dolar_canadense_ante_anteontem = dolar_canadense_ptax.reset_index().loc[3,'dolar canadense']

variacao_hoje_canadense = dolar_canadense_percentual.reset_index().loc[0, 'dolar canadense']
variacao_ontem_canadense = dolar_canadense_percentual.reset_index().loc[1,'dolar canadense']

###Euro
pd.set_option('float_format', '{:.2}'.format)

euro_hoje = euro_ptax.reset_index().loc[0,'euro']
euro_ontem = euro_ptax.reset_index().loc[1,'euro']
euro_anteontem = euro_ptax.reset_index().loc[2,'euro']
euro_ante_anteontem = euro_ptax.reset_index().loc[3,'euro']

variacao_hoje_euro = euro_percentual.reset_index().loc[0, 'euro']
variacao_ontem_euro = euro_percentual.reset_index().loc[1,'euro']

###Libra
pd.set_option('float_format', '{:.2}'.format)

libra_hoje = libra_ptax.reset_index().loc[0,'libra']
libra_ontem = libra_ptax.reset_index().loc[1,'libra']
libra_anteontem = libra_ptax.reset_index().loc[2,'libra']
libra_ante_anteontem = libra_ptax.reset_index().loc[3,'libra']

variacao_hoje_libra = libra_percentual.reset_index().loc[0, 'libra']
variacao_ontem_libra = libra_percentual.reset_index().loc[1,'libra']
  
------------------------------------------------------------------------------------------------------------------------------------------------------------------  
  
  
#PROCESSANDO O DÓLAR AMERICANO

pd.set_option('float_format', '{:.2%}'.format)

def dolar_percentual():

  dolar_percentual = (dolar['dolar'] / dolar['dolar'].shift(1) - 1)
  dolar_percentual = dolar_percentual.sort_index(ascending=False).reset_index()

  return dolar_percentual

###As cotações do dólar hoje, ontem, anteontem e do dia antes de anteontem

pd.set_option('float_format', '{:.2%}'.format)

dolar_ptax_hoje = dolar_ptax().sort_index(ascending=False).loc[0,'Dólar']
dolar_ptax_ontem = dolar_ptax().sort_index(ascending=False).loc[1,'Dólar']
dolar_ptax_anteontem = dolar_ptax().sort_index(ascending=False).loc[2,'Dólar']
dolar_ptax_ante_anteontem = dolar_ptax().sort_index(ascending=False).loc[3,'Dólar']


###Percentuais do dólar

pd.set_option('float_format', '{:.1f}'.format)

dolar_percentual = (dolar['dolar'] / dolar['dolar'].shift(1) - 1)
dolar_percentual = dolar_percentual.sort_index(ascending=False).reset_index()
dolar_percentual = dolar['dolar'].pct_change().sort_index(ascending=False)

variacao_hoje = dolar_percentual.loc[dolar_percentual.index[0]]
variacao_ontem = dolar_percentual.loc[dolar_percentual.index[1]]

###Processando os dados do dólar americano

def dolar_variacao():
  
  if dolar_ptax_hoje > dolar_ptax_ontem:
    return (f'O dólar fechou o dia em R${dolar_ptax_hoje:.4}, patamar {variacao_hoje:.0}% acima de ontem. No dia anterior, a moeda americana havia encerrado em R${dolar_ptax_ontem:.4}')
  
  else:
      return (f'O dólar fechou o dia em R${dolar_ptax_hoje:.4}, percentual {variacao_hoje:.0}% abaixo de ontem. No dia anterior, a moeda americana havia encerrado em R${dolar_ptax_ontem:.4} ')

dolar_variacao()    

------------------------------------------------------------------------------------------------------------------------------------------------------------------ 

#PROCESSANDO O DÓLAR CANADENSE

pd.set_option('float_format', '{:.2%}'.format)

def dolar_canadense_percentual():
    dolar_canadense_percentual = (dolar_canadense['dolar_canadense'] / dolar_canadense['dolar_canadense'].shift(1) - 1)
    dolar_canadense_percentual = dolar_canadense_percentual.sort_index(ascending=False).reset_index()
    
    return dolar_canadense_percentual

###salvando em variáveis as cotações do dólar canadense dos últimos dias

pd.set_option('float_format', '{:.1f}'.format)

dolar_canadense_ptax_hoje = dolar_canadense_ptax().sort_index(ascending=False).loc[0,'dólar canadense']
dolar_canadense_ptax_ontem = dolar_canadense_ptax().sort_index(ascending=False).loc[1,'dólar canadense']
dolar_canadense_ptax_anteontem = dolar_canadense_ptax().sort_index(ascending=False).loc[2,'dólar canadense']
dolar_canadense_ptax_ante_anteontem = dolar_canadense_ptax().sort_index(ascending=False).loc[3,'dólar canadense']

dolar_canadense_percentual = dolar_canadense['dolar_canadense'].pct_change().sort_index(ascending=False)
variacao_canadense_hoje = dolar_canadense_percentual.loc[dolar_canadense_percentual.index[0]]
variacao_canadense_ontem = dolar_canadense_percentual.loc[dolar_canadense_percentual.index[1]]

###Processando os dados do dólar canadense

def dolar_canadense_variacao():
  
  if dolar_canadense_ptax_hoje > dolar_canadense_ptax_ontem:
    return (f'O dólar canadense fechou o dia em R${dolar_canadense_ptax_hoje:.4}, patamar {variacao_canadense_hoje:.0}% acima de ontem. No dia anterior, a moeda canadense havia encerrado em R${dolar_canadense_ptax_ontem:.4}')
  
  else:
      return (f'O dólar canadense fechou o dia em R${dolar_canadense_ptax_hoje:.4}, percentual {variacao_canadense_hoje:.0}% abaixo de ontem. No dia anterior, a moeda canadense havia encerrado em R${dolar_canadense_ptax_ontem:.4} ')

dolar_canadense_variacao()  

------------------------------------------------------------------------------------------------------------------------------------------------------------------ 

#PROCESSANDO OS DADOS DO EURO

pd.set_option('float_format', '{:.2%}'.format)

def euro_percentual():
    euro_percentual = (euro['euro'] / euro['euro'].shift(1) - 1)
    euro_percentual = euro_percentual.sort_index(ascending=False).reset_index()
    
    return euro_percentual

###Salvando em variáveis as cotações do dólar canadense dos últimos dias

pd.set_option('float_format', '{:.1f}'.format)

euro_ptax_hoje = euro_ptax().sort_index(ascending=False).loc[0,'Euro']
euro_ptax_ontem = euro_ptax().sort_index(ascending=False).loc[1,'Euro']
euro_ptax_anteontem = euro_ptax().sort_index(ascending=False).loc[2,'Euro']
euro_ptax_ante_anteontem = euro_ptax().sort_index(ascending=False).loc[3,'Euro']

euro_percentual = euro['euro'].pct_change().sort_index(ascending=False)
variacao_euro_hoje = euro_percentual.loc[euro_percentual.index[0]]
variacao_euro_ontem = euro_percentual.loc[euro_percentual.index[1]]

###Processando os dados do euro

def euro_variacao():
  
  if euro_ptax_hoje > euro_ptax_ontem:
    return (f'O euro fechou o dia em R${euro_ptax_hoje:.4}, patamar {variacao_euro_hoje:.0}% acima de ontem. No dia anterior, a moeda europeia havia encerrado em R${euro_ptax_ontem:.4}')
  
  else:
      return (f'O euro fechou o dia em R${euro_ptax_hoje:.4}, percentual {variacao_euro_ontem:.0}% abaixo de ontem. No dia anterior, a moeda europeia havia encerrado em R${euro_ptax_ontem:.4} ')

euro_variacao()  


------------------------------------------------------------------------------------------------------------------------------------------------------------------ 

#Consultando os percentuais da libra

pd.set_option('float_format', '{:.2%}'.format)

def libra_percentual():
    libra_percentual = (libra['libra'] / libra['libra'].shift(1) - 1)
    libra_percentual = libra_percentual.sort_index(ascending=False).reset_index()
    
    return libra_percentual
  
  
###Salvando em variáveis as cotações da libra dos últimos dias

pd.set_option('float_format', '{:.1f}'.format)

libra_ptax_hoje = libra_ptax().sort_index(ascending=False).loc[0,'libra']
libra_ptax_ontem = libra_ptax().sort_index(ascending=False).loc[1,'libra']
libra_ptax_anteontem = libra_ptax().sort_index(ascending=False).loc[2,'libra']
libra_ptax_ante_anteontem = libra_ptax().sort_index(ascending=False).loc[3,'libra']

libra_percentual = libra['libra'].pct_change().sort_index(ascending=False)
variacao_libra_hoje = libra_percentual.loc[libra_percentual.index[0]]
variacao_libra_ontem = libra_percentual.loc[libra_percentual.index[1]]

###Processando os dados da libra

def libra_variacao():
  
  if libra_ptax_hoje > libra_ptax_ontem:
    return (f'A libra fechou o dia em R${libra_ptax_hoje:.4}, patamar {variacao_libra_hoje:.0}% acima de ontem. No dia anterior, a moeda europeia havia encerrado em R${libra_ptax_ontem:.4}')
  
  else:
      return (f'A libra fechou o dia em R${libra_ptax_hoje:.4}, patamar {variacao_euro_hoje:.0}% abaixo de ontem. No dia anterior, a moeda europeia havia encerrado em R${libra_ptax_ontem:.4} ')

libra_variacao()  

------------------------------------------------------------------------------------------------------------------------------------------------------------------ 

###Salvando as cotações na planilha

sheetcotacao.update("A2", f'"R$ {dolar_ptax_hoje}')
sheetcotacao.update("A3", f'"R$ {dolar_ptax_ontem}')
sheetcotacao.update("A4", f'"R$ {dolar_ptax_anteontem}')
sheetcotacao.update("A5", f'"R$ {dolar_ptax_ante_anteontem}'

sheetcotacao.update("D2", f'"R$ {dolar_canadense_ptax_hoje}')
sheetcotacao.update("D3", f'"R$ {dolar_canadense_ptax_ontem}')
sheetcotacao.update("D4", f'"R$ {dolar_canadense_ptax_anteontem}')
sheetcotacao.update("D5", f'"R$ {dolar_canadense_ptax_ante_anteontem}')

sheetcotacao.update("B2", f'"R$ {euro_ptax_hoje}')
sheetcotacao.update("B3", f'"R$ {euro_ptax_ontem}')
sheetcotacao.update("B4", f'"R$ {euro_ptax_anteontem}')
sheetcotacao.update("B5", f'"R$ {euro_ptax_ante_anteontem}')

sheetcotacao.update("C2", f'"R$ {libra_ptax_hoje}')
sheetcotacao.update("C3", f'"R$ {libra_ptax_ontem}')
sheetcotacao.update("C4", f'"R$ {libra_ptax_anteontem}')
sheetcotacao.update("C5", f'"R$ {libra_ptax_ante_anteontem}')
                    
------------------------------------------------------------------------------------------------------------------------------------------------------------------

                    
###Configuração do bot

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    texto_resposta = "Olá! Seja bem-vindo(a).\nSou um robô criado no curso de Jornalismo de Dados do Insper para mostrar informações econômicas.\n\nVocê gostaria de saber sobre dólar, euro, a libra ou o dólar canadense?\nPressione 1 para dólar, 2 para euro, 3 para a libra e 4 para dólar canadense"
    context.bot.send_message(chat_id=update.effective_chat.id, text=texto_resposta)

def echo(update, context):
    message = update.message.text
    id_do_bot = update.effective_chat.id
        
    if message == "1":
        texto_resposta = return dolar_variacao()
    elif message == "2":
        texto_resposta = return euro_variacao()
    elif message == "3":
        texto_resposta = return libra_variacao()
    elif message == "4":
        texto_resposta = return dolar_canadense_variacao()
    else:
        texto_resposta = "Não entendi. Pode repetir, por favor?"
    context.bot.send_message(chat_id=id_do_bot, text=texto_resposta)

def webhook(request):
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'


