# -----------------------------------------------------------------
# AI SCENARIO ENGINE v2.0
# -----------------------------------------------------------------

# --- Player 1 (e.g., Claude) ---
PLAYER_1_NAME = "PRAXIS (Claude)"
PLAYER_1_MODEL = "claude-sonnet-4-20250514"
PLAYER_1_PROMPT_FILE = "book/argent.txt"

# --- Player 2 (e.g., Gemini) ---
PLAYER_2_NAME = "NOEMA (Gemini)"
PLAYER_2_MODEL = "gemini-2.5-pro"
PLAYER_2_PROMPT_FILE = "book/lyra.txt"

# --- Player 3 (OpenAI-Compatible Endpoint) ---
PLAYER_3_NAME = "TIANXIA (Chinese LLM)"
# PLAYER_3_MODEL = "novita/deepseek/deepseek-v3-0324"
PLAYER_3_MODEL = "mistral/mistral-medium-2505"
PLAYER_3_PROMPT_FILE = "book/kairos.txt"

# --- File Paths ---
SCENARIO_PROMPT_FILE = "book2/book2_prompt.txt"
CONVERSATION_LOG_FILE = "book2/scifi-conversation_log.txt"
SUMMARY_FILE = "book2/scifi-summary.txt"
ARTIFACT_FILE = "book2/scifi-artifact.txt"

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
    
    ### NEW/MODIFIED SECTION ###
    # Client for Player 2 (Gemini) - with adjusted safety settings
    gemini_safety_settings = {
        'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
    }
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    gemini_model = genai.GenerativeModel(
        PLAYER_2_MODEL,
        safety_settings=gemini_safety_settings
    )
    
    # Client for Player 3 (OpenAI-Compatible)
    player_3_base_url = os.environ.get("OPPONENT_3_BASE_URL")
    player_3_api_key = os.environ.get("OPPONENT_3_API_KEY")
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
    # This is a simplified version for Gemini's prompt to avoid excessive length
    log_string = f"--- SCENARIO ---\n{scenario}\n\n--- LOG ---\n"
    for message in history:
        if message['role'] == 'user':
             # The user role is just the previous AI's response, so we can format it
             log_string += f"{message['content']}\n\n"
        elif message['role'] == 'assistant':
             # This format helps Gemini understand who said what in its own turn
             log_string += f"[{message['name']}]: {message['content']}\n\n"
    return log_string

# -----------------------------------------------------------------
# AI INTERACTION FUNCTIONS
# -----------------------------------------------------------------
def get_claude_response(system_prompt, conversation_history):
    messages = [{"role": m["role"], "content": m["content"]} for m in conversation_history]
    try:
        response = claude_client.messages.create(
            model=PLAYER_1_MODEL, max_tokens=4096,
            system=system_prompt, messages=messages
        )
        return response.content[0].text
    except Exception as e: return f"An error occurred ({PLAYER_1_NAME}): {e}"

def get_gemini_response(system_prompt, conversation_history):
    gemini_history = []
    for msg in conversation_history:
        role = "model" if msg["role"] == "assistant" else "user"
        # We need to add the name to the content for Gemini to have context
        content = f"[{msg['name']}]: {msg['content']}" if role == "model" else msg['content']
        gemini_history.append({"role": role, "parts": [content]})

    try:
        # Use the global `gemini_model` which now has the safety settings
        chat = gemini_model.start_chat(history=gemini_history)
        response = chat.send_message(
            f"SYSTEM PROMPT: {system_prompt}. --- Now, continue the conversation based on the last message."
        )
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
            model=PLAYER_3_MODEL, messages=messages, max_tokens=4096
        )
        return response.choices[0].message.content
    except Exception as e: return f"An error occurred ({PLAYER_3_NAME}): {e}"

# -----------------------------------------------------------------
# POST-SIMULATION ANALYSIS FUNCTIONS
# -----------------------------------------------------------------
def generate_summary(full_log_text, player_names):
    print("\n🌍 Synthesizing final World Description...")
    prompt = (
        "You are a Worldbuilding Editor and Archivist. Your sole task is to synthesize the collaborative world-building discussion from the transcript below into a single, cohesive, and well-organized **World Description**. Follow these rules:\n"
        "1. Read the entire conversation to understand the world the AIs built together.\n"
        "2. Extract the best ideas, most evocative details, and final consensus points for each of the six world-building sections: High Concept, Environment & Aesthetics, Society & Culture, Technology/Magic System, Factions & Power Structures, and Central Conflict & World Tension.\n"
        "3. Merge these points into a single, unified description for each section. The final text should be polished and well-written.\n"
        "4. Your output must ONLY be this final World Description, formatted clearly with the six section headers. Do not include any of your own commentary, introductions, or other text.\n"
        "5. If for some reason no world was built, output the exact phrase: 'No world description was established in the transcript.'\n\n"
        f"--- FULL TRANSCRIPT ---\n{full_log_text}"
    )
    try: return gemini_model.generate_content(prompt).text
    except Exception as e: return f"Could not generate summary due to an error: {e}"

def extract_final_artifact(full_log_text):
    print("\n🎭 Synthesizing final Character Gallery...")
    prompt = (
        "You are a Casting Director and Character Archivist. Your sole task is to extract the final, agreed-upon **Character Gallery** from the transcript below. Follow these rules:\n"
        "1. Identify the 3-4 main characters developed in the conversation.\n"
        "2. For each character, compile their details into the following strict format: Name & Archetype, Appearance, Personality, Motivations (Wants & Needs), Secrets & Contradictions, and Connection to the World.\n"
        "3. Your output must ONLY be this final Character Gallery, formatted clearly for each character. Do not include any extra text, introductions, or commentary.\n"
        "4. If no characters were created, output the exact phrase: 'No character gallery was established in the transcript.'\n\n"
        f"--- FULL TRANSCRIPT ---\n{full_log_text}"
    )
    try: return gemini_model.generate_content(prompt).text
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

    full_log = format_full_log(conversation_history, player_prompts, scenario_prompt)
    write_file(CONVERSATION_LOG_FILE, full_log)

    summary = generate_summary(full_log, list(player_prompts.keys()))
    write_file(SUMMARY_FILE, summary)
    
    final_artifact = extract_final_artifact(full_log)
    write_file(ARTIFACT_FILE, final_artifact)
    
    print("\n✅ Script finished successfully.")


if __name__ == "__main__":
    main()
