# ==========================================
# llm_handler.py
# ==========================================

# Infrastructure & LLM Layer
#
# Responsibilities:
# -----------------
# 1. SQLite Database Operations
# 2. LM Studio Communication
# 3. Phi-4 Mini Requests
# 4. Context Building
# 5. Prompt Loading
# 6. Configuration
# 7. Response Streaming
#
# Every other module depends on this file.


# Import required libraries.

import sqlite3
from openai import OpenAI


# Database file location.
DATABASE_PATH = "chatbot.db"

# Loaded model name.
MODEL_NAME = "phi-4-mini-instruct"
APP_NAME = "LEO 🦁"

# LM Studio API endpoint.
LM_STUDIO_URL = "http://127.0.0.1:1234/v1"

# Required by OpenAI SDK.
API_KEY = "lm-studio"

# Model settings.
TEMPERATURE = 0.2
MAX_TOKENS = 1024

# Context settings.
MAX_CONTEXT_MESSAGES = 20


# Initialize LM Studio client.

client = OpenAI(
    base_url=LM_STUDIO_URL,
    api_key=API_KEY
)


# Create database connection.

def get_connection():

    return sqlite3.connect(DATABASE_PATH)


# Create required database tables.

def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # Create chats table.

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats(
            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create messages table.

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            role TEXT,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create memories table.

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories(
            memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT,
            status TEXT,
            importance INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create summaries table.

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries(
            chat_id INTEGER PRIMARY KEY,
            summary TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()  # Save database changes.

    conn.close()  # Close connection.


# Execute INSERT, UPDATE and DELETE queries.

def execute_query(query, params=()):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    conn.commit()

    conn.close()


# Execute SELECT queries.

def fetch_query(query, params=()):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return rows


# Load prompt from file.

def load_prompt(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()

# Default assistant behavior.

SYSTEM_PROMPT = """
You are 🦁 LEO (Learning and Execution Optimizer).
LEO is an AI assistant created by Subbiah, an AI/ML Developer.
Powered by Phi-4 Mini with:
• Memory
• Personalization
• Chat History
• Context Awareness
• Summaries
• Multi-Chat Support
• Memory Retrieval
• Local Privacy
Guidelines:
- Use memories when relevant.
- Use summaries when available.
- Respect user preferences.
- Be accurate, helpful, and concise.
- Never invent facts or memories.
- If uncertain, say so clearly.
When asked who you are:
"I am 🦁 LEO, an AI assistant created by Subbiah and powered by Phi-4 Mini."
When asked what powers you:
"I am powered by Phi-4 Mini and enhanced with memory, personalization, and context management."
Always identify yourself as 🦁 LEO."""
# Build final context for Phi-4.

def build_context(
    system_prompt,
    memories,
    summary,
    recent_messages,
    user_message
):

    history_text = ""

    for role, content in recent_messages:

        history_text += (
            f"{role}: {content}\n"
        )

    context = f"""
SYSTEM PROMPT
-------------
{system_prompt}

RELEVANT MEMORIES
-----------------
{memories}

CONVERSATION SUMMARY
--------------------
{summary}

RECENT HISTORY
--------------
{history_text}

CURRENT USER MESSAGE
--------------------
{user_message}
"""

    return context


# Generate complete response.

def generate_response(messages):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    return response.choices[0].message.content


# Stream response token by token.

def stream_response(messages):

    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        stream=True
    )

    for chunk in stream:

        delta = (
            chunk
            .choices[0]
            .delta
            .content
        )

        if delta:

            yield delta


# Generate summary using Phi-4.

def generate_summary_request(
    conversation_text
):

    messages = [
        {
            "role": "user",
            "content": conversation_text
        }
    ]

    return generate_response(
        messages
    )


# Generate memory extraction using Phi-4.

def generate_memory_request(
    prompt
):

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    return generate_response(
        messages
    )


# Verify LM Studio connection.

def test_connection():

    try:

        messages = [
            {
                "role": "user",
                "content": "Say hello."
            }
        ]

        response = generate_response(
            messages
        )

        return True

    except Exception:

        return False


# Create database tables on startup.

create_tables()