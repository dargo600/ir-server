import os
import csv


class ParsedRCButton:
    """
    Parsed Remote Control Button Configurations shows which buttons a specific
    file uses and which Remote Configuration it is associated with
    """
    def __init__(self, config_index, button_type, pronto_code):
        self.config_index = config_index
        self.button_type = button_type
        self.pronto_code = pronto_code


class ParsedDeviceConfig:
    """
    Parsed DeviceConfig is a generic mapping to a config that may be used by
    different models from a manufacturer
    """
    def __init__(self, device_config_index, name):
        self.device_config_index = device_config_index
        self.name = name
        self.rc_buttons = []

    def add_button(self, rc_button):
        self.rc_buttons.append(rc_button)

    def get_buttons(self):
        return self.rc_buttons


class ParsedDevice:
    """
    Parsed Device maps a specific Model to a Remote Control
    Configuration
    """
    def __init__(self, model_num, manufacturer, device_type, remote_config):
        self.model_num = model_num
        self.manufacturer = manufacturer
        self.device_type = device_type
        self.remote_config = remote_config


class RemoteConfiguration:
    """
    Handles the Reading of the Configuration Files so that the database
    can be initialized and populated based on them
    """
    def __init__(self):
        self.config_index = 0
        self.device_configs = {}
        self.device_config = None
        self.devices = []

    def get_device_configs(self):
        return self.device_configs

    def get_devices(self):
        return self.devices

    def process_ir_dir(self, ir_config_dir):
        csv_files = self.get_csv_files(ir_config_dir)
        for csv_file in csv_files:
            self.process_csv(csv_file)

    def get_csv_files(self, ir_config_dir):
        csv_files = [];
        for root, dir, files in os.walk(ir_config_dir, topdown=False):
            for name in files:
                if self.is_csv_file(name):
                    csv_files.append(root + "/" + name)
        return csv_files

    @staticmethod
    def is_csv_file(name):
        return name.split('.')[1] == "csv"

    def process_csv(self, rel_csv_file):
        with open(rel_csv_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            header_type = "undefined"
            for row in csv_reader:
                if self.is_comment(row):
                    continue
                if header_type == "undefined":
                    header_type = self.parse_header(row, rel_csv_file)
                    if header_type == "unrecognized_type":
                        break
                else:
                    self.parse_line(row, header_type)

    @staticmethod
    def is_comment(row):
        return row[0].startswith("#")

    def parse_header(self, row, rel_csv_file):
        header_column = row[0]
        if header_column != "button" and header_column != "model_num":
            print(f'Unrecognized column {header_column}')
            return "unrecognized_type"
        if header_column == "button":
            self.add_device_config(rel_csv_file)
        return header_column

    def add_device_config(self, rel_csv_file):
        self.config_index += 1
        name = self.parse_config_name(rel_csv_file)
        dc = ParsedDeviceConfig(self.config_index, name)
        self.device_config = dc
        self.device_configs[name] = dc

    def parse_line(self, row, header_type):
        if header_type == "button":
            self.parse_button_line(row)
        else:
            self.parse_device_line(row)

    @staticmethod
    def parse_config_name(rel_csv_file):
        config_name = rel_csv_file.split('/')[-1]
        return config_name.split('.')[0]

    def parse_button_line(self, row):
        button_type, pronto_code = row
        button = ParsedRCButton(self.config_index, button_type,
                                pronto_code.strip())
        self.device_config.add_button(button)

    def parse_device_line(self, row):
        model_num, manufacturer, device_type, remote_config = row
        device = ParsedDevice(model_num, manufacturer.strip(),
                              device_type.strip(), remote_config.strip())
        self.devices.append(device)

