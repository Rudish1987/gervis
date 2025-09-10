import os
from datetime import datetime
import speech_recognition as sr

note_dir = "notes"
os.makedirs(note_dir, exist_ok=True)
today = datetime.today().strftime("%Y-%m-%d")
note_path = os.path.join(note_dir, f"{today}.txt")

recognizer = sr.Recognizer()
mic = sr.Microphone()

print("🎤 Speak your daily note. Say 'Pa' before tomorrow's tasks.")
print("Listening... (10 seconds max)")

with mic as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source, timeout=10)

try:
    text = recognizer.recognize_google(audio)
    print("📝 Transcription:\n", text)
except sr.UnknownValueError:
    print("Could not understand audio.")
    text = ""
except sr.RequestError as e:
    print("Speech recognition error:", str(e))
    text = ""

# Parse note sections
note_lines = [f"Date: {today}", "", "Tasks Done:"]
pending = []
done = []
if "Pa" in text:
    print('ifpart')
    parts = text.split("Pa")
    #done_text = parts[0].strip()
    pending_text = parts[1].strip()
    #done = [f"- {line.strip()}" for line in done_text.split(".") if line.strip()]
    pending = [f"- {line.strip()}" for line in pending_text.split(".") if line.strip()]
else:
    done = [f"- {line.strip()}" for line in text.split(".") if line.strip()]
    print('else')

note_lines.extend(done)
note_lines.append("")
note_lines.append("Pending / Tomorrow:")
note_lines.extend(pending)

with open(note_path, "w") as f:
    f.write("\n".join(note_lines))

print(f"✅ Note saved to {note_path}")
