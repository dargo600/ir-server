/*
 * JavaScript file for the application to demonstrate
 * using the API
 */

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/devices',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(device) {
            let ajax_options = {
                type: 'POST',
                url: 'api/devices',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(device)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(device) {
            let ajax_options = {
                type: 'PUT',
                url: `api/devices/${device.device_id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(device)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(device_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `api/devices/${device_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $device_id = $('#device_id'),
        $model_num = $('#model_num'),
        $manufacturer = $('#manufacturer'),
        $device_type = $('#device_type'),
        $remote_config = $('#remote_config');

    // return the API
    return {
        reset: function() {
            $device_id.val('');
            $manufacturer.val('');
            $device_type.val('');
            $remote_config.val('');
            $model_num.val('').focus();
        },
        update_editor: function(device) {
            $device_id.val(device.device_id);
            $model_num.val(device.model_num).focus();
            $manufacturer.val(device.manufacturer);
            $device_type.val(device.device_type);
            $remote_config.val(device.remote_config);
        },
        build_table: function(devices) {
            let rows = ''

            // clear the table
            $('.devices table > tbody').empty();

            // did we get a devices array?
            if (devices) {
                for (let i=0, l=devices.length; i < l; i++) {
                    rows += `<tr data-device-id="${devices[i].device_id}">
                        <td class="model_num">${devices[i].model_num}</td>
                        <td class="manufacturer">${devices[i].manufacturer}</td>
                        <td class="device_type">${devices[i].device_type}</td>
                        <td class="remote_config">${devices[i].remote_config}</td>
                        <td>${devices[i].timestamp}</td>
                    </tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $device_id = $('#device_id'),
        $manufacturer = $('#manufacturer'),
        $device_type = $('#device_type'),
        $remote_config = $('#remote_config'),
        $model_num = $('#model_num');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(model_num, manufacturer, device_type, remote_config) {
        return model_num !== "" && manufacturer !== "" && device_type !== "" && remote_config !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let manufacturer = $manufacturer.val(),
            device_type = $device_type.val(),
            remote_config = $remote_config.val(),
            model_num = $model_num.val();

        e.preventDefault();

        if (validate(manufacturer, model_num, device_type, remote_config)) {
            model.create({
                'model_num': model_num,
                'manufacturer': manufacturer,
                'device_type': device_type,
                'remote_config': remote_config,
            })
        } else {
            alert('Problem with Manufacturer, Model, Device Type or Remote Configuration input');
        }
    });

    $('#update').click(function(e) {
        let device_id = $device_id.val(),
            manufacturer = $manufacturer.val(),
            remote_config = $remote_config.val(),
            device_type = $device_type.val(),
            model_num = $model_num.val();

        e.preventDefault();

        if (validate(manufacturer, model_num, device_type, remote_config)) {
            model.update({
                device_id: device_id,
                model_num: model_num,
                manufacturer: manufacturer,
                device_type: device_type,
                remote_config: remote_config,
            })
        } else {
            alert('Problem with Manufacturer, Model, Device Type or Remote Configuration input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let device_id = $device_id.val();

        e.preventDefault();

        if (validate('placeholder', manufacturer)) {
            model.delete(device_id)
        } else {
            alert('Problem with Manufacturer, Model, Device Type or Remote Configuration input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            device_id,
            manufacturer,
            device_type,
            remote_config,
            model_num;

        device_id = $target
            .parent()
            .attr('data-device-id');

        model_num = $target
            .parent()
            .find('td.model_num')
            .text();

        manufacturer = $target
            .parent()
            .find('td.manufacturer')
            .text();

        remote_config = $target
            .parent()
            .find('td.remote_config')
            .text();

        device_type = $target
            .parent()
            .find('td.device_type')
            .text();

        view.update_editor({
            device_id: device_id,
            model_num: model_num,
            manufacturer: manufacturer,
            remote_config: remote_config,
            device_type:device_type,
        });
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));