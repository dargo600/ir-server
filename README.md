# REST - IR Server

A REST server in Flask/Python with Swagger for storing pronto hex codes to avoid code duplication between Apple and Samsung Devices.

To start up:
```text
docker-compose build
docker-compose up
```
* http://localhost:5000 - alter database
* http://localhost:5000/api/ui - to access swagger interface

## Usage

All responses will have the form

```json
{
  "data:": "Mixed type holding the content of the response",
  "message": "Description of what happened"
}
```

Subsequent definitions will only detail the expected value of the data field"

### List of all Devices


**Definitions**

`GET /devices`

**Response**
- `200 OK` on success

```json
{
  {
    "model_num": "ln46C630k1fkxzc",
    "manufacturer": "samsung",
    "device_type": "tv",
    "remote_config": "samsungConfig1"
  },
  {
    "model_num": "v2",
    "manufacturer": "apple",
    "device_type": "apple-tv",
    "remote_config": "appleTVConfig1" 
  },
}
```

### Registering a new device

**Definition** 

`POST /devices`

***Arguments***
- `"model_num":string` The model name to identify the product
- `"manufacturer":string` The manufacturer of the device
- `"device_type":string` The type of device, eg: tv, smartTV, mediaDevice
- `"remote_config":string` String to map to /remoteconfig

If a device with the given model and manufacturer already exists it will not be added.  The primary key consists of model_num and Manufacturer as model_num may theoretically not be unique.

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

