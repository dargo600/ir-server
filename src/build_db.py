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
rc_buttons = remote_config.get_rc_buttons()
rc_configs = remote_config.get_remote_control_configs()
devices = remote_config.get_device_configs()

for key,value in rc_configs.items():
    print(f'Inserting into device config {value} {key}')
    p = DeviceConfig(device_config_id=value,
                     device_config_name=key)
    db.session.add(p)

for button in rc_buttons:
    print(f'Inserting into rc_buttons {button.config_index}, {button.button_type}')
    p = RCButton(device_config_id=button.config_index,
                 rc_type=button.button_type,
                 rc_ir_code=button.pronto_code)
    db.session.add(p)

# Iterate over the DEVICES structure and populate the database
for device in devices:
    print(f'Inserting into device {device.model_num}, {device.manufacturer},'
          f'{device.remote_config}, {rc_configs[device.remote_config]}')
    p = Device(model_num=device.model_num,
               manufacturer=device.manufacturer,
               device_type=device.device_type,
               device_config_id=rc_configs[device.remote_config])
    db.session.add(p)


db.session.commit()
