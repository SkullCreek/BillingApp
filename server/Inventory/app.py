from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import jwt
import psycopg2 as postgre
import MultipleProduct

app = Flask(__name__)
CORS(app)

@app.route('/addproduct', methods=['POST'])
def add_product():
    # file = request.files['excel_file']
    # df = pd.read_excel(file)
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        decoded = {}
        try:
            decoded = jwt.decode(token, "123", algorithms=["HS256"])
            
        except Exception as e:
            print(e.args)
            return jsonify('Invalid or expired token.'), 401
        
        file = request.files['excel_file']
        df = pd.read_excel(file)
        required_columns = ['pname', 'sku', 'stock', 'price', 'image', 'category']
        for col in required_columns:
            if col not in df.columns:
                return jsonify('Invalid file format.'), 404
        else:
            con = postgre.connect(database="iftqwlwu",user="iftqwlwu",host="satao.db.elephantsql.com",port="5432",password="sKxhxsNLIblOuhLGBPEiy7O4iXhF1nsP")
            cur = con.cursor()
            cur.execute("SELECT gst_number FROM users WHERE username = %s AND user_password = %s",(decoded['username'], decoded['password']))
            rows = cur.fetchone()
            table = str(request.form['branch']) + "_" + str(rows[0])
            cur.close()
            con.close()
            
            a = MultipleProduct.AddProduct()
            if a.connect():
                if a.store(table,df):
                    a.close()
                    return jsonify("Success")
                else:
                    return jsonify("Not able to store")
            else:
                return jsonify("Connection Error")

        
    else:
        return jsonify('Missing or invalid Authorization header.'), 401

if __name__ == '__main__':
    app.run()