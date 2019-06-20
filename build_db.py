import os
from config import db
from models import Device

# Data to initialize database with
DEVICES = [
    { "model_num": "ln46C630k1fkxzc", "manufacturer": "samsung", "device_type": "tv", "remote_config": "samsungConfig1"},
    { "model_num": "v2", "manufacturer": "apple", "device_type": "MediaDevice", "remote_config": "appleConfig1"},
]

# Delete database file if it exists currently
if os.path.exists('devices.db'):
    os.remove('devices.db')

# Create the database
db.create_all()

# Iterate over the DEVICES structure and populate the database
for device in DEVICES:
    p = Device(model_num=device['model_num'], manufacturer=device['manufacturer'], device_type=device['device_type'], remote_config=device['remote_config'])
    db.session.add(p)

db.session.commit()
