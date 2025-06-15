import json
import os
import yaml
from src.utils.logger import logger
from src.models.camera_models import CameraConfig

class ConfigManager:
    """
    Manages application configuration.
    Loads, validates, and provides access to configuration settings.
    """
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """
        Loads the configuration from a JSON or YAML file.
        Environment variables can override file settings.
        """
        config_data = self._load_from_file()

        # Override with environment variables
        self._override_with_env_vars(config_data)

        if not self.validate_config(config_data):
            raise ValueError("Invalid configuration")

        return config_data

    def _load_from_file(self):
        """Loads configuration from JSON or YAML file."""
        if not os.path.exists(self.config_path):
            logger.error(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        try:
            with open(self.config_path, 'r') as f:
                if self.config_path.endswith('.json'):
                    return json.load(f)
                elif self.config_path.endswith(('.yml', '.yaml')):
                    return yaml.safe_load(f)
                else:
                    raise ValueError("Unsupported config file format. Use .json, .yml, or .yaml")
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            logger.error(f"Error decoding configuration file: {e}")
            raise

    def _override_with_env_vars(self, config):
        """Override configuration with environment variables."""
        # Example for camera IP
        camera_ip = os.environ.get('CAMERA_IP')
        if camera_ip:
            config['camera']['ip'] = camera_ip
            logger.info(f"Overridden camera IP with environment variable: {camera_ip}")

        # Add other environment variable overrides here

    def validate_config(self, config_data):
        """
        Validates the configuration data.
        """
        try:
            # Validate camera config
            camera_conf = config_data.get('camera')
            if not camera_conf:
                logger.error("'camera' section is missing in config")
                return False
            CameraConfig(**camera_conf) # Use dataclass for validation

            # Validate logging config
            log_conf = config_data.get('logging')
            if not log_conf or 'level' not in log_conf or 'file' not in log_conf:
                 logger.error("'logging' section is incomplete or missing")
                 return False

        except (TypeError, ValueError) as e:
            logger.error(f"Configuration validation failed: {e}")
            return False

        return True

    def get_camera_config(self) -> CameraConfig:
        """Returns the camera configuration as a CameraConfig object."""
        return CameraConfig(**self.config['camera'])

    def get_logging_config(self):
        """Returns the logging configuration."""
        return self.config['logging']

# Global config instance
# config_manager = ConfigManager() 