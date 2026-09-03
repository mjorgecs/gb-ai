import os
import sys

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage


def main():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY environment variable is not set.")
        print('Run: export GOOGLE_API_KEY="your-api-key-here"')
        sys.exit(1)

    print("Connecting to Gemini...")
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)
    except Exception as e:
        print(f"Failed to initialize model: {e}")
        sys.exit(1)

    print("Connected! Type your message below (or 'quit' to exit).\n")

    # Keep a running conversation history
    history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        history.append(HumanMessage(content=user_input))

        try:
            response = llm.invoke(history)
        except Exception as e:
            print(f"\nError calling the model: {e}\n")
            continue

        print(f"AI: {response.content}\n")
        history.append(AIMessage(content=response.content))


if __name__ == "__main__":
    main()