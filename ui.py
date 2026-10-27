
# import streamlit as st
# import json
# from pathlib import Path
# from backend import get_response

# from tools import get_memories

# MEMORY_FILE = Path(__file__).with_name("memory.json")


# def load_saved_memories():
#     """Load persistent memories from memory.json."""
#     try:
#         with MEMORY_FILE.open("r", encoding="utf-8") as file:
#             data = json.load(file)

#         if isinstance(data, dict) and isinstance(
#             data.get("memories"), list
#         ):
#             return get_memories(data["memories"])

#     except (FileNotFoundError, json.JSONDecodeError):
#         pass

#     return []

# st.set_page_config(
#     page_title="DevMate AI",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# st.markdown("""
# <style>
# .stApp {
#     background: #0b1020;
#     color: #e5e7eb;
# }
# [data-testid="stSidebar"] {
#     background: #111827;
#     border-right: 1px solid #273449;
# }
# .hero {
#     padding: 24px;
#     border: 1px solid #29364b;
#     border-radius: 18px;
#     background: linear-gradient(135deg, #172554, #111827 70%);
#     margin-bottom: 24px;
# }
# .hero h1 {
#     color: #f8fafc;
#     margin-bottom: 8px;
# }
# .hero p {
#     color: #cbd5e1;
#     margin-bottom: 0;
# }
# .status {
#     display: inline-block;
#     padding: 5px 10px;
#     border-radius: 20px;
#     background: #12372b;
#     color: #86efac;
#     font-size: 13px;
# }
# [data-testid="stChatMessage"] {
#     border: 1px solid #293449;
#     border-radius: 14px;
#     padding: 12px;
#     background: #111827;
# }
# textarea {
#     color: #f8fafc !important;
# }
# </style>
# """, unsafe_allow_html=True)

# with st.sidebar:
#     st.markdown("## 🤖 DevMate AI")
#     st.caption("Your personal AI programming tutor")
#     st.divider()

#     st.markdown("### Navigation")
#     page = st.radio(
#         "Choose a page",
#         ["💬 Chat", "🧠 Memory", "⚙️ About"],
#         label_visibility="collapsed",
#     )

#     st.divider()
#     st.markdown("### System status")
#     st.success("UI running")
#     st.info("Offline demo mode")
#     st.caption("OpenAI integration: Coming later")

# st.markdown("""
# <div class="hero">
#     <span class="status">● SYSTEM ONLINE</span>
#     <h1>DevMate AI</h1>
#     <p>Your personal AI assistant for learning programming,
#     managing memories, and exploring agentic AI.</p>
# </div>
# """, unsafe_allow_html=True)

# if page == "💬 Chat":
#     st.subheader("Chat with your assistant")
#     st.caption("Ask questions, explore ideas, and learn something new.")

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     if st.button("＋ New conversation"):
#         st.session_state.messages = []
#         st.rerun()

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     question = st.chat_input("Message DevMate AI...")

#     if question:
#         st.session_state.messages.append(
#             {"role": "user", "content": question}
#         )

#         with st.chat_message("user"):
#             st.markdown(question)

#         with st.spinner("DevMate AI is thinking..."):
#             try:
#                 answer = get_response(question)
#             except Exception as error:
#                 answer = f"Sorry, something went wrong: {error}"

#                 st.session_state.messages.append(
#                     {"role": "assistant", "content": answer}
#                 )
#          with st.chat_message("assistant"):
#             st.markdown(answer)       





# elif page == "🧠 Memory":
#     st.subheader("Memory management")
#     st.caption("Manage DevMate AI's persistent memories.")

#     memories = load_saved_memories()

#     with st.form("add_memory_form"):
#         memory_type = st.selectbox(
#             "Memory type",
#             ["fact", "name", "preference"]
#         )
#         value = st.text_input("Memory content")

#         submitted = st.form_submit_button("Save memory")

#         if submitted:
#             if value.strip():
#                 new_memory = {
#     "type": memory_type,
#     "value": value.strip()
# }

# if new_memory not in memories:
#     memories.append(new_memory)
# else:
#     st.warning("This memory is already saved.")
#     st.stop()
                

#                 with MEMORY_FILE.open("w", encoding="utf-8") as file:
#                     json.dump({"memories": memories}, file, indent=2)

#                 st.success("Memory saved successfully!")
#                 st.rerun()
#             else:
#                 st.warning("Please enter memory content.")

#     st.divider()
#     st.metric("Saved memories", len(memories))

#     if memories:
#         options = {
#             f"{i + 1}. [{m.get('type', 'fact')}] {m.get('value', '')}": i
#             for i, m in enumerate(memories)
#         }

#         selected = st.selectbox(
#             "Select a memory to delete",
#             list(options.keys())
#         )

#         if st.button("Delete selected memory"):
#             memories.pop(options[selected])

#             with MEMORY_FILE.open("w", encoding="utf-8") as file:
#                 json.dump({"memories": memories}, file, indent=2)

#             st.success("Memory deleted.")
#             st.rerun()
#     else:
#         st.info("No saved memories yet.")



# elif page == "⚙️ About":
#     st.subheader("About DevMate AI")

#     st.markdown("""
#     **DevMate AI** is a personal AI assistant project built with Python.

#     **Current architecture**
#     - Python application and command router
#     - Reusable memory tools
#     - Persistent JSON memory
#     - Streamlit web interface

#     **Planned enhancements**
#     - Live backend integration
#     - Agent tool execution
#     - OpenAI-powered responses
#     - Improved memory management
#     """)

# st.divider()
# st.caption("DevMate AI • Built with Python and Streamlit")




import streamlit as st
import json
from pathlib import Path

from backend import get_response
from tools import get_memories


MEMORY_FILE = Path(__file__).with_name("memory.json")


def load_saved_memories():
    """Load persistent memories from memory.json."""
    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict) and isinstance(
            data.get("memories"), list
        ):
            return get_memories(data["memories"])

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return []


def save_saved_memories(memories):
    """Save memories to memory.json."""
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump({"memories": memories}, file, indent=2)


st.set_page_config(
    page_title="DevMate AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    .stApp {
        background: #0b1020;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #273449;
    }

    .hero {
        padding: 24px;
        border: 1px solid #29364b;
        border-radius: 18px;
        background: linear-gradient(135deg, #172554, #111827 70%);
        margin-bottom: 24px;
    }

    .hero h1 {
        color: #f8fafc;
        margin-bottom: 8px;
    }

    .hero p {
        color: #cbd5e1;
        margin-bottom: 0;
    }

    .status {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        background: #12372b;
        color: #86efac;
        font-size: 13px;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid #293449;
        border-radius: 14px;
        padding: 12px;
        background: #111827;
    }

    textarea {
        color: #f8fafc !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Sidebar
with st.sidebar:
    st.markdown("## 🤖 DevMate AI")
    st.caption("Your personal AI programming tutor")
    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "Choose a page",
        ["💬 Chat", "🧠 Memory", "⚙️ About"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### System status")
    st.success("UI running")
    st.info("Offline demo mode")
    st.caption("OpenAI integration: Coming later")


# Main header
st.markdown(
    """
    <div class="hero">
        <span class="status">● SYSTEM ONLINE</span>
        <h1>DevMate AI</h1>
        <p>
            Your personal AI assistant for learning programming,
            managing memories, and exploring agentic AI.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# Chat page
if page == "💬 Chat":
    st.subheader("Chat with your assistant")
    st.caption(
        "Ask questions, explore ideas, and learn something new."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("＋ New conversation"):
        st.session_state.messages = []
        st.rerun()

    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Receive user input
    question = st.chat_input("Message DevMate AI...")

    if question:
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        # Get a response from the Python backend
        with st.spinner("DevMate AI is thinking..."):
            try:
                answer = get_response(question)
            except Exception as error:
                answer = (
                    f"Sorry, something went wrong: {error}"
                )

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)


# Memory page
elif page == "🧠 Memory":
    st.subheader("Memory management")
    st.caption("Manage DevMate AI's persistent memories.")

    memories = load_saved_memories()

    # Add memory form
    with st.form("add_memory_form"):
        memory_type = st.selectbox(
            "Memory type",
            ["fact", "name", "preference"],
        )

        value = st.text_input("Memory content")

        submitted = st.form_submit_button("Save memory")

        if submitted:
            if not value.strip():
                st.warning("Please enter memory content.")
            else:
                new_memory = {
                    "type": memory_type,
                    "value": value.strip(),
                }

                if new_memory in memories:
                    st.warning("This memory is already saved.")
                else:
                    memories.append(new_memory)
                    save_saved_memories(memories)
                    st.success("Memory saved successfully!")
                    st.rerun()

    st.divider()

    # Display saved memories
    memories = load_saved_memories()
    st.metric("Saved memories", len(memories))

    if memories:
        options = {
            (
                f"{i + 1}. "
                f"[{memory.get('type', 'fact')}] "
                f"{memory.get('value', '')}"
            ): i
            for i, memory in enumerate(memories)
        }

        selected = st.selectbox(
            "Select a memory to delete",
            list(options.keys()),
        )

        if st.button("Delete selected memory"):
            memories.pop(options[selected])
            save_saved_memories(memories)

            st.success("Memory deleted.")
            st.rerun()

    else:
        st.info("No saved memories yet.")


# About page
elif page == "⚙️ About":
    st.subheader("About DevMate AI")

    st.markdown(
        """
        **DevMate AI** is a personal AI assistant project
        built with Python.

        **Current architecture**
        - Python application and command router
        - Reusable memory tools
        - Persistent JSON memory
        - Streamlit web interface
        - Python backend connected to the chat interface

        **Planned enhancements**
        - Agent tool execution
        - OpenAI-powered responses
        - Improved memory management
        """
    )


st.divider()
st.caption("DevMate AI • Built with Python and Streamlit")
