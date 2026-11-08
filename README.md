# Autonomous Agent Framework

This project provides a modular framework for creating autonomous agents capable of interacting with a project's files, utilizing LLMs to reason about tasks, execute tool calls, and maintain conversation state.

## Core Components

- **`core/`**: Contains the core logic and interfaces:
    - `agent.py`: Orchestrates the agent's goal-oriented loop, managing memory and action execution.
    - `environment.py`: Executes actions safely, providing error handling and logging.
    - `action.py`: Definitions for actions and the `ActionRegistry` to manage them.
    - `memory.py`: Tracks conversation history and task context.
    - `models.py`: Data structures for prompts, tool calls, and assistant messages.
    - `language.py`: Handles formatting prompts and parsing LLM responses for the framework.
- **`agents/`**:
    - `readme_agent.py`: A specialized agent implementation that demonstrates the framework by navigating the project to generate documentation.
    - `tools.py`: Contains the actual implementation of project interaction tools (listing, reading, writing files).
- **`services/`**:
    - `llm/service.py`: A wrapper for LiteLLM to handle API communication, rate-limiting, and response parsing.
- **`main.py`**: The entry point to run the agent.

## Configuration

The project uses a `.env` file for configuration. Required variables include:
- `LLM_DEFAULT_MODEL`: The LLM to be used (e.g., `gpt-4o`).
- `MAX_RESPONSE_TOKENS`
- `MAX_RETRIES`
- `MAX_ITERATIONS`
- (Optional) `FREE_TIER` and `FREE_TIER_RPM` for rate-limiting configurations.

## How it works

1. The agent is initialized with a set of `Goal`s.
2. In the `run()` loop, the agent:
    - Constructs a prompt based on its memory and available tools.
    - Sends the prompt to the configured LLM service.
    - Parses the returned tools/actions.
    - Executes the tools via the `Environment`.
    - Updates its memory with the results.
    - Continues until a `terminate` tool call is issued or the max iteration limit is reached.
