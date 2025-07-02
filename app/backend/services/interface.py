import os
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import openai
from groq import Groq

@dataclass
class Response:
    text: str
    input_tokens: int
    output_tokens: int

class AIServiceInterface(ABC):
    """Abstract base class for AI services"""
    
    @abstractmethod
    def query(self, prompt: str, **kwargs) -> Response:
        """Query the AI service with a prompt"""
        pass


class AzureOpenAIService(AIServiceInterface):
    """Service for Azure OpenAI with managed identity"""
    
    def __init__(self, endpoint: str, deployment_name: str, api_version: str = "2024-02-01"):
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
        token = credential.get_token("https://cognitiveservices.azure.com/.default")
        
        # Configure OpenAI client for Azure
        self.client = openai.AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=token.token,
            api_version=api_version
        )
    
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
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000),
                top_p=kwargs.get("top_p", 1.0)
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Azure OpenAI query failed: {str(e)}")


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
            secret = secret_client.get_secret(secret_name)
            api_key = secret.value
        except Exception as e:
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
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000),
                top_p=kwargs.get("top_p", 1.0)
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Groq query failed: {str(e)}")


class AIServiceFactory:
    """Factory class to create appropriate AI service based on configuration"""
    
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load config file: {str(e)}")
    
    @staticmethod
    def create_service(config: Dict[str, Any]) -> AIServiceInterface:
        """
        Create appropriate AI service based on configuration
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Configured AI service instance
        """
        use_azure_openai = config.get("USE_AZURE_OPENAI", False)
        
        if use_azure_openai:
            # Create Azure OpenAI service
            required_keys = ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT_NAME"]
            missing_keys = [key for key in required_keys if key not in config]
            if missing_keys:
                raise ValueError(f"Missing required Azure OpenAI config keys: {missing_keys}")
            
            return AzureOpenAIService(
                endpoint=config["AZURE_OPENAI_ENDPOINT"],
                deployment_name=config["AZURE_OPENAI_DEPLOYMENT_NAME"],
                api_version=config.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
            )
        else:
            # Create Groq service
            required_keys = ["GROQ_KEYVAULT_URL", "GROQ_SECRET_NAME"]
            missing_keys = [key for key in required_keys if key not in config]
            if missing_keys:
                raise ValueError(f"Missing required Groq config keys: {missing_keys}")
            
            return GroqService(
                keyvault_url=config["GROQ_KEYVAULT_URL"],
                secret_name=config["GROQ_SECRET_NAME"],
                model_name=config.get("GROQ_MODEL_NAME", "mixtral-8x7b-32768")
            )


# Example usage
def main():
    """Example usage of the AI service factory"""
    try:
        # Load configuration
        config = AIServiceFactory.load_config("config.json")
        
        # Create appropriate service
        ai_service = AIServiceFactory.create_service(config)
        
        # Query the service
        prompt = "What is the capital of France?"
        response = ai_service.query(prompt, temperature=0.5, max_tokens=500)
        
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()


# Example config.json structure:
"""
For Azure OpenAI:
{
    "USE_AZURE_OPENAI": true,
    "AZURE_OPENAI_ENDPOINT": "https://your-resource.openai.azure.com/",
    "AZURE_OPENAI_DEPLOYMENT_NAME": "gpt-4",
    "AZURE_OPENAI_API_VERSION": "2024-02-01"
}

For Groq:
{
    "USE_AZURE_OPENAI": false,
    "GROQ_KEYVAULT_URL": "https://your-keyvault.vault.azure.net/",
    "GROQ_SECRET_NAME": "groq-api-key",
    "GROQ_MODEL_NAME": "mixtral-8x7b-32768"
}
"""