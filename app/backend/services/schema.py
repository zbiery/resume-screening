from abc import ABC, abstractmethod

class AIServiceInterface(ABC):
    """Abstract base class for AI services"""

    @abstractmethod
    async def query(self, prompt: str, **kwargs) -> str:
        """Simple one-turn query to the AI service"""
        pass

    @abstractmethod
    async def structured_query(self, text: str, system_prompt: str, functions: list[dict], function_call: str | dict = "auto") -> dict:
        """
        Structured query using system prompts and function calling.
        
        Args:
            text: Input string (e.g., job description or resume)
            system_prompt: System-level instruction prompt
            functions: List of OpenAI-style function definitions
            function_call: Optional. The name of the function to call

        Returns:
            Parsed dictionary from model's function call output
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """Closes HTTP connection for the client service"""
        pass
