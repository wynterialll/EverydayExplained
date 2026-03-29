import os
import json
from script_gen import ScriptGenerator
from voice_gen import VoiceGenerator

def generate_video_assets(topic):
    # Initialize the team
    writer = ScriptGenerator()
    narrator = VoiceGenerator()
    
    print(f"🚀 Starting consolidated RPD-optimized pipeline for: {topic}")
    
    # 1. Generate the viral script (1 API call)
    script = writer.generate_viral_script(topic)
    writer.save_script(script, f"{topic}_script.json")
    
    # 2. Combine all parts into one long narration string
    # We add "..." between sections to tell the AI to take a brief breath/pause
    full_narration = (
        f"{script['hook']} ... "
        f"{script['mystery']} ... "
        f"{script['reveal']} ... "
        f"{script['cta']}"
    )
    
    # 3. Create a folder and generate ONE audio file (1 API call)
    os.makedirs(topic, exist_ok=True)
    output_file = f"{topic}/full_voiceover.wav"
    
    print(f"🎙️ Generating full voiceover (Reducing RPD usage)...")
    narrator.generate_audio(full_narration, output_file)
    
    print(f"\n🎉 Success! Single audio file saved to /{topic}/full_voiceover.wav")

if __name__ == "__main__":
    user_topic = input("Enter the topic for your next video: ")
    generate_video_assets(user_topic)