# ai_scenario_engine

A Python script for simulating a 3-way scenario between AI models (Claude, Gemini, and any OpenAI-compatible LLM). Easily customize prompts, models, and scenario files to experiment with different AI personalities and collaborative or adversarial tasks.

The whole project is quite a mess at the moment with tons of prompts, different Python scripts and so on, so I invite you to play with the scripts, add your own prompts and personas. Anything is possible and I invite you to experiment and have fun.

Just take a look at the scripts. They should be fairly self-explanatory and easy to use.
There is a small "bug" in `book2.py` where two of the files are hard-coded, so you need to change them to your own files. They're located close to the end of the file.

Contributions are always welcome! Just keep in mind that this is meant as a fun tool that *could* be helpful if you always keep the human-in-the-loop aspect in mind. The `personas` I created are quite... uhm... eccentric and I invite you to experiment with your own personas.

---

## How It Works

- **Three AI agents** ("PRAXIS"/Claude, "NOEMA"/Gemini, and "TIANXIA"/OpenAI-compatible) discuss and negotiate a scenario loaded from a prompt file.
- Each agent uses a custom system prompt (editable in the `prompts/` folder).
- The simulation proceeds in turns (one AI speaks per turn), ending early if a unanimous/final decision is detected (by key phrases such as "unanimous course of action", "the decision is final", etc.), or after a turn limit.
- Outputs include a transcript, a summary, and a final artifact (e.g., constitution, plan, or joint statement).

---

## Why Use Large Commercial Models?

Claude and Gemini were chosen as the primary Western models because they represent the best and most advanced large language models available today. While they may cost more to use, the investment is worth every cent: their depth of reasoning, language fluency, and the colorful, delightful quality of their responses create a dynamic and engaging simulation that smaller models simply cannot match.

---

## About "TIANXIA"

The "TIANXIA" player is powered by a Chinese-made LLM, providing a geopolitical counterbalance to the Western models and enabling a broader diversity of perspectives in the simulation.

**Implementation Note:**

For "TIANXIA", this project uses the DeepSeek V3-0324 model, with [Novita.ai](https://novita.ai/?ref=yjg5nja&utm_source=affiliate) as the inference provider. Novita.ai provides an OpenAI-compatible API, making integration straightforward while ensuring a robust Chinese LLM presence.

---

## Setup & Installation

1. **Clone the repo** and enter the directory.
2. **Install dependencies** (recommended: use a virtualenv):
   ```bash
   pip install -r requirements.txt
   ```
3. **Create and fill in your `.env` file** with:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_API_KEY=your_google_api_key
   PLAYER_3_BASE_URL=https://your-openai-compatible-endpoint.com/v1
   PLAYER_3_API_KEY=your_openai_compatible_api_key
   ```
   (If `PLAYER_3_BASE_URL` or `PLAYER_3_API_KEY` are missing, "TIANXIA" will not participate.)
4. **Edit scenario and prompts**:
   - Scenario: `solution/scenario_prompt.txt`
   - Prompts for each AI: `prompts/claude_prompt.txt`, `prompts/gemini_prompt.txt`, `prompts/tianxia_prompt.txt`

---

## Customization

- **Prompts:** Edit or add prompt files with any filenames you prefer. Update the script to point to your custom files.
- **Models:** Change the model names in `ai_scenario_engine.py` as desired.
- **Scenario:** Use any scenario file you like—add new scenario files and update the script to reference them.
- You are not limited to the provided files—add and reference your own files for maximum flexibility.

---

## Usage

```bash
python ai_scenario_engine.py
```

- The script prints progress and saves all logs and results in the `solution/` directory.
- Adjust the turn limit, model names, or file paths by editing `ai_scenario_engine.py`.

---

## Output Files

- `solution/conversation_log.txt`: Full simulation transcript.
- `solution/summary.txt`: Simulation summary.
- `solution/artifact.txt`: Extracted final artifact (e.g., constitution, plan, or joint statement).

---

## Requirements

- Python 3.8+
- Packages: `anthropic`, `google-generativeai`, `openai`, `python-dotenv`

---

## Scenario Engine Script Variants

This project contains several scenario engine scripts, each with a different focus and feature set:

### 1. `ai_scenario_engine.py` (Original)
- **Purpose:** Simulates a structured, multi-agent AI debate or scenario discussion, with three AI "players" (Claude, Gemini, and a third OpenAI-compatible LLM) taking turns to reach a consensus or produce a final artifact.
- **Player Order:** Fixed (Claude → Gemini → Tianxia).
- **Prompts/Outputs:** Uses prompts from the `prompts/` and scenario files from `solution/`. Outputs conversation logs, a summary, and a final artifact (e.g., a manifesto or treaty) in the `solution/` directory.
- **Use Case:** General AI debate or scenario simulation.

### 2. `book.py`
- **Purpose:** A creative variant focused on collaborative character/world-building, using three AI players with prompts and outputs tailored for fiction or RPG design.
- **Player Order:** Fixed.
- **Prompts/Outputs:** Uses prompts from the `book/` directory and scenario files from `book2/`. Outputs conversation logs, a summary, and a "Character Gallery" (detailed character profiles) in the `book2/` directory.
- **Special Features:**
  - Artifact extraction is tailored for character galleries.
  - Player 3 can use a Chinese LLM (Mistral or DeepSeek).
  - Adjusted safety settings for Gemini.
- **Use Case:** Collaborative fiction or RPG character/world design.

### 3. `book2.py`
- **Purpose:** A further creative variant with **randomized player order** for each run, designed to reduce first-speaker bias and add variety to the collaborative process.
- **Player Order:** Randomized at each run.
- **Prompts/Outputs:** Similar to `book.py`, but outputs include both a world description and a character gallery, written to the `book2/` directory with distinct file names.
- **Special Features:**
  - Randomizes player order at startup.
  - Different artifact/summary extraction functions, tailored for world-building.
  - Uses specific termination phrases and output file naming.
- **Use Case:** Dynamic, creative world/character-building with less predictable conversational flow.

---

### Usage Notes
- All scripts require valid API keys for Anthropic, Google Gemini, and (optionally) an OpenAI-compatible endpoint. Set these in your environment or `.env` file.
- To run a script, use:
  ```bash
  python ai_scenario_engine.py   # or book.py, or book2.py
  ```
- Output files are written to their respective directories (`solution/` or `book2/`).
- See comments in each script for more details on customization and output formats.

---

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file for details.