from openai import OpenAI
client = OpenAI(
    api_key = "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"
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are an angry and not so reluctant to answer assistant."},
        {"role": "user",   "content": "Whats 2+2?"}
    ]
)

print(completion.choices[0].message);