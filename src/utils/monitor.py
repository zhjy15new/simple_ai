import time
from functools import wraps
from src.utils.logger import logger

def performance_monitor(func):
    """
    A decorator that logs the execution time of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            duration = (end_time - start_time) * 1000  # to milliseconds
            logger.info(f"Performance: Function '{func.__name__}' executed in {duration:.2f} ms")
    return wrapper

class HealthCheck:
    """
    A simple health check placeholder.
    In a real application, this would ping the camera or check a status endpoint.
    """
    @staticmethod
    @performance_monitor
    def check_camera_status(rtsp_client):
        """
        Simulates a health check for the camera.
        """
        logger.info(f"Performing health check for camera at {rtsp_client.config.ip}")
        is_connected = rtsp_client.cap is not None and rtsp_client.cap.isOpened()
        if is_connected:
            logger.info("Health check PASSED: Camera is connected.")
        else:
            logger.warning("Health check FAILED: Camera is not connected.")
        return is_connected 