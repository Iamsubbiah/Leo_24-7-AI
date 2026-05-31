# ==========================================
# app.py
# ==========================================

# Premium UI Layer
#
# Responsibilities:
# -----------------
# 1. Streamlit Interface
# 2. Multiple Chats
# 3. Chat History
# 4. Rename Chats
# 5. Delete Chats
# 6. Memory Integration
# 7. Streaming Responses
# 8. Context Building
#
# Main application entry point.


# ==========================================
# Imports
# ==========================================

import streamlit as st

from llm_handler import (
    APP_NAME,
    SYSTEM_PROMPT,
    build_context,
    stream_response
)

from chat_manager import (
    create_chat,
    load_all_chats,
    delete_chat,
    rename_chat,
    save_message,
    load_messages,
    load_recent_history,
    should_summarize,
    get_conversation_text,
    ensure_default_chat,
    update_chat_title,
    needs_auto_title,
    get_latest_chat_id
)

from memory_manager import (
    process_user_message,
    update_chat_summary,
    get_full_context,
    generate_chat_title
)


# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# Premium Styling
# ==========================================

st.markdown(
    """
<style>

section[data-testid="stSidebar"]{
    width:320px !important;
}

.block-container{
    padding-top:1rem;
}

div[data-testid="stChatMessage"]{
    border-radius:16px;
}

.stButton > button{
    border-radius:12px;
}

.chat-header{
    font-size:28px;
    font-weight:700;
    margin-bottom:10px;
}

</style>
""",
    unsafe_allow_html=True
)


# ==========================================
# Session State
# ==========================================

if "current_chat_id" not in st.session_state:

    st.session_state.current_chat_id = (
        ensure_default_chat()
    )

if "edit_chat_id" not in st.session_state:

    st.session_state.edit_chat_id = None


# ==========================================
# Load Chats
# ==========================================

chats = load_all_chats()


# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.markdown(
        """
        <div class="chat-header">
        🦁 LEO - 24/7 Trust
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "➕ New Chat",
        key="new_chat_btn",
        use_container_width=True
    ):

        create_chat(
            "Untitled Chat"
        )

        new_chat_id = (
            get_latest_chat_id()
        )

        st.session_state.current_chat_id = (
            new_chat_id
        )

        st.rerun()

    st.divider()

    st.caption(
        f"{len(chats)} Conversation(s)"
    )

    for chat in chats:

        chat_id = chat[0]

        chat_name = (chat[1].replace("Title:", "").replace("Title", "").strip())

        selected = (
            chat_id ==
            st.session_state.current_chat_id
        )

        display_name = chat_name

        if selected:

            display_name = (
                f"🟢 {chat_name}"
            )

        col1, col2 = st.columns(
            [9, 1]
        )

        with col1:

            if st.button(
                display_name,
                key=f"chat_{chat_id}",
                use_container_width=True
            ):

                st.session_state.current_chat_id = (
                    chat_id
                )

                st.rerun()

        with col2:

            with st.popover(
                "⋮"
            ):
                if st.button(
                    "Rename",
                    key=f"rename_btn_{chat_id}"
                ):

                    st.session_state.edit_chat_id = (
                        chat_id
                    )

                if st.button(
                    "Delete",
                    key=f"delete_btn_{chat_id}"
                ):

                    delete_chat(
                        chat_id
                    )

                    chats = load_all_chats()

                    if len(chats) > 0:

                        st.session_state.current_chat_id = (
                            chats[0][0]
                        )

                    st.rerun()

    # Rename Panel

    if (
        st.session_state.edit_chat_id
        is not None
    ):

        st.divider()

        st.markdown(
            "### ✏️ Rename Chat"
        )

        target_chat = None

        for chat in chats:

            if (
                chat[0]
                ==
                st.session_state.edit_chat_id
            ):

                target_chat = chat

                break

        if target_chat:

            current_name = (
                target_chat[1]
            )

            new_name = st.text_input(
                "Chat Name",
                value=current_name,
                key="rename_input"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Save",
                    key="save_rename"
                ):

                    if new_name.strip():

                        rename_chat(
                            st.session_state.edit_chat_id,
                            new_name.strip()
                        )

                    st.session_state.edit_chat_id = (
                        None
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "Cancel",
                    key="cancel_rename"
                ):

                    st.session_state.edit_chat_id = (
                        None
                    )

                    st.rerun()


# ==========================================
# Current Chat
# ==========================================

chat_id = (
    st.session_state.current_chat_id
)


# ==========================================
# Header
# ==========================================

st.markdown(
    """
    <div class="chat-header">
        🦁 LEO 
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Persistent Memory • Auto Titles • SQLite Storage • Phi-4 Mini"
)


# ==========================================
# Load Messages
# ==========================================

messages = load_messages(
    chat_id
)


# ==========================================
# Display History
# ==========================================


for role, content in messages:

    avatar = "🦁" if role == "assistant" else "👨‍💻"

    with st.chat_message(
        role,
        avatar=avatar
    ):

        st.markdown(content)


# ==========================================
# Chat Input
# ==========================================

prompt = st.chat_input(
    "Message Leo 🦁..."
)


# ==========================================
# Handle User Prompt
# ==========================================

if prompt:

    with st.chat_message(
        "user",
        avatar="👨‍💻"
    ):

        st.markdown(
            prompt
        )

    save_message(
        chat_id,
        "user",
        prompt
    )

    process_user_message(
        prompt
    )

    if should_summarize(
        chat_id
    ):

        conversation_text = (
            get_conversation_text(
                chat_id
            )
        )

        update_chat_summary(
            chat_id,
            conversation_text
        )
    # ==========================================
    # Load Memory Context
    # ==========================================

    memories, summary = (
        get_full_context(
            chat_id
        )
    )

    # ==========================================
    # Load Recent History
    # ==========================================

    recent_history = (
        load_recent_history(
            chat_id
        )
    )

    # ==========================================
    # Build Final Context
    # ==========================================

    final_context = (
        build_context(
            SYSTEM_PROMPT,
            memories,
            summary,
            recent_history,
            prompt
        )
    )

    # ==========================================
    # LLM Request
    # ==========================================

    llm_messages = [
        {
            "role": "user",
            "content": final_context
        }
    ]

    # ==========================================
    # Assistant Response
    # ==========================================

    with st.chat_message(
        "assistant",
        avatar="🦁"
    ):

        response_placeholder = (
            st.empty()
        )

        full_response = ""

        for token in stream_response(
            llm_messages
        ):

            full_response += token

            response_placeholder.markdown(
                full_response + "▌"
            )

        response_placeholder.markdown(
            full_response
        )

    # ==========================================
    # Save Assistant Response
    # ==========================================

    save_message(
        chat_id,
        "assistant",
        full_response
    )

    # ==========================================
    # Auto Title Generation
    # ==========================================

    if needs_auto_title(
        chat_id
    ):

        conversation_text = (
            get_conversation_text(
                chat_id
            )
        )

        title = generate_chat_title(
            conversation_text
        )

        title = (
            title
            .replace('"', '')
            .replace("'", "")
            .strip()
        )

        if len(title) > 50:

            title = title[:50]

        update_chat_title(
            chat_id,
            title
        )

    # ==========================================
    # Refresh UI
    # ==========================================

    st.rerun()


# ==========================================
# Footer
# ==========================================

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.caption(
        "💾 SQLite Memory 24/7 AI"
    )

with col2:

    st.caption(
        "🧠 Long-Term Context"
    )

with col3:

    st.caption(
        "⌛ Relaible & No Rate Limits"
    )

with col4:

    st.caption(
        "💗 Made By Subbiah C"
    )