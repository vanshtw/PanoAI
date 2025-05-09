from openai import AzureOpenAI 
import os
import streamlit as st

client = AzureOpenAI(  
    azure_endpoint="https://rg-pmgdev-pano-oa1.openai.azure.com/",  
    api_key = os.getenv('AZURE_KEY'), 
    api_version = "2024-05-01-preview" 
)  

# Streamlit UI
st.set_page_config(page_title="Pano AI", page_icon="🤖")
st.title("🤖 Pano AI via OpenAI")

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


