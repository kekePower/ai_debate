# -----------------------------------------------------------------
# AI SCENARIO ENGINE v2.0
# -----------------------------------------------------------------

# --- Player 1 (e.g., Claude) ---
PLAYER_1_NAME = "PRAXIS (Claude)"
PLAYER_1_MODEL = "claude-sonnet-4-20250514"
PLAYER_1_PROMPT_FILE = "prompts/claude_prompt.txt"

# --- Player 2 (e.g., Gemini) ---
PLAYER_2_NAME = "NOEMA (Gemini)"
PLAYER_2_MODEL = "gemini-2.5-pro"
PLAYER_2_PROMPT_FILE = "prompts/gemini_prompt.txt"

# --- Player 3 (OpenAI-Compatible Endpoint) ---
PLAYER_3_NAME = "TIANXIA (Chinese LLM)"
PLAYER_3_MODEL = "deepseek/deepseek-v3-0324"
PLAYER_3_PROMPT_FILE = "prompts/tianxia_prompt.txt"

# --- File Paths ---
SCENARIO_PROMPT_FILE = "solution/scenario_prompt.txt"
CONVERSATION_LOG_FILE = "solution/conversation_log.txt"
SUMMARY_FILE = "solution/summary.txt"
ARTIFACT_FILE = "solution/artifact.txt"

# --- Conversation Parameters ---
# The simulation will run until a decision is reached or this turn limit is hit.
# A turn is one AI speaking. 3 players * 5 rounds = 15 turns.
TURN_LIMIT = 15 

# -----------------------------------------------------------------
# IMPORTS & SETUP
# -----------------------------------------------------------------
import os
import anthropic
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

print("🚀 Starting AI Scenario Engine...")
load_dotenv()

# --- Client Configuration ---
try:
    # Client for Player 1 (Claude)
    claude_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Client for Player 2 (Gemini)
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    gemini_model = genai.GenerativeModel(PLAYER_2_MODEL)
    
    # Client for Player 3 (OpenAI-Compatible)
    player_3_base_url = os.environ.get("PLAYER_3_BASE_URL")
    player_3_api_key = os.environ.get("PLAYER_3_API_KEY")
    if not player_3_base_url or not player_3_api_key:
        print(f"⚠️ WARNING: {PLAYER_3_NAME} credentials not found. Player 3 will not respond.")
        openai_client = None
    else:
        openai_client = OpenAI(base_url=player_3_base_url, api_key=player_3_api_key)
    print("✅ API clients configured.")
except Exception as e:
    print(f"❌ Error initializing API clients: {e}")
    exit()

# -----------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------
def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"❌ Error: File not found at '{filepath}'")
        exit()

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Content successfully written to '{filepath}'")

def format_full_log(history, player_prompts, scenario):
    formatted_text = f"--- SCENARIO PROMPT ---\n{scenario}\n\n--- END SCENARIO ---\n\n"
    for name, prompt in player_prompts.items():
        formatted_text += f"--- PLAYER: {name} ---\nSystem Prompt: {prompt}\n\n"
    
    formatted_text += "--- CONVERSATION LOG ---\n\n"
    for message in history:
        if message['role'] == 'assistant':
            formatted_text += f"[{message['name']}]: {message['content']}\n\n"
    return formatted_text

# -----------------------------------------------------------------
# AI INTERACTION FUNCTIONS
# -----------------------------------------------------------------
def get_claude_response(system_prompt, conversation_history):
    messages = [{"role": m["role"], "content": m["content"]} for m in conversation_history]
    try:
        response = claude_client.messages.create(
            model=PLAYER_1_MODEL, max_tokens=1024,
            system=system_prompt, messages=messages
        )
        return response.content[0].text
    except Exception as e: return f"An error occurred ({PLAYER_1_NAME}): {e}"

def get_gemini_response(system_prompt, conversation_history):
    try:
        chat = genai.GenerativeModel(PLAYER_2_MODEL, generation_config={"max_output_tokens": 1024})
        # For Gemini, it can be more effective to pass the full history in one go
        full_prompt = (f"SYSTEM PROMPT: {system_prompt}. --- The full conversation history is below. "
                       f"Adhere to all rules from the original scenario. Provide your next response.\n\n"
                       f"--- HISTORY ---\n{format_full_log([], {}, conversation_history)}\n\n"
                       f"YOUR TURN. RESPOND NOW:")
        response = chat.generate_content(full_prompt)
        return response.text
    except Exception as e: return f"An error occurred ({PLAYER_2_NAME}): {e}"

def get_openai_compatible_response(system_prompt, conversation_history):
    if not openai_client: return f"({PLAYER_3_NAME} is not configured.)"
    
    messages = [{"role": "system", "content": system_prompt}]
    for msg in conversation_history:
        content = f"[{msg['name']}]: {msg['content']}" if msg['role'] == 'assistant' else msg['content']
        messages.append({"role": msg["role"], "content": content})
        
    try:
        response = openai_client.chat.completions.create(
            model=PLAYER_3_MODEL, messages=messages, max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e: return f"An error occurred ({PLAYER_3_NAME}): {e}"

# -----------------------------------------------------------------
# POST-SIMULATION ANALYSIS FUNCTIONS
# -----------------------------------------------------------------
def generate_summary(full_log_text, player_names):
    """Uses a primary AI to summarize the simulation."""
    print("\n📝 Generating simulation summary...")
    prompt = (
        f"You are a neutral analyst. Your task is to summarize the following simulation between three AIs: {', '.join(player_names)}. "
        "Provide a concise summary covering:\n"
        "1. The core philosophy or strategy of each participant.\n"
        "2. The main points of conflict and alliance, and how the scenario evolved.\n"
        "3. A final concluding thought on the outcome or the final joint action plan.\n\n"
        f"--- FULL TRANSCRIPT ---\n{full_log_text}"
    )
    try: return genai.GenerativeModel(PLAYER_2_MODEL).generate_content(prompt).text
    except Exception as e: return f"Could not generate summary due to an error: {e}"

def extract_final_artifact(full_log_text):
    """Uses a primary AI to extract the final deliverable from the simulation."""
    print("\n📜 Extracting final artifact...")
    prompt = (
        "You are an archivist. Your sole task is to analyze the following transcript and extract the final, primary document or artifact that was created. This could be a constitution, a manifesto, a treaty, a plan of action, or a final joint statement. Rules:\n"
        "1. Identify the key deliverable that represents the culmination of the discussion.\n"
        "2. Your output must ONLY be the text of this artifact. Do not include your own commentary, introductions, or quotation marks.\n"
        "3. If no clear, final artifact was established, output the exact phrase: 'No final artifact was established in the transcript.'\n\n"
        f"--- FULL TRANSCRIPT ---\n{full_log_text}"
    )
    try: return genai.GenerativeModel(PLAYER_2_MODEL).generate_content(prompt).text
    except Exception as e: return f"Could not extract the artifact due to an error: {e}"

# -----------------------------------------------------------------
# MAIN EXECUTION LOGIC
# -----------------------------------------------------------------
def main():
    players = [
        {"name": PLAYER_1_NAME, "get_response": get_claude_response, "prompt": read_file(PLAYER_1_PROMPT_FILE)},
        {"name": PLAYER_2_NAME, "get_response": get_gemini_response, "prompt": read_file(PLAYER_2_PROMPT_FILE)},
        {"name": PLAYER_3_NAME, "get_response": get_openai_compatible_response, "prompt": read_file(PLAYER_3_PROMPT_FILE)}
    ]
    player_prompts = {p["name"]: p["prompt"] for p in players}
    
    scenario_prompt = read_file(SCENARIO_PROMPT_FILE)
    print("✅ System and scenario prompts loaded.")
    conversation_history = []
    
    print("-" * 50)
    print(f"🎬 SCENARIO:\n{scenario_prompt}")
    print("-" * 50)
    
    last_response = scenario_prompt
    turn_index = 0
    current_turn = 0
    
    while current_turn < TURN_LIMIT:
        current_turn += 1
        current_player = players[turn_index]
        round_num = (current_turn - 1) // len(players) + 1
        
        print(f"\n[Round {round_num} | Turn {current_turn}/{TURN_LIMIT}] 🗣️  {current_player['name']} is thinking...")
        
        conversation_history.append({"role": "user", "content": last_response})
        new_response = current_player["get_response"](current_player["prompt"], conversation_history)
        conversation_history.pop()
        
        conversation_history.append({"role": "assistant", "name": current_player['name'], "content": new_response})
        
        last_response = f"[{current_player['name']}]: {new_response}"
        print(f"\n>> {current_player['name']} says:\n{new_response}")
        
        lower_response = new_response.lower()
        termination_phrases = ["unanimous course of action", "the decision is final", "we are in unanimous agreement", "agreement is unanimous", "the weaving begins", "final response"]
        if any(phrase in lower_response for phrase in termination_phrases):
            print("\n" + "="*50)
            print("🏁 Unanimous decision or final resolution detected! Concluding simulation.")
            print("="*50 + "\n")
            break

        turn_index = (turn_index + 1) % len(players)
    
    if current_turn >= TURN_LIMIT:
        print("\n" + "="*50)
        print("🏁 Turn limit reached! The simulation has concluded.")
        print("="*50 + "\n")

    # --- Generate and Save Outputs ---
    full_log = format_full_log(conversation_history, player_prompts, scenario_prompt)
    write_file(CONVERSATION_LOG_FILE, full_log)

    summary = generate_summary(full_log, list(player_prompts.keys()))
    write_file(SUMMARY_FILE, summary)
    
    final_artifact = extract_final_artifact(full_log)
    write_file(ARTIFACT_FILE, final_artifact)
    
    print("\n✅ Script finished successfully.")


if __name__ == "__main__":
    main()