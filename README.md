# Nika — AI Companion with Live2D Avatar

<video src="Record_Nika_1.mp4" controls width="100%"></video>

A local AI companion with a live 2D avatar, voice synthesis, and conversational AI.
Nika acts as an English teacher, programming assistant, and friendly companion.
Activated by wake word **"Nika"** — no cloud, no subscriptions, runs fully offline.

![Platform](https://img.shields.io/badge/platform-Windows%2011-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## Features

- Wake word activation — say **"Nika"** to start talking
- Auto-stop recording on silence — natural conversation flow
- Voice synthesis via Piper TTS (runs on CPU, no GPU needed)
- Speech recognition via Whisper (understands broken English and Russian)
- Live2D avatar with lip sync in VTube Studio
- English teacher — gently corrects one mistake per response
- Programming assistant — helps with code and debugging
- Fully local — no internet required after setup

---

## Requirements

### Hardware
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 16 GB | 16 GB+ |
| GPU VRAM | 6 GB | 8 GB |
| CPU | Any modern | Any modern |
| Microphone | Required | Required |

### Software
- Windows 11
- Python 3.10 or higher
- LM Studio
- VTube Studio (Steam)

---

## Installation

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/nika-companion.git
cd nika-companion
```

### Step 2 — Install Python dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If you get errors with `openai-whisper`, try:
> ```bash
> pip install openai-whisper --no-deps
> pip install tiktoken more-itertools
> ```

### Step 3 — Download Piper TTS voice model

Download both files from HuggingFace:
```
https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/amy/medium
```

Files needed:
- `en_US-amy-medium.onnx`
- `en_US-amy-medium.onnx.json`

Place them in:
```
C:\AI\VTubeModels\TTS\piper_voices\
```

Or change `VOICE_PATH` in `nika.py` to your preferred location.

### Step 4 — Install LM Studio

1. Download from [lmstudio.ai](https://lmstudio.ai)
2. Install and open LM Studio
3. Download a model — recommended: `gemma-3n-e4b` or `mistral-7b-instruct` (Q4)
4. Go to **Developer** tab → click **Start Server**
5. Confirm server is running on `http://localhost:1234`

### Step 5 — Install VTube Studio

1. Open Steam → search **VTube Studio** → Install (free)
2. Download a Live2D model from [booth.pm](https://booth.pm) (search: `Live2D model free`)
3. Unzip the model to `C:\AI\VTubeModels\`

---

## VTube Studio Setup

### Load your model
1. Launch VTube Studio → **Start without VR**
2. Click the **folder icon** → **Load Model**
3. Navigate to your model's `.model3.json` file

### Configure Lip Sync
1. Click the **gear icon** → Settings
2. Find **"Lip Sync"** section
3. Set:
   - Lip Sync Type: **Simple Lip Sync**
   - Use microphone: **ON**
   - Select your microphone from the dropdown
   - Sensitivity: **60–70%**
4. Find parameter **`MouthOpen`** in the Parameters list
5. Link it to **Lip Sync input**

### Test Lip Sync
- Speak into your microphone
- The **Live** column next to `MouthOpen` should move
- The model's mouth should open and close

---

## VB-Cable Setup (Optional — Better Lip Sync)

By default the model reacts to your microphone.
With VB-Cable the model reacts to **Nika's voice** instead — more natural.

### Install VB-Cable
1. Download from [vb-audio.com/Cable](https://vb-audio.com/Cable/)
2. Run installer as Administrator
3. Restart your computer

### Configure Windows Audio
1. Right-click speaker icon → **Sounds**
2. **Playback** tab → set **CABLE Input** as default device
3. Right-click **CABLE Input** → **Properties** → **Listen** tab
4. Check **"Listen to this device"**
5. Select your real speakers/headphones in the dropdown
6. Click OK

### Configure VTube Studio
1. Settings → Lip Sync
2. Microphone → select **"CABLE Output"**

Now Nika's voice drives the lip sync, and you still hear audio through your speakers.

---

## Configuration

Open `nika.py` and edit the settings at the top:

```python
# Path to your Piper voice model
VOICE_PATH = r"C:\AI\VTubeModels\TTS\piper_voices\en_US-amy-medium.onnx"

# LM Studio API (default port 1234)
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

# Wake word to activate Nika
WAKE_WORD = "nika"

# Seconds of silence before recording stops
SILENCE_SECONDS = 1.5

# Microphone sensitivity — raise if noisy environment (0.01–0.1)
SILENCE_THRESHOLD = 0.02
```

---

## Launch

### Option A — Automatic launcher (recommended)

1. Open `launch.bat` in a text editor
2. Set your paths:

```batch
set LM_STUDIO_PATH=C:\Program Files\LM Studio\LM Studio.exe
set VTUBE_PATH=C:\Program Files (x86)\Steam\steamapps\common\VTube Studio\VTube Studio.exe
set NIKA_SCRIPT=C:\AI\nika.py
```

3. Double-click `launch.bat`

The script will:
- Start LM Studio (waits 15 seconds for it to load)
- Start VTube Studio (waits 8 seconds)
- Start Nika

### Option B — Manual launch

Start in this order:

```
1. LM Studio → load model → Start Server
2. VTube Studio → load model → enable Lip Sync
3. python nika.py
```

---

## Usage

| Action | How |
|--------|-----|
| Start talking | Say **"Nika"** |
| Speak your message | Talk naturally, pause when done |
| Type instead | Type your message and press Enter |
| Reset conversation | Type `reset` + Enter |
| Exit | Type `quit` + Enter |

### Tips for better recognition
- Speak clearly when saying the wake word **"Nika"**
- Pause for ~1.5 seconds when you finish speaking
- Works with mixed Russian/English input
- Whisper auto-detects language — no need to switch modes

---

## Project Structure

```
nika-companion/
├── nika.py           # Main script
├── launch.bat        # Auto-launcher for all apps
├── requirements.txt  # Python dependencies
├── .gitignore
└── README.md
```

---

## Troubleshooting

### "LM Studio is not running"
- Make sure LM Studio server is started
- Check it runs on port `1234`
- Try: `curl http://localhost:1234/v1/models` in PowerShell

### Wake word not detected
- Raise microphone volume in Windows settings
- Lower `SILENCE_THRESHOLD` to `0.01` in `nika.py`
- Try saying "Ника" in Russian pronunciation

### Lip sync not working
- Check `MouthOpen` parameter is linked in VTube Studio
- Raise sensitivity to 70–80%
- Try VB-Cable method described above

### Audio is choppy or delayed
- Lower Whisper model size: change `whisper.load_model("base")` to `"tiny"`
- Reduce `max_tokens` to `150` in `nika.py`

### `wave.Error: # channels not specified`
- Use `wave.open()` not `open()` when writing WAV files
- This is handled correctly in the current version

---

## Hardware Notes

**Intel GPU users:** Whisper and Piper TTS run on CPU — Intel GPU is used only by LM Studio for the language model. This is the optimal split for 8GB VRAM.

**16GB RAM:** Sufficient for running all components simultaneously:
- LM Studio (7–8B model): ~8GB RAM
- Whisper base: ~1GB RAM  
- Piper TTS: ~200MB RAM
- VTube Studio: ~500MB RAM

---

## Roadmap

- [ ] Streaming TTS response (lower latency)
- [ ] Conversation history saved to file
- [ ] Custom wake word training
- [ ] VTube Studio API integration for expressions
- [ ] Support for multiple voice models

---

## License

MIT License — free to use, modify, and distribute.

---

## Acknowledgements

- [Piper TTS](https://github.com/rhasspy/piper) — fast local TTS
- [OpenAI Whisper](https://github.com/openai/whisper) — speech recognition
- [LM Studio](https://lmstudio.ai) — local LLM inference
- [VTube Studio](https://denchisoft.com) — Live2D avatar software
- Live2D models from [booth.pm](https://booth.pm)
