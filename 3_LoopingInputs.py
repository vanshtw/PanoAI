from openai import OpenAI
import os

#from dotenv import load_dotenv
#load_dotenv()

client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [{"role": "system", "content": "You are a helpful chatbot."},
                    {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Interactive chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "okay", "done", "bye", "ok", "thanks", "thank you", "sure", "ok bye"]:
        break
    response = chat_with_gpt(user_input)
    print("Bot:", response)
