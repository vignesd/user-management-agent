import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client once
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="ChatGPT Chatbot", page_icon="🤖")

st.title("🤖 ChatGPT Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


def api_calling(messages):
    """Send the conversation history to OpenAI."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.5,
        max_tokens=1024,
    )

    return response.choices[0].message.content


# Display previous conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input (automatically clears after Enter)
if prompt := st.chat_input("Type your message..."):

    # Save and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = api_calling(st.session_state.messages)

        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

