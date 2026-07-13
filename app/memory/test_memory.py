from app.memory.conversation_memory import ConversationMemory


def test():

    session = "travel-session-001"

    ConversationMemory.save_message(
        session,
        "user",
        "Book a train from Bangalore to Shimoga"
    )

    ConversationMemory.save_message(
        session,
        "assistant",
        "Sure. Which date would you like to travel?"
    )

    messages = ConversationMemory.get_messages(session)

    print("\nConversation\n")

    for message in messages:
        print(message)

    ConversationMemory.clear(session)


if __name__ == "__main__":
    test()