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
devices = remote_config.get_devices()

devices_added = 0
added_configs = {}
for key, parsed_config in device_configs.items():
    p = DeviceConfig(device_config_name=key)
    buttons = parsed_config.get_buttons()
    for button in buttons:
        p.buttons.append(RCButton(rc_type=button.button_type,
                                  rc_ir_code=button.pronto_code))
    arr = []
    if key in devices:
        arr = devices[key]
    else:
        print(f'{key} no device uses this config')
    for device in arr:
        p.devices.append(Device(model_num=device.model_num,
                                manufacturer=device.manufacturer,
                                device_type=device.device_type))
        devices_added = devices_added + 1
    db.session.add(p)

if devices_added == 0:
    raise Exception('devices is at 0 for some reason')

db.session.commit()
