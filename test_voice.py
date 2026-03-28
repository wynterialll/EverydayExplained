import os
from script_gen import ScriptGenerator
from voice_gen import VoiceGenerator

def run_pipeline(topic):
    # Initialize our AI team
    writer = ScriptGenerator()
    narrator = VoiceGenerator()
    
    print(f"🚀 Starting EverydayExplained pipeline for: {topic}")
    
    # Step 1: Generate the Script
    script = writer.generate_viral_script(topic)
    writer.save_script(script, f"{topic}_script.json")
    
    # Step 2: Create a folder for this video's assets
    os.makedirs(topic, exist_ok=True)
    
    # Step 3: Generate Audio for each section
    # We iterate through the JSON keys: hook, mystery, reveal, cta
    for section, text in script.items():
        filename = f"{topic}/{section}.wav"
        print(f"🎙️ Recording {section}...")
        narrator.generate_audio(text, filename)
    
    print(f"\n🎉 Done! All assets for '{topic}' are ready in the /{topic} folder.")

if __name__ == "__main__":
    target_topic = input("Enter a topic for EverydayExplained: ")
    run_pipeline(target_topic)