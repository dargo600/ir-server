"""
This is the rc buttons module and supports all the ReST actions for the
RC Buttons collection
"""

from flask import make_response, abort
from config import db
from models import RCButton, RCButtonSchema


def read_all():
    """
    This function responds to a request for /api/rcbuttons
    with the complete lists of rcbuttons
    :return:        json string of list of rc_buttons
    """
    # Create the list of rc_buttons from our data
    rc_buttons = RCButton.query.order_by(RCButton.rc_button_id).all()

    # Serialize the data for the response
    rc_button_schema = RCButtonSchema(many=True)
    data = rc_button_schema.dump(rc_buttons).data
    return data


def read_one(rc_button_id):
    """
    This function responds to a request for /api/rc_buttons/{rc_button_id}
    with one matching rc_button from rc_buttons
    :param rc_button_id:   Id of rc_button to find
    :return:            rc_button matching id
    """
    rc_button = RCButton.query\
                        .filter(RCButton.rc_button_id == rc_button_id)\
                        .one_or_none()

    if rc_button is not None:
        # Serialize the data for the response
        rc_button_schema = RCButtonSchema()
        data = rc_button_schema.dump(rc_button).data
        return data
    else:
        abort(404, f"RC_button not found for Id: {rc_button_id}")


def create(rc_button):
    """
    This function creates a new rc_button in the rc_buttons structure
    based on the passed in rc_button data
    :param rc_button:  rc_button to create in rc_buttons structure
    :return:        201 on success, 406 on rc_button exists
    """
    rc_button_type = rc_button.get("rc_type")
    device_config_id = rc_button.get("device_config_id")

    existing_rc_button = (
        RCButton.query.filter(RCButton.rc_type == rc_button_type)
        .filter(RCButton.device_config_id == device_config_id)
        .one_or_none()
    )

    if existing_rc_button is None:
        schema = RCButtonSchema()
        new_rc_button = schema.load(rc_button, session=db.session).data
        db.session.add(new_rc_button)
        db.session.commit()
        data = schema.dump(new_rc_button).data
        return data, 201
    else:
        abort(409,
              f"rc_button {rc_button_type} and {device_config_id} exists already")


def update(rc_button_id, rc_button):
    """
    This function updates an existing rc_button in the rc_button structure
    Throws an error if a rc_button with the name we want to update to
    already exists in the database.
    :param rc_button_id:   Id of the rc_button to update in the people structure
    :param rc_button:      rc_button to update
    :return:            updated rc_button structure
    """
    update_rc_button = RCButton.query\
                                .filter(RCButton.rc_button_id == rc_button_id)\
                                .one_or_none()
    if update_rc_button is not None:
        schema = RCButtonSchema()
        new_update = schema.load(rc_button, session=db.session).data
        new_update.rc_button_id = update_rc_button.rc_button_id
        # merge the new object into the old and commit it to the db
        db.session.merge(new_update)
        db.session.commit()
        data = schema.dump(update_rc_button).data
        return data, 200
    else:
        abort(404, f"rc_button not found for Id: {rc_button_id}")


def delete(rc_button_id):
    """
    This function deletes a rc_button from the rc_button structure
    :param rc_button_id:   Id of the rc_button to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the rc_button requested
    rc_button = RCButton.query.filter(RCButton.rc_button_id == rc_button_id)\
                        .one_or_none()
    if rc_button is not None:
        db.session.delete(rc_button)
        db.session.commit()
        return make_response(f"rc_button {rc_button_id} deleted", 200)
    else:
        abort(404, f"rc_button not found for Id: {rc_button_id}")