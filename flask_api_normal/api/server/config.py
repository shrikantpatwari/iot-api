# project/server/config.py

import os
import boto3

basedir = os.path.abspath(os.path.dirname(__file__))
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    REGION = 'us-east-2'
    DEVICES_TABLE_NAME = 'iot-devices'
    DEVICE_SENSORS_TABLE_NAME = 'iot-device-sensors'
    DEVICE_SENSORS_DATA_TABLE_NAME = 'iot-device-sensors-data'
    dynamodb = boto3.client(
        'dynamodb',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION
    )


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    REGION = 'us-east-2'
    DEVICES_TABLE_NAME = 'iot-devices'
    DEVICE_SENSORS_TABLE_NAME = 'iot-device-sensors'
    DEVICE_SENSORS_DATA_TABLE_NAME = 'iot-device-sensors-data'
    dynamodb = boto3.client(
        'dynamodb',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        endpoint_url='http://dynamodb:8000'
    )

class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    REGION = 'us-east-2'
    DEVICES_TABLE_NAME = 'iot-devices'
    DEVICE_SENSORS_TABLE_NAME = 'iot-device-sensors'
    DEVICE_SENSORS_DATA_TABLE_NAME = 'iot-device-sensors-data'
    dynamodb = boto3.client(
        'dynamodb',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION
    )
