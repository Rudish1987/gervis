import os
from datetime import datetime, timedelta
import speech_recognition as sr

note_dir = "notes"
os.makedirs(note_dir, exist_ok=True)

recognizer = sr.Recognizer()
mic = sr.Microphone()

print("🎤 Say 'Today' or 'Tomorrow' followed by your note. Say 'Stop listening' to end.")

while True:
    print("Listening...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("📝 Transcription:\n", text)
    except sr.UnknownValueError:
        print("Could not understand audio.")
        continue
    except sr.RequestError as e:
        print("Speech recognition error:", str(e))
        continue

    text = text.strip()
    lower_text = text.lower()

    if lower_text == "stop listening":
        print("🛑 Stopped listening.")
        break

    # Check for "Today" or "Tomorrow" as a command to enter recording mode
    if lower_text == "today":
        note_date = datetime.today()
        note_path = os.path.join(note_dir, f"{note_date.strftime('%Y-%m-%d')}.txt")
        print("Recording for today. Say 'Stop listening' to end.")
        while True:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            try:
                segment = recognizer.recognize_google(audio)
                print("📝 Transcription:\n", segment)
            except sr.UnknownValueError:
                print("Could not understand audio.")
                continue
            except sr.RequestError as e:
                print("Speech recognition error:", str(e))
                continue
            segment = segment.strip()
            if segment.lower() == "stop listening":
                print("🛑 Stopped listening.")
                break
            with open(note_path, "a") as f:
                f.write(segment + "\n")
            print(f"✅ Note saved to {note_path}")
        continue

    if lower_text == "tomorrow":
        note_date = datetime.today() + timedelta(days=1)
        note_path = os.path.join(note_dir, f"{note_date.strftime('%Y-%m-%d')}.txt")
        print("Recording for tomorrow. Say 'Stop listening' to end.")
        while True:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            try:
                segment = recognizer.recognize_google(audio)
                print("📝 Transcription:\n", segment)
            except sr.UnknownValueError:
                print("Could not understand audio.")
                continue
            except sr.RequestError as e:
                print("Speech recognition error:", str(e))
                continue
            segment = segment.strip()
            if segment.lower() == "stop listening":
                print("🛑 Stopped listening.")
                break
            with open(note_path, "a") as f:
                f.write(segment + "\n")
            print(f"✅ Note saved to {note_path}")
        continue

    # Original functionality for "Today ..." or "Tomorrow ..." one-liners
    if lower_text.startswith("today"):
        note_date = datetime.today()
        note_content = text[5:].strip()  # Remove "Today"
    elif lower_text.startswith("tomorrow"):
        note_date = datetime.today() + timedelta(days=1)
        note_content = text[8:].strip()  # Remove "Tomorrow"
    else:
        print("Please start your note with 'Today' or 'Tomorrow'.")
        note_date = datetime.today()
        note_content = text

    note_path = os.path.join(note_dir, f"{note_date.strftime('%Y-%m-%d')}.txt")

    with open(note_path, "a") as f:
        f.write(note_content + "\n")

    print(f"✅ Note saved to {note_path}")