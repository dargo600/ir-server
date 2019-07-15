import os
from pathlib import Path
import csv

"""
Remote Control Button Configurations used when reading from the file
"""
class RCButtonConfig:
    def __init__(self, remote_config, button_type, pronto_code):
        self.remote_config = remote_config
        self.button_type = button_type
        self.pronto_code = pronto_code


"""
Handles the Reading of the Configuration Files
"""
class RemoteConfiguration:
    def __init__(self):
        self.rc_buttons = []
        self.rc_configs = []


    def getRCButtons(self):
        return self.rc_buttons


    def process_ir_dir(self, ir_config_dir):
        csv_files = self.get_csv_files(ir_config_dir)
        for csv_file in csv_files:
            self.process_csv(csv_file)


    def get_csv_files(self, ir_config_dir):
        csv_files = [];
        for root, dir, files in os.walk(ir_config_dir, topdown=False):
            for name in files:
                file_extension = name.split('.')[1]
                if file_extension == 'csv':
                    csv_files.append(root + "/" + name)
        return csv_files


    def process_csv(self, rel_csv_file):
        cur_config = Path(rel_csv_file)
        absolute_file = os.path.abspath(cur_config)
        with open(absolute_file) as csv_file:
            remote_config = rel_csv_file.split('/')[-1]
            remote_config = remote_config.split('.')[0]
            csv_reader = csv.reader(csv_file, delimiter=',')
            header_line = True
            for row in csv_reader:
                if row[0].startswith("#"):
                    continue
                if header_line:
                    header_line = False
                else:
                    button_type = row[0]
                    ir_label = row[1]
                    self.rc_buttons.append(RCButtonConfig(remote_config, button_type, ir_label))

