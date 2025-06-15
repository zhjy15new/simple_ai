"""
Initializes the models package and exposes the core data classes for easy access.
This allows other parts of the application to import them directly from the `models` package.
"""

from .camera_models import (
    CameraConfig,
    ConnectionStatus,
    ImageInfo,
    CaptureResult,
)

__all__ = [
    "CameraConfig",
    "ConnectionStatus",
    "ImageInfo",
    "CaptureResult",
] 