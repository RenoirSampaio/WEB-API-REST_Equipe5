from flask import Flask, make_response, jsonify, request

app = Flask(__name__)

@app.route('/hello')
def hello():
  return 'Hello World!'

if __name__ == '__main__':
  app.run()