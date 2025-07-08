# import json
# import jsbeautifier

# from azure.identity import DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient
# from langchain_groq import ChatGroq
# from langchain.schema import HumanMessage, SystemMessage

# from .schema import AIServiceInterface
# from ..common.logger import get_logger

# logger = get_logger(__name__)


# class GroqService(AIServiceInterface):
#     """Service for interacting with Groq via LangChain and Azure Key Vault."""

#     def __init__(self, keyvault_url: str, secret_name: str, model_name: str = "mixtral-8x7b-32768"):
#         self.model_name = model_name

#         # Get API key from Azure Key Vault
#         credential = DefaultAzureCredential()
#         secret_client = SecretClient(vault_url=keyvault_url, credential=credential)
#         try:
#             logger.debug("Retrieving Groq API key from Azure Key Vault...")
#             secret = secret_client.get_secret(secret_name)
#             api_key = secret.value
#             logger.debug("Groq API key retrieved.")
#         except Exception as e:
#             logger.error(f"Failed to retrieve Groq API key: {e}")
#             raise

#         self.llm = ChatGroq(api_key=api_key, model=model_name, temperature=0.7)

#     def query(self, prompt: str, **kwargs) -> str:
#         """
#         Simple one-shot query to the Groq model.

#         Args:
#             prompt: Prompt to send
#             **kwargs: Optional parameters like temperature

#         Returns:
#             The LLM's response text
#         """
#         try:
#             logger.info(f"Sending basic query to Groq model '{self.model_name}'...")
#             if "temperature" in kwargs:
#                 self.llm.temperature = kwargs["temperature"]

#             result = self.llm.predict_messages([HumanMessage(content=prompt)])
#             return result.content
#         except Exception as e:
#             logger.error(f"Simple Groq query failed: {e}")
#             raise

#     def structured_query(self, text: str, system_prompt: str, functions: list[dict]) -> dict:
#         """
#         Advanced query with system prompt and OpenAI-style function calling.

#         Args:
#             text: The input text (e.g., job description, resume)
#             system_prompt: Instructions to guide the LLM
#             functions: A list of function definitions for structured output

#         Returns:
#             Parsed JSON object from function call output
#         """
#         try:
#             logger.info("Running structured function-calling query...")
#             completion = self.llm.predict_messages(
#                 messages=[
#                     SystemMessage(content=system_prompt),
#                     HumanMessage(content=text)
#                 ],
#                 functions=functions,
#                 function_call="auto"
#             )

#             output = completion.additional_kwargs
#             function_call = output.get("function_call")

#             if not function_call or "arguments" not in function_call:
#                 logger.error(f"Function call missing or no arguments returned: {output}")
#                 raise ValueError("Function call with arguments was not returned by the model.")

#             raw_args = function_call["arguments"]
#             logger.debug(f"Raw function call arguments: {raw_args}")

#             beautified = jsbeautifier.beautify(raw_args)
#             logger.debug(f"Beautified JSON string: {beautified}")

#             parsed = json.loads(beautified)
#             return parsed

#         except Exception as e:
#             logger.error(f"Structured Groq query failed: {e}")
#             raise

from azure.identity.aio import DefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import json, jsbeautifier

from .schema import AIServiceInterface
from ..common.logger import get_logger

logger = get_logger(__name__)

class GroqService(AIServiceInterface):
    def __init__(self, keyvault_url: str, secret_name: str, model_name: str = "mixtral-8x7b-32768"):
        self.keyvault_url = keyvault_url
        self.secret_name = secret_name
        self.model_name = model_name
        self.llm = None
        self._credential: DefaultAzureCredential | None = None

    async def initialize(self):
        self._credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=self.keyvault_url, credential=self._credential)

        try:
            logger.debug("Retrieving Groq API key from Azure Key Vault...")
            secret = await secret_client.get_secret(self.secret_name)
            api_key = secret.value
            logger.debug("Groq API key retrieved.")
        except Exception as e:
            logger.error(f"Failed to retrieve Groq API key: {e}")
            raise
        finally:
            await secret_client.close()

        self.llm = ChatGroq(api_key=api_key, model=self.model_name, temperature=0.7)  # type: ignore

    async def query(self, prompt: str, **kwargs) -> str:
        if not self.llm:
            await self.initialize()

        try:
            logger.info(f"Calling Groq model '{self.model_name}' using ainvoke...")
            if "temperature" in kwargs:
                self.llm.temperature = kwargs["temperature"]  # type: ignore

            result = await self.llm.ainvoke([HumanMessage(content=prompt)])  # type: ignore
            return result.content  # type: ignore
        except Exception as e:
            logger.error(f"Groq ainvoke query failed: {e}")
            raise

    async def structured_query(self, text: str, system_prompt: str, functions: list[dict]) -> dict:
        if not self.llm:
            await self.initialize()

        try:
            logger.info("Running structured query with function calling using ainvoke...")
            response = await self.llm.ainvoke(  # type: ignore
                input=[
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=text)
                ],
                functions=functions,
                function_call="auto"
            )

            function_call = response.additional_kwargs.get("function_call")
            if not function_call or "arguments" not in function_call:
                logger.error(f"Missing function_call or arguments: {response.additional_kwargs}")
                raise ValueError("No function_call with arguments returned.")

            raw_args = function_call["arguments"]
            beautified = jsbeautifier.beautify(raw_args)
            logger.debug(f"Beautified JSON args:\n{beautified}")
            return json.loads(beautified)

        except Exception as e:
            logger.error(f"Structured Groq ainvoke query failed: {e}")
            raise

    async def close(self):
        """Clean up async resources like DefaultAzureCredential"""
        if self._credential:
            await self._credential.close()
            logger.info("GroqService credential closed.")
