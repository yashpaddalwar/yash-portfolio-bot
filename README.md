# 🌟 Yash Paddalwar - LLM Chat Interface

This is a **Streamlit-based interactive chat interface** that allows users to have engaging conversations with a virtual assistant named *Yash Paddalwar*. The application uses **Groq's LLaMA 3.3 70B model** for generating intelligent responses and integrates **Langfuse** for observability and tracing of LLM interactions.

---

## 🚀 Features

- **Interactive Streamlit Chat UI**
- **Context-aware query rephrasing**
- **LLM-powered responses using Groq API (LLaMA 3.3 70B)**
- **Langfuse integration** for monitoring and tracing LLM requests
- Maintains conversation history across sessions
- Option to **clear chat** anytime

---

## 🧠 How It Works

1. Users interact via the chat input.
2. The last few chat messages are used to rephrase the current query using a prompt (`Prompts/rephrase.txt`).
3. A second prompt (`Prompts/main.txt`) is populated with info from `info.txt` and the rephrased query.
4. The query is sent to the Groq API using the LLaMA 3.3 70B model.
5. The assistant responds based on the prompt.
6. All interactions are traced with **Langfuse** for observability.

---

## 🧠 Powered By
- 🧠 Groq — LLM
- 🧪 Langfuse — Observability for LLM Apps
- 🎈 Streamlit — Interactive Python Apps in Seconds

✨ Author
Yash Paddalwar
🔗 https://www.linkedin.com/in/yashpaddalwar
🐍 AI & Data Science Professional | Generative AI & RAG Systems