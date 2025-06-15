"""
This module defines the core data structures (data classes) used throughout the application.
These structures ensure data consistency and provide clear definitions for a-ntities 
like Camera Configuration, Connection Status, and Capture Results.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum, auto

@dataclass
class CameraConfig:
    """
    Represents the configuration for a single camera.
    
    Attributes:
        ip (str): The IP address of the camera.
        port (int): The port number for the connection (e.g., 554 for RTSP).
        username (str): The username for authentication.
        password (str): The password for authentication.
        protocol (str): The protocol to use ('rtsp', 'onvif', 'http'). Defaults to 'rtsp'.
        timeout (int): Connection timeout in seconds. Defaults to 10.
        retry_count (int): Number of retries on connection failure. Defaults to 3.
        camera_id (str): A unique identifier for the camera.
        rtsp_path (str): The RTSP path for the camera. Defaults to an empty string.
    """
    ip: str
    username: str
    password: str
    camera_id: str
    port: int = 554
    rtsp_path: str = ""
    protocol: str = "rtsp"
    timeout: int = 10
    retry_count: int = 3
    
@dataclass
class ConnectionStatus:
    """
    Holds the current connection status of a camera client.
    
    Attributes:
        is_connected (bool): True if the client is currently connected.
        last_error (Optional[str]): The last error message, if any.
        retry_count (int): The current retry count.
        last_attempt_time (Optional[datetime]): Timestamp of the last connection attempt.
    """
    is_connected: bool = False
    last_error: Optional[str] = None
    retry_count: int = 0
    last_attempt_time: Optional[datetime] = None

@dataclass
class ImageInfo:
    """
    Contains metadata about a captured image.
    
    Attributes:
        timestamp (datetime): The timestamp when the image was captured.
        file_path (str): The full path where the image is saved.
        size (int): The size of the image file in bytes.
        format (str): The image format (e.g., 'JPEG').
        metadata (Dict[str, Any]): A dictionary for additional metadata (e.g., EXIF data).
    """
    timestamp: datetime
    file_path: str
    size: int
    format: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CaptureResult:
    """
    Represents the result of a capture operation.
    
    This object is returned by the capture engine to provide a clear and structured
    summary of what happened during the capture attempt.
    
    Attributes:
        success (bool): True if the capture was successful, False otherwise.
        image_info (Optional[ImageInfo]): ImageInfo object if successful.
        error_message (Optional[str]): Error message if the capture failed.
        execution_time_ms (float): Total time for the operation in milliseconds.
    """
    success: bool
    image_info: Optional[ImageInfo] = None
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0 