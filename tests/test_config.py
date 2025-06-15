import unittest
import os
import json
from unittest.mock import patch, mock_open
from src.config.config_manager import ConfigManager
from src.models.camera_models import CameraConfig

class TestConfigManager(unittest.TestCase):

    def setUp(self):
        """Set up for the tests."""
        self.config_data = {
            "camera": {
                "ip": "127.0.0.1",
                "port": 8554,
                "rtsp_path": "live.stream",
                "username": "testuser",
                "password": "testpassword",
                "camera_id": "test_cam"
            },
            "logging": {
                "level": "DEBUG",
                "file": "logs/test.log"
            }
        }

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_config_json_success(self, mock_file, mock_exists):
        """Test successful loading of a JSON config file."""
        mock_exists.return_value = True
        mock_file().read.return_value = json.dumps(self.config_data)
        
        with patch.dict(os.environ, {}, clear=True):
             manager = ConfigManager(config_path='config.json')
             self.assertEqual(manager.config, self.config_data)

    @patch.dict(os.environ, {"CAMERA_IP": "192.168.1.100"})
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_env_var_override(self, mock_file, mock_exists):
        """Test that environment variables override file settings."""
        mock_exists.return_value = True
        mock_file().read.return_value = json.dumps(self.config_data)
        
        manager = ConfigManager()
        self.assertEqual(manager.get_camera_config().ip, "192.168.1.100")

    def test_get_camera_config(self):
        """Test the getter for camera configuration."""
        with patch.object(ConfigManager, 'load_config', return_value=self.config_data):
            manager = ConfigManager()
            camera_config = manager.get_camera_config()
            self.assertIsInstance(camera_config, CameraConfig)
            self.assertEqual(camera_config.ip, "127.0.0.1")

    @patch("os.path.exists", return_value=False)
    def test_load_config_file_not_found(self, mock_exists):
        """Test FileNotFoundError when config file is missing."""
        with self.assertRaises(FileNotFoundError):
            ConfigManager()

    def test_validate_config_invalid(self):
        """Test validation failure for incomplete config."""
        invalid_config = {"camera": {"ip": "127.0.0.1"}} # Missing fields
        with patch.object(ConfigManager, '_load_from_file', return_value=invalid_config):
            with self.assertRaises(ValueError):
                 ConfigManager()

if __name__ == '__main__':
    unittest.main() 