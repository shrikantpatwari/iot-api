## Table defination

<code>

    // device
    {
        // device ID
        deviceId: uuid()
        // device name
        deviceName: string
        // list of sid associated with device
        sensors: []
        // user id who added device
        userId: forain_key_uid
        // created at timestamp
        createdAt: timestamp
        // updated at timestamp
        updatedAt: timestamp
    }

    // sensors
    {
        // sensor ID
        sensorId: uuid()
        // type of sensor
        type: string
        // name of sensor
        name: string
        // created at timestamp
        createdAt: timestamp
        // updated at timestamp
        updatedAt: timestamp
    }

    // device_sensors_data
    {
        // device id
        deviceId: forain_key_did-compositeKey
        // sensor id
        sensorId: forain_key_sid-compositeKey
        // time data
        timeKey: timestamp-primary_key
        // actual data
        data: string
        // created at timestamp
        createdAt: timestamp
        // updated at timestamp
        updatedAt: timestamp
    }

    // user
    {
        // user email
        email: string
        // user password
        password: string
        // user name
        name: string
        // created at timestamp
        createdAt: timestamp
        // updated at timestamp
        updatedAt: timestamp
    }
</code>