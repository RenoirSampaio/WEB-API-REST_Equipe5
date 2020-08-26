from flask import Flask, make_response, jsonify, request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

app = Flask(__name__)

@app.route('/hello')
def hello():
  return 'Hello World!'

if __name__ == '__main__':
  app.run()

# Possíveis rotas:
# @app.route('/api/ocorr/total/<UF:name>', methods=['GET'])
# @app.route('/api/vit/total/<UF:name>', methods=['GET'])
# @app.route('/api/vit/<Município:name>', methods=['GET'])
# @app.route('/api/ocorr/<Tipo Crime:name>', methods=['GET'])
# @app.route('/api/vit/br/<Tipo Crime:name>', methods=['GET'])
# @app.route('/api/vit/epoc/<Ano:name>', methods=['GET'])
# @app.route('/api/ocorr/crim/tipos', methods=['GET'])
# @app.route('/api/vit/crim/tipos', methods=['GET'])