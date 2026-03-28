import unittest
import os
from voice_gen import VoiceGenerator

class TestVoiceGen(unittest.TestCase):
    def setUp(self):
        self.vo = VoiceGenerator()

    def test_audio_file_creation(self):
        # We define what success looks like: a real MP3 file on your disk
        text = "This is a test for Everyday Explained."
        output_path = "test_voice_output.mp3"
        
        self.vo.generate_audio(text, output_path)
        
        # Validation: Does the file exist and is it not empty?
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 0)
        
        # Cleanup: Remove the test file after the pass
        # if os.path.exists(output_path):
        #     os.remove(output_path)

if __name__ == "__main__":
    unittest.main()