!pip install tchan

from flask import Flask
from tchan import ChannelScraper

app = Flask(__name__)

"""
<a href="/">Página inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
<br>
"""

@app.route("/")
def hello_world():
  return menu + "Olá, mundo! Esse é meu site. (Fernando Barbosa)"

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página contato"

@app.route("/promocoes")
def ultimas_promocoes():
  scraper = ChannelScraper()
  contador = 0
  resultado = []
  for message in scraper.messages("promocoeseachadinhos"):
    contador += 1
    texto = message.text.strip().splitlines()[0]
    resultado.append(f"{message.created_at} {texto}")
    if contador == 10:
      return resultado
