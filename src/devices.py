"""
This is the devices module and supports all the ReST actions for the
Devices collection
"""

from flask import make_response, abort
from config import db
from models import Device, DeviceSchema


def read_all():
    """
    This function responds to a request for /api/devices
    with the complete lists of devices
    :return:        json string of list of devices
    """
    devices = Device.query.order_by(Device.manufacturer).all()
    device_schema = DeviceSchema(many=True)
    data = device_schema.dump(devices).data
    return data


def read_one(device_id):
    """
    This function responds to a request for /api/devices/{device_id}
    with one matching device from devices
    :param device_id:   Id of device to find
    :return:            device matching id
    """
    device = Device.query.filter(Device.device_id == device_id).one_or_none()
    if device is not None:
        device_schema = DeviceSchema()
        data = device_schema.dump(device).data
        return data
    else:
        abort(404, f"Device not found for Id: {device_id}")


def create(device):
    """
    This function creates a new device in the devices structure
    based on the passed in device data
    :param device:  device to create in devices structure
    :return:        201 on success, 406 on device exists
    """
    model_num = device.get("model_num")
    manufacturer = device.get("manufacturer")
    existing_device = (
        Device.query.filter(Device.model_num == model_num)
        .filter(Device.manufacturer == manufacturer)
        .one_or_none())
    if existing_device is None:
        schema = DeviceSchema()
        new_device = schema.load(device, session=db.session).data
        db.session.add(new_device)
        db.session.commit()
        data = schema.dump(new_device).data
        return data, 201
    else:
        abort(409, f"Device {model_num} {manufacturer} exists already")


def update(device_id, device):
    """
    This function updates an existing device in the devices structure
    Throws an error if a device with the name we want to update to
    already exists in the database.
    :param device_id:   Id of the device to update in the people structure
    :param device:      device to update
    :return:            updated device structure
    """
    update_device = Device.query\
        .filter(Device.device_id == device_id).one_or_none()
    model_num = device.get("model_num")
    manufacturer = device.get("manufacturer")
    existing_device = Device.query\
        .filter(Device.model_num == model_num)\
        .filter(Device.manufacturer == manufacturer)\
        .one_or_none()
    if update_device is None:
        abort(404, f"Device not found for Id: {device_id}")
    elif (existing_device is not None and
          existing_device.device_id != device_id):
        abort(409, f"Device {model_num} {manufacturer} exists already")
    else:
        schema = DeviceSchema()
        new_device = schema.load(device, session=db.session).data
        new_device.device_id = update_device.device_id
        db.session.merge(new_device)
        db.session.commit()
        data = schema.dump(update_device).data
        return data, 200


def delete(device_id):
    """
    This function deletes a device from the devices structure
    :param device_id:   Id of the device to delete
    :return:            200 on successful delete, 404 if not found
    """
    device = Device.query.filter(Device.device_id == device_id).one_or_none()
    if device is not None:
        db.session.delete(device)
        db.session.commit()
        return make_response(f"Device {device_id} deleted", 200)
    else:
        abort(404, f"Device not found for Id: {device_id}")
