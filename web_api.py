from flask import Flask, make_response, jsonify, request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json 

df1 = pd.concat(pd.read_excel('indicadoressegurancapublicamunicmar20.xlsx', sheet_name=None), ignore_index=True)
df2 = pd.read_excel('indicadoressegurancapublicaufmar20_ocorrencias.xlsx')
df3 = pd.read_excel('indicadoressegurancapublicaufmar20_vítimas.xlsx')

df1['Mês/Ano'] = pd.to_datetime(df1['Mês/Ano'], errors='coerce', format='%Y-%m-%d %H:%M:%S')
df1["Ano"] = df1["Mês/Ano"].dt.year

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/hello', methods=['GET'])
def hello():
  return 'Hello World!'

################################################################
# GET ocorrências totais por UF
# /api/ocorr/total/<UF:name>
# Aqui ta retornando uma Series
# Um tipo de dado do pandas
@app.route('/ocorr/total/<UF>', methods=['GET'])
def getOcorrTotalByUf(UF):
  df2_prov = df2.loc[df2['UF'] == UF]
  res = df2_prov.groupby("UF")["Ocorrências"].sum().to_json()
  return res
################################################################

# GET vítimas totais por UF
# vit/total/<UF:name>
@app.route('/vit/total/<UF>', methods=['GET'])
def getVitTotal(UF):
  df3_prov = df3.loc[df3['UF'] == UF]
  res = df3_prov.groupby("UF")["Vítimas"].sum().to_json()
  return res
################################################################

# GET vítimas por Municípios
# /vit/<city>
@app.route('/vit/<city>', methods=['GET'])
def getVitCity(city):
  df1_prov = df1.loc[df1['Município'] == city]
  res = df1_prov.groupby("Município")["Vítimas"].sum().to_json()
  return res
################################################################

# GET ocorrências de um tipo de crime no Brasil
# /ocorr/<crime>
@app.route('/ocorr/<crime>', methods=['GET'])
def getOcorrCrimeBrasil(crime):
  df2_prov = df2.loc[df2['Tipo Crime'] == crime]
  res = df2_prov["Ocorrências"].sum()
  return jsonify(int(res))
################################################################

# GET vítimas de um tipo de crime no Brasil
# /vit/br/<crime>
@app.route('/vit/br/<crime>', methods=['GET'])
def getVitBrasil(crime):
  df3_prov = df3.loc[df3['Tipo Crime'] == crime]
  res = df3_prov["Vítimas"].sum()
  return jsonify(int(res))
################################################################

# GET vítimas por Ano
# # /vit/epoc/<ano>
@app.route('/vit/epoc/<ano>', methods=['GET'])
def getVitByAno(ano):
  df1_prov = df1.loc[df1['Ano'] == int(ano)]
  res = df1_prov["Vítimas"].sum()
  return jsonify(int(res))
################################################################
# GET tipos de crime das ocorrencias
# /api/ocorr/crim/tipos
# Aqui ta retornando um array de strings.
@app.route('/ocorr/crim/tipos', methods=['GET'])
def getTiposCrimes():
  res = np.unique(df2['Tipo Crime'])
  a = res.tolist()
  return json.dumps(a)
################################################################

# GET tipos de crime onde há vitimas
# /vit/crim/tipos
@app.route('/vit/crim/tipos', methods=['GET'])
def getTiposCrimes2():
  return json.dumps(np.unique(df3['Tipo Crime']).tolist())
################################################################

# GET ocorrências de um tipo de crime em um estado
# /ocorr/<crime>/<UF>
@app.route('/ocorr/<crime>/<UF>', methods=['GET'])
def getOcorrTipoCrimeEstado(crime, UF):
  df2_prov = df2.loc[df2['Tipo Crime'] == crime]
  df2_prov = df2_prov.loc[df2_prov['UF'] == UF]
  res = df2_prov["Ocorrências"].sum()
  return jsonify(int(res))
################################################################

# GET vítimas de um tipo de crime em um estado 
# /vit/<crime>/<UF>
@app.route('/vit/<crime>/<UF>', methods=['GET'])
def getVitTipoCrimeEstado(crime, UF):
  df3_prov = df3.loc[df3['Tipo Crime'] == crime]
  df3_prov = df3_prov.loc[df3_prov['UF'] == UF]
  res = df3_prov["Vítimas"].sum()
  return jsonify(int(res))
################################################################

# GET vítimas de um tipo de crime por ano 
# /vit/crim/epoc/<crime>/<ano>
@app.route('/vit/crim/epoc/<crime>/<ano>', methods=['GET'])
def getVitTipoCrimeByAno(crime, ano):
  df3_prov = df3.loc[df3['Tipo Crime'] == crime]
  df3_prov = df3_prov.loc[df3_prov['Ano'] == int(ano)]
  res = df3_prov["Vítimas"].sum()
  return jsonify(int(res))
################################################################

# GET ocorrências de um tipo de crime por ano
# /ocorr/crim/epoc/<crime>/<ano>
@app.route('/ocorr/crim/epoc/<crime>/<ano>', methods=['GET'])
def getOcorrTipoCrimeByAno(crime, ano):
  df2_prov = df2.loc[df2['Tipo Crime'] == crime]
  df2_prov = df2_prov.loc[df2_prov['Ano'] == int(ano)]
  res = df2_prov["Ocorrências"].sum()
  return jsonify(int(res))
################################################################

# /max/munc/vit
# GET top 10 municípios com mais vítimas
@app.route('/max/munc/vit', methods=['GET'])
def getTop10VitByCity():
  df1_prov = df1.groupby("Município")["Vítimas"].sum()
  res = df1_prov.nlargest(10).to_json()
  return res

# GET top 10 municípios com menos vítimas
@app.route('/min/munc/vit', methods=['GET'])
def getTop10MinVitByCity():
  df1_prov = df1.groupby("Município")["Vítimas"].sum()
  res = df1_prov.nsmallest(10).to_json()
  return res

# GET top 10 estados com mais vítimas
@app.route('/max/estad/vit', methods=['GET'])
def getMaxEstadVit():
  df1_prov = df1.groupby("Sigla UF")["Vítimas"].sum()
  res = df1_prov.nlargest(10).to_json()
  return res

# GET top 10 estados com menos vítimas
@app.route('/min/estad/vit', methods=['GET'])
def getTop10EstadosMinVit():
  df1_prov = df1.groupby("Sigla UF")["Vítimas"].sum()
  res = df1_prov.nsmallest(10).to_json()
  return res


# GET top 10 estados com mais ocorrências 
@app.route('/max/estad/ocorr', methods=['GET'])
def getTop10EstadosMaisOcorr():
  df2_prov = df2.groupby("UF")["Ocorrências"].sum()
  res = df2_prov.nlargest(10).to_json()
  return res

# GET top 10 estados com menos ocorrências
@app.route('/min/estad/ocorr', methods=['GET'])
def getTop10EstadosMenosOcorr():
  df2_prov = df2.groupby("UF")["Ocorrências"].sum()
  res = df2_prov.nsmallest(10).to_json()
  return res



if __name__ == '__main__':
  app.run()

# Possíveis rotas:
