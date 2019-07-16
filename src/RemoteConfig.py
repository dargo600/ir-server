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
        self.rc_config_index = 1

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

    @staticmethod
    def get_csv_files(ir_config_dir):
        csv_files = [];
        for root, dir, files in os.walk(ir_config_dir, topdown=False):
            for name in files:
                file_extension = name.split('.')[1]
                if file_extension == 'csv':
                    csv_files.append(root + "/" + name)
        return csv_files

    def process_csv(self, rel_csv_file):
        with open(rel_csv_file) as csv_file:
            config_type = "undefined"
            header_parsed = False
            config_index = 0
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                line_type = self.parse_line(row, config_type, config_index)
                if line_type == "comment":
                    continue
                config_type = "bad_type" if line_type == "bad_header" else line_type
                if config_type == "bad_type":
                    break
                if not header_parsed:
                    if config_type == "button":
                        config_index = self.generate_config_index(rel_csv_file)
                    header_parsed = True

    def parse_line(self, row, config_type, config_index):
        if row[0].startswith("#"):
            return "comment"
        if config_type == "undefined":
            header_column = row[0]
            if header_column != "button" and header_column != "model_num":
                print(f'Unrecognized column {header_column}')
                return "bad_header"
            return header_column
        if config_type == "button":
            self.parse_button_line(config_index, row)
        else:
            self.parse_device_line(row)
        return config_type

    def parse_button_line(self, config_index, row):
        button_type, pronto_code = row
        button = ParsedRCButton(config_index, button_type,
                                pronto_code.strip())
        self.rc_buttons.append(button)

    def parse_device_line(self, row):
        model_num,manufacturer,device_type,remote_config = row
        device = ParsedDeviceConfig(model_num,
                                    manufacturer.strip(),
                                    device_type.strip(),
                                    remote_config.strip())
        self.device_configs.append(device)

    def generate_config_index(self, rel_csv_file):
        config_idx = self.rc_config_index
        config_name = rel_csv_file.split('/')[-1]
        config_name = config_name.split('.')[0]
        self.remote_control_configs[config_name] = config_idx
        self.rc_config_index += 1
        return config_idx

