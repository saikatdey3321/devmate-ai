# DevMate AI

Building an AI agent from scratch while learning Agentic AI.

## Day 1: Project Foundation

### Features
- Python project setup
- OpenAI API integration code
- Environment variable configuration
- Basic question-answer workflow

## Tech Stack
- Python
- OpenAI API
- python-dotenv

## Current Status
- [x] Environment setup
- [x] Dependencies installed
- [x] Initial application code written
- [ ] API connection tested
- [ ] GitHub repository published

## Learning Roadmap
- Day 1: Basic LLM application
- Day 2: Interactive chatbot
- Day 3: Conversation history
- Day 4: Persistent memory
- Day 5: File handling
- Day 6 onwards: RAG, tools, agents and LangGraph



## Day 2: Interactive Chatbot

### Features
- Continuous conversation loop
- Greeting and help commands
- Empty input validation
- Exit command
- Offline demo mode
- Error handling for AI requests

### Learning
- Python functions
- While loops
- Conditional statements
- Break and continue
- Exception handling



## Day 3: Conversation History and Session Memory

### Features
- Stores conversation messages during the current session
- Answers name-related questions using stored messages
- Clear command to reset conversation memory
- Follow-up question support
- Offline demo mode maintained

### Learning
- Python lists and dictionaries
- Conversation history management
- Reverse iteration
- Clearing session state
- Context handling for AI applications


## Day 5 — Persistent Memory

- Added persistent memory using a local JSON file.
- Saved the user's name to `memory.json`.
- Loaded saved memories when the application starts.
- Enabled name recall after restarting the application.
- Added a command to inspect saved memories.
- Kept session history separate from persistent memory.
- Tested the feature in offline demo mode.


## Day 6 — Custom Persistent Memory

- Added a custom `remember` command for saving personal facts.
- Added persistent storage for custom memories using `memory.json`.
- Preserved existing name memory functionality.
- Added memory retrieval for saved facts.
- Added favorite language memory retrieval.
- Verified persistent memories survive application restarts.
- Kept temporary conversation history separate from persistent memory.
- Continued development in offline demo mode without requiring an OpenAI API key.

## Day 7 — Memory Lifecycle Management

- Added `forget <keyword>` command to remove matching persistent memories.
- Added `clear memory` command to remove all persistent memories.
- Preserved the existing `clear` command for temporary conversation history.
- Added persistent memory deletion using `memory.json`.
- Verified deleted memories remain deleted after application restart.
- Added memory lifecycle management for creating, viewing, retrieving, and deleting memories.
- Tested all memory commands in offline demo mode.


## Day 8 — Intent Routing

- Added a dedicated `router.py` module for intent detection.
- Separated user intent detection from application command execution.
- Added routing for `remember`, `forget`, `memory`, `clear`, `clear memory`, `help`, `exit`, and normal chat.
- Connected the intent router to the main DevMate AI application.
- Added router debug output to visualize detected intents.
- Tested command routing without breaking existing memory functionality.
- Continued development in offline demo mode without requiring an OpenAI API key.




