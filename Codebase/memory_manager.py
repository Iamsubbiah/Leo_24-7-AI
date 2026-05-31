# ==========================================
# memory_manager.py
# ==========================================

# Memory & Knowledge Layer
#
# Responsibilities:
# -----------------
# 1. Long-Term Memory Extraction
# 2. Memory Storage
# 3. Memory Retrieval
# 4. Conversation Summaries
# 5. Summary Updates
# 6. Self-Correction
# 7. Conflict Resolution
#
# This module makes the chatbot
# capable of remembering users,
# projects, preferences and decisions.


# Import required functions.

from llm_handler import (
    execute_query,
    fetch_query,
    generate_memory_request,
    generate_response
)


# Extract important long-term memories.

def extract_memories(user_message):

    prompt = f"""
Extract only long-term useful memories.

Store:
- User names
- Preferences
- Goals
- Project decisions
- Important personal facts

Do not store:
- Greetings
- Small talk
- Temporary questions

Message:

{user_message}

Return one memory per line.

If nothing should be stored:

NONE
"""

    return generate_memory_request(
        prompt
    )


# Save memory.

def save_memory(
    fact,
    importance=1
):

    execute_query(
        """
        INSERT INTO memories(
            fact,
            status,
            importance
        )
        VALUES (?, ?, ?)
        """,
        (
            fact,
            "active",
            importance
        )
    )


# Load active memories.

def retrieve_memories():

    return fetch_query(
        """
        SELECT fact
        FROM memories
        WHERE status='active'
        ORDER BY importance DESC
        """
    )


# Convert memories into context text.

def retrieve_memory_text():

    memories = retrieve_memories()

    if not memories:

        return ""

    memory_text = ""

    for memory in memories:

        memory_text += (
            f"- {memory[0]}\n"
        )

    return memory_text


# Search memories.

def search_memories(keyword):

    return fetch_query(
        """
        SELECT fact
        FROM memories
        WHERE fact LIKE ?
        AND status='active'
        """,
        (
            f"%{keyword}%",
        )
    )


# Generate conversation summary.

def generate_summary(
    conversation_text
):

    prompt = f"""
Summarize the conversation.

Preserve:
- Names
- Preferences
- Decisions
- Goals
- Project Information

Conversation:

{conversation_text}
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    return generate_response(
        messages
    )


# Save summary.

def save_summary(
    chat_id,
    summary
):

    execute_query(
        """
        INSERT OR REPLACE INTO summaries(
            chat_id,
            summary
        )
        VALUES (?, ?)
        """,
        (
            chat_id,
            summary
        )
    )


# Load summary.

def load_summary(chat_id):

    result = fetch_query(
        """
        SELECT summary
        FROM summaries
        WHERE chat_id = ?
        """,
        (chat_id,)
    )

    if result:

        return result[0][0]

    return ""


# Convert summary into context text.

def retrieve_summary_text(
    chat_id
):

    summary = load_summary(
        chat_id
    )

    if not summary:

        return ""

    return summary


# Build memory and summary context.

def get_context_data(
    chat_id
):

    return {
        "memories":
            retrieve_memory_text(),

        "summary":
            retrieve_summary_text(
                chat_id
            )
    }


# Detect conflicting memories.

def detect_conflicts(
    old_fact,
    new_fact
):

    prompt = f"""
Old Fact:
{old_fact}

New Fact:
{new_fact}

Do these facts conflict?

Answer only:

YES

or

NO
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    result = generate_response(
        messages
    )

    return (
        "YES"
        in result.upper()
    )


# Resolve memory conflicts.

def resolve_conflicts(
    new_fact
):

    memories = retrieve_memories()

    for memory in memories:

        existing_fact = memory[0]

        if detect_conflicts(
            existing_fact,
            new_fact
        ):

            execute_query(
                """
                UPDATE memories
                SET status='obsolete'
                WHERE fact = ?
                """,
                (existing_fact,)
            )

    save_memory(
        new_fact
    )


# Update conversation summary.

def update_chat_summary(
    chat_id,
    conversation_text
):

    summary = generate_summary(
        conversation_text
    )

    save_summary(
        chat_id,
        summary
    )

# Get full memory and summary context.

def get_full_context(
    chat_id
):

    context = build_memory_context(
        chat_id
    )

    return (
        context["memories"],
        context["summary"]
    )
# Generate chat title from conversation.

def generate_chat_title(
    conversation_text
):

    prompt = f"""
Generate a concise title describing
the main topic of the conversation.

Rules:

- 2 to 4 words
- Use title case
- No quotes
- No punctuation
- Be specific
- Focus on the primary topic

Examples:

Conversation:
Why is the sky blue?

Title:
Why The Sky Is Blue

Conversation:
Help me build a Streamlit chatbot.

Title:
Building A Streamlit Chatbot

Conversation:
hey hi, how are you?

Title:
Casual Conversation

Conversation:

{conversation_text}
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    title = generate_response(
        messages
    )

    return title.strip()

# Build final memory context.

def build_memory_context(
    chat_id
):

    memories = (
        retrieve_memory_text()
    )

    summary = (
        retrieve_summary_text(
            chat_id
        )
    )

    return {
        "memories": memories,
        "summary": summary
    }

# Process user message and update memories.

def process_user_message(
    user_message
):

    extracted = extract_memories(
        user_message
    )

    lines = extracted.split(
        "\n"
    )

    for line in lines:

        fact = line.strip()

        if not fact:

            continue

        if (
            fact.upper()
            == "NONE"
        ):

            continue

        resolve_conflicts(
            fact
        )