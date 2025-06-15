import unittest
import os
import cv2
import numpy as np
from unittest.mock import patch, MagicMock
from src.utils.image_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):

    def setUp(self):
        """Set up for the tests."""
        self.output_dir = "test_output"
        # Create a dummy blank image
        self.valid_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        self.invalid_frame = None

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.output_dir):
            for f in os.listdir(self.output_dir):
                os.remove(os.path.join(self.output_dir, f))
            os.rmdir(self.output_dir)

    def test_validate_image_valid(self):
        """Test validation with a valid image."""
        self.assertTrue(ImageProcessor.validate_image(self.valid_frame))

    def test_validate_image_invalid(self):
        """Test validation with an invalid image."""
        self.assertFalse(ImageProcessor.validate_image(self.invalid_frame))
        self.assertFalse(ImageProcessor.validate_image(np.array([])))

    @patch("os.makedirs")
    @patch("cv2.imwrite")
    def test_save_image_success(self, mock_imwrite, mock_makedirs):
        """Test successful image saving."""
        mock_imwrite.return_value = True
        
        filepath = ImageProcessor.save_image(self.valid_frame, directory=self.output_dir)
        
        self.assertIsNotNone(filepath)
        mock_makedirs.assert_called_once_with(self.output_dir)
        mock_imwrite.assert_called_once()
        self.assertTrue(filepath.startswith(self.output_dir))

    @patch("cv2.imwrite")
    def test_save_image_failure(self, mock_imwrite):
        """Test failure in image saving."""
        mock_imwrite.return_value = False
        
        filepath = ImageProcessor.save_image(self.valid_frame, directory=self.output_dir)
        self.assertIsNone(filepath)

    def test_save_image_invalid_frame(self):
        """Test saving with an invalid frame."""
        filepath = ImageProcessor.save_image(self.invalid_frame, directory=self.output_dir)
        self.assertIsNone(filepath)

if __name__ == '__main__':
    unittest.main() 