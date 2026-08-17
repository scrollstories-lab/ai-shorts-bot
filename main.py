import os
import requests
from openai import OpenAI
from moviepy.editor import VideoFileClip, AudioFileClip

# Pobieramy klucze z "sejfu" GitHub (tzw. Secrets)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# 1. OpenAI: Generowanie historii
print("--- Generuję historię ---")
client = OpenAI(api_key=OPENAI_API_KEY)
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a viral YouTube Shorts scriptwriter. Write a shocking, engaging 30-second Reddit story script. No intro, start immediately."},
        {"role": "user", "content": "Write a short viral story script."}
    ]
)
script_text = response.choices[0].message.content

# 2. ElevenLabs: Generowanie głosu
print("--- Generuję głos ---")
VOICE_ID = "pNInz6obpgDQGcFmaJgB" # Głos 'Adam'
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY}
data = {"text": script_text, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}

res = requests.post(url, json=data, headers=headers)
with open("auto_voice.mp3", "wb") as f:
    f.write(res.content)

# 3. Montaż wideo
print("--- Montaż ---")
audio = AudioFileClip("auto_voice.mp3")
video = VideoFileClip("background.mp4")
final_video = video.subclip(0, audio.duration).set_audio(audio)
final_video.write_videofile("auto_shorts_final.mp4", codec="libx264", audio_codec="aac", fps=30, preset="ultrafast")

print("GOTOWE!")
