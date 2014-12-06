from flask import Flask, request,jsonify
import json
from bson import json_util
from bson.objectid import ObjectId
from pymongo import Connection
import time
import datetime
from sqlalchemy import create_engine
import mysql.connector
 
# Flask
app = Flask(__name__)
 


conn = mysql.connector.connect(user='root', password='password',host='127.0.0.1',database='storeapi')
cursor=conn.cursor()	



# MongoDB connection
connection = Connection('localhost', 27017)
db = connection.store
def toJson(data):
	return json.dumps(data, default=json_util.default)
 
@app.route('/shirt/<shirtid>', methods=['GET'])
def getData(shirtid):
	if request.method == 'GET':
		results = db['productcollection'].find({"shirtId":shirtid})
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
		db['productcollection'].insert(data)
		db['productcollection'].update({"shirtId":shirtid},{"$set":{"createdBy":sysdate}})
		return request.data

@app.route('/shirts', methods=['PUT'])
def updateData():
	if request.method == 'PUT':
		data = request.get_json(request.data);
		shirtid=request.get_json().get('shirtId', '')
		#db['productcollection'].insert(data)
		db['productcollection'].update({"shirtId":shirtid},{"$set":data})
		return shirtid

@app.route('/shirts', methods=['DELETE'])
def deleteData():
	if request.method == 'DELETE':
		data = request.get_json(request.data);
		shirtid=request.get_json().get('shirtId', '')
		#db['productcollection'].insert(data)
		db['productcollection'].remove({"shirtId":shirtid})
		return shirtid





@app.route('/shoes/<shoeid>', methods=['GET'])
def getdata(shoeid):
	if request.method == 'GET':
		addshoe = "SELECT shoeid,shoename,shoeQuantity,createdBy FROM shoe WHERE shoeid='%s'" %(shoeid)

		cursor.execute(addshoe)
		rows=cursor.fetchall()
		rowarray_list = []
		#for row in rows:
		#	t = (row.shoeid, row.shoename, row.shoeQuantity, row.createdBy) 
		#	rowarray_list.append(t)
		j = jsonify(rows)
		conn.commit()
		conn.close()
		return rows


@app.route('/shoes', methods=['POST'])
def insdata():
	if request.method == 'POST':
		data = request.get_json(request.data);
		shoeId=request.get_json().get('shoeId','');
		shoeName=request.get_json().get('shoeName','');
		shoeQuantity=request.get_json().get('shoeQuantity','');
		ts = time.time()
		sysdate = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		datashoe=(shoeId,shoeName,shoeQuantity);
		#temp="INSERT INTO shoe(shoeid,shoename,shoequantity) VALUES (%d, '%s', %d)" %(shoeId,shoeName,shoeQuantity) 
		#cursor.execute("INSERT INTO shoe(shoeid,shoename,shoequantity) VALUES (%d, %s, %d)" %(shoeId,shoeName,shoeQuantity))
		addshoe = ("INSERT INTO shoe"
							"(shoeid,shoename,shoequantity,createdBy) "
							"VALUES (%s, %s, %s,%s)")
		datashoe = (shoeId,shoeName,shoeQuantity,sysdate)
		cursor.execute(addshoe,datashoe)
		conn.commit()
		conn.close()
		return "OK"


@app.route('/shoes', methods=['PUT'])
def updata():
	if request.method == 'PUT':
		data = request.get_json(request.data);
		shoeId=request.get_json().get('shoeId','');
		shoeName=request.get_json().get('shoeName','');
		shoeQuantity=request.get_json().get('shoeQuantity','');
		ts = time.time()
		sysdate = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		datashoe=(shoeId,shoeName,shoeQuantity);
		#temp="INSERT INTO shoe(shoeid,shoename,shoequantity) VALUES (%d, '%s', %d)" %(shoeId,shoeName,shoeQuantity) 
		#cursor.execute("INSERT INTO shoe(shoeid,shoename,shoequantity) VALUES (%d, %s, %d)" %(shoeId,shoeName,shoeQuantity))
		addshoe = ("UPDATE shoe SET"
							" shoename=%s,shoequantity=%s,createdBy=%s "
							"WHERE shoeid=%s")
		datashoe = (shoeName,shoeQuantity,sysdate,shoeId)
		cursor.execute(addshoe,datashoe)
		conn.commit()
		conn.close()
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
		addshoe = "DELETE FROM shoe WHERE shoeid='%s'" %(shoeId)
		#datashoe = ()
		cursor.execute(addshoe)
		conn.commit()
		conn.close()
		return (addshoe)


#def updateData(product_id):
#	if request.method == 'PUT':
#		data = request.get_json(request.data);
#		db['productcollection'].update({"price":product_id},{"$set":{"Brand":"Samsung"}})
#		return toJson(data)



 
if __name__ == '__main__':
	app.run(port=8080,debug=True)