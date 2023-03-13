from flask import Flask

app = Flask(_name_)

@app.route("/")
def hello_world():
  return "Olá, mundo! Esse é meu site. (Fernando Barbosa)"
