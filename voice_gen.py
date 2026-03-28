import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class VoiceGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def generate_audio(self, text, output_path):
        """Converts text to audio bytes using the specialized TTS model."""
        # 1. Define the voice configuration (puck is a supported voice)
        voice_config = types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='puck'
            )
        )
        
        speech_config = types.SpeechConfig(voice_config=voice_config)
        
        # 2. Use the preview model ID and specify 'AUDIO' modality
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-tts", # Corrected Model ID
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"], # Required for audio output
                speech_config=speech_config
            )
        )
        
        # 3. Extract audio bytes from the response
        # The audio data is in response.parts[0].inline_data.data
        try:
            audio_data = response.parts[0].inline_data.data
            
            with open(output_path, "wb") as f:
                f.write(audio_data)
            print(f"Successfully generated audio: {output_path}")
            
        except (AttributeError, IndexError) as e:
            raise Exception(f"Failed to extract audio: {e}. Response parts: {response.parts}")