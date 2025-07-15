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

    async def structured_query(self, text: str, system_prompt: str, functions: list[dict], function_call: str = "default") -> dict:
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
                function_call=function_call
            )

            function_call = response.additional_kwargs.get("function_call") # type: ignore
            if not function_call or "arguments" not in function_call:
                logger.error(f"Missing function_call or arguments: {response.additional_kwargs}")
                raise ValueError("No function_call with arguments returned.")

            raw_args = function_call["arguments"] # type: ignore
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
