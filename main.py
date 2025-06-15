import cv2
from src.utils.logger import logger
from src.config.config_manager import ConfigManager
from src.camera.rtsp_client import RTSPClient
from src.utils.image_processor import ImageProcessor
from src.utils.monitor import HealthCheck

def main():
    """
    Main function to run the application.
    """
    logger.info("Application starting...")

    try:
        # Manually create a ConfigManager instance
        config_manager = ConfigManager()
        camera_config = config_manager.get_camera_config()

        with RTSPClient(camera_config) as client:
            # Perform a health check before capturing
            if HealthCheck.check_camera_status(client):
                frame = client.capture_frame()
                if frame is not None:
                    # Use ImageProcessor to save the frame
                    ImageProcessor.save_image(
                        frame=frame,
                        camera_id=camera_config.camera_id
                    )
                else:
                    logger.error("Failed to capture frame.")
            else:
                logger.error("Health check failed. Could not connect to the camera.")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    logger.info("Application finished.")

if __name__ == "__main__":
    main() 