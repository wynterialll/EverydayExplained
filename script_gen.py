import os
import time
from google import genai
from google.api_core import exceptions
from dotenv import load_dotenv

load_dotenv()

class ScriptGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        # FIX: Switched to 2.5 Flash (Retired 2.0 was causing your error)
        self.model_id = "gemini-2.5-flash"
        self.system_instruction = "You are the lead writer for 'EverydayExplained'..."

    def generate_viral_script(self, topic, retries=3):
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    config={'system_instruction': self.system_instruction, 'response_mime_type': 'application/json'},
                    contents=f"Create a 50-second script about {topic}."
                )
                return response.parsed
            except exceptions.ResourceExhausted:
                if attempt < retries - 1:
                    print(f"Rate limit hit. Waiting 30s... (Attempt {attempt+1}/{retries})")
                    time.sleep(30) # Wait for the 'Token Bucket' to refill
                else:
                    raise