from datetime import datetime
from config import db, ma
from marshmallow import fields

class Device(db.Model):
    """ Database associated with the Remote Device Creation

    It may be worth while to prevent certain buttons that are in the csv
    files from being used as they may or may not be used or work.
    eg.: Apple's ext/play seems to do something but not anything useful
    This could be done by adding something like:
    #supported_buttons = db.Column(db.String(32))
    """
    __tablename__ = 'device'
    device_id = db.Column(db.Integer, primary_key=True)
    model_num = db.Column(db.String(32))
    manufacturer = db.Column(db.String(32))
    device_type = db.Column(db.String(32))
    device_config = db.relationship("DeviceConfig",backref="device")
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class DeviceConfig(db.Model):
    __tablename__ = 'device_config'
    device_config_id = db.Column(db.Integer, primary_key=True)
    device_config_name = db.Column(db.String(32))
    device_id = db.Column(db.Integer, db.ForeignKey("device.device_id"))
    buttons = db.relationship(
        "RCButton",
        backref="device_config",
        single_parent=True,
        order_by="desc(RCButton.rc_type)",
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


class DeviceSchema(ma.ModelSchema):
    class Meta:
        model = Device
        sqla_session = db.session
    device_config = fields.Nested("DeviceDeviceConfigSchema", default=[], many=True)


class DeviceButtonSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    device_config_id = fields.Int()
    device_config_name = fields.Str()
    device_id = fields.Int()
    rc_button_id = fields.Int()
    rc_type = fields.Str()
    rc_ir_code = fields.Str()


class DeviceDeviceConfigSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    rc_button_id = fields.Int()
    rc_type = fields.Str()
    rc_ir_code = fields.Str()
    device_id = fields.Int()
    device_config_id = fields.Int()
    timestamp = fields.Str()


class DeviceConfigSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)
    class Meta:
        model = DeviceConfig
        sqla_session = db.session
    buttons = fields.Nested("DeviceConfigButtonSchema", default=[], many=True)


class DeviceConfigButtonSchema(ma.ModelSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    device_config_id = fields.Int()
    rc_button_id = fields.Int()
    rc_button_type = fields.Str()
    device_config_name = fields.Str()
    rc_ir_code = fields.Str()
    timestamp = fields.Str()

class RCButtonSchema(ma.ModelSchema):
    class Meta:
        model = RCButton
        sqla_session = db.session

