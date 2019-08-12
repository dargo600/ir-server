from datetime import datetime
from config import db, ma
from marshmallow import fields


class DeviceConfig(db.Model):
    __tablename__ = 'device_config'
    device_config_id = db.Column(db.Integer, primary_key=True)
    device_config_name = db.Column(db.String(32))
    buttons = db.relationship(
        "RCButton",
        backref="device_config",
        single_parent=True,
        order_by="desc(RCButton.rc_type)",
    )
    devices = db.relationship(
        "Device",
        backref="device_config",
        single_parent=True,
        order_by="desc(Device.model_num)",
    )
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class RCButton(db.Model):
    __tablename__ = 'rc_button'
    device_config_id = db.Column(db.Integer, db.ForeignKey("device_config.device_config_id"))
    rc_button_id = db.Column(db.Integer, primary_key=True)
    rc_type = db.Column(db.String, nullable=False)
    rc_ir_code = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Device(db.Model):
    """
    Database associated with the Remote Device Creation
    """
    __tablename__ = 'device'
    device_id = db.Column(db.Integer, primary_key=True)
    model_num = db.Column(db.String(32))
    manufacturer = db.Column(db.String(32))
    device_type = db.Column(db.String(32))
    device_config_id = db.Column(db.Integer, db.ForeignKey("device_config.device_config_id"))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class DeviceSchema(ma.ModelSchema):
    class Meta:
        model = Device
        sqla_session = db.session


class RCButtonSchema(ma.ModelSchema):
    class Meta:
        model = RCButton
        sqla_session = db.session


class DeviceConfigSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = DeviceConfig
        sqla_session = db.session

    buttons = fields.Nested("DeviceConfigButtonSchema", default=[], many=True)
    devices = fields.Nested("DeviceConfigDeviceSchema", default=[], many=True)


class DeviceConfigButtonSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    device_config_name = fields.Str()
    rc_type = fields.Str()
    rc_ir_code = fields.Str()


class DeviceConfigDeviceSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    device_config_name = fields.Str()
    device_id = fields.Int()
    model_num = fields.Str()
    manufacturer = fields.Str()
    device_type = fields.Str()

