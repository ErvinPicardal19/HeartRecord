from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_jwt_extended import create_access_token, jwt_required
import json
import datetime


def getHeartData():
    with open('./heart.json', 'r') as readData:
        heartData = json.load(readData)

        return heartData
    
def writeNewRecord(heartData):
    with open('./heart.json', 'w') as writeData:
        writeData.write(json.dumps(heartData))
    

class HeartRate(Resource):
    def get(self):
        heartData = getHeartData()
        
        return make_response({"data": heartData}, 200)
    
    @jwt_required()
    def post(self):
        body = request.get_json().get("heart_rate")
        heartData = getHeartData()
        
        if (body == None or body == ''): return make_response({"message": "Please provide heart rate data"}, 400)
        
        id = 1 if len(heartData) <= 0 else heartData[-1].get("id") + 1
        
        newRecord = {
            "id": id,
            "heart_rate": body,
            "date": str(datetime.datetime.today())
        }
        
        heartData.append(newRecord)
        
        writeNewRecord(heartData)
        
        return make_response({"success": True, "data": heartData}, 200)
    
class HeartRateSingle(Resource):
    
    def get(self, id):
        
        heartData = getHeartData()
        
        foundRecord = ''
        
        for data in heartData:
            if data.get("id") == int(id):
                foundRecord = data
               
        if foundRecord == '': return make_response({"success": False, "message": "Record does not exist"}, 404)
        
        return make_response({"success": True, "data": foundRecord}, 200)
    
    @jwt_required()
    def patch(self, id):
        
        body = request.get_json()
        
        heartData = getHeartData()
        
        foundRecord = ''
        
        for data in heartData:
            if data.get("id") == int(id):
                foundRecord = data
               
        if foundRecord == '': return make_response({"success": False, "message": "Record does not exist"}, 404)

        foundRecord["heart_rate"] = body.get("heart_rate")
        
        writeNewRecord(heartData)
        
        return make_response({"success": True, "data": heartData}, 200)
    
    @jwt_required()
    def delete(self, id):
        
        heartData = getHeartData()
        
        filterRecord = []
        
        for data in heartData:
            if data.get("id") != int(id):
                filterRecord.append(data)
                
        heartData = filterRecord
        
        writeNewRecord(heartData)
        
        return make_response({"success": True, "data": heartData}, 200)
    

class Login(Resource):
    def post(self):
        body = request.get_json()
        
        username = body.get("username")
        
        if(username == None or username == ''): return make_response({"success": False, "message": "Please provide credentials"}, 400)
        
        if(username != "admin"): return make_response({"success": False, "message": "Invalid Username"}, 400)
        
        expiration = datetime.timedelta(days=1)
        accessToken = create_access_token(identity=username, expires_delta=expiration)
        
        return make_response({"success": True, "accessToken": accessToken.decode("utf-8")}, 200)
    