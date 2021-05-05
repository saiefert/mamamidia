from flask import Flask
from mapamidia import resultado


app = Flask(__name__)


@app.route('/consultaADHuna')
def consultaAD():
    return resultado


@app.route('/atualizaADHuna')
def atualizaAD():
    return resultado


if __name__ == '__main__':
    app.run(host='0.0.0.0')
