# ==========================================
# chat_manager.py
# ==========================================

# Conversation Management Layer
#
# Responsibilities:
# -----------------
# 1. Multiple Chats
# 2. Chat History
# 3. Message Storage
# 4. Recent History Retrieval
# 5. Token Counting
# 6. Summarization Triggers
#
# This module manages conversations only.
#
# It does NOT:
# - Talk to Phi-4
# - Generate Summaries
# - Extract Memories
#
# Those belong elsewhere.


# Import required functions.

from llm_handler import (
    execute_query,
    fetch_query,
    MAX_CONTEXT_MESSAGES
)


# Token threshold before summary update.

SUMMARY_THRESHOLD = 60000


# Create a new chat.

def create_chat(chat_name):

    execute_query(
        """
        INSERT INTO chats(chat_name)
        VALUES(?)
        """,
        (chat_name,)
    )


# Load all chats.

def load_all_chats():

    return fetch_query(
        """
        SELECT *
        FROM chats
        ORDER BY created_at DESC
        """
    )


# Rename existing chat.

def rename_chat(
    chat_id,
    new_name
):

    execute_query(
        """
        UPDATE chats
        SET chat_name = ?
        WHERE chat_id = ?
        """,
        (
            new_name,
            chat_id
        )
    )


# Delete chat and related data.

def delete_chat(chat_id):

    execute_query(
        """
        DELETE FROM messages
        WHERE chat_id = ?
        """,
        (chat_id,)
    )

    execute_query(
        """
        DELETE FROM summaries
        WHERE chat_id = ?
        """,
        (chat_id,)
    )

    execute_query(
        """
        DELETE FROM chats
        WHERE chat_id = ?
        """,
        (chat_id,)
    )


# Save message to database.

def save_message(
    chat_id,
    role,
    content
):

    execute_query(
        """
        INSERT INTO messages(
            chat_id,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            chat_id,
            role,
            content
        )
    )


# Load all messages.

def load_messages(chat_id):

    return fetch_query(
        """
        SELECT role, content
        FROM messages
        WHERE chat_id = ?
        ORDER BY timestamp ASC
        """,
        (chat_id,)
    )


# Load recent messages for context.

def load_recent_history(
    chat_id,
    limit=MAX_CONTEXT_MESSAGES
):

    rows = fetch_query(
        """
        SELECT role, content
        FROM messages
        WHERE chat_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (
            chat_id,
            limit
        )
    )

    return list(reversed(rows))


# Convert messages into OpenAI format.

def format_messages_for_llm(chat_id):

    messages = load_messages(
        chat_id
    )

    formatted = []

    for role, content in messages:

        formatted.append(
            {
                "role": role,
                "content": content
            }
        )

    return formatted


# Estimate token count.

def estimate_tokens(text):

    words = len(
        text.split()
    )

    return int(words * 1.3)


# Count total tokens in chat.

def count_chat_tokens(chat_id):

    messages = load_messages(
        chat_id
    )

    total_tokens = 0

    for role, content in messages:

        total_tokens += (
            estimate_tokens(
                content
            )
        )

    return total_tokens


# Check whether summarization is needed.

def should_summarize(chat_id):

    total_tokens = (
        count_chat_tokens(
            chat_id
        )
    )

    return (
        total_tokens
        >= SUMMARY_THRESHOLD
    )


# Get total message count.

def get_chat_message_count(
    chat_id
):

    result = fetch_query(
        """
        SELECT COUNT(*)
        FROM messages
        WHERE chat_id = ?
        """,
        (chat_id,)
    )

    return result[0][0]


# Get chat information.

def get_chat_info(chat_id):

    result = fetch_query(
        """
        SELECT *
        FROM chats
        WHERE chat_id = ?
        """,
        (chat_id,)
    )

    if result:

        return result[0]

    return None


# Get latest chat id.

def get_latest_chat_id():

    result = fetch_query(
        """
        SELECT chat_id
        FROM chats
        ORDER BY chat_id DESC
        LIMIT 1
        """
    )

    if result:

        return result[0][0]

    return None


# Create default chat if none exists.

def ensure_default_chat():

    chats = load_all_chats()

    if len(chats) == 0:

        create_chat(
            "New Chat"
        )

    return get_latest_chat_id()


# Build conversation text.

def get_conversation_text(
    chat_id
):

    messages = load_messages(
        chat_id
    )

    conversation = ""

    for role, content in messages:

        conversation += (
            f"{role}: {content}\n"
        )

    return conversation


# Get recent context text.

def get_recent_context_text(
    chat_id
):
    

    messages = (
        load_recent_history(
            chat_id
        )
    )

    context = ""

    for role, content in messages:

        context += (
            f"{role}: {content}\n"
        )

    return context
# Update chat title.

def update_chat_title(
    chat_id,
    title
):

    execute_query(
        """
        UPDATE chats
        SET chat_name = ?
        WHERE chat_id = ?
        """,
        (
            title,
            chat_id
        )
    )
# Check if automatic title generation is needed.

def needs_auto_title(
    chat_id
):

    chat_info = get_chat_info(
        chat_id
    )

    if not chat_info:

        return False

    chat_name = chat_info[1]

    if chat_name != "Untitled Chat":

        return False

    message_count = (
        get_chat_message_count(
            chat_id
        )
    )

    return message_count >= 2