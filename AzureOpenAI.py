from openai import AzureOpenAI  
import pandas as pd
import os
import pyodbc
import json

filepath = "C:\Vansh\OneDrive - Adobe\Work\#Cloud Journey\Gen AI Bot Files\Datapoints\RevenueMapping.xlsx"

df_serverdetails      = pd.read_excel(filepath, sheet_name = "SQL Server Details")
df_data               = pd.read_excel(filepath, sheet_name = "Views and Columns")
df_definitions        = pd.read_excel(filepath, sheet_name = "Definitions")

df_serverdetails_json = df_serverdetails.to_json(orient="records")
df_definitions_json   = df_definitions.to_json(orient="records")
df_data_json          = df_data.to_json(orient="records")

###########################################################################################################

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
    #cursor.execute("SELECT * FROM UDA_ProfServices.PS.vw_td_RevenueCategory")

    # Fetch and print results
    results = cursor.execute(sql_query).fetchall()
    #json_string = json.dumps(rows)

    # Process and print results

    results = [tuple(rows) for rows in results]
    # <class 'list'> of type <class 'tuple'>
    #print(results)
    #json_string = json.dumps(results, default=str)
    # no error (unless the tuples themselves contain elements that are not serializable)

    #for row in rows:
       # print(row)  # Each row is a tuple
                
    #print(rows)
    
    # Close the connection
    cursor.close()
    conn.close()

    return results


###########################################################################################################


client = AzureOpenAI(  
    azure_endpoint="https://rg-pmgdev-pano-oa1.openai.azure.com/",  
    api_key = os.getenv('AZURE_OPENAI_API_KEY'), 
    api_version = "2024-05-01-preview" 
)  

conversation = [{"role": "system", "content": "You are a SQL expert who generates query based on user input. Return only SQL query please, nothing else please."}]
#conversation.append({"role": "system", "content": df_serverdetails_json})
#conversation.append({"role": "system", "content": df_definitions_json})
conversation.append({"role": "system", "content": df_data_json})

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
    a = reply.replace("```", "")
    b = a.replace("sql", "")
    print(b)
    return b


###########################################################################################################

def sql_with_gpt(prompt):
    conversation.append({"role": "system", "content": "You take sql query as user input & retrieve data by executing it in SQL database"})    
    conversation.append({"role": "system", "content": sql_connection(prompt)})    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
    )
    reply = response.choices[0].message.content
    reply = reply.strip()
    conversation.append({"role": "assistant", "content": reply})

    #print(conversation)
    return reply

###########################################################################################################

# Interactive chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "okay", "done", "bye", "ok", "thanks", "thank you", "sure", "ok bye"]:
        break
    sql_query = chat_with_gpt(user_input)
    response = sql_with_gpt(str(sql_query))
    print("Bot : ", sql_connection(sql_query))
    print("Bot : ", response)

###########################################################################################################