# REST - IR Server

A REST server in Flask/Python with Swagger for storing pronto hex codes to
avoid code duplication between Apple and Samsung Devices.

To start up:
```text
cd src
docker-compose build
docker-compose up
```
* http://localhost:5000 - alter database
* http://localhost:5000/api/ui - to access swagger interface

## Todo:
- add a field for buttons that don't work?
- add more devices
- add more tests

## Usage

All responses will have the form

```json
{
  "data:": "Mixed type holding the content of the response",
  "message": "Description of what happened"
}
```

Subsequent definitions will only detail the expected value of the data field"

### List of all Device Configs


**Definitions**

`GET /device_configs`

**Response**
- `200 OK` on success

```json
[
  {
    "buttons": [
      {
        "rc_ir_code": "0000 006E 0022 0002 0155 00AC 0015 0015 0015 0041 0015 0041 0015 0041 0015 0015 0015 0041 0015 0041 0015 0041 0015 0041 0015 0041 0015 0041 0015 0015 0015 0015 0015 0015 0015 0015 0015 0041 0015 0041 0015 0041 0015 0015 0015 0041 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0041 0015 0041 0015 0015 0015 05E6 0155 0056 0015 0E45",
        "rc_type": "up"
      },
      {
        "rc_ir_code": "0000 006E 0022 0002 0156 00AC 0015 0015 0015 0041 0015 0041 0015 0041 0015 0015 0015 0041 0015 0041 0015 0041 0015 0041 0015 0041 0015 0041 0015 0015 0015 0015 0015 0015 0015 0015 0015 0041 0015 0041 0015 0015 0015 0041 0015 0041 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0015 0041 0015 0041 0015 0015 0015 05E6 0156 0056 0015 0E45",
        "rc_type": "down"
      }
    ],
    "device": 1,
    "device_config_id": 1,
    "device_config_name": "appleConfig1",
    "timestamp": "2019-07-21T14:44:22.215650+00:00"
  },
  {
    "buttons": [
      {
        "rc_ir_code": "0000 006C 0000 0027 00AC 00AC 0013 0013 0013 0013 0013 0013 0013 0013 0013 003A 0013 003A 0013 0013 0013 0013 0013 003A 0013 003A 0013 003A 0013 003A 0013 0013 0013 0013 0013 0013 0013 0013 0013 00AC 0013 0013 0013 0013 0013 0013 0013 0013 0013 003A 0013 003A 0013 003A 0013 0013 0013 003A 0013 003A 0013 003A 0013 0013 0013 0013 0013 0013 0013 0013 0013 003A 0013 0013 0013 0013 0013 0013 0013 003A 0013 0856",
        "rc_type": "volup"
      },
      {
        "rc_ir_code": "0000 006C 0000 0027 00AC 00AC 0013 0013 0013 0013 0013 0013 0013 0013 0013 003A 0013 003A 0013 0013 0013 0013 0013 003A 0013 003A 0013 003A 0013 003A 0013 0013 0013 0013 0013 0013 0013 0013 0013 00AC 0013 0013 0013 0013 0013 0013 0013 0013 0013 0013 0013 0013 0013 0013 0013 0013 0013 003A 0013 003A 0013 003A 0013 0013 0013 003A 0013 003A 0013 003A 0013 003A 0013 0013 0013 0013 0013 0013 0013 003A 0013 0856",
        "rc_type": "power"
      }
    ],
    "device": null,
    "device_config_id": 2,
    "device_config_name": "samsungConfig2",
    "timestamp": "2019-07-21T14:44:22.222443+00:00"
  }
]
```

### List of all Devices


**Definitions**

`GET /devices`

**Response**
- `200 OK` on success

```json
[
  {
    "device_config": [
      {
        "device_config_id": 1,
        "device_id": 1,
        "timestamp": "2019-07-21 14:44:22.215650"
      }
    ],
    "device_id": 1,
    "device_type": "MediaDevice",
    "manufacturer": "apple",
    "model_num": "v2",
    "timestamp": "2019-07-21T14:44:22.195630+00:00"
  },
  {
    "device_config": [
      {
        "device_config_id": 4,
        "device_id": 2,
        "timestamp": "2019-07-21 14:44:22.227126"
      }
    ],
    "device_id": 2,
    "device_type": "MediaDevice",
    "manufacturer": "roku",
    "model_num": "streamstick",
    "timestamp": "2019-07-21T14:44:22.207500+00:00"
  },
  {
    "device_config": [
      {
        "device_config_id": 3,
        "device_id": 3,
        "timestamp": "2019-07-21 14:44:22.225033"
      }
    ],
    "device_id": 3,
    "device_type": "tv",
    "manufacturer": "samsung",
    "model_num": "ln46C630k1fkxzc",
    "timestamp": "2019-07-21T14:44:22.211588+00:00"
  }
]
```

### Registering a new device

**Definition** 

`POST /devices`

***Arguments***
- `"model_num":string` The model name to identify the product
- `"manufacturer":string` The manufacturer of the device
- `"device_type":string` The type of device, eg: tv, smartTV, mediaDevice
- `"remote_config":string` String to map to /remoteconfig

If a device with the given model and manufacturer already exists it will not
be added.  The primary key consists of model_num and Manufacturer as
model_num may theoretically not be unique.

- `201 Created` on success

```json
  {
    "model_num": "ln46C630k1fkxzc",
    "manufacturer": "samsung",
    "device_type": "tv",
    "remote_config": "samsungConfig1"
  }
```

## Lookup device details

**Definition**

`GET /device/<identifier>`

**Response**

- `404 Not Found` if the device does not exist
- `200 OK` on sucess
```json
  {
    "model_num": "ln46C630k1fkxzc",
    "manufacturer": "samsung",
    "device_type": "tv",
    "remote_config": "samsungConfig1"
  }
```

## Delete a device

**Definition**

`DELETE /devices/<identifier>`

**Response**
- `404 Not Found` if the device does not exist
- `204 No Content` on success

