from pydantic import BaseModel

class Feedback(BaseModel):
    """
    Represents feedback from the evaluator agent.

    Attributes:
        accepted (bool): Whether the answer is accepted.
        comments (str): Feedback or suggestions for improvement.
    """
    accepted: bool
    comments: str
