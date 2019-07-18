"""
This is the device configs module and supports all the ReST actions for the
Device Configurations collection
"""

from flask import make_response, abort
from config import db
from models import DeviceConfig, DeviceConfigSchema


def read_all():
    """
    This function responds to a request for /api/devices
    with the complete lists of devices
    :return:        json string of list of devices
    """
    # Create the list of devices from our data
    device_configs = DeviceConfig.query.order_by(DeviceConfig.device_config_id).all()

    # Serialize the data for the response
    device_config_schema = DeviceConfigSchema(many=True)
    data = device_config_schema.dump(device_configs).data
    return data


def read_one(device_config_id):
    """
    This function responds to a request for /api/device_configs/{device_config_id}
    with one matching device config from device_ocnfigs
    :param device_config_id:   Id of device to find
    :return:            device matching id
    """
    device_config =\
        DeviceConfig.query\
                    .filter(DeviceConfig.device_config_id == device_config_id)\
                    .one_or_none()
    if device_config is not None:
        # Serialize the data for the response
        device_config_schema = DeviceConfigSchema()
        data = device_config_schema.dump(device_config).data
        return data
    else:
        abort(404, f"Device Config not found for Id: {device_config_id}")


def create(device_config):
    """
    This function creates a new device config in the device_configs structure
    based on the passed in device config data
    :param device_config:  device_config to create in devices structure
    :return:        201 on success, 406 on device exists
    """
    device_config_name = device_config.get("device_config_name")

    existing_device = (
        DeviceConfig
            .query
            .filter(DeviceConfig.device_config_name == device_config_name)
            .one_or_none()
    )

    if existing_device is None:
        # Create a device config instance using the schema and the passed in device
        schema = DeviceConfigSchema()
        new_device_config = schema.load(device_config, session=db.session).data

        # Add the device_config to the database
        db.session.add(new_device_config)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_device_config).data

        return data, 201
    else:
        abort(409, f"DeviceConfig {device_config_name} exists already")


def update(device_config_id, device_config):
    """
    This function updates an existing device in the devices structure
    Throws an error if a device with the name we want to update to
    already exists in the database.
    :param device_config_id:   Id of the device to update in the people structure
    :param device_config:      device to update
    :return:            updated device structure
    """
    # Get the person requested from the db into session
    update_device_config = DeviceConfig.query.filter(
        DeviceConfig.device_config_id == device_config_id
    ).one_or_none()

    # Try to find an existing device with the same name as the update
    device_config_name = device_config.get("device_config_name")

    existing_device_config = (
        DeviceConfig
            .query
            .filter(DeviceConfig.device_config_name, device_config_name)
            .one_or_none()
    )

    # Are we trying to find a device_config that does not exist?
    if update_device_config is None:
        abort(404, f"Device Config not found for Id: {device_config_id}")
    elif (
        existing_device_config is not None and existing_device_config.device_config_id != device_config_id
    ):
        abort(409, f"Device {device_config_name} exists already")
    else:

        # turn the passed in person into a db object
        schema = DeviceConfigSchema()
        update_device = schema.load(device_config, session=db.session).data

        # Set the id to the device we want to update
        update.device_config_id = update_device.device_config_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_device_config).data

        return data, 200


def delete(device_config_id):
    """
    This function deletes a device from the devices structure
    :param device_config_id:   Id of the device to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the device requested
    device_config = DeviceConfig.query.filter(DeviceConfig.device_config_id == device_config_id).one_or_none()

    # Did we find a person?
    if device_config is not None:
        db.session.delete(device_config)
        db.session.commit()
        return make_response(f"DeviceConfig {device_config_id} deleted", 200)
    else:
        abort(404, f"Device not found for Id: {device_id}")