from flask import Flask
from flask_cors import CORS

from source.Invoice_details import Invoice
from source.utilities import utilities

app = Flask(__name__)

@app.route("/")
def home():
   return "POS Backend"

@app.route("/invoices", methods=['POST', 'PUT', 'GET', 'DELETE'])
def Invoice_detail():
   return Invoice()

@app.route("/utilities", methods=['POST', 'PUT', 'GET', 'DELETE'])
def util():
   return utilities()

CORS(app)


if __name__ == '__main__':
    app.run(debug=True, port=9005, host="0.0.0.0")