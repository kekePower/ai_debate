# ai_scenario_engine

A Python script for simulating a 3-way scenario between AI models (Claude, Gemini, and any OpenAI-compatible LLM). Easily customize prompts, models, and scenario files to experiment with different AI personalities and collaborative or adversarial tasks.

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

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file for details.