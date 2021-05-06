from flask import Flask
from mapamidia import resultado
from atualizaMapamidia import arquivo


app = Flask(__name__)


@app.route('/consultaADHuna')
def consultaAD():
    return resultado


@app.route('/atualizaADHuna')
def atualizaAD():
    return arquivo


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
