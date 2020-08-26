from flask import Flask, make_response, jsonify, request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json 


df1 = pd.concat(pd.read_excel('indicadoressegurancapublicamunicmar20.xlsx', sheet_name=None), ignore_index=True)
df2 = pd.read_excel('indicadoressegurancapublicaufmar20_ocorrencias.xlsx')
df3 = pd.read_excel('indicadoressegurancapublicaufmar20_vítimas.xlsx')


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/hello', methods=['GET'])
def hello():
  return 'Hello World!'



# GET ocorrências totais por UF
# /api/ocorr/total/<UF:name>
# Aqui ta retornando uma Series
# Um tipo de dado do pandas
@app.route('/ocorr/total/<UF>', methods=['GET'])
def getOcorrTotalByUf(UF):
  # if 'UF' in request.args:
  #     UF = request.args['UF']
  # else:
  #     return "Error: Especifique o UF da consulta"
  df2_prov = df2.loc[df2['UF'] == UF]
  res = df2_prov.groupby("UF")["Ocorrências"].sum().to_json()
  return res



# # /api/ocorr/crim/tipos
# Aqui ta retornando um array de strings.
@app.route('/ocorr/crim/tipos', methods=['GET'])
def getTiposCrimes():
  res = np.unique(df2['Tipo Crime'])
  a = res.tolist()
  return json.dumps(a)




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