import os
import cv2
import numpy as np
from datetime import datetime
from src.utils.logger import logger

class ImageProcessor:
    """
    Handles image processing tasks like saving, validation, and format conversion.
    """
    @staticmethod
    def save_image(
        frame: np.ndarray,
        directory: str = "output",
        camera_id: str = "cam1",
        file_format: str = "jpg",
        jpeg_quality: int = 95
    ) -> str | None:
        """
        Saves a single frame to a file with a timestamp-based name.

        Args:
            frame: The image frame (numpy array).
            directory: The directory to save the image in.
            camera_id: An identifier for the camera.
            file_format: The desired file format ('jpg' or 'png').
            jpeg_quality: The quality for JPEG saving (0-100).

        Returns:
            The path to the saved image, or None on failure.
        """
        if not ImageProcessor.validate_image(frame):
            return None

        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Created output directory: {directory}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{timestamp}_{camera_id}.{file_format}"
            filepath = os.path.join(directory, filename)

            if file_format.lower() == 'jpg':
                params = [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality]
                success = cv2.imwrite(filepath, frame, params)
            elif file_format.lower() == 'png':
                success = cv2.imwrite(filepath, frame)
            else:
                logger.error(f"Unsupported image format: {file_format}")
                return None

            if success:
                logger.info(f"Successfully saved image to {filepath}")
                return filepath
            else:
                logger.error(f"Failed to save image to {filepath}")
                return None

        except Exception as e:
            logger.error(f"An error occurred while saving the image: {e}")
            return None

    @staticmethod
    def validate_image(frame: np.ndarray) -> bool:
        """
        Validates if the given frame is a valid image.
        """
        if frame is None or frame.size == 0:
            logger.error("Image validation failed: Frame is empty or None.")
            return False
        
        # Add more checks if needed, e.g., dimensions, channels
        if len(frame.shape) < 2:
            logger.error(f"Image validation failed: Invalid shape {frame.shape}")
            return False

        return True 