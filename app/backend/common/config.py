import json
import os
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv(override=True)

class AppConfig:
    def __init__(self):
        config_path = os.getenv("CONFIG_PATH", "config/config.json")
        environment = os.getenv("ENVIRONMENT", "dev")
        self.environment = environment

        full_path = Path(config_path)
        if not full_path.exists():
            raise FileNotFoundError(f"Config file not found: {full_path.resolve()}")

        with open(config_path, "r") as f:
            self._full_config: Dict[str, Any] = json.load(f)

        if environment not in self._full_config:
            raise ValueError(f"Environment '{environment}' not found in config.")

        self.config = self._full_config[environment]

    @property
    def keyvault_name(self) -> str:
        return self.config["KEYVAULT"]["NAME"]

    @property
    def keyvault_url(self) -> str:
        return f"https://{self.keyvault_name}.vault.azure.net"

    @property
    def storage_account_name(self) -> str:
        return self.config["STORAGE"]["ACCOUNT_NAME"]

    @property
    def storage_blob_url(self) -> str:
        return f"https://{self.storage_account_name}.blob.core.windows.net"

    @property
    def container_name(self) -> str:
        return self.config["STORAGE"]["CONTAINER_NAME"]

    @property
    def use_azure_openai(self) -> bool:
        return self.config["LLM"].get("USE_AZURE_OPENAI", True)

    @property
    def openai_endpoint(self) -> str:
        return self.config["LLM"]["AZURE_OPENAI"]["ENDPOINT"]

    @property
    def openai_model(self) -> str:
        return self.config["LLM"]["AZURE_OPENAI"]["MODEL"]
    
    @property
    def openai_api_version(self) -> str:
        return self.config["LLM"]["AZURE_OPENAI"]["API_VERSION"]

    @property
    def groq_endpoint(self) -> str:
        return self.config["LLM"]["GROQ"]["ENDPOINT"]

    @property
    def groq_model(self) -> str:
        return self.config["LLM"]["GROQ"]["MODEL"]

    @property
    def groq_secret_name(self) -> str:
        return self.config["LLM"]["GROQ"]["SECRET_NAME"]

    @property
    def log_level(self) -> str:
        return self.config["LOGGING"]["LOG_LEVEL"].upper()

    def as_dict(self) -> Dict[str, Any]:
        return self.config



