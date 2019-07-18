import unittest
from src.RemoteConfig import RemoteConfiguration


class TestBuildDB(unittest.TestCase):

    def test_process_ir_dir(self):
        remote_config = RemoteConfiguration()
        remote_config.process_ir_dir("../src/ir_dir")
        buttons = remote_config.get_rc_buttons()
        self.assertTrue(len(buttons) != 0)

    def test_get_csv_files(self):
        remote_config = RemoteConfiguration()
        csv_files = remote_config.get_csv_files("../src/ir_dir")
        self.assertIn("../src/ir_dir/apple/appleConfig1.csv", csv_files)
        self.assertIn("../src/ir_dir/roku/rokuConfig1.csv", csv_files)
        self.assertIn("../src/ir_dir/samsung/samsungConfig1.csv", csv_files)
        self.assertIn("../src/ir_dir/samsung/samsungConfig2.csv", csv_files)
        self.assertIn("../src/ir_dir/device_configs.csv", csv_files)
        self.assertEqual(len(csv_files), 5)

    def test_get_csv_files_is_empty(self):
        remote_config = RemoteConfiguration()
        csv_files = remote_config.get_csv_files("../src/static")
        self.assertEqual(len(csv_files), 0)

    def test_process_ir_dir_pronto_begins_with_zero(self):
        remote_config = RemoteConfiguration()
        remote_config.process_ir_dir("../src/ir_dir")
        buttons = remote_config.get_rc_buttons()
        self.assertTrue(len(buttons) != 0)
        for button in buttons:
            self.assertTrue(button.pronto_code.startswith("0000"))

    def test_process_ir_dir_sets_samsung_tv_correctly(self):
        remote_config = RemoteConfiguration()
        remote_config.process_ir_dir("../src/ir_dir")
        device_configs = remote_config.get_device_configs()
        for config in device_configs:
            if config.model_num == "ln46C630k1fkxzc":
                self.assertEqual(config.remote_config, "samsungConfig1")

    def test_process_ir_dir_get_remote_control_configs(self):
        remote_config = RemoteConfiguration()
        remote_config.process_ir_dir("../src/ir_dir")
        unique_remote_configs = remote_config.get_remote_control_configs()
        self.assertEqual(len(unique_remote_configs), 4)


if __name__ == '__main__':
    unittest.main()
