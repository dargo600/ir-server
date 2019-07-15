from datetime import datetime
from config import db, ma

class Device(db.Model):
    __tablename__ = 'device'
    device_id = db.Column(db.Integer, primary_key=True)
    model_num = db.Column(db.String(32))
    manufacturer = db.Column(db.String(32))
    device_type = db.Column(db.String(32))
    remote_config = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DeviceSchema(ma.ModelSchema):
    class Meta:
        model = Device
        sqla_session = db.session

