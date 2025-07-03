from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from groq import Groq

from .schema import AIServiceInterface, Response
from ..common.logger import get_logger

logger = get_logger(__name__)

class GroqService(AIServiceInterface):
    """Service for Groq with API key from Azure Key Vault"""
    
    def __init__(self, keyvault_url: str, secret_name: str, model_name: str = "mixtral-8x7b-32768"):
        """
        Initialize Groq service with API key from Azure Key Vault
        
        Args:
            keyvault_url: Azure Key Vault URL
            secret_name: Name of the secret containing Groq API key
            model_name: Groq model to use
        """
        self.model_name = model_name
        
        # Get API key from Azure Key Vault using managed identity
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=keyvault_url, credential=credential)
        
        try:
            logger.debug("Retrieving credentials using token auth.")
            secret = secret_client.get_secret(secret_name)
            api_key = secret.value
            logger.debug("Credentials received.")
        except Exception as e:
            logger.error(f"Failed to retrieve Groq API key from Key Vault: {str(e)}")
            raise Exception(f"Failed to retrieve Groq API key from Key Vault: {str(e)}")
        
        # Initialize Groq client
        self.client = Groq(api_key=api_key)
    
    def query(self, prompt: str, **kwargs) -> Response:
        """
        Query Groq model
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
        
        Returns:
            Response from the model
        """
        try:
            logger.info(f"Querying Groq model '{self.model_name}'...")
            response = self.client.chat.completions.create(
                model=self.model_name,
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
            raise Exception(f"Groq query failed: {str(e)}")
