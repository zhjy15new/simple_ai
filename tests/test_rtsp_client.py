import unittest
from unittest.mock import patch, MagicMock
from src.camera.rtsp_client import RTSPClient
from src.models.camera_models import CameraConfig
import numpy as np

class TestRTSPClient(unittest.TestCase):

    def setUp(self):
        """Set up for the tests."""
        self.config = CameraConfig(
            ip="127.0.0.1",
            port=8554,
            rtsp_path="live.stream",
            username="testuser",
            password="testpassword"
        )
        self.rtsp_url = "rtsp://testuser:testpassword@127.0.0.1:8554/live.stream"

    def test_build_rtsp_url(self):
        """Test the construction of the RTSP URL."""
        client = RTSPClient(self.config)
        self.assertEqual(client.rtsp_url, self.rtsp_url)

    @patch('cv2.VideoCapture')
    def test_connect_success(self, mock_video_capture):
        """Test successful connection to the RTSP stream."""
        mock_cap_instance = MagicMock()
        mock_cap_instance.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap_instance

        client = RTSPClient(self.config)
        self.assertTrue(client.connect())
        mock_video_capture.assert_called_with(self.rtsp_url, cv2.CAP_FFMPEG)
        self.assertIsNotNone(client.cap)

    @patch('cv2.VideoCapture')
    def test_connect_failure(self, mock_video_capture):
        """Test failed connection to the RTSP stream."""
        mock_cap_instance = MagicMock()
        mock_cap_instance.isOpened.return_value = False
        mock_video_capture.return_value = mock_cap_instance

        client = RTSPClient(self.config)
        self.assertFalse(client.connect())
        self.assertIsNone(client.cap)

    def test_capture_frame_not_connected(self):
        """Test frame capture when not connected."""
        client = RTSPClient(self.config)
        client.cap = None
        self.assertIsNone(client.capture_frame())

    @patch('cv2.VideoCapture')
    def test_capture_frame_success(self, mock_video_capture):
        """Test successful frame capture."""
        mock_cap_instance = MagicMock()
        mock_cap_instance.isOpened.return_value = True
        dummy_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_cap_instance.read.return_value = (True, dummy_frame)
        mock_video_capture.return_value = mock_cap_instance

        client = RTSPClient(self.config)
        client.connect()
        frame = client.capture_frame()

        self.assertIsNotNone(frame)
        np.testing.assert_array_equal(frame, dummy_frame)

    @patch('cv2.VideoCapture')
    def test_capture_frame_failure(self, mock_video_capture):
        """Test failed frame capture (read fails)."""
        mock_cap_instance = MagicMock()
        mock_cap_instance.isOpened.return_value = True
        mock_cap_instance.read.return_value = (False, None)
        mock_video_capture.return_value = mock_cap_instance

        client = RTSPClient(self.config)
        client.connect()
        frame = client.capture_frame()

        self.assertIsNone(frame)
        
    @patch('cv2.VideoCapture')
    def test_disconnect(self, mock_video_capture):
        """Test disconnection."""
        mock_cap_instance = MagicMock()
        mock_cap_instance.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap_instance

        client = RTSPClient(self.config)
        client.connect()
        client.disconnect()

        mock_cap_instance.release.assert_called_once()
        self.assertIsNone(client.cap)

if __name__ == '__main__':
    unittest.main() 