import asyncio
import streamlit as st

from agent import ask_agent

st.set_page_config(
    page_title="User Management Assistant",
    page_icon="🤖",
)

st.title("🤖 User Management Assistant")

# Chat history
if "messages" not in st.session_state:

    
    st.session_state.messages = []

# Show previous conversation
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Ask something about users..."):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Running MCP Agent..."):

            response = asyncio.run(ask_agent(prompt))

        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
