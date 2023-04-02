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


app = Flask(__name__)

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

hoje = date.today()
###hoje = hoje.date()

###Definindo amanhã
amanha = hoje + timedelta(days=1)

###Definindo ontem
ontem = hoje - timedelta(days=1)



menu = """
<a href="/">Página inicial</a> |  
<br>
<br>
"""

@app.route("/")
def hello_world():
  return menu + "Olá! Eu sou um robô que compila e automatiza dados do Banco Central"

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

#Consultando diferentes moedas

###Dólar
pd.set_option('float_format', '{:.4}'.format)
dolar_ptax = dolar_ptax.sort_index(ascending=False)
dolar_ptax.head(5)

###Dólar Canadense
pd.set_option('float_format', '{:.4}'.format)
dolar_canadense_ptax = dolar_canadense_ptax.sort_index(ascending=False)
dolar_canadense_ptax.head(5)

###Euro
pd.set_option('float_format', '{:.4}'.format)
euro_ptax = euro_ptax.sort_index(ascending=False)
euro_ptax.head(5)

###Libra
pd.set_option('float_format', '{:.4}'.format)
libra_ptax = libra_ptax.sort_index(ascending=False)
libra_ptax.head(10)

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

#Dólar
pd.set_option('float_format', '{:.0}'.format)
dolar_percentual = dolar_ptax['dolar'].pct_change(periods=-1)
dolar_percentual = dolar_percentual.reset_index()
dolar_percentual

###Indicando a variação do dólar com o processamento dos dados
pd.set_option('float_format', '{:.2}'.format)

dolar_hoje = dolar_ptax.reset_index().loc[0,'dolar']
dolar_ontem = dolar_ptax.reset_index().loc[1,'dolar']
dolar_anteontem = dolar_ptax.reset_index().loc[2,'dolar']
dolar_ante_anteontem = dolar_ptax.reset_index().loc[3,'dolar']

variacao_hoje = dolar_percentual.reset_index().loc[0, 'dolar']
variacao_ontem = dolar_percentual.reset_index().loc[1,'dolar']

if dolar_hoje > dolar_ontem:
  print(f'O dólar fechou o dia em R${dolar_hoje:.4}, patamar {variacao_hoje:.1}% acima de ontem. No dia anterior, a moeda americana havia encerrado em R${dolar_ontem:.4}')

else:
  dolar_hoje < dolar_ontem 
  print(f'O dólar fechou o dia em R${dolar_hoje:.4}, percentual {variacao_hoje:.1}% abaixo de ontem. No dia anterior, a moeda americana havia encerrado em R${dolar_ontem:.4} ')
  
 ###Jogando os dados da variação do dólar na planilha
sheetcotacao.update("A2", f'"R$ {dolar_hoje}')
sheetcotacao.update("A3", f'"R$ {dolar_ontem}')
sheetcotacao.update("A4", f'"R$ {dolar_anteontem}')
sheetcotacao.update("A5", f'"R$ {dolar_ante_anteontem}')

#Dólar Canadense

pd.set_option('float_format', '{:.0}'.format)
dolar_canadense_percentual = dolar_canadense_ptax['dolar canadense'].pct_change(periods=-1)
dolar_canadense_percentual = dolar_canadense_percentual.reset_index()
dolar_canadense_percentual

###Indicando a variação do dólar com o processamento dos dados
pd.set_option('float_format', '{:.2}'.format)

dolar_canadense_hoje = dolar_canadense_ptax.reset_index().loc[0,'dolar canadense']
dolar_canadense_ontem = dolar_canadense_ptax.reset_index().loc[1,'dolar canadense']
dolar_canadense_anteontem = dolar_canadense_ptax.reset_index().loc[2,'dolar canadense']
dolar_canadense_ante_anteontem = dolar_canadense_ptax.reset_index().loc[3,'dolar canadense']

variacao_hoje_canadense = dolar_canadense_percentual.reset_index().loc[0, 'dolar canadense']
variacao_ontem_canadense = dolar_canadense_percentual.reset_index().loc[1,'dolar canadense']

if dolar_canadense_hoje > dolar_canadense_ontem:
  print(f'O dólar canadense fechou o dia em R${dolar_canadense_hoje:.4}, patamar {variacao_hoje_canadense:.1}% acima de ontem. No dia anterior, a moeda canadense havia encerrado em R${dolar_canadense_ontem:.4}')

else:
  dolar_canadense_hoje < dolar_canadense_ontem 
  print(f'O dólar canadense fechou o dia em R${dolar_canadense_hoje:.4}, patamar {variacao_hoje_canadense:.1}% abaixo de ontem. No dia anterior, a moeda canadense havia encerrado em R${dolar_canadense_ontem:.4} ')
  
###Jogando os dados da variação da libra na planilha
sheetcotacao.update("D2", f'"R$ {dolar_canadense_hoje}')
sheetcotacao.update("D3", f'"R$ {dolar_canadense_ontem}')
sheetcotacao.update("D4", f'"R$ {dolar_canadense_anteontem}')
sheetcotacao.update("D5", f'"R$ {dolar_canadense_ante_anteontem}')

### Consultando o percentual do euro

pd.set_option('float_format', '{:.0}'.format)
euro_percentual = euro_ptax['euro'].pct_change(periods=-1)
euro_percentual = euro_percentual.reset_index()
euro_percentual


###Indicando a variação do dólar com o processamento dos dados
pd.set_option('float_format', '{:.2}'.format)

euro_hoje = euro_ptax.reset_index().loc[0,'euro']
euro_ontem = euro_ptax.reset_index().loc[1,'euro']
euro_anteontem = euro_ptax.reset_index().loc[2,'euro']
euro_ante_anteontem = euro_ptax.reset_index().loc[3,'euro']

variacao_hoje_euro = euro_percentual.reset_index().loc[0, 'euro']
variacao_ontem_euro = euro_percentual.reset_index().loc[1,'euro']

if euro_hoje > euro_ontem:
  print(f'O euro fechou o dia em R${euro_hoje:.4}, patamar {variacao_hoje_euro:.1}% acima de ontem. No dia anterior, a moeda europeia havia encerrado em R${euro_ontem:.4}')

else:
  euro_hoje < euro_ontem 
  print(f'O euro fechou o dia em R${euro_hoje:.4}, percentual {variacao_hoje_euro:.1}% abaixo de ontem. No dia anterior, a moeda europeia havia encerrado em R${euro_ontem:.4} ')
  
###Jogando os dados da variação do euro na planilha
sheetcotacao.update("B2", f'"R$ {euro_hoje}')
sheetcotacao.update("B3", f'"R$ {euro_ontem}')
sheetcotacao.update("B4", f'"R$ {euro_anteontem}')
sheetcotacao.update("B5", f'"R$ {euro_ante_anteontem}')

###Pegando os valores da libra de hoje, ontem, anteontem e do dia antes de anteontem
pd.set_option('float_format', '{:.2}'.format)

libra_hoje = libra_ptax.reset_index().loc[0,'libra']
libra_ontem = libra_ptax.reset_index().loc[1,'libra']
libra_anteontem = libra_ptax.reset_index().loc[2, 'libra']
libra_ante_anteontem = libra_ptax.reset_index().loc[3,'libra']

###Consultando o percentual da libra
pd.set_option('float_format', '{:.0}'.format)
libra_percentual = libra_ptax['libra'].pct_change(periods=-1)
libra_percentual = libra_percentual.reset_index()
libra_percentual


###Indicando a variação da libra com o processamento dos dados
pd.set_option('float_format', '{:.2}'.format)

libra_hoje = libra_ptax.reset_index().loc[0,'libra']
libra_ontem = libra_ptax.reset_index().loc[1,'libra']
libra_anteontem = libra_ptax.reset_index().loc[2,'libra']
libra_ante_anteontem = libra_ptax.reset_index().loc[3,'libra']

variacao_hoje_libra = libra_percentual.reset_index().loc[0, 'libra']
variacao_ontem_libra = libra_percentual.reset_index().loc[1,'libra']

if libra_hoje > libra_ontem:
  print(f'A libra fechou o dia em R${libra_hoje:.4}, patamar {variacao_hoje_libra:.1}% acima de ontem. No dia anterior, a moeda inglesa havia encerrado em R${libra_ontem:.4}')

else:
  libra_hoje < libra_ontem 
  print(f'A libra fechou o dia em R${libra_hoje:.4}, percentual {variacao_hoje_libra:.1}% abaixo de ontem. No dia anterior, a moeda inglesa havia encerrado em R${libra_ontem:.4} ')
  
  ###Jogando os dados da variação da libra na planilha

sheetcotacao.update("C2", f'"R$ {libra_hoje}')
sheetcotacao.update("C3", f'"R$ {libra_ontem}')
sheetcotacao.update("C4", f'"R$ {libra_anteontem}')
sheetcotacao.update("C5", f'"R$ {libra_ante_anteontem}')

###Guardando o token do robô com segurança
import getpass
token = getpass.getpass()

###Fazendo a requisição para o robô
resposta = requests.get(f"https://api.telegram.org/bot{token}/getMe")


###Utilizando o dicionário do robô
dados = resposta.json()
dados_internos = dados['result']
nome_do_bot = dados_internos['username']
id_do_bot = dados_internos['id']

print(f'Robô Dados do Banco Central @{nome_do_bot} ({id_do_bot})')

resposta = requests.get(f"https://api.telegram.org/bot{token}/getUpdates")
dados = resposta.json()['result']
print(dados)

#Deixar o dicionário visualmente mais legível
import json
print(json.dumps(dados, indent=2))

import pandas as pd 
valor = 1675722349 # número de segundos desde 00/01/1970 00:00:00

import datetime
convertido = datetime.datetime.fromtimestamp(valor)
update_id = 0
updates_processados = []

# Pegar na planilha do sheets o último update_id
resposta = sheet.get("B2")
celula = resposta[0][0] ###Pegando os valores dentro dos dicionários
update = int(celula) ###Transformando a string em número

###Parâmetros de uma URL (query strings)

resposta = requests.get(f"https://api.telegram.org/bot{token}/getUpdates?offset={update_id + 1}" )
dados = resposta.json()['result']
print(f"Temos {len(dados)} novas atualizações:")
mensagens = []

for update in dados:
  update_id = update["update_id"]
###Extraindo as respostas dos usuários
  first_name = update["message"]["from"]["first_name"]
  last_name = update["message"]["from"]["last_name"]
  sender_id = update["message"]["from"]["id"]
  if "text" not in update["message"]: ###Ignorando mensagens que não sejam textos
    continue
  message = update["message"]["text"]
  id_do_bot = update["message"]["chat"]["id"]
  datahora = str(datetime.datetime.fromtimestamp(update["message"]["date"]))
  if "nome_do_bot" in update ["message"]["from"]:
    nome_do_bot = f' @{update["message"]["from"]["first_name"]["last_name"]}'
  else:
    nome_do_bot = ""
  print(f"[{datahora}]Nova mensagem de {first_name} {last_name}{nome_do_bot} ({id_do_bot}): {message}" )
  mensagens.append([str(datahora), "recebida", first_name, id_do_bot, message]) ###Para colocar na tabela as mensagens enviadas

###Definindo resposta para os usuários

  if message == "/start":
    texto_resposta = "Olá! Seja bem-vindo(a).\nSou um robô criado no curso de Jornalismo de Dados do Insper para mostrar informações econômicas.\n\nVocê gostaria de saber sobre dólar, euro ou libra?\nPressione 1 para dólar, 2 para euro e 3 para a libra"

  elif message == "1":
    texto_resposta = (f'O dólar fechou o dia em R${dolar_hoje}')

  elif message == "2":
    texto_resposta = (f'O euro fechou o dia em R${euro_hoje}')

  elif message == "3":
    texto_resposta = (f'A libra fechou o dia em R${libra_hoje}')

  elif message == "4":
    texto_resposta = (f'O dólar canadense fechou o dia em R${libra_hoje}')

  else:
    texto_resposta = "Não entendi. Pode repetir, por favor?"
  nova_mensagem = {"chat_id": id_do_bot, "text": texto_resposta}
  requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=nova_mensagem)
  mensagens.append([str(datahora), "enviada", first_name, id_do_bot, texto_resposta]) ###Para colocar na tabela as mensagens enviadas

###Atualiza a planilha do sheets com o último update
sheet.append_rows(mensagens)
sheet.update("B2", update_id)


