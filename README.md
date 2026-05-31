# Leo_24/7-AI
# 🦁 LEO

**LEO (Learning and Execution Optimizer)** is a local AI assistant built on top of **Phi-4 Mini** that combines conversational intelligence with long-term memory, personalized interactions, conversation summaries, and multi-chat management.

Unlike a basic chatbot, LEO is designed to remember important information, maintain context across conversations, organize multiple chats, and provide a more personalized user experience.

---

# 🚀 Features

## 🧠 Long-Term Memory

LEO extracts important facts from conversations and stores them for future use.

Example:

User:

> My name is Subu.

Stored Memory:

> User name is Subu.

Later:

User:

> What's my name?

LEO:

> Your name is Subu.

---

## 💬 Persistent Chat History

All conversations are stored in SQLite and can be revisited at any time.

LEO remembers previous messages within a chat and uses them to maintain context.

---

## 📚 Conversation Summaries

When conversations become large, LEO automatically generates summaries.

This allows important information to be preserved while reducing context size.

Benefits:

* Better performance
* Lower context usage
* Improved long-term recall

---

## 🎯 Personalized Conversations

LEO adapts responses using:

* User preferences
* Stored memories
* Conversation history
* Existing summaries

This makes interactions more personalized over time.

---

## 🔍 Intelligent Memory Retrieval

LEO retrieves only relevant memories when generating responses.

Instead of loading all past conversations, it focuses on information related to the current topic.

---

## 🗂 Multi-Chat Management

Users can create and manage multiple independent conversations.

Examples:

* Python Learning
* AI Projects
* Personal Notes
* Interview Preparation

Each chat maintains its own history and summary.

---

## 🏷 Automatic Chat Titles

LEO automatically generates meaningful chat titles based on conversation content.

Example:

Conversation:

> How do I build a Streamlit chatbot?

Generated Title:

> Streamlit Chatbot Development

---

## ⚡ Real-Time Streaming Responses

Responses are streamed token-by-token, providing a modern conversational experience similar to popular AI assistants.

---

## 🔒 Local-First Privacy

All conversations, memories, and summaries are stored locally using SQLite.

No external databases are required.

Benefits:

* Privacy
* Offline capability
* Full ownership of data

---

# 🏗 System Architecture

LEO consists of four major modules.

## app.py

Main Streamlit user interface.

Responsibilities:

* Chat interface
* Sidebar management
* Chat selection
* Message display
* Streaming responses

---

## llm_handler.py

Core infrastructure layer.

Responsibilities:

* LM Studio communication
* Phi-4 Mini requests
* SQLite utilities
* Context construction
* Prompt management

---

## chat_manager.py

Conversation management layer.

Responsibilities:

* Create chats
* Store messages
* Load history
* Auto-title generation
* Token counting
* Summarization triggers

---

## memory_manager.py

Memory and knowledge layer.

Responsibilities:

* Memory extraction
* Memory storage
* Memory retrieval
* Conversation summaries
* Conflict resolution
* Context enrichment

---

# 🗄 Database Structure

LEO uses SQLite.

## chats

Stores chat metadata.

Fields:

* chat_id
* chat_name
* created_at

---

## messages

Stores conversation history.

Fields:

* message_id
* chat_id
* role
* content
* timestamp

---

## memories

Stores important extracted facts.

Fields:

* memory_id
* fact
* status
* importance
* created_at

---

## summaries

Stores conversation summaries.

Fields:

* chat_id
* summary
* updated_at

---

# 🔄 Response Pipeline

1. User sends message
2. Message saved to database
3. Memory extraction performed
4. Relevant memories retrieved
5. Conversation summary loaded
6. Recent chat history loaded
7. Context assembled
8. Phi-4 Mini generates response
9. Response streamed to user
10. Response saved to database
11. Chat title generated (if needed)

---

# 🧩 Technology Stack

## AI Model

* Phi-4 Mini

## LLM Runtime

* LM Studio

## Frontend

* Streamlit

## Database

* SQLite

## Language

* Python

---

# 📦 Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Run LEO:

```bash
python -m streamlit run app.py
```

---

# 📋 Requirements

* Python 3.10+
* LM Studio
* Phi-4 Mini
* Streamlit
* OpenAI Python SDK

---

# 👨‍💻 Author

**Subbiah**

AI/ML Developer

Creator of **🦁 LEO (Learning and Execution Optimizer)**

Powered by Phi-4 Mini.
