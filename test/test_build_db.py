import unittest
from src.RemoteConfig import RemoteConfiguration


class TestBuild_DB(unittest.TestCase):


    def test_process_ir_dir(self):
        remoteConfig = RemoteConfiguration()
        remoteConfig.process_ir_dir("../src/ir_dir")
        buttons = remoteConfig.getRCButtons()
        self.assertTrue(len(buttons) != 0)
        samsungConfig1Buttons = 0
        for button in buttons:
            if button.remote_config == "samsungConfig1":
                samsungConfig1Buttons += 1
        self.assertEqual(samsungConfig1Buttons, 34)


    def test_get_csv_files(self):
        remoteConfig = RemoteConfiguration()
        csv_files = remoteConfig.get_csv_files("../src/ir_dir")
        self.assertIn("../src/ir_dir/apple/appleConfig1.csv", csv_files)
        self.assertIn("../src/ir_dir/roku/rokuConfig1.csv", csv_files)
        self.assertIn("../src/ir_dir/samsung/samsungConfig1.csv", csv_files)
        self.assertIn("../src/ir_dir/samsung/samsungConfig2.csv", csv_files)
        self.assertEqual(len(csv_files), 4)


    def test_get_csv_files_is_empty(self):
        remoteConfig = RemoteConfiguration()
        csv_files = remoteConfig.get_csv_files("../src/static")
        self.assertEqual(len(csv_files), 0)


if __name__ == '__main__':
    unittest.main()
