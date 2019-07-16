from datetime import datetime
from config import db, ma


class Device(db.Model):
    """ Database associated with the Remote Device Creation

    It may be worth while to prevent certain buttons that are in the csv
    files from being used as they may or may not be used or work.
    eg.: Apple's ext/play seems to do something but not anything useful
    This could be done by adding something like:
    #supported_buttons = db.Column(db.String(32))
    @todo determine how to make a relation between dbs
    #device_config_id = db.Column(db.Integer, db.ForeignKey("device_config.device_config_id"))
    """
    __tablename__ = 'device'
    device_id = db.Column(db.Integer, primary_key=True)
    model_num = db.Column(db.String(32))
    manufacturer = db.Column(db.String(32))
    device_type = db.Column(db.String(32))
    device_config_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DeviceConfig(db.Model):
    __tablename__ = 'device_config'
    device_config_id = db.Column(db.Integer, primary_key=True)
    device_config_name = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class RCButton(db.Model):
    __tablename__ = 'rc_button'
    rc_button_id = db.Column(db.Integer, primary_key=True)
    device_config_id = db.Column(db.Integer, db.ForeignKey("device_config.device_config_id"))
    rc_type = db.Column(db.String, nullable=False)
    rc_ir_code = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class DeviceSchema(ma.ModelSchema):
    class Meta:
        model = Device
        sqla_session = db.session


class DeviceConfigSchema(ma.ModelSchema):
    class Meta:
        model = DeviceConfig
        sqla_session = db.session


class RCButtonSchema(ma.ModelSchema):
    class Meta:
        model = RCButton
        sqla_session = db.session

