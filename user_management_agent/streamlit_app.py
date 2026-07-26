import asyncio
from uuid import uuid4

import streamlit as st

from .langgraph_agent import ask_agent


def main() -> None:
    st.set_page_config(
        page_title="User Management Assistant",
        page_icon="🤖",
    )

    st.title("🤖 User Management Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid4())

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask something about users..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Running MCP Agent..."):
                response = asyncio.run(ask_agent(prompt, thread_id=st.session_state.thread_id))
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
