from flask import Flask, request,jsonify
import json
from bson import json_util
from bson.objectid import ObjectId
from pymongo import Connection
import time
import datetime
from sqlalchemy import create_engine
import mysql.connector
#import MYSQLdb
 
# Flask
app = Flask(__name__)
 


conn = mysql.connector.connect(user='root', password='tiny',host='127.0.0.1',database='shop')
cursor=conn.cursor()	


# MongoDB connection
connection = Connection('localhost', 27017)
db = connection.shopping
def toJson(data):
	return json.dumps(data, default=json_util.default)
 
@app.route('/shirt/<shirtid>', methods=['GET'])
def getData(shirtid):
	if request.method == 'GET':
		results = db['shop'].find({"shirtId":shirtid})
		json_results = []
		for result in results:
			json_results.append(result)
		return toJson(json_results)


@app.route('/shirts', methods=['POST'])
def insertData():
	if request.method == 'POST':
		data = request.get_json(request.data);
		shirtid=request.get_json().get('shirtId','');
		tstamp = time.time()
		sysdate = datetime.datetime.fromtimestamp(tstamp).strftime('%Y-%m-%d %H:%M:%S')
		db['shop'].insert(data)
		db['shop'].update({"shirtId":shirtid},{"$set":{"createdBy":sysdate}})
		return request.data

@app.route('/shirts', methods=['PUT'])
def updateData():
	if request.method == 'PUT':
		data = request.get_json(request.data);
		shirtid=request.get_json().get('shirtId', '')
		#db['productcollection'].insert(data)
		db['shop'].update({"shirtId":shirtid},{"$set":data})
		return shirtid

@app.route('/shirts', methods=['DELETE'])
def deleteData():
	if request.method == 'DELETE':
		data = request.get_json(request.data);
		shirtid=request.get_json().get('shirtId', '')
		#db['productcollection'].insert(data)
		db['shop'].remove({"shirtId":shirtid})
		return shirtid

#sql query ad conn
@app.route('/shoes/<shoeId>', methods=['GET'])
def getdata(shoeId):
	print request.method
	if request.method == 'GET':
		addshoe = "SELECT shoeId,shoeName,shoeQuantity,createdBy FROM shoe_tbl WHERE shoeId='%s'" %(shoeId)
		cursor.execute(addshoe)
		columns = [desc[0] for desc in cursor.description]
		rows=cursor.fetchall()
		print rows
		result = []
		result_laa = []
		for row in rows:
			row = dict(zip(columns, row))
        	result.append(row)
		#shoeId = row[0]
		#sho
		#jsonify(rows)
		conn.commit()
		#conn.close()
		result_laa=result
		return json.dumps(result_laa)


@app.route('/shoes', methods=['POST'])	
def insdata():
	if request.method == 'POST':
		data = request.get_json(request.data);
		shoeId=request.get_json().get('shoeId','');
		shoeName=request.get_json().get('shoeName','');
		shoeQuantity=request.get_json().get('shoeQuantity','');
		ts = time.time()
		sysdate = unicode(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
		datashoe=(shoeId,shoeName,shoeQuantity);
		#temp="INSERT INTO shoe(shoeid,shoename,shoequantity) VALUES (%d, '%s', %d)" %(shoeId,shoeName,shoeQuantity) 
		#cursor.execute("INSERT INTO shoe(shoeid,shoename,shoequantity) VALUES (%d, %s, %d)" %(shoeId,shoeName,shoeQuantity))
		addshoe = ("INSERT INTO shoe_tbl"
							"(shoeId,shoeName,shoeQuantity,createdBy) "
							"VALUES (%s, %s, %s,%s)")
		datashoe = (shoeId,shoeName,shoeQuantity,sysdate)
		cursor.execute(addshoe,datashoe)
		conn.commit()
		#conn.close()
		return "OK"


@app.route('/shoes', methods=['PUT'])
def updata():
	if request.method == 'PUT':
		data = request.get_json(request.data);
		shoeId=request.get_json().get('shoeId','');
		shoeName=request.get_json().get('shoeName','');
		shoeQuantity=request.get_json().get('shoeQuantity','');
		ts = time.time()
		sysdate = unicode(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
		datashoe=(shoeId,shoeName,shoeQuantity);
		#temp="INSERT INTO shoe(shoeid,shoename,shoequantity) VALUES (%d, '%s', %d)" %(shoeId,shoeName,shoeQuantity) 
		#cursor.execute("INSERT INTO shoe(shoeid,shoename,shoequantity) VALUES (%d, %s, %d)" %(shoeId,shoeName,shoeQuantity))
		addshoe = ("UPDATE shoe_tbl SET"
							" shoeName=%s,shoeQuantity=%s,createdBy=%s "
							"WHERE shoeId=%s")
		datashoe = (shoeName,shoeQuantity,sysdate,shoeId)
		cursor.execute(addshoe,datashoe)
		conn.commit()
		#conn.close()
		return "OK"


@app.route('/shoes', methods=['DELETE'])
def dedata():
	if request.method == 'DELETE':
		data = request.get_json(request.data);
		shoeId=request.get_json().get('shoeId','');
		shoeName=request.get_json().get('shoeName','');
		shoeQuantity=request.get_json().get('shoeQuantity','');
		ts = time.time()
		sysdate = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		datashoe=(shoeId,shoeName,shoeQuantity);
		#temp="INSERT INTO shoe(shoeid,shoename,shoequantity) VALUES (%d, '%s', %d)" %(shoeId,shoeName,shoeQuantity) 
		#cursor.execute("INSERT INTO shoe(shoeid,shoename,shoequantity) VALUES (%d, %s, %d)" %(shoeId,shoeName,shoeQuantity))
		addshoe = "DELETE FROM shoe_tbl WHERE shoeId='%s'" %(shoeId)
		#datashoe = ()
		cursor.execute(addshoe)
		conn.commit()
		conn.close()
		return (addshoe)

if __name__ == '__main__':
	app.run(port=5000,debug=True)