from openai import AzureOpenAI
import os
import streamlit as st
import pyodbc
import json

client = AzureOpenAI(  
    azure_endpoint="https://rg-pmgdev-pano-oa1.openai.azure.com/",  
    api_key = os.getenv('AZURE_OPENAI_API_KEY'), 
    api_version = "2024-05-01-preview" 
)  


# Define connection parameters
server = 'OR1DRA851' 
database = 'Panoroma'

# Establish connection
conn = pyodbc.connect(f'DRIVER={{SQL Server}};'
                      f'SERVER={server};'
                      f'DATABASE={database};'
                      f'Trusted_Connection=yes;')

# Create a cursor object
cursor = conn.cursor()
sql__Query = "SELECT * FROM [panoai].[vw_tdContextMaster]"
cursor.execute(sql__Query)


# Streamlit UI
st.set_page_config(page_title="Pano AI", page_icon="🤖")
st.title("🤖 Pano AI ")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful chatbot."}]

# Chat input box
user_input = st.text_input("You:", "")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=st.session_state.messages
    )

    bot_response = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Display chat history
    for message in st.session_state.messages[1:]:
        role = "User" if message["role"] == "user" else "Bot"
        st.write(f"**{role}:** {message['content']}")

# Add a "Clear Chat" button
if st.button("Clear Chat"):
    st.session_state.messages = [{"role": "system", "content": "You are a helpful chatbot."}]
    st.rerun()


