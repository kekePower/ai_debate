# ai_scenario_engine

A Python script for simulating a 3-way scenario between AI models (Claude, Gemini, and any OpenAI-compatible LLM). Easily customize prompts, models, and scenario files to experiment with different AI personalities and collaborative or adversarial tasks.

---

## How It Works

- **Three AI agents** ("PRAXIS"/Claude, "NOEMA"/Gemini, and "TIANXIA"/OpenAI-compatible) discuss and negotiate a scenario loaded from a prompt file.
- Each agent uses a custom system prompt (editable in the `prompts/` folder).
- The simulation cycles through a set number of turns, logging each response.
- The simulation ends if a unanimous/final decision is detected or after the turn limit.
- Outputs include a transcript, a summary, and a final artifact (e.g., constitution, plan, or joint statement).

---

## Environment Variables

Create a `.env` file in the project directory with the following variables:

```
# Claude (Anthropic)
ANTHROPIC_API_KEY=your_anthropic_api_key

# Gemini (Google)
GOOGLE_API_KEY=your_google_api_key

# OpenAI-Compatible LLM (e.g., DeepSeek, OpenRouter, etc)
PLAYER_3_BASE_URL=https://your-openai-compatible-endpoint.com/v1
PLAYER_3_API_KEY=your_openai_compatible_api_key
```

- If `PLAYER_3_BASE_URL` or `PLAYER_3_API_KEY` are missing, the script will run but "TIANXIA" will not participate.

---

## Setup & Installation

1. **Clone the repo** and enter the directory.
2. **Install dependencies** (recommended: use a virtualenv):
   ```bash
   pip install -r requirements.txt
   ```
3. **Create and fill in your `.env` file** as shown above.
4. **Edit scenario and prompts**:
   - Scenario: `solution/scenario_prompt.txt`
   - Prompts for each AI: `prompts/claude_prompt.txt`, `prompts/gemini_prompt.txt`, `prompts/tianxia_prompt.txt`

---

## Usage

```bash
python ai_scenario_engine.py
```

- The script prints progress and will stop early if a unanimous/final decision is reached, or continue until the turn limit (`TURN_LIMIT`) is hit.
- All logs and results are saved in the `solution/` directory.
- You can adjust the turn limit or model names by editing `ai_scenario_engine.py`.

---

## Simulation Logic & Termination

- The simulation proceeds in turns (one AI speaks per turn).
- The simulation ends if the AIs reach a unanimous or final decision (detected by key phrases such as "unanimous course of action", "the decision is final", "the weaving begins", etc.), or when the turn limit is reached.
- This allows for both decisive and stalemate outcomes, which are reflected in the outputs.

---

## Why Use Large Commercial Models?

Claude and Gemini were chosen as the primary Western models because they represent the best and most advanced large language models available today. While they may cost more to use, the investment is worth every cent: their depth of reasoning, language fluency, and the colorful, delightful quality of their responses create a dynamic and engaging simulation that smaller models simply cannot match. The interplay between these leading models ensures a level of insight, creativity, and debate quality that stands out in every scenario.

---

## About "TIANXIA"

The "TIANXIA" player is powered by a Chinese-made LLM. This was chosen intentionally to provide a geopolitical counterbalance to the Western models (Claude and Gemini), allowing for a broader diversity of perspectives in the simulation.

### Implementation Note

For "TIANXIA", this project uses the DeepSeek V3-0324 model, with [Novita.ai](https://novita.ai/?ref=yjg5nja&utm_source=affiliate) as the inference provider. Novita.ai provides an OpenAI-compatible API, making integration straightforward while ensuring a robust Chinese LLM presence in the simulation.

---

## Customization

- **Prompts**: Edit the files in `prompts/` to change each AI's personality or instructions.
- **Models**: Change the model names in `ai_debate.py` if you want to use different versions.
- **Scenario**: Change the scenario by editing `prompts/scenario_prompt.txt`.

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
