"""
tests/test_main.py

Unit tests for the multi-agent researcher system.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from main import run_research_loop

@pytest.mark.asyncio
async def test_accepts_on_first_iteration(monkeypatch):
    """
    Test that the loop accepts the answer on the first iteration.
    """
    # Mock research_agent and evaluator_agent to accept immediately
    with patch("research_system.research_agent.run", new_callable=AsyncMock) as mock_research_run, \
         patch("research_system.evaluator_agent.run", new_callable=AsyncMock) as mock_eval_run:
        class DummyOutput:
            output = type("Answer", (), {"text": "A good answer."})()
        class DummyFeedback:
            output = type("Feedback", (), {"accepted": True, "comments": ""})()
        mock_research_run.return_value = DummyOutput()
        mock_eval_run.return_value = DummyFeedback()
        result = await run_research_loop("Test question?", max_iterations=3)
        assert result.text == "A good answer."

@pytest.mark.asyncio
async def test_reaches_iteration_limit(monkeypatch):
    """
    Test that the loop stops after the maximum number of iterations if not accepted.
    """
    with patch("research_system.research_agent.run", new_callable=AsyncMock) as mock_research_run, \
         patch("research_system.evaluator_agent.run", new_callable=AsyncMock) as mock_eval_run:
        class DummyOutput:
            output = type("Answer", (), {"text": "Try again."})()
        class DummyFeedback:
            output = type("Feedback", (), {"accepted": False, "comments": "Not good enough."})()
        mock_research_run.return_value = DummyOutput()
        mock_eval_run.return_value = DummyFeedback()
        result = await run_research_loop("Test question?", max_iterations=2)
        assert result is None

@pytest.mark.asyncio
async def test_accepts_after_improvement(monkeypatch):
    """
    Test that the loop accepts after an improved answer.
    """
    with patch("research_system.research_agent.run", new_callable=AsyncMock) as mock_research_run, \
         patch("research_system.evaluator_agent.run", new_callable=AsyncMock) as mock_eval_run:
        # First answer is not accepted, second is accepted
        class DummyOutput:
            def __init__(self, text):
                self.output = type("Answer", (), {"text": text})()
        class DummyFeedback:
            def __init__(self, accepted, comments):
                self.output = type("Feedback", (), {"accepted": accepted, "comments": comments})()
        mock_research_run.side_effect = [DummyOutput("First try."), DummyOutput("Improved answer.")]
        mock_eval_run.side_effect = [DummyFeedback(False, "Needs improvement."), DummyFeedback(True, "Good.")]
        result = await run_research_loop("Test question?", max_iterations=3)
        assert result.text == "Improved answer."
