#!/usr/bin/python
from flask import Flask
from flask_restful import Resource, Api
from flask import request
from flask.json import jsonify
from flask import render_template
import json
import postgresLibrary as pL
import uuid

from datetime import date, datetime

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

PORT_NUMBER = 8000

app = Flask(__name__)
api = Api(app)

class Index(Resource):
    def get(self):
        # rooms = pL.getRooms()
        # for room in rooms:
        #     print(room)
        #     room['pheripherals'] = pL.getPeripheralsbyRoom(room['uuid'])
        # return rooms
        return app.send_static_file('static/ManagementApp.html')

api.add_resource(Index, '/')


####################################
# Management App API Requirements
####################################

####################################
#            Room Info
####################################

# Get all rooms
@app.route('/api/admin/rooms', methods=['GET', 'POST'])
def getRooms():
    rooms = pL.getRooms()
    for room in rooms:
        print(room)
    return jsonify({'rooms': rooms})

# Get guest by room
@app.route('/api/admin/rooms/<room_uuid>', methods=['GET', 'POST'])
def getGuest(room_uuid):
    guest = pL.getGuestbyRoomUUID(room_uuid)
    print(guest)
    return jsonify({'guest': guest})

####################################
#       Room Service Requests
####################################

# Get all room service requests
@app.route('/api/admin/requests/room-service', methods=['GET', 'POST'])
def getRoomServiceRequests():
    requestsRoomService = pL.getRoomServiceRequests()
    for request in requestsRoomService:
        print(request)
    return jsonify({'Room Servive Requests': requestsRoomService})

# Get a specific room service request given a room service request uuid
@app.route('/api/admin/requests/room-service/<rsreqUUID>', methods=['GET', 'POST'])
def getRoomServiceRequest(rsreqUUID):
    requestRoomService = pL.getRoomServiceRequestbyUUID(rsreqUUID)
    print(requestRoomService)
    return jsonify({'Room Servive Request': requestRoomService})

# Set room service request as completed given a room service request uuid
@app.route('/api/admin/requests/room-service/<rsreqUUID>', methods=['GET', 'POST'])
def completeRoomServiceRequest(rsreqUUID):
    completeRoomSerive = pL.updateRoomServiceRequestCompleted('TRUE', rsreqUUID)
    print(completeRoomSerive)
    return jsonify({'Room Servive Request': pL.getRoomServiceRequestbyUUID(rsreqUUID)})

####################################
#       Maintenace Requests
####################################

# Get all maintenance requests
@app.route('/api/admin/requests/maintenance', methods=['GET', 'POST'])
def getMaintenanceRequests():
    requestsMaintenance = pL.getMaintenanceRequests()
    for request in requestsMaintenance:
        print(request)
    return jsonify({'Maintenance Request': requestsMaintenance})

# Get a specific maintenance request given a maintenance request uuid
@app.route('/api/admin/requests/maintenance/<mreqUUID>', methods=['GET', 'POST'])
def getMaintenanceRequest(mreqUUID):
    requestMaintenance = pL.getMaintenanceRequestbyUUID(mreqUUID)
    print(requestMaintenance)
    return jsonify({'Room Servive Request': requestMaintenance})

# Set maintenance request as completed given a maintenance request uuid
@app.route('/api/admin/requests/maintenance/complete/<mreqUUID>', methods=['GET', 'POST'])
def completeMaintenanceRequest(mreqUUID):
    completeMaintenance = pL.updateMaintenanceRequestCompleted('TRUE', mreqUUID)
    print(completeMaintenance)
    return jsonify({'Maintenance Request': pL.getMaintenanceRequestbyUUID(mreqUUID)})


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=PORT_NUMBER)
