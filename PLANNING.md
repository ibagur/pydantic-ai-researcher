# Pydantic-AI Researcher Multi-Agent System

## Project Overview
This project aims to create a multi-agent research system using Pydantic-AI that follows the evaluator-optimizer workflow pattern. The system will consist of two primary agents:

1. **Agent A (Researcher/Optimizer)**: Generates responses to user research questions, leveraging external knowledge tools.
2. **Agent B (Evaluator)**: Evaluates and provides feedback on Agent A's responses against predefined criteria.

These agents will operate in a feedback loop, where Agent A iteratively improves its responses based on Agent B's feedback until a satisfactory response is achieved or until a maximum number of iterations is reached.

## Core Architecture

### Evaluator-Optimizer Workflow
The evaluator-optimizer pattern is a powerful approach where one agent generates content while another provides structured feedback to improve it. This creates a self-improvement loop that typically produces higher quality results than a single-pass approach.

The workflow consists of:
1. **Initial Response Generation**: Agent A creates an initial response to the research question
2. **Evaluation**: Agent B evaluates the response against specific criteria
3. **Feedback**: Agent B provides structured feedback to Agent A
4. **Optimization**: Agent A improves the response based on feedback
5. **Loop Continuation**: Steps 2-4 repeat until acceptance criteria are met or iteration limit is reached

### Knowledge Enhancement
Agent A will be augmented with external search capabilities using:
- Brave Search MCP
- (Optionally) Tavily Search MCP

This will allow the system to gather real-time information from the web to enhance research quality.

## Technical Stack
- **Core Framework**: Pydantic-AI for agent construction, providing type safety and dependency injection
- **Agent Structure**: Structured Pydantic models for input/output types and validation
- **External Tools**: Integration with search APIs via MCP tools
- **Evaluation Mechanism**: Predefined rubrics and criteria for response assessment

## Design Principles
1. **Type Safety**: Leverage Pydantic's type validation for robust agent interactions
2. **Modularity**: Separate concerns between research generation and evaluation
3. **Iteration Control**: Implement safeguards against infinite loops
4. **Structured Feedback**: Use structured formats for feedback to facilitate improvement
5. **Extensibility**: Design the system for easy addition of new tools or evaluation criteria

## Limitations and Considerations
- Iteration limit to prevent infinite loops
- Potential network dependencies for search tools
- Need for well-defined evaluation criteria to guide the improvement process
- Balancing evaluation stringency with practical completion requirements