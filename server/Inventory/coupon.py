import psycopg2 as postgre
import jwt
from flask import jsonify

class Coupon:

    def __init__(self) -> None:
        pass

    def connect(self):
        self.con = postgre.connect(database="iftqwlwu",user="iftqwlwu",host="satao.db.elephantsql.com",port="5432",password="sKxhxsNLIblOuhLGBPEiy7O4iXhF1nsP")
        self.cur = self.con.cursor()

    def add(self, decoded):
        try:
            self.cur.execute("SELECT gst_number FROM users WHERE username = %s AND user_password = %s",(decoded['username'], decoded['password']))
            rows = self.cur.fetchone()
            self.table = str("coupon_" + str(rows[0]))
        except Exception as e:
            return "User Not Found"
        
    def checkTable(self):
        self.cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '"+self.table+"')")
        rows = self.cur.fetchall()
        if rows[0][0] != False :
            return True
        else:
            self.cur.execute("CREATE TABLE "+ self.table +"(coupon_id text, percentage int, min_amount int)")
            self.con.commit()
            self.checkTable()
    def addCoupon(self, coupon_id, percentage, min_value):
        try:
            query = "INSERT INTO "+ self.table + "(coupon_id, percentage, min_amount) VALUES('"+ coupon_id +"', "+ percentage +", "+ min_value +" )"
            self.cur.execute(query)
            self.con.commit()
            return True
        except Exception as e:
            return False