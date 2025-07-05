# -----------------------------------------------------------------
# AI SCENARIO ENGINE v2.3 (Randomized Start)
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
PLAYER_3_MODEL = "novita/deepseek/deepseek-v3-0324"
# PLAYER_3_MODEL = "mistral/mistral-medium-2505"
PLAYER_3_PROMPT_FILE = "book/kairos.txt"

# --- File Paths ---
SCENARIO_PROMPT_FILE = "book2/book2_prompt.txt"
CONVERSATION_LOG_FILE = "book2/scifi4-conversation_log.txt"
SUMMARY_FILE = "book2/scifi4-summary.txt"
ARTIFACT_FILE = "book2/scifi4-artifact.txt"

# --- Conversation Parameters ---
# The simulation will run until a decision is reached or this turn limit is hit.
# A turn is one AI speaking. 3 players * 5 rounds = 15 turns.
TURN_LIMIT = 15 
MAX_OUTPUT_TOKENS = 4096

# -----------------------------------------------------------------
# IMPORTS & SETUP
# -----------------------------------------------------------------
import os
import random ### NEW ###
import anthropic
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

print("🚀 Starting AI Scenario Engine...")
load_dotenv()

# --- Client Configuration ---
try:
    claude_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    gemini_safety_settings = {'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE','HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE','HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE','HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'}
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    player_3_base_url = os.environ.get("OPPONENT_3_BASE_URL")
    player_3_api_key = os.environ.get("OPPONENT_3_API_KEY")
    if not player_3_base_url or not player_3_api_key:
        print(f"⚠️ WARNING: {PLAYER_3_NAME} credentials not found.")
        openai_client = None
    else:
        openai_client = OpenAI(base_url=player_3_base_url, api_key=player_3_api_key)
    print("✅ API clients configured.")
except Exception as e: print(f"❌ Error initializing API clients: {e}"); exit()

# -----------------------------------------------------------------
# HELPER & AI FUNCTIONS (No changes in this section)
# -----------------------------------------------------------------
def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f: return f.read().strip()
    except FileNotFoundError: print(f"❌ Error: File not found at '{filepath}'"); exit()

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f: f.write(content)
    print(f"✅ Content successfully written to '{filepath}'")

def format_full_log(history):
    log_string = ""
    for message in history:
        if message['role'] == 'user': log_string += f"PROMPT: {message['content']}\n\n"
        elif message['role'] == 'assistant': log_string += f"[{message['name']}]: {message['content']}\n\n"
    return log_string

def get_claude_response(system_prompt, conversation_history):
    messages = [{"role": m["role"], "content": m["content"]} for m in conversation_history]
    try:
        response = claude_client.messages.create(model=PLAYER_1_MODEL, max_tokens=MAX_OUTPUT_TOKENS, system=system_prompt, messages=messages)
        return response.content[0].text
    except Exception as e: return f"An error occurred ({PLAYER_1_NAME}): {e}"

def get_gemini_response(system_prompt, conversation_history):
    gemini_history = []
    for msg in conversation_history:
        role = "model" if msg["role"] == "assistant" else "user"
        content = f"[{msg['name']}]: {msg['content']}" if role == "model" else msg['content']
        gemini_history.append({"role": role, "parts": [content]})
    try:
        model = genai.GenerativeModel(PLAYER_2_MODEL, safety_settings=gemini_safety_settings, generation_config={"max_output_tokens": MAX_OUTPUT_TOKENS})
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(f"SYSTEM PROMPT: {system_prompt}. --- Now, continue the collaboration based on the last message.")
        return response.text
    except Exception as e: return f"An error occurred ({PLAYER_2_NAME}): {e}"

def get_openai_compatible_response(system_prompt, conversation_history):
    if not openai_client: return f"({PLAYER_3_NAME} is not configured.)"
    messages = [{"role": "system", "content": system_prompt}]
    for msg in conversation_history:
        content = f"[{msg['name']}]: {msg['content']}" if msg['role'] == 'assistant' else msg['content']
        messages.append({"role": msg["role"], "content": content})
    try:
        response = openai_client.chat.completions.create(model=PLAYER_3_MODEL, messages=messages, max_tokens=MAX_OUTPUT_TOKENS)
        return response.choices[0].message.content
    except Exception as e: return f"An error occurred ({PLAYER_3_NAME}): {e}"

def synthesize_world_description(full_log_text):
    print("\n🌍 Synthesizing final World Description...")
    prompt = ("You are a Worldbuilding Editor... (omitted for brevity)")
    try:
        model = genai.GenerativeModel(PLAYER_2_MODEL, safety_settings=gemini_safety_settings)
        return model.generate_content(prompt).text
    except Exception as e: return f"Could not synthesize World Description due to an error: {e}"

def synthesize_character_gallery(full_log_text):
    print("\n🎭 Synthesizing final Character Gallery...")
    prompt = ("You are a Casting Director... (omitted for brevity)")
    try:
        model = genai.GenerativeModel(PLAYER_2_MODEL, safety_settings=gemini_safety_settings)
        return model.generate_content(prompt).text
    except Exception as e: return f"Could not synthesize Character Gallery due to an error: {e}"

# -----------------------------------------------------------------
# MAIN EXECUTION LOGIC
# -----------------------------------------------------------------
def main():
    players = [
        {"name": PLAYER_1_NAME, "get_response": get_claude_response, "prompt": read_file(PLAYER_1_PROMPT_FILE)},
        {"name": PLAYER_2_NAME, "get_response": get_gemini_response, "prompt": read_file(PLAYER_2_PROMPT_FILE)},
        {"name": PLAYER_3_NAME, "get_response": get_openai_compatible_response, "prompt": read_file(PLAYER_3_PROMPT_FILE)}
    ]
    
    ### NEW/MODIFIED SECTION ###
    # Randomize the player order for each run to prevent first-speaker bias.
    random.shuffle(players)
    print(" randomize the order of the players.")
    
    # The rest of the setup remains the same
    player_prompts = {p["name"]: p["prompt"] for p in players}
    scenario_prompt = read_file(SCENARIO_PROMPT_FILE)
    print("✅ System and scenario prompts loaded.")
    
    # Announce the starting order
    starting_order = [p['name'] for p in players]
    print(f" randomised order is: {' -> '.join(starting_order)}")

    conversation_history = []
    
    print("-" * 50)
    print(f"🎬 SCENARIO:\n{scenario_prompt}")
    print("-" * 50)
    
    last_response = scenario_prompt
    turn_index = 0
    current_turn = 0
    
    while current_turn < TURN_LIMIT:
        current_turn += 1
        # The logic now uses the shuffled 'players' list
        current_player = players[turn_index]
        round_num = (current_turn - 1) // len(players) + 1
        
        print(f"\n[Round {round_num} | Turn {current_turn}/{TURN_LIMIT}] ✍️  {current_player['name']} is contributing...")
        
        conversation_history.append({"role": "user", "content": last_response})
        new_response = current_player["get_response"](current_player["prompt"], conversation_history)
        conversation_history.pop()
        
        conversation_history.append({"role": "assistant", "name": current_player['name'], "content": new_response})
        
        last_response = f"[{current_player['name']}]: {new_response}"
        print(f"\n>> {current_player['name']} says:\n{new_response}")
        
        lower_response = new_response.lower()
        termination_phrases = ["world is complete", "character gallery is final", "genesis complete", "the foundation is laid"]
        if any(phrase in lower_response for phrase in termination_phrases):
            print("\n" + "="*50)
            print("🏁 Creative session complete! Finalizing documents.")
            print("="*50 + "\n")
            break

        turn_index = (turn_index + 1) % len(players)
    
    if current_turn >= TURN_LIMIT:
        print("\n" + "="*50)
        print("🏁 Turn limit reached! The creative session has concluded.")
        print("="*50 + "\n")

    # The post-simulation analysis functions are renamed to match the script's purpose
    full_log = format_full_log(conversation_history)
    write_file(CONVERSATION_LOG_FILE, full_log)

    world_description = synthesize_world_description(full_log)
    write_file("book2/world4_description.txt", world_description) # Using simplified names directly
    
    character_gallery = synthesize_character_gallery(full_log)
    write_file("book2/character4_gallery.txt", character_gallery) # Using simplified names directly
    
    print("\n✅ Script finished successfully.")


if __name__ == "__main__":
    main()
