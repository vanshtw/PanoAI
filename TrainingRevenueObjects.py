import pandas as pd
from openai import OpenAI
import os
import pyodbc

#import socket
#socket.getaddrinfo('localhost', 8080)
#from dotenv import load_dotenv
#load_dotenv()

filepath = "C:\Vansh\OneDrive - Adobe\Work\#Cloud Journey\Gen AI Bot Files\Datapoints\RevenueMapping.xlsx"

df_serverdetails      = pd.read_excel(filepath, sheet_name = "SQL Server Details")
df_data               = pd.read_excel(filepath, sheet_name = "Views and Columns")
df_definitions        = pd.read_excel(filepath, sheet_name = "Definitions")

df_serverdetails_json = df_serverdetails.to_json(orient="records")
df_definitions_json   = df_definitions.to_json(orient="records")
df_data_json          = df_data.to_json(orient="records")

###########################################################################################################
'''
def sql_connection(sql_query):

    # Define connection parameters
    server = 'OR1DRA862' 
    database = 'UDA_ProfServices'

    # Establish connection
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};'
                      f'SERVER={server};'
                      f'DATABASE={database};'
                      f'Trusted_Connection=yes;')

    # Create a cursor object
    cursor = conn.cursor()

    # Execute a query
    cursor.execute(sql_query)
    #cursor.execute("SELECT * FROM UDA_ProfServices.PS.vw_td_RevenueCategory")

    # Fetch and print results
    rows = cursor.fetchall()

    # Process and print results
    #for row in rows:
        #print(row)  # Each row is a tuple
        
    print(rows)

    # Close the connection
    cursor.close()
    conn.close()

'''
###########################################################################################################

client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)
conversation = [{"role": "system", "content": "You are a helpful chatbot who answers in concise manner."}]
#conversation.append({"role": "system", "content": df_serverdetails_json})
#conversation.append({"role": "system", "content": df_definitions_json})
conversation.append({"role": "system", "content": df_data_json})
#conversation.append({"role": "system", "content": sql_connection("SELECT 100")})

###########################################################################################################

def chat_with_gpt(prompt):
    conversation.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )
    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})

    #print(conversation)
    return reply

###########################################################################################################

# Interactive chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "okay", "done", "bye", "ok", "thanks", "thank you", "sure", "ok bye"]:
        break
    response = chat_with_gpt(user_input)
    print("Bot:", response)

###########################################################################################################