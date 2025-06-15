import cv2
from src.utils.logger import logger
from src.models.camera_models import CameraConfig
from src.utils.monitor import performance_monitor
import numpy as np

class RTSPClient:
    """
    A client for connecting to an RTSP stream and capturing frames.
    """
    def __init__(self, config: CameraConfig):
        self.config = config
        self.rtsp_url = self._build_rtsp_url()
        self.cap = None

    def _build_rtsp_url(self) -> str:
        """Constructs the RTSP URL from the configuration."""
        return (
            f"rtsp://{self.config.username}:{self.config.password}@"
            f"{self.config.ip}:{self.config.port}/{self.config.rtsp_path}"
        )

    @performance_monitor
    def connect(self) -> bool:
        """
        Connects to the RTSP stream.
        Returns True if connection is successful, False otherwise.
        """
        logger.info(f"Attempting to connect to RTSP stream: {self.config.ip}")
        try:
            # Using CAP_FFMPEG backend for better compatibility
            self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
            
            # Set buffer size to 1 to get the latest frame
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if not self.cap.isOpened():
                logger.error(f"Failed to open RTSP stream at {self.rtsp_url}")
                self.cap = None
                return False
            
            logger.info("Successfully connected to RTSP stream.")
            return True
        except Exception as e:
            logger.error(f"An error occurred while connecting to RTSP stream: {e}")
            self.cap = None
            return False

    @performance_monitor
    def capture_frame(self) -> np.ndarray | None:
        """
        Captures a single frame from the RTSP stream.
        Returns the frame as a numpy array, or None if capture fails.
        """
        if not self.cap or not self.cap.isOpened():
            logger.warning("Not connected to RTSP stream. Cannot capture frame.")
            return None

        try:
            # The buffer is cleared and the latest frame is read.
            ret, frame = self.cap.read()
            if not ret or frame is None:
                logger.error("Failed to read frame from RTSP stream.")
                return None
            
            logger.info("Successfully captured a frame.")
            return frame
        except Exception as e:
            logger.error(f"An error occurred while capturing frame: {e}")
            return None

    @performance_monitor
    def disconnect(self):
        """
        Disconnects from the RTSP stream and releases resources.
        """
        if self.cap:
            logger.info("Disconnecting from RTSP stream.")
            self.cap.release()
            self.cap = None
            logger.info("RTSP stream disconnected.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect() 