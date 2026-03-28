import os
import time
import json
import re
from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()


class ScriptGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_id = "gemini-2.5-flash"

        self.system_instruction = (
            "You are the lead writer for 'EverydayExplained'. "
            "Every script MUST start with a 'Logic Glitch' mystery. "
            "Output Format: Strictly raw JSON with keys: 'hook', 'mystery', 'reveal', 'cta'. "
            "Do NOT include markdown code blocks or any text outside the JSON."
        )

    def _clean_json_text(self, text):
        """Removes markdown code blocks and invisible characters."""
        # Remove markdown triple backticks if present
        text = re.sub(r"```json|```", "", text).strip()
        # Remove non-breaking spaces and other weird whitespace
        text = text.replace("\xa0", " ")
        return text

    def generate_viral_script(self, topic, retries=3):
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    config={
                        "system_instruction": self.system_instruction,
                        "response_mime_type": "application/json",
                    },
                    contents=f"Create a 50-second script about {topic}.",
                )

                # Manual Parse Strategy
                raw_text = self._clean_json_text(response.text)
                try:
                    return json.loads(raw_text)
                except json.JSONDecodeError:
                    print(f"DEBUG: Parse failed on attempt {attempt+1}. Retrying...")
                    continue

            except errors.ClientError as e:
                if "429" in str(e) and attempt < retries - 1:
                    print(f"Rate limit hit. Waiting 30s...")
                    time.sleep(30)
                else:
                    raise e

        raise Exception("AI failed to generate a valid script after multiple attempts.")

    def save_script(self, script, filename="latest_script.json"):
        with open(filename, "w") as f:
            json.dump(script, f, indent=4)
        print(f"Script saved to {filename}")
