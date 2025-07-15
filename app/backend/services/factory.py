from .schema import AIServiceInterface
from .groq import GroqService
from .openai import AzureOpenAIService
from ..common.config import AppConfig
import asyncio

class AIServiceFactory:
    """Factory to create and asynchronously initialize an AI service instance (Groq or Azure OpenAI) based on configuration."""

    @staticmethod
    async def create_service() -> AIServiceInterface:
        """
        Create and asynchronously initialize the appropriate AI service implementation.

        Returns:
            An initialized instance of GroqService or AzureOpenAIService

        Raises:
            ValueError: If required configuration fields are missing
        """
        config = AppConfig()

        if config.use_azure_openai:
            required_keys = ['openai_api_version', 'openai_endpoint', 'openai_model']
            missing = [key for key in required_keys if not getattr(config, key, None)]

            if missing:
                raise ValueError(f"Missing required Azure OpenAI config values: {missing}")

            service = AzureOpenAIService(
                endpoint=config.openai_endpoint,
                deployment_name=config.openai_model,
                api_version=config.openai_api_version
            )
        else:
            required_keys = ['keyvault_url', 'groq_secret_name', 'groq_model']
            missing = [key for key in required_keys if not getattr(config, key, None)]

            if missing:
                raise ValueError(f"Missing required Groq config values: {missing}")

            service = GroqService(
                keyvault_url=config.keyvault_url,
                secret_name=config.groq_secret_name,
                model_name=config.groq_model
            )

        # Initialize async (if the service has initialize method)
        if hasattr(service, "initialize"):
            await service.initialize()

        return service
