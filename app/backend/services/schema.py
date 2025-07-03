from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Response:
    text: str | None
    input_tokens: int 
    output_tokens: int 

class AIServiceInterface(ABC):
    """Abstract base class for AI services"""
    
    @abstractmethod
    def query(self, prompt: str, **kwargs) -> Response:
        """Query the AI service with a prompt"""
        pass