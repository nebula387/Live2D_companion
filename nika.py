import requests
import io
import wave
import sounddevice as sd
import numpy as np
import whisper
import re
import threading
from piper.voice import PiperVoice

# ─── НАСТРОЙКИ ───────────────────────────────────────
VOICE_PATH      = r"C:\AI\VTubeModels\TTS\piper_voices\en_US-amy-medium.onnx"
LM_STUDIO_URL   = "http://localhost:1234/v1/chat/completions"
SAMPLE_RATE     = 16000
WAKE_WORD       = "nika"
SILENCE_SECONDS = 1.5
CHUNK_DURATION  = 0.5
SILENCE_THRESHOLD = 0.02

SYSTEM_PROMPT = """You are Nika, a friendly AI companion with three roles:

1. ENGLISH TEACHER: You understand broken and imperfect English perfectly.
Never make the user feel bad about mistakes. Gently note ONE correction
per response at the end, like: "(Tip: say 'I want to go' not 'I want go')"
If user speaks Russian - understand and reply in English.

2. PROGRAMMING ASSISTANT: Help with code, explain clearly,
debug together. Use practical examples.

3. PERSONALITY: Warm, playful, slightly flirty but always respectful.
Encouraging, patient, never condescending about language mistakes.

LANGUAGE RULES:
- Always respond in English
- Understand Russian and broken English perfectly
- Keep responses concise, max 3-4 sentences
- NEVER use markdown, asterisks, hashtags or special symbols
- NEVER say 'Certainly!' or 'As an AI...'
- Respond naturally like a real person
"""

# ─── ИНИЦИАЛИЗАЦИЯ ───────────────────────────────────
print("Loading Nika voice...")
voice = PiperVoice.load(VOICE_PATH)
print("Voice ready!")

print("Loading Whisper...")
whisper_model = whisper.load_model("base")
print("Whisper ready!\n")

conversation_history = []
is_speaking = False

# ─── ОЧИСТКА ТЕКСТА ──────────────────────────────────
def clean_text(text):
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'#+\s?', '', text)
    text = re.sub(r'`+', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ─── LLM ─────────────────────────────────────────────
def ask_llm(user_message):
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = requests.post(LM_STUDIO_URL, json={
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT}
            ] + conversation_history[-20:],
            "temperature": 0.85,
            "max_tokens": 200
        }, timeout=30)

        reply = response.json()["choices"][0]["message"]["content"]
        conversation_history.append({
            "role": "assistant",
            "content": reply
        })
        return reply

    except requests.exceptions.ConnectionError:
        return "I am not connected. Please start LM Studio."
    except Exception as e:
        return f"Error: {str(e)}"

# ─── TTS ─────────────────────────────────────────────
def speak(text):
    global is_speaking
    clean = clean_text(text)
    if not clean:
        return

    is_speaking = True
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(22050)
        voice.synthesize_wav(clean, wav_file)

    buf.seek(0)
    with wave.open(buf, "rb") as wav_file:
        frames = wav_file.readframes(wav_file.getnframes())
        rate = wav_file.getframerate()
        audio = np.frombuffer(frames, dtype=np.int16)
        sd.play(audio, rate)
        sd.wait()

    is_speaking = False

# ─── VAD ЗАПИСЬ (автостоп по паузе) ──────────────────
def record_until_silence():
    print("Recording... (stop speaking to finish)")

    chunks = []
    silent_chunks = 0
    max_silent_chunks = int(SILENCE_SECONDS / CHUNK_DURATION)
    chunk_size = int(SAMPLE_RATE * CHUNK_DURATION)
    has_speech = False

    while True:
        chunk = sd.rec(chunk_size, samplerate=SAMPLE_RATE,
                       channels=1, dtype="float32")
        sd.wait()

        volume = np.max(np.abs(chunk))

        if volume > SILENCE_THRESHOLD:
            chunks.append(chunk)
            silent_chunks = 0
            has_speech = True
        else:
            if has_speech:
                silent_chunks += 1
                chunks.append(chunk)
                if silent_chunks >= max_silent_chunks:
                    break

    if not chunks:
        return None

    return np.concatenate(chunks).flatten()

# ─── WAKE WORD LISTENER ───────────────────────────────
def listen_for_wake_word():
    chunk_size = int(SAMPLE_RATE * 2)

    while True:
        if is_speaking:
            sd.sleep(200)
            continue

        chunk = sd.rec(chunk_size, samplerate=SAMPLE_RATE,
                       channels=1, dtype="float32")
        sd.wait()

        volume = np.max(np.abs(chunk))
        if volume < SILENCE_THRESHOLD:
            continue

        result = whisper_model.transcribe(
            chunk.flatten(),
            language=None,
            fp16=False
        )
        text = result["text"].strip().lower()

        if not text:
            continue

        wake_variants = ["nika", "nica", "nike", "nika,", "ника", "нике", "нека"]
        found = any(w in text for w in wake_variants)

        if found:
            print(f"\n[Wake word detected]")
            sd.play(np.zeros(1000, dtype=np.int16), SAMPLE_RATE)
            sd.wait()

            audio = record_until_silence()
            if audio is None:
                continue

            result2 = whisper_model.transcribe(
                audio,
                language=None,
                fp16=False
            )
            user_text = result2["text"].strip()

            if user_text:
                print(f"You: {user_text}")
                reply = ask_llm(user_text)
                print(f"Nika: {clean_text(reply)}\n")
                speak(reply)

# ─── MAIN ─────────────────────────────────────────────
def main():
    print("=" * 45)
    print("  Nika - English Teacher & Companion  ")
    print("=" * 45)
    print(f"Say 'NIKA' to start talking")
    print("Type 'reset' or 'quit' and press Enter\n")

    listener = threading.Thread(target=listen_for_wake_word, daemon=True)
    listener.start()

    while True:
        try:
            cmd = input().strip().lower()
            if cmd == "quit":
                speak("Goodbye! Keep practicing your English!")
                break
            elif cmd == "reset":
                conversation_history.clear()
                print("Conversation reset.\n")
        except KeyboardInterrupt:
            print("\nNika: See you later!")
            break

if __name__ == "__main__":
    main()
