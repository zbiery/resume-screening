from .schema import AIServiceInterface
from .groq import GroqService
from .openai import AzureOpenAIService
from ..common.config import AppConfig

class AIServiceFactory:
    """Factory class to create appropriate AI service based on configuration"""  
    
    @staticmethod
    def create_service() -> AIServiceInterface:
        """
        Create appropriate AI service based on configuration
        
        Returns:
            Configured AI service instance
        """
        config = AppConfig()
        
        if config.use_azure_openai:
            # Create Azure OpenAI service
            required_props = ['openai_api_version', 'openai_endpoint', 'openai_model']
            missing_keys = [prop for prop in required_props if not getattr(config, prop, None)]

            if missing_keys:
                raise ValueError(f"Missing required Azure OpenAI config keys or they are empty: {missing_keys}")

            return AzureOpenAIService(
                endpoint=config.openai_endpoint,
                deployment_name=config.openai_model,
                api_version=config.openai_api_version
            )
        else:
            # Create Groq service
            required_props = ['keyvault_url', 'groq_secret_name', 'groq_model']
            missing_keys = [prop for prop in required_props if not getattr(config, prop, None)]
            if missing_keys:
                raise ValueError(f"Missing required Groq config keys: {missing_keys}")
            
            return GroqService(
                keyvault_url=config.keyvault_url,
                secret_name=config.groq_secret_name,
                model_name=config.groq_model
            )
