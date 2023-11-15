import os
import streamlit as st
from streamlit_chat import message
from src.agent.agent import Agent
import time


def get_topic(path):
    folder_list = os.listdir(path)
    topics = {}
    for folder in folder_list:
        unit_list = []
        folder_path = os.path.join(path, folder)
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            unit = file_name.split('.')[0]
            unit_list.append(unit)
        topics[folder] = unit_list
    return topics

topics = get_topic('src/data')
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
openai_key = "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"
st.session_state["agent"] = Agent(openai_api_key=openai_key)
selected_topic = st.selectbox(
    'Please select course!',
    list(sorted(topics.keys()))
)
option_unit = st.selectbox(
    'Please select unit!',
    sorted(topics[selected_topic])
)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.session_state["agent"].forget()  # to reset the knowledge base
st.session_state["messages"] = []
learning_unit = ""
if option_unit:
    learning_unit = option_unit
    file_selected = os.path.join('src/data', selected_topic , option_unit + '.pdf')
    st.session_state["agent"].ingest(file_selected)

if prompt := st.chat_input('Say something'):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("Teacher"):
    message_placeholder = st.empty()
    answer = ""
    full_response = ""
    if not prompt:
        if learning_unit:
            answer = f"Let's study the topic: {learning_unit}"
        else:
            answer = "Hi there, please select an unit top get started!"
    else:
        answer = st.session_state["agent"].ask(selected_topic, learning_unit ,prompt)
    for chunk in answer.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + " ")
    message_placeholder.markdown(full_response)

st.session_state.messages.append({"role": "Teacher", "content": full_response})