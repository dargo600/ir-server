import os
from config import db
from models import Device, DeviceConfig, RCButton
from RemoteConfig import RemoteConfiguration, ParsedDeviceConfig, ParsedRCButton

devices_db="devices.db"
ir_config_dir = "ir_dir"

# Delete database file if it exists currently
if os.path.exists(devices_db):
    os.remove(devices_db)
# Create the database
db.create_all()
remote_config = RemoteConfiguration()
remote_config.process_ir_dir(ir_config_dir)
device_configs = remote_config.get_device_configs()

added_configs = {}
for key, parsed_config in device_configs.items():
    p = DeviceConfig(device_config_name=key)
    buttons = parsed_config.get_buttons()
    for button in buttons:
        p.buttons.append(RCButton(rc_type=button.button_type,
                                  rc_ir_code=button.pronto_code))
    db.session.add(p)
    added_configs[key] = p

devices = remote_config.get_devices()
for device in devices:
    device_config = added_configs[device.remote_config]
    p = Device(model_num=device.model_num,
               manufacturer=device.manufacturer,
               device_type=device.device_type)
    p.device_config.append(device_config)
    db.session.add(p)


db.session.commit()
