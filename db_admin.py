import sqlite3
import shutil

DATABASE_PATH = "chatbot.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def view_chats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM chats
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    print("\n===== CHATS =====\n")

    for row in rows:
        print(row)

    conn.close()


def view_messages():

    chat_id = input("Chat ID: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            message_id,
            role,
            content,
            timestamp
        FROM messages
        WHERE chat_id = ?
        ORDER BY timestamp
    """, (chat_id,))

    rows = cursor.fetchall()

    print("\n===== MESSAGES =====\n")

    for row in rows:

        print(f"\nMessage ID : {row[0]}")
        print(f"Role       : {row[1]}")
        print(f"Timestamp  : {row[3]}")
        print(f"\nContent:\n{row[2]}")
        print("-" * 60)

    conn.close()


def edit_message():

    message_id = input("Message ID: ")

    new_content = input(
        "New Content:\n"
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE messages
        SET content = ?
        WHERE message_id = ?
    """, (
        new_content,
        message_id
    ))

    conn.commit()
    conn.close()

    print("Message Updated")


def delete_message():

    message_id = input(
        "Message ID: "
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM messages
        WHERE message_id = ?
    """, (message_id,))

    conn.commit()
    conn.close()

    print("Message Deleted")


def view_memories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM memories
    """)

    rows = cursor.fetchall()

    print("\n===== MEMORIES =====\n")

    for row in rows:
        print(row)

    conn.close()


def edit_memory():

    memory_id = input(
        "Memory ID: "
    )

    new_fact = input(
        "New Fact:\n"
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE memories
        SET fact = ?
        WHERE memory_id = ?
    """, (
        new_fact,
        memory_id
    ))

    conn.commit()
    conn.close()

    print("Memory Updated")


def delete_memory():

    memory_id = input(
        "Memory ID: "
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM memories
        WHERE memory_id = ?
    """, (memory_id,))

    conn.commit()
    conn.close()

    print("Memory Deleted")


def backup_database():

    shutil.copy(
        DATABASE_PATH,
        "chatbot_backup.db"
    )

    print(
        "Backup Created"
    )


while True:

    print("""
=========================
LEO DB ADMIN
=========================

1. View Chats
2. View Messages
3. Edit Message
4. Delete Message

5. View Memories
6. Edit Memory
7. Delete Memory

8. Backup Database
9. Exit

=========================
""")

    choice = input(
        "Choice: "
    )

    if choice == "1":
        view_chats()

    elif choice == "2":
        view_messages()

    elif choice == "3":
        edit_message()

    elif choice == "4":
        delete_message()

    elif choice == "5":
        view_memories()

    elif choice == "6":
        edit_memory()

    elif choice == "7":
        delete_memory()

    elif choice == "8":
        backup_database()

    elif choice == "9":
        break

    else:
        print("Invalid Choice")