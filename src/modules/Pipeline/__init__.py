from .Pipe_for_evaluation import Pipeline_For_Eval
from .Pipe_for_service import Pipeline_For_Service

pipe_eval = Pipeline_For_Eval
pipe_service = Pipeline_For_Service
__all__ = [
    "pipe_eval",
    "pipe_service"
]