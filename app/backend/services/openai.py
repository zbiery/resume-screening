# from azure.identity import DefaultAzureCredential
# from openai import AzureOpenAI
# import json
# import jsbeautifier

# from .schema import AIServiceInterface
# from ..common.logger import get_logger

# logger = get_logger(__name__)


# class AzureOpenAIService(AIServiceInterface):
#     """Service for Azure OpenAI using managed identity"""

#     def __init__(self, endpoint: str, deployment_name: str = "gpt-4o", api_version: str = "2024-02-01"):
#         """
#         Initialize Azure OpenAI service with managed identity
#         """
#         self.endpoint = endpoint
#         self.deployment_name = deployment_name
#         self.api_version = api_version

#         credential = DefaultAzureCredential()
#         logger.debug("Retrieving Azure AD token for Azure OpenAI...")
#         token = credential.get_token("https://cognitiveservices.azure.com/.default")
#         logger.debug("Token retrieved successfully.")

#         self.client = AzureOpenAI(
#             azure_endpoint=endpoint,
#             azure_ad_token=token.token,
#             api_version=api_version,
#         )
#         logger.info("Azure OpenAI client initialized.")

#     def query(self, prompt: str, **kwargs) -> str:
#         """
#         Simple one-turn query to Azure OpenAI

#         Args:
#             prompt: The user prompt
#             **kwargs: Optional parameters like temperature, max_tokens

#         Returns:
#             The response text
#         """
#         try:
#             logger.info(f"Querying Azure OpenAI model '{self.deployment_name}'...")
#             response = self.client.chat.completions.create(
#                 model=self.deployment_name,
#                 messages=[{"role": "user", "content": prompt}],
#                 temperature=kwargs.get("temperature", 0.7),
#                 max_tokens=kwargs.get("max_tokens", 1000),
#                 top_p=kwargs.get("top_p", 1.0)
#             )
#             logger.info("Query successful.")
#             return response.choices[0].message.content
#         except Exception as e:
#             logger.error(f"Azure OpenAI query failed: {e}")
#             raise

#     def structured_query(self, text: str, system_prompt: str, functions: list[dict]) -> dict:
#         """
#         Structured query using function calling.

#         Args:
#             text: Input content (e.g., job description)
#             system_prompt: System prompt for guidance
#             functions: List of function definitions

#         Returns:
#             Dictionary parsed from model's function_call response
#         """
#         try:
#             logger.info("Running structured function-calling query with Azure OpenAI...")
#             response = self.client.chat.completions.create(
#                 model=self.deployment_name,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": text},
#                 ],
#                 functions=functions,
#                 function_call="auto"
#             )

#             function_call = response.choices[0].message.function_call
#             if not function_call or not function_call.arguments:
#                 raise ValueError("Function call arguments not found in the response.")

#             raw_args = function_call.arguments
#             beautified = jsbeautifier.beautify(raw_args)
#             return json.loads(beautified)

#         except Exception as e:
#             logger.error(f"Azure OpenAI structured query failed: {e}")
#             raise

import json
import jsbeautifier
import asyncio
from concurrent.futures import ThreadPoolExecutor

from azure.identity import DefaultAzureCredential
from openai import AsyncAzureOpenAI
from .schema import AIServiceInterface
from ..common.logger import get_logger

logger = get_logger(__name__)

class AzureOpenAIService(AIServiceInterface):
    """Async service for Azure OpenAI using managed identity"""

    def __init__(
        self,
        endpoint: str,
        deployment_name: str = "gpt-4o",
        api_version: str = "2024-02-01",
    ):
        self.endpoint = endpoint
        self.deployment_name = deployment_name
        self.api_version = api_version

        # Acquire token synchronously (wrap in async if needed)
        self._token = None
        self._client = None

    async def initialize(self):
        """Initialize client asynchronously (fetch token and set up client)"""
        def get_token_sync():
            credential = DefaultAzureCredential()
            logger.debug("Retrieving Azure AD token for Azure OpenAI...")
            token = credential.get_token("https://cognitiveservices.azure.com/.default")
            logger.debug("Token retrieved successfully.")
            return token.token

        # Run blocking token retrieval in executor
        loop = asyncio.get_event_loop()
        self._token = await loop.run_in_executor(None, get_token_sync)

        self._client = AsyncAzureOpenAI(
            azure_endpoint=self.endpoint,
            azure_ad_token=self._token,
            api_version=self.api_version,
        )
        logger.info("Azure OpenAI client initialized.")

    async def query(self, prompt: str, **kwargs) -> str:
        """
        Async simple one-turn query to Azure OpenAI

        Args:
            prompt: The user prompt
            **kwargs: Optional parameters like temperature, max_tokens

        Returns:
            The response text
        """
        if self._client is None:
            raise RuntimeError("Client not initialized. Call 'await initialize()' first.")

        try:
            logger.info(f"Querying Azure OpenAI model '{self.deployment_name}' asynchronously...")

            completion = await self._client.chat.completions.create(
                model=self.deployment_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000),
                top_p=kwargs.get("top_p", 1.0),
            )

            logger.info("Query successful.")
            return completion.choices[0].message.content # type: ignore

        except Exception as e:
            logger.error(f"Azure OpenAI async query failed: {e}")
            raise

    async def structured_query(self, text: str, system_prompt: str, functions: list[dict]) -> dict:
        """
        Async structured query using function calling.

        Args:
            text: Input content (e.g., job description)
            system_prompt: System prompt for guidance
            functions: List of function definitions

        Returns:
            Dictionary parsed from model's function_call response
        """
        if self._client is None:
            raise RuntimeError("Client not initialized. Call 'await initialize()' first.")

        try:
            logger.info("Running async structured function-calling query with Azure OpenAI...")

            completion = await self._client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
                functions=functions, # type: ignore
                function_call="auto",
            )

            function_call = completion.choices[0].message.function_call
            if not function_call or not function_call.arguments:
                raise ValueError("Function call arguments not found in the response.")

            raw_args = function_call.arguments
            beautified = jsbeautifier.beautify(raw_args)
            return json.loads(beautified)

        except Exception as e:
            logger.error(f"Azure OpenAI async structured query failed: {e}")
            raise

    async def close(self):
        if self._client:
            await self._client.close()
