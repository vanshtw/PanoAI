from openai import OpenAI
import os

client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)

def chat_with_gpt(prompt):
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": prompt
        }
    ]
    )
    return completion.choices[0].message.content

user_input = input("You: ");
response = chat_with_gpt(user_input);
print(response)
