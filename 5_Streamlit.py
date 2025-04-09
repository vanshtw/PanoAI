





from openai import AzureOpenAI  
import pandas as pd
import os



client = AzureOpenAI(  
    azure_endpoint="https://rg-pmgdev-pano-oa1.openai.azure.com/",  
    api_key = os.getenv('AZURE_KEY'), 
    api_version = "2024-05-01-preview" 
)  

conversation = [{"role": "system", "content": "You are helpful bot"}]


###########################################################################################################

def chat_with_gpt(prompt):
    conversation.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )
    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})

    #print(reply)

    return reply


###########################################################################################################


###########################################################################################################

# Interactive chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "okay", "done", "bye", "ok", "thanks", "thank you", "sure", "ok bye"]:
        break
   
    response = chat_with_gpt(user_input)
    print("Bot : ", response)

###########################################################################################################
