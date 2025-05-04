# Pydantic-AI Researcher Multi-Agent System

## Overview

This project implements a simple multi-agent research system using [Pydantic-AI](https://github.com/pydantic/pydantic-ai). The system follows an **evaluator-optimizer workflow**:
- **Agent A (Researcher/Optimizer):** Generates answers to user research questions, using web search tools for up-to-date information.
- **Agent B (Evaluator):** Evaluates Agent A's answers, providing structured feedback until the answer is accepted or a maximum number of iterations is reached.

The system is modular, type-safe, and easily extensible for new tools or evaluation criteria.

---

## Features

- **Evaluator-Optimizer Loop:** Iterative improvement of answers based on feedback.
- **Tavily Search Integration:** Agent A can use Tavily Search (via MCP) to gather real-time web knowledge.
- **Pydantic Models:** All data is validated and structured using Pydantic.
- **Iteration Limit:** Prevents infinite loops by enforcing a configurable maximum.
- **Unit Tests:** Pytest suite covers expected, edge, and failure cases.

---

## File Structure

```
.
├── models.py              # Pydantic models for questions, answers, feedback
├── tools.py               # Tavily Search tool integration
├── research_system.py     # Agent definitions and tool registration
├── main.py                # Orchestration loop and entrypoint
├── tests/
│   └── test_main.py       # Pytest unit tests
├── TASK.md                # Project task tracking
├── PLANNING.md            # Project architecture and design notes
└── README.md              # This documentation
```

---

## Setup

1. **Install Python 3.9+**  
   Ensure you have Python 3.9 or newer installed.

2. **Install dependencies**  
   ```
   pip install pydantic pydantic-ai pytest
   ```
   If using MCP tools, follow their setup instructions for authentication and API keys.

3. **(Optional) Configure Tavily MCP**  
   Replace the placeholder `tavily_mcp_tool` in `research_system.py` with the actual MCP tool integration for production use.

---

## Usage

To run the system with a sample research question:

```bash
python main.py
```

- By default, the system will answer "What are the main causes of climate change?".
- To customize, modify the `user_question` variable in `main.py` or adapt the script for CLI input.

---

## Testing

Run the unit tests with:

```bash
pytest tests/
```

Tests use mocks to simulate agent/tool behavior and cover:
- Acceptance on first try
- Iteration limit reached
- Acceptance after improvement

---

## Extending the System

- **Add new tools:** Implement and register new tools in `tools.py` and with the researcher agent.
- **Change evaluation criteria:** Modify the evaluator agent's system prompt or feedback model.
- **Integrate other search providers:** Add wrappers for other MCP tools as needed.

---

## Acknowledgements

- [Pydantic-AI](https://github.com/pydantic/pydantic-ai) for agent framework and type safety.
- [Tavily Search MCP](https://github.com/tavily-ai/tavily-mcp) for web search integration.

---

## Further Resources

- See `PLANNING.md` for architecture and design details.
- See `TASK.md` for project progress and TODOs.

---

*For questions or contributions, please open an issue or pull request!*
