import streamlit as st
import os
from langfuse import Langfuse
from langfuse.decorators import observe
from groq import Groq
import os

os.environ["GROQ_API_KEY"] = "gsk_...."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-...."
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-...."
# 🇪🇺 EU region
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"


langfuse = Langfuse(
  secret_key="sk-lf-....",
  public_key="pk-lf-....",
  host="https://cloud.langfuse.com"
)



# Set page configuration
st.set_page_config(page_title="Chat Interface", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session state for chat history as a dictionary
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Main interface
st.title("🌟 Interact with Yash Paddalwar")
st.write("Engage in a delightful chat experience!")

# Function to rephrase the query based on chat history
def rephrase_query(current_query, chat_history):
    # Take the last four interactions from the chat history
    last_four = chat_history[-4:] if len(chat_history) >= 4 else chat_history

    # Create a string representation of the chat history
    history_str = ""
    for interaction in last_four:
        for role, content in interaction.items():
            history_str += f"{role}: {content}\n"

    # Load the rephrase prompt from the file
    with open("Prompts/rephrase.txt", "r") as file:
        rephrase_prompt = file.read()

    # Replace placeholders in the prompt
    rephrase_prompt = rephrase_prompt.replace("{previous_messages}", history_str)
    rephrase_prompt = rephrase_prompt.replace("{current_query}", current_query)

    # Call the LLM to rephrase the query
    client = Groq(api_key=os.environ['GROQ_API_KEY'])
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": rephrase_prompt
            }
        ],
        temperature=0.07,
        max_tokens=1024,
        top_p=1,
        stop=None,
    )

    r = completion.choices[0].message.content
    print("Rephrased: ",r)
    # Return the rephrased query
    return r


@observe()
def answer_llm(query):
    client = Groq(
        api_key = os.environ['GROQ_API_KEY']
    )

    with open("info.txt","r") as file:
        info = file.read()

    with open("Prompts/main.txt") as file:
        prompt = file.read()

    prompt = prompt.replace("{info}",info)
    prompt = prompt.replace("{query}",query)


    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.07,
        max_tokens=1024,
        top_p=1,
        stop=None,
    )

    return completion.choices[0].message.content


# Clear Chat button
if st.button("🧹 Clear Chat"):
    # Clear chat history
    st.session_state.messages.clear()
    st.session_state.chat_history.clear()

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Append the user's message to chat history
    st.session_state.messages.append(("user", prompt))
    st.session_state.chat_history.append({"user": prompt})

    # Rephrase the query if chat history is not empty
    if st.session_state.chat_history:
        rephrased_prompt = rephrase_query(prompt, st.session_state.chat_history)
    else:
        rephrased_prompt = prompt
    
    # Append the assistant's response to chat history
    with st.spinner("Yash is typing...."):
        response = answer_llm(rephrased_prompt)  # Simple echo for now
        st.session_state.messages.append(("assistant", response))
        st.session_state.chat_history.append({"assistant": response})

# Display chat history
for msg_type, content in st.session_state.messages:
    if msg_type == "user":
        st.chat_message("user").write(content)
    elif msg_type == "assistant":
        st.chat_message("assistant").write(content)
