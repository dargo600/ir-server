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
    Parsed Device Configuration maps a specific Model to a Remote Control
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
        self.rc_buttons = []
        self.device_configs = []
        self.remote_control_configs = {}
        self.rc_config_index = 0

    def get_rc_buttons(self):
        return self.rc_buttons

    def get_device_configs(self):
        return self.device_configs

    def get_remote_control_configs(self):
        return self.remote_control_configs;

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
            expected_line_type = "undefined"
            for row in csv_reader:
                line_type,config_type = self.parse_line(row, rel_csv_file, expected_line_type)
                if line_type == "comment":
                    continue
                if config_type == "unrecognized_type":
                    break
                expected_line_type = config_type

    def parse_line(self, row, rel_csv_file, expected_line_type):
        if row[0].startswith("#"):
            return "comment", "undefined"
        if expected_line_type == "undefined":
            return "header", self.parse_header(row, rel_csv_file)
        if expected_line_type == "button":
            self.parse_button_line(row)
        else:
            self.parse_device_line(row)
        return expected_line_type,expected_line_type

    def parse_header(self, row, rel_csv_file):
        header_column = row[0]
        if header_column != "button" and header_column != "model_num":
            print(f'Unrecognized column {header_column}')
            return "unrecognized_type"
        if header_column == "button":
            self.update_config_index(rel_csv_file)
        return header_column

    def update_config_index(self, rel_csv_file):
        self.rc_config_index += 1
        config_name = rel_csv_file.split('/')[-1]
        config_name = config_name.split('.')[0]
        self.remote_control_configs[config_name] = self.rc_config_index

    def parse_button_line(self, row):
        button_type, pronto_code = row
        button = ParsedRCButton(self.rc_config_index, button_type,
                                pronto_code.strip())
        self.rc_buttons.append(button)

    def parse_device_line(self, row):
        model_num,manufacturer,device_type,remote_config = row
        device = ParsedDeviceConfig(model_num,
                                    manufacturer.strip(),
                                    device_type.strip(),
                                    remote_config.strip())
        self.device_configs.append(device)

