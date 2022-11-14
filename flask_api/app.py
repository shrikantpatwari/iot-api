import os
import uuid
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key
from flask import jsonify, request
from flask_lambda import FlaskLambda

EXEC_ENV = os.environ['EXEC_ENV']
REGION = os.environ['REGION_NAME']
DEVICES_TABLE_NAME = os.environ['DEVICES_TABLE_NAME']
DEVICE_SENSORS_TABLE_NAME = os.environ['DEVICE_SENSORS_TABLE_NAME']
DEVICE_SENSORS_DATA_TABLE_NAME = os.environ['DEVICE_SENSORS_DATA_TABLE_NAME']


app = FlaskLambda(__name__)

if EXEC_ENV == 'local':
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://dynamodb:8000')
else:
    dynamodb = boto3.resource('dynamodb', region_name=REGION)


def db_table(table_name=DEVICES_TABLE_NAME):
    return dynamodb.Table(table_name)


def parse_user_id(req):
    '''this will parse and decode token to get user identification'''
    return req.headers['Authorization'].split()[1]

def create_sensor(name, type):
    sensorId = str(uuid.uuid4())
    tbl = db_table(DEVICE_SENSORS_TABLE_NAME)
    tbl.put_item(Item={
        "sensorId": {
            "S": sensorId
        },
        "sensorName": {
            "S": name
        },
        "sensorType": {
            "S": type
        },
        "createdAt": {
            "N": datetime.utcnow().timestamp() * 1000
        },
        "updatedAt": {
            "N": datetime.utcnow().timestamp() * 1000
        }
    })
    return sensorId


@app.route('/devices')
def get_devices():
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    tbl_response = db_table(DEVICES_TABLE_NAME).query(KeyConditionExpression=Key('userId').eq(user_id))
    return jsonify(tbl_response['Items'])


@app.route('/device', methods=('POST',))
def create_device():
    deviceId = str(uuid.uuid4())
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    tempSensorId = create_sensor('temp_sensor', 'TEMP')
    pressureSensorId = create_sensor('pressure_sensor', 'PRESSURE')
    device_data = request.get_json()
    createdAt = datetime.utcnow().timestamp() * 1000
    device_data.update(userId=user_id, deviceId=deviceId, sensors=[tempSensorId, pressureSensorId], createdAt=createdAt, updatedAt=createdAt)
    tbl = db_table()
    tbl.put_item(Item=device_data)
    tbl_response = tbl.get_item(Key={'userId': user_id, 'deviceId': deviceId})
    return jsonify(tbl_response['Item']), 201


@app.route('/device/<string:device_id>', methods=('PUT',))
def update_device(device_id):
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    device_data = {k: {'Value': v, 'Action': 'PUT'}
                for k, v in request.get_json().items()}
    tbl_response = db_table().update_item(Key={'userId': user_id, 'deviceId': device_id},
                                          AttributeUpdates=device_data)
    tbl_response = db_table().get_item(Key={'userId': user_id, 'deviceId': device_id})
    return jsonify(tbl_response['Item'])


@app.route('/device/<string:device_id>/sensor/<string:sensor_id>', methods=('POST',))
def add_sensor_data(device_id, sensor_id):
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    reqParam = request.get_json()
    sensorDataItem = {
        "sensorId": {
            "S": sensor_id
        },
        "deviceId": {
            "S": device_id
        },
        "timeKey": {
            "N": reqParam['timeKey']
        },
        "data": {
            "S": reqParam['data']
        },
        "createdAt": {
            "N": datetime.utcnow().timestamp() * 1000
        },
        "updatedAt": {
            "N": datetime.utcnow().timestamp() * 1000
        }
    }
    tbl = db_table(DEVICE_SENSORS_DATA_TABLE_NAME)
    tbl.put_item(Item=sensorDataItem)
    tbl_response = tbl.get_item(Key={'time_key': reqParam['timeKey'], 'deviceId': device_id, 'sensorId': sensor_id})
    return jsonify(tbl_response['Item']), 200


@app.route('/device/sensor/data', methods=('POST',))
def get_sensor_data():
    try:
        user_id = parse_user_id(request)
    except:
        return jsonify('Unauthorized'), 401

    try:
        reqParam = request.get_json()
        result = db_table(DEVICE_SENSORS_DATA_TABLE_NAME).query(KeyConditionExpression=(Key('sensorId').eq(reqParam['sensorId']) & Key('deviceId').eq(reqParam['deviceid']) & Key('timeKey').between(reqParam['start_time_key'], reqParam['end_time_key'])))
        return jsonify(result['Items'])
    except:
        return jsonify({'error': True, 'msg': 'something went wrong'})
