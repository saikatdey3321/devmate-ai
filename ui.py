
# # import streamlit as st
# # import json
# # from pathlib import Path
# # from backend import get_response

# # from tools import get_memories

# # MEMORY_FILE = Path(__file__).with_name("memory.json")


# # def load_saved_memories():
# #     """Load persistent memories from memory.json."""
# #     try:
# #         with MEMORY_FILE.open("r", encoding="utf-8") as file:
# #             data = json.load(file)

# #         if isinstance(data, dict) and isinstance(
# #             data.get("memories"), list
# #         ):
# #             return get_memories(data["memories"])

# #     except (FileNotFoundError, json.JSONDecodeError):
# #         pass

# #     return []

# # st.set_page_config(
# #     page_title="DevMate AI",
# #     page_icon="🤖",
# #     layout="wide",
# #     initial_sidebar_state="expanded",
# # )

# # st.markdown("""
# # <style>
# # .stApp {
# #     background: #0b1020;
# #     color: #e5e7eb;
# # }
# # [data-testid="stSidebar"] {
# #     background: #111827;
# #     border-right: 1px solid #273449;
# # }
# # .hero {
# #     padding: 24px;
# #     border: 1px solid #29364b;
# #     border-radius: 18px;
# #     background: linear-gradient(135deg, #172554, #111827 70%);
# #     margin-bottom: 24px;
# # }
# # .hero h1 {
# #     color: #f8fafc;
# #     margin-bottom: 8px;
# # }
# # .hero p {
# #     color: #cbd5e1;
# #     margin-bottom: 0;
# # }
# # .status {
# #     display: inline-block;
# #     padding: 5px 10px;
# #     border-radius: 20px;
# #     background: #12372b;
# #     color: #86efac;
# #     font-size: 13px;
# # }
# # [data-testid="stChatMessage"] {
# #     border: 1px solid #293449;
# #     border-radius: 14px;
# #     padding: 12px;
# #     background: #111827;
# # }
# # textarea {
# #     color: #f8fafc !important;
# # }
# # </style>
# # """, unsafe_allow_html=True)

# # with st.sidebar:
# #     st.markdown("## 🤖 DevMate AI")
# #     st.caption("Your personal AI programming tutor")
# #     st.divider()

# #     st.markdown("### Navigation")
# #     page = st.radio(
# #         "Choose a page",
# #         ["💬 Chat", "🧠 Memory", "⚙️ About"],
# #         label_visibility="collapsed",
# #     )

# #     st.divider()
# #     st.markdown("### System status")
# #     st.success("UI running")
# #     st.info("Offline demo mode")
# #     st.caption("OpenAI integration: Coming later")

# # st.markdown("""
# # <div class="hero">
# #     <span class="status">● SYSTEM ONLINE</span>
# #     <h1>DevMate AI</h1>
# #     <p>Your personal AI assistant for learning programming,
# #     managing memories, and exploring agentic AI.</p>
# # </div>
# # """, unsafe_allow_html=True)

# # if page == "💬 Chat":
# #     st.subheader("Chat with your assistant")
# #     st.caption("Ask questions, explore ideas, and learn something new.")

# #     if "messages" not in st.session_state:
# #         st.session_state.messages = []

# #     if st.button("＋ New conversation"):
# #         st.session_state.messages = []
# #         st.rerun()

# #     for message in st.session_state.messages:
# #         with st.chat_message(message["role"]):
# #             st.markdown(message["content"])

# #     question = st.chat_input("Message DevMate AI...")

# #     if question:
# #         st.session_state.messages.append(
# #             {"role": "user", "content": question}
# #         )

# #         with st.chat_message("user"):
# #             st.markdown(question)

# #         with st.spinner("DevMate AI is thinking..."):
# #             try:
# #                 answer = get_response(question)
# #             except Exception as error:
# #                 answer = f"Sorry, something went wrong: {error}"

# #                 st.session_state.messages.append(
# #                     {"role": "assistant", "content": answer}
# #                 )
# #          with st.chat_message("assistant"):
# #             st.markdown(answer)       





# # elif page == "🧠 Memory":
# #     st.subheader("Memory management")
# #     st.caption("Manage DevMate AI's persistent memories.")

# #     memories = load_saved_memories()

# #     with st.form("add_memory_form"):
# #         memory_type = st.selectbox(
# #             "Memory type",
# #             ["fact", "name", "preference"]
# #         )
# #         value = st.text_input("Memory content")

# #         submitted = st.form_submit_button("Save memory")

# #         if submitted:
# #             if value.strip():
# #                 new_memory = {
# #     "type": memory_type,
# #     "value": value.strip()
# # }

# # if new_memory not in memories:
# #     memories.append(new_memory)
# # else:
# #     st.warning("This memory is already saved.")
# #     st.stop()
                

# #                 with MEMORY_FILE.open("w", encoding="utf-8") as file:
# #                     json.dump({"memories": memories}, file, indent=2)

# #                 st.success("Memory saved successfully!")
# #                 st.rerun()
# #             else:
# #                 st.warning("Please enter memory content.")

# #     st.divider()
# #     st.metric("Saved memories", len(memories))

# #     if memories:
# #         options = {
# #             f"{i + 1}. [{m.get('type', 'fact')}] {m.get('value', '')}": i
# #             for i, m in enumerate(memories)
# #         }

# #         selected = st.selectbox(
# #             "Select a memory to delete",
# #             list(options.keys())
# #         )

# #         if st.button("Delete selected memory"):
# #             memories.pop(options[selected])

# #             with MEMORY_FILE.open("w", encoding="utf-8") as file:
# #                 json.dump({"memories": memories}, file, indent=2)

# #             st.success("Memory deleted.")
# #             st.rerun()
# #     else:
# #         st.info("No saved memories yet.")



# # elif page == "⚙️ About":
# #     st.subheader("About DevMate AI")

# #     st.markdown("""
# #     **DevMate AI** is a personal AI assistant project built with Python.

# #     **Current architecture**
# #     - Python application and command router
# #     - Reusable memory tools
# #     - Persistent JSON memory
# #     - Streamlit web interface

# #     **Planned enhancements**
# #     - Live backend integration
# #     - Agent tool execution
# #     - OpenAI-powered responses
# #     - Improved memory management
# #     """)

# # st.divider()
# # st.caption("DevMate AI • Built with Python and Streamlit")




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


# def save_saved_memories(memories):
#     """Save memories to memory.json."""
#     with MEMORY_FILE.open("w", encoding="utf-8") as file:
#         json.dump({"memories": memories}, file, indent=2)


# st.set_page_config(
#     page_title="DevMate AI",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )


# st.markdown(
#     """
#     <style>
#     .stApp {
#         background: #0b1020;
#         color: #e5e7eb;
#     }

#     [data-testid="stSidebar"] {
#         background: #111827;
#         border-right: 1px solid #273449;
#     }

#     .hero {
#         padding: 24px;
#         border: 1px solid #29364b;
#         border-radius: 18px;
#         background: linear-gradient(135deg, #172554, #111827 70%);
#         margin-bottom: 24px;
#     }

#     .hero h1 {
#         color: #f8fafc;
#         margin-bottom: 8px;
#     }

#     .hero p {
#         color: #cbd5e1;
#         margin-bottom: 0;
#     }

#     .status {
#         display: inline-block;
#         padding: 5px 10px;
#         border-radius: 20px;
#         background: #12372b;
#         color: #86efac;
#         font-size: 13px;
#     }

#     [data-testid="stChatMessage"] {
#         border: 1px solid #293449;
#         border-radius: 14px;
#         padding: 12px;
#         background: #111827;
#     }

#     textarea {
#         color: #f8fafc !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # Sidebar
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


# # Main header
# st.markdown(
#     """
#     <div class="hero">
#         <span class="status">● SYSTEM ONLINE</span>
#         <h1>DevMate AI</h1>
#         <p>
#             Your personal AI assistant for learning programming,
#             managing memories, and exploring agentic AI.
#         </p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )


# # Chat page
# if page == "💬 Chat":
#     st.subheader("Chat with your assistant")
#     st.caption(
#         "Ask questions, explore ideas, and learn something new."
#     )

#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     if st.button("＋ New conversation"):
#         st.session_state.messages = []
#         st.rerun()

#     # Display conversation history
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Receive user input
#     question = st.chat_input("Message DevMate AI...")

#     if question:
#         st.session_state.messages.append(
#             {"role": "user", "content": question}
#         )

#         with st.chat_message("user"):
#             st.markdown(question)

#         # Get a response from the Python backend
#         with st.spinner("DevMate AI is thinking..."):
#             try:
#                 answer = get_response(question)
#             except Exception as error:
#                 answer = (
#                     f"Sorry, something went wrong: {error}"
#                 )

#         st.session_state.messages.append(
#             {"role": "assistant", "content": answer}
#         )

#         with st.chat_message("assistant"):
#             st.markdown(answer)


# # Memory page
# elif page == "🧠 Memory":
#     st.subheader("Memory management")
#     st.caption("Manage DevMate AI's persistent memories.")

#     memories = load_saved_memories()

#     # Add memory form
#     with st.form("add_memory_form"):
#         memory_type = st.selectbox(
#             "Memory type",
#             ["fact", "name", "preference"],
#         )

#         value = st.text_input("Memory content")

#         submitted = st.form_submit_button("Save memory")

#         if submitted:
#             if not value.strip():
#                 st.warning("Please enter memory content.")
#             else:
#                 new_memory = {
#                     "type": memory_type,
#                     "value": value.strip(),
#                 }

#                 if new_memory in memories:
#                     st.warning("This memory is already saved.")
#                 else:
#                     memories.append(new_memory)
#                     save_saved_memories(memories)
#                     st.success("Memory saved successfully!")
#                     st.rerun()

#     st.divider()

#     # Display saved memories
#     memories = load_saved_memories()
#     st.metric("Saved memories", len(memories))

#     if memories:
#         options = {
#             (
#                 f"{i + 1}. "
#                 f"[{memory.get('type', 'fact')}] "
#                 f"{memory.get('value', '')}"
#             ): i
#             for i, memory in enumerate(memories)
#         }

#         selected = st.selectbox(
#             "Select a memory to delete",
#             list(options.keys()),
#         )

#         if st.button("Delete selected memory"):
#             memories.pop(options[selected])
#             save_saved_memories(memories)

#             st.success("Memory deleted.")
#             st.rerun()

#     else:
#         st.info("No saved memories yet.")


# # About page
# elif page == "⚙️ About":
#     st.subheader("About DevMate AI")

#     st.markdown(
#         """
#         **DevMate AI** is a personal AI assistant project
#         built with Python.

#         **Current architecture**
#         - Python application and command router
#         - Reusable memory tools
#         - Persistent JSON memory
#         - Streamlit web interface
#         - Python backend connected to the chat interface

#         **Planned enhancements**
#         - Agent tool execution
#         - OpenAI-powered responses
#         - Improved memory management
#         """
#     )


# st.divider()
# st.caption("DevMate AI • Built with Python and Streamlit")


# import streamlit as st
# import json
# from pathlib import Path

# from backend import get_response, reset_conversation
# from tools import get_memories
# from app import get_ai_mode


# # ==================================================
# # CONFIGURATION
# # ==================================================

# MEMORY_FILE = Path(__file__).with_name("memory.json")

# st.set_page_config(
#     page_title="DevMate AI",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )


# # ==================================================
# # MEMORY FUNCTIONS
# # ==================================================

# def load_saved_memories():
#     """Load persistent memories."""

#     try:
#         with MEMORY_FILE.open("r", encoding="utf-8") as file:
#             data = json.load(file)

#         if isinstance(data, dict) and isinstance(data.get("memories"), list):
#             return get_memories(data["memories"])

#     except (FileNotFoundError, json.JSONDecodeError):
#         pass

#     return []


# def save_saved_memories(memories):
#     """Save persistent memories."""

#     with MEMORY_FILE.open("w", encoding="utf-8") as file:
#         json.dump(
#             {"memories": memories},
#             file,
#             indent=2,
#             ensure_ascii=False,
#         )


# # ==================================================
# # SESSION STATE
# # ==================================================

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "active_page" not in st.session_state:
#     st.session_state.active_page = "Chat"


# # ==================================================
# # CUSTOM CSS
# # ==================================================

# st.markdown(
#     """
#     <style>
#     .stApp {
#         background-color: #0b1020;
#         color: #e5e7eb;
#     }

#     [data-testid="stSidebar"] {
#         background-color: #111827;
#         border-right: 1px solid #293449;
#     }

#     .hero {
#         padding: 25px;
#         border: 1px solid #29364b;
#         border-radius: 18px;
#         background: linear-gradient(135deg, #172554, #111827 75%);
#         margin-bottom: 25px;
#     }

#     .hero h1 {
#         color: #f8fafc;
#         font-size: 34px;
#         margin-bottom: 8px;
#     }

#     .hero p {
#         color: #cbd5e1;
#         font-size: 15px;
#         margin-bottom: 0;
#     }

#     .status {
#         display: inline-block;
#         padding: 6px 12px;
#         border-radius: 20px;
#         background: #12372b;
#         color: #86efac;
#         font-size: 12px;
#         font-weight: 600;
#     }

#     [data-testid="stChatMessage"] {
#         background: #111827;
#         border: 1px solid #293449;
#         border-radius: 14px;
#         padding: 14px;
#     }

#     .section-card {
#         background: #111827;
#         border: 1px solid #293449;
#         padding: 18px;
#         border-radius: 14px;
#     }

#     div.stButton > button {
#         border-radius: 9px;
#     }

#     textarea {
#         color: #f8fafc !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # ==================================================
# # SIDEBAR
# # ==================================================

# with st.sidebar:

#     st.markdown("## 🤖 DevMate AI")
#     st.caption("Your AI developer workspace")

#     st.divider()

#     st.markdown("### Navigation")

#     page = st.radio(
#         "Navigate",
#         ["Chat", "Memory", "About"],
#         label_visibility="collapsed",
#         key="navigation",
#     )

#     st.divider()

#     st.markdown("### System status")

#     st.success("Application running")

#     if get_ai_mode() == "OpenAI API":
#         st.success("OpenAI API connected")
#     else:
#         st.info("Offline demo mode")

#     st.caption("DevMate AI • Development version")

#     st.divider()

#     st.markdown("### Quick information")
#     st.caption("Programming tutor")
#     st.caption("Persistent memory")
#     st.caption("Agentic AI development")


# # ==================================================
# # MAIN HEADER
# # ==================================================

# st.markdown(
#     """
#     <div class="hero">
#         <span class="status">● SYSTEM ONLINE</span>
#         <h1>DevMate AI</h1>
#         <p>
#             Your personal AI assistant for programming,
#             development, and Agentic AI learning.
#         </p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )


# # ==================================================
# # CHAT PAGE
# # ==================================================

# if page == "Chat":

#     st.subheader("💬 Chat workspace")

#     st.caption(
#         "Ask programming questions, explore ideas, "
#         "and learn with your AI assistant."
#     )

#     if st.button("＋ New conversation", use_container_width=False):

#         st.session_state.messages = []
#         reset_conversation()

#         st.rerun()

#     st.divider()

#     # Display previous messages
#     for message in st.session_state.messages:

#         with st.chat_message(message["role"]):
#             st.markdown(
#                 message["content"],
#                 unsafe_allow_html=False,
#             )

#     # User input
#     question = st.chat_input("Message DevMate AI...")

#     if question:

#         st.session_state.messages.append({
#             "role": "user",
#             "content": question,
#         })

#         with st.chat_message("user"):
#             st.markdown(question)

#         with st.chat_message("assistant"):

#             with st.spinner("DevMate AI is thinking..."):

#                 try:
#                     answer = get_response(question)

#                 except Exception as error:
#                     answer = (
#                         "Sorry, something went wrong.\n\n"
#                         f"Error: {error}"
#                     )

#             st.markdown(
#                 answer,
#                 unsafe_allow_html=False,
#             )

#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": answer,
#         })


# # ==================================================
# # MEMORY PAGE
# # ==================================================

# elif page == "Memory":

#     st.subheader("🧠 Memory management")

#     st.caption(
#         "Manage the information DevMate AI remembers."
#     )

#     memories = load_saved_memories()

#     st.metric(
#         "Total saved memories",
#         len(memories),
#     )

#     st.divider()

#     st.markdown("### Add new memory")

#     with st.form("add_memory_form"):

#         memory_type = st.selectbox(
#             "Memory type",
#             ["fact", "name", "preference"],
#         )

#         value = st.text_input(
#             "Memory content",
#             placeholder="Enter information to remember...",
#         )

#         submitted = st.form_submit_button(
#             "Save memory",
#             use_container_width=True,
#         )

#         if submitted:

#             if not value.strip():
#                 st.warning("Please enter memory content.")

#             else:

#                 normalized = value.strip().lower()

#                 duplicate = any(
#                     str(item.get("value", "")).strip().lower() == normalized
#                     and item.get("type", "fact") == memory_type
#                     for item in memories
#                 )

#                 if duplicate:
#                     st.warning("This memory already exists.")

#                 else:

#                     memories.append({
#                         "type": memory_type,
#                         "value": value.strip(),
#                     })

#                     save_saved_memories(memories)

#                     st.success("Memory saved successfully!")

#                     st.rerun()

#     st.divider()

#     st.markdown("### Saved memories")

#     memories = load_saved_memories()

#     if memories:

#         for index, memory in enumerate(memories):

#             with st.container(border=True):

#                 col1, col2 = st.columns([5, 1])

#                 with col1:

#                     st.markdown(
#                         f"**{index + 1}. {memory.get('type', 'fact').title()}**"
#                     )

#                     st.write(memory.get("value", ""))

#                 with col2:

#                     if st.button(
#                         "🗑️",
#                         key=f"delete_memory_{index}",
#                         help="Delete this memory",
#                     ):

#                         memories.pop(index)

#                         save_saved_memories(memories)

#                         st.rerun()

#     else:

#         st.info("No saved memories yet.")


# # ==================================================
# # ABOUT PAGE
# # ==================================================

# elif page == "About":

#     st.subheader("⚙️ About DevMate AI")

#     st.markdown(
#         """
#         ### Your personal AI developer assistant

#         DevMate AI is a Python-based AI assistant designed
#         to help developers learn programming and explore
#         Agentic AI technologies.

#         ### Current architecture

#         - Python application
#         - OpenAI API integration
#         - Offline response engine
#         - Intent detection and routing
#         - Persistent JSON memory
#         - Streamlit user interface
#         - Conversation context management

#         ### Planned features

#         - AI-powered tool calling
#         - Agent planning and execution
#         - Developer tools
#         - Code analysis
#         - RAG-based knowledge retrieval
#         - Agent activity monitoring
#         - Improved conversation management

#         ### Technology stack

#         - Python
#         - Streamlit
#         - OpenAI API
#         - JSON
#         """
#     )


# # ==================================================
# # FOOTER
# # ==================================================

# st.divider()

# st.caption(
#     "DevMate AI • Built with Python, Streamlit and OpenAI"
# )



import json
from pathlib import Path

import streamlit as st

from app import get_ai_mode
from backend import get_response, reset_conversation
from tools import get_memories


# ==================================================
# CONFIGURATION
# ==================================================

MEMORY_FILE = Path(__file__).with_name("memory.json")

st.set_page_config(
    page_title="DevMate AI | Developer Workspace",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ==================================================
# MEMORY FUNCTIONS
# ==================================================

def load_memories():
    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict) and isinstance(data.get("memories"), list):
            return data["memories"]

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return []


def save_memories(memories):
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            {"memories": memories},
            file,
            indent=2,
            ensure_ascii=False,
        )


# ==================================================
# THEME
# ==================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #090e1b;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background: #0d1424;
        border-right: 1px solid #202b40;
    }

    [data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .brand {
        font-size: 25px;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -1px;
    }

    .brand span {
        color: #818cf8;
    }

    .brand-subtitle {
        color: #8492a9;
        font-size: 12px;
        margin-top: 3px;
    }

    .top-label {
        color: #818cf8;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .page-title {
        font-size: 32px;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -1px;
        margin-top: 5px;
    }

    .page-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 22px;
    }

    .metric-card {
        background: linear-gradient(145deg, #172239, #111a2d);
        border: 1px solid #273651;
        border-radius: 14px;
        padding: 19px;
        min-height: 112px;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 600;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 25px;
        font-weight: 800;
        margin-top: 10px;
    }

    .metric-note {
        color: #818cf8;
        font-size: 11px;
        margin-top: 4px;
    }

    .panel {
        background: #111a2b;
        border: 1px solid #26344c;
        border-radius: 15px;
        padding: 20px;
    }

    .panel-title {
        color: #f8fafc;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .panel-description {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.6;
    }

    .status-pill {
        display: inline-block;
        background: #12372d;
        color: #86efac;
        border: 1px solid #1b5a42;
        border-radius: 30px;
        padding: 5px 11px;
        font-size: 11px;
        font-weight: 700;
    }

    .welcome-panel {
        background: linear-gradient(120deg, #182b52, #131d35 75%);
        border: 1px solid #334b76;
        border-radius: 18px;
        padding: 25px;
        margin-bottom: 20px;
    }

    .welcome-panel h2 {
        color: #ffffff;
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .welcome-panel p {
        color: #bdc9e0;
        font-size: 14px;
        margin-bottom: 0;
    }

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 40px;
    }

    [data-testid="stChatMessage"] {
        background: #111a2b;
        border: 1px solid #27354c;
        border-radius: 13px;
        padding: 13px;
    }

    [data-testid="stChatInput"] {
        border-color: #34435e;
    }

    .sidebar-status {
        background: #151f32;
        border: 1px solid #293851;
        border-radius: 10px;
        padding: 12px;
        color: #cbd5e1;
        font-size: 12px;
    }

    hr {
        border-color: #26344b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# DATA
# ==================================================

memories = load_memories()
ai_mode = get_ai_mode()
message_count = len(st.session_state.messages)


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">DevMate<span> AI.</span></div>
        <div class="brand-subtitle">INTELLIGENT DEVELOPER WORKSPACE</div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption("WORKSPACE")

    pages = {
        "Dashboard": "🏠",
        "Chat Workspace": "💬",
        "Memory Center": "🧠",
        "Project Overview": "⚙️",
    }

    for page_name, page_icon in pages.items():

        if st.button(
            f"{page_icon}  {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if st.session_state.page == page_name else "secondary",
        ):
            st.session_state.page = page_name
            st.rerun()

    st.divider()

    st.caption("ENVIRONMENT")

    if ai_mode == "OpenAI API":
        st.success("OpenAI API mode")
    else:
        st.info("Offline demo mode")

    st.markdown(
        f"""
        <div class="sidebar-status">
            <b>System</b><br>
            ● Application running<br><br>
            <b>Memory records</b><br>
            {len(memories)} saved
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption("DevMate AI • Version 0.2.0")


# ==================================================
# DASHBOARD
# ==================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        '<div class="top-label">OVERVIEW / DASHBOARD</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-title">Developer Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Your AI development environment at a glance.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="welcome-panel">
            <div class="status-pill">● SYSTEM ONLINE</div>
            <h2>Welcome to DevMate AI</h2>
            <p>
                Your intelligent programming assistant.
                Learn, build, explore and develop with AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">AI ENVIRONMENT</div>
                <div class="metric-value" style="font-size:20px">{ai_mode}</div>
                <div class="metric-note">Current response engine</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">SAVED MEMORIES</div>
                <div class="metric-value">{len(memories)}</div>
                <div class="metric-note">Persistent memory records</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">CHAT MESSAGES</div>
                <div class="metric-value">{message_count}</div>
                <div class="metric-note">Current chat session</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    left, right = st.columns([1.5, 1])

    with left:

        st.markdown(
            """
            <div class="panel">
                <div class="panel-title">🚀 Development Workspace</div>
                <div class="panel-description">
                    Ask technical questions, understand programming
                    concepts, generate examples and explore AI development.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Open Chat Workspace →",
            use_container_width=True,
        ):
            st.session_state.page = "Chat Workspace"
            st.rerun()

    with right:

        st.markdown(
            """
            <div class="panel">
                <div class="panel-title">🧠 Memory Center</div>
                <div class="panel-description">
                    Manage saved facts, preferences and learning information.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Manage Memories →",
            use_container_width=True,
        ):
            st.session_state.page = "Memory Center"
            st.rerun()

    st.write("")

    st.markdown("### Current Technology Stack")

    st.write(
        "🐍 Python  ·  🤖 OpenAI  ·  ⚡ Streamlit  ·  🧠 JSON Memory"
    )


# ==================================================
# CHAT WORKSPACE
# ==================================================

elif st.session_state.page == "Chat Workspace":

    st.markdown(
        '<div class="top-label">WORKSPACE / AI ASSISTANT</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-title">Chat Workspace</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Talk to your programming assistant and explore technical topics.</div>',
        unsafe_allow_html=True,
    )

    chat_col, info_col = st.columns([2.4, 1])

    with info_col:

        st.markdown(
            f"""
            <div class="panel">
                <div class="panel-title">Assistant Status</div>
                <div class="panel-description">
                    <b>Response engine</b><br>
                    {ai_mode}<br><br>
                    <b>Conversation</b><br>
                    {len(st.session_state.messages)} messages<br><br>
                    <b>Memory records</b><br>
                    {len(memories)} saved
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            """
            <div class="panel">
                <div class="panel-title">What can I do?</div>
                <div class="panel-description">
                    • Explain programming<br>
                    • Generate code examples<br>
                    • Answer technical questions<br>
                    • Remember useful information<br>
                    • Help with Agentic AI learning
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if st.button("＋ New Chat", use_container_width=True):

            st.session_state.messages = []
            reset_conversation()

            st.rerun()

    with chat_col:

        st.markdown("#### 💬 Conversation")

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.markdown(
                    message["content"],
                    unsafe_allow_html=False,
                )

        question = st.chat_input(
            "Ask DevMate AI anything..."
        )

        if question:

            st.session_state.messages.append({
                "role": "user",
                "content": question,
            })

            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    try:
                        answer = get_response(question)

                    except Exception as error:
                        answer = (
                            "Something went wrong while processing your request.\n\n"
                            f"Error: {error}"
                        )

                st.markdown(
                    answer,
                    unsafe_allow_html=False,
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
            })


# ==================================================
# MEMORY CENTER
# ==================================================

elif st.session_state.page == "Memory Center":

    st.markdown(
        '<div class="top-label">MANAGEMENT / MEMORY</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-title">Memory Center</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Control the information DevMate AI stores.</div>',
        unsafe_allow_html=True,
    )

    memories = load_memories()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total memories", len(memories))

    with col2:
        st.metric(
            "Memory file",
            "Available" if MEMORY_FILE.exists() else "Not created",
        )

    st.divider()

    left, right = st.columns([1, 1.4])

    with left:

        st.markdown("### Add Memory")

        with st.form("add_memory_form"):

            memory_type = st.selectbox(
                "Category",
                ["fact", "name", "preference"],
            )

            value = st.text_area(
                "Memory content",
                placeholder="Enter information to remember...",
                height=120,
            )

            submitted = st.form_submit_button(
                "Save Memory",
                use_container_width=True,
            )

            if submitted:

                if not value.strip():
                    st.warning("Please enter memory content.")

                else:

                    duplicate = any(
                        item.get("type", "fact") == memory_type
                        and item.get("value", "").strip().lower() == value.strip().lower()
                        for item in memories
                    )

                    if duplicate:
                        st.warning("This memory already exists.")

                    else:

                        memories.append({
                            "type": memory_type,
                            "value": value.strip(),
                        })

                        save_memories(memories)

                        st.success("Memory saved.")

                        st.rerun()

    with right:

        st.markdown("### Stored Memories")

        if memories:

            for index, memory in enumerate(memories):

                with st.container(border=True):

                    first, second = st.columns([5, 1])

                    with first:
                        st.caption(
                            memory.get("type", "fact").upper()
                        )
                        st.write(memory.get("value", ""))

                    with second:

                        if st.button(
                            "🗑️",
                            key=f"remove_{index}",
                        ):

                            memories.pop(index)
                            save_memories(memories)

                            st.rerun()

        else:
            st.info("No memories stored yet.")


# ==================================================
# PROJECT OVERVIEW
# ==================================================

elif st.session_state.page == "Project Overview":

    st.markdown(
        '<div class="top-label">SYSTEM / PROJECT</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-title">Project Overview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Architecture and development roadmap of DevMate AI.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Project Information")

    st.markdown(
        """
        <div class="panel">
            <div class="panel-title">🤖 DevMate AI</div>
            <div class="panel-description">
                An intelligent programming assistant built with Python.
                The application supports an OpenAI response engine and
                a local offline response engine.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown("### Current Architecture")

    architecture = [
        ("User Interface", "Streamlit dashboard and chat workspace"),
        ("Backend", "Python response processing"),
        ("AI Engine", "OpenAI API with offline fallback"),
        ("Router", "Intent detection and command handling"),
        ("Memory", "Persistent JSON memory"),
        ("Tools", "Reusable memory utility functions"),
    ]

    for name, description in architecture:

        with st.container(border=True):
            st.markdown(f"**{name}**")
            st.caption(description)

    st.write("")

    st.markdown("### Development Roadmap")

    roadmap = [
        "Core application and offline responses",
        "Conversation context and memory",
        "Professional developer dashboard",
        "Real Agentic AI tool calling",
        "Planning and multi-step execution",
        "RAG and knowledge retrieval",
        "Testing and deployment",
    ]

    for index, item in enumerate(roadmap, start=1):
        st.write(f"{index}. {item}")


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "DevMate AI  |  Intelligent Developer Workspace  |  Built with Python"
)
