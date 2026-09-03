import os
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI


api_key = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(
    model= "gemini-3.5-flash",
    temperature = 1.0,
    max_retries = 2,
    google_api_key = api_key,
)

while True:
    print("\n======BEGIN SESSION=======\n")
    user_input = input("🤠: ").strip()

    if user_input.lower() in ("quit", "exit"):
        print("\n======FINNISH SESSION=======")
        break
    if not user_input:
        continue

    try:
        response = llm.invoke(user_input)
    except Exception as e:
        print(f"\nError calling the model: {e}\n")
        continue

    print(f"🤖: {response.text}\n")