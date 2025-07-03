from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

from .schema import AIServiceInterface, Response
from ..common.logger import get_logger

logger = get_logger(__name__)

class AzureOpenAIService(AIServiceInterface):
    """Service for Azure OpenAI with managed identity"""
    
    def __init__(self, endpoint: str, deployment_name: str = "gpt-4o", api_version: str = "2024-02-01"):
        """
        Initialize Azure OpenAI service with managed identity
        
        Args:
            endpoint: Azure OpenAI endpoint URL
            deployment_name: Name of the deployed model
            api_version: API version to use
        """
        self.endpoint = endpoint
        self.deployment_name = deployment_name
        self.api_version = api_version
        
        # Use managed identity for authentication
        credential = DefaultAzureCredential()
        logger.debug("Retrieving credentials using token auth.")
        token = credential.get_token("https://cognitiveservices.azure.com/.default")
        logger.debug("Credentials received.")
        
        # Configure OpenAI client for Azure
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token=token.token,
            api_version=api_version
        )
        logger.info("Azure OpenAI client initialized.")
    
    def query(self, prompt: str, **kwargs) -> Response:
        """
        Query Azure OpenAI model
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
        
        Returns:
            Response from the model
        """
        try:
            logger.info(f"Querying AzureOpenAI model '{self.deployment_name}'...")
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000),
                top_p=kwargs.get("top_p", 1.0)
            )
            logger.info('Query successful.')
            return Response(
                text = response.choices[0].message.content, 
                output_tokens = response.usage.completion_tokens, # type: ignore
                input_tokens= response.usage.prompt_tokens # type: ignore
            )
        except Exception as e:
            raise Exception(f"Azure OpenAI query failed: {str(e)}")

