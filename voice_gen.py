import os
import wave
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class VoiceGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def generate_audio(self, text, output_path):
        """Converts text to a playable WAV file with a standard 24kHz header."""
        voice_config = types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='puck'
            )
        )
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(voice_config=voice_config)
            )
        )
        
        try:
            raw_pcm_data = response.candidates[0].content.parts[0].inline_data.data
            
            # Gemini TTS outputs 16-bit Mono PCM at 24kHz
            with wave.open(output_path, "wb") as wav_file:
                wav_file.setnchannels(1)      # Mono
                wav_file.setsampwidth(2)      # 16-bit
                wav_file.setframerate(24000) # 24kHz
                wav_file.writeframes(raw_pcm_data)
                
            print(f"✅ Generated audio: {output_path}")
            
        except (AttributeError, IndexError) as e:
            raise Exception(f"Failed to extract audio: {e}")